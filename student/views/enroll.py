from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from myadmin.models import Info, Organizer, File, Team, Registration, Contest, User
import datetime


def sc_list(request,pIndex=1):
    if request.method == "GET":
        con = Contest.objects.filter(contest_status=2)
        pIndex = int(pIndex)
        page = Paginator(con,10)
        maxpages = page.num_pages
        plist = page.page_range
        if pIndex > maxpages:
            pIndex = maxpages
        if pIndex < 1 :
            pIndex = 1
        conlist = page.page(pIndex)
        us_id = request.session.get('user_id')
        df = 0
        for r_id in conlist:
            # print(r_id.contest_pt)
            sc_en = Registration.objects.filter(con_id=r_id.id)   #拿到所有该比赛的参赛记录
            for team_id in sc_en:
                team = Team.objects.filter(registration__id=team_id.id)   #拿到各参赛队伍的队员记录
                for user in team:
                    if us_id in User.objects.get(id=user.use_id).user_id:
                        df = r_id.id
        print(df)
        context = {'conlist':conlist,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'df':df}
        return render(request,'student/sc_list.html',context)


def sc_enroll(request,id):
    name = Contest.objects.get(id=id).contest_name
    user = User.objects.get(user_id=request.session.get('user_id'))
    team = Team.objects.create(head=True,con_id=id,use_id=user.id,u_name=request.session.get('user_name'),c_name=name)
    Registration.objects.create(c_name=name,type=Contest.objects.get(id=id).contest_type,status=False,con_id=id,t_id=team.id)
    return render(request,'student/sc_enroll.html')