from ..models import Contest, File, Stage, Tyep, Organizer, Registration, User, Match, Team,Match,W_Q,Works,UWQ
from django.shortcuts import render,HttpResponse,redirect
from django.db.models import Q, Count
from django.core.paginator import Paginator
from ..forms import PostForm
import os,datetime
from django.conf import settings
from django.urls import reverse


def match_con_show(request,pIndex):
    con = Contest.objects.filter(Q(contest_status=1) & Q(audit=True))
    conlist = []

    for i in con:
        qualify = False
        if  Match.objects.filter(con_id=i.id):
            if request.session.get('identify') in i.contest_organizer or int(User.objects.get(user_id=request.session.get('user_id')).permissions) == 2:
                qualify = True
            conlist.append((i,UWQ.objects.get(con_id=i.id),qualify))

    pIndex = int(pIndex)
    page = Paginator(conlist,10)
    maxpages = page.num_pages
    plist = page.page_range
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    pdata = page.page(pIndex)

    context = {'conlist':pdata,'plist':plist,'pIndex':pIndex,'maxpages':maxpages}

    return render(request,'admin/match_con_show.html',context)


def match_team_list(request,pIndex,con_id):
    mteam = Match.objects.filter(Q(status=True) & Q(con_id=con_id))
    data = []
    for i in mteam:
        try:
            data.append((i, Works.objects.get(Q(match_id=i.id) & Q(stage=1)).name))
        except:
            data.append((i,''))
    mteam = data
    cname = Contest.objects.get(id=con_id).contest_name

    #前端便于管理员辨识比赛的各个阶段
    st = int(Contest.objects.get(id=con_id).contest_stage)
    if st == 1:
        stage = {'决赛':1}
    elif st == 2:
        stage = {'预赛':1,'决赛':2}
    elif st == 3:
        stage = {'预赛':1,'复赛':2,'决赛':3}

    con_stage = Contest.objects.get(id=con_id).contest_stage

    mywhere = []
    cst = request.GET.get('stage',None)
    if cst:
        if int(cst) > 1:
            conlist, mteam = mteam,[]

            mywhere.append('stage='+cst)
            cst = int(cst)-1
            # print(cst)
            for i,k in conlist:
                try:
                    if W_Q.objects.filter(Q(stage=cst) & Q(qualify=True) &Q(match_id=i.id)):

                        mteam.append((i,Works.objects.get(Q(stage=cst+1) & Q(match_id=i.id)).name,))
                except:
                    if W_Q.objects.filter(Q(stage=cst) & Q(qualify=True) & Q(match_id=i.id)):
                        mteam.append((i,'',))



    pIndex = int(pIndex)
    page = Paginator(mteam,10)
    maxpages = page.num_pages
    plist = page.page_range
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    pdata = page.page(pIndex)
    context = {'conlist': pdata, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages,'con_id':con_id,'cname':cname,'stage':stage,'con_stage':con_stage,'mywhere':mywhere}
    return render(request,'admin/match_tlist.html',context)


def match_wq(request,match):

    grade = request.POST.get('grade')
    stag = request.POST.get('stag')
    qualify = request.POST.get('qualify')
    medal = request.POST.get('medal')

    stage = request.GET.get('stage')
    con_id = request.GET.get('con_id')
    pIndex = request.GET.get('pIndex')
    # print(stage,con_id,pIndex)
    #如果该队伍此阶段的成绩已存在，则进行修改
    try:
        wq = W_Q.objects.get(Q(match_id=match) & Q(stage=stag))
        if wq :
            wq.grade = grade
            wq.qualify = qualify
            wq.medal = medal
            wq.save()
    #否则新增一条成绩、晋级记录
    except:
        W_Q.objects.create(grade=grade, stage=stag, qualify=qualify, medal=medal, match_id=match)

    if stage:
        return redirect('/admin/match_team_list/'+pIndex+'/'+con_id+'?stage='+stage)
    else:
        return redirect(reverse('match_team_list' , args=(pIndex, con_id,)))

#该视图函数用于展示此队伍的成绩，以及各阶段的作品
def match_stu(request,match):
    h_c_id = Match.objects.get(id=match).h_c_id
    wq = W_Q.objects.filter(match_id=match).order_by('stage')
    works = Works.objects.filter(match_id=match).order_by('stage')
    # work = None
    st = int(Contest.objects.get(id=Team.objects.filter(h_c_id=h_c_id)[0].con_id).contest_stage)
    #前端显示作品时，辨识作品属于哪个阶段的产物
    w = []
    for i in works:
        if st == 1:

            if i.stage == 1:
                w.append((i,'决赛'))

        elif st == 2:

            if i.stage == 1:
                w.append((i,'预赛'))
            elif i.stage == 2:
                w.append((i,'决赛'))

        elif st == 3:

            if i.stage == 1:
                w.append((i, '预赛'))
            elif i.stage == 2:
                w.append((i,'复赛'))
            elif i.stage == 3:
                w.append((i, '决赛'))
    works = w

    conlist = list(zip(wq,works))
    # print(conlist)
    context = {'conlist':conlist,'h_c_id':h_c_id,'work_data':works}

    return render(request,'admin/match_stu.html',context)