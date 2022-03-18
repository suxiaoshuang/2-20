from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render,redirect,HttpResponse
from django.core.paginator import Paginator
from myadmin.models import Info, Organizer, File, Team, Registration, Contest, User





def sc_team_list(request,pIndex):
    user_name = request.session.get('user_name')
    user_id = request.session.get("user_id")
    #拿到用户的所有team记录
    team = Team.objects.filter(use_id=User.objects.get(user_id=user_id).id)

    ct = []
    cf = []
    #分别取已结束的竞赛对应的队伍cf，和进行中的竞赛对应的队伍ct
    for t in team:
        for st in Contest.objects.filter(team__id=t.id):
            if st.contest_status > 0:
                t_name = Team.objects.get(id=t.id).t_name
                c_name = Contest.objects.get(team__id=t.id).contest_name
                time = Registration.objects.get(t_id=Team.objects.get(Q(head=True)&Q(h_c_id=t.h_c_id)).id).time
                h_c_id = t.h_c_id
                status = st.contest_status
                ct.append((t_name,c_name,time,h_c_id,status,))

            elif st.contest_status == 0:
                t_name = Team.objects.get(id=t.id).t_name
                c_name = Contest.objects.get(team__id=t.id).contest_name
                time = Registration.objects.get(t_id=Team.objects.get(Q(head=True)&Q(h_c_id=t.h_c_id)).id).time
                h_c_id = t.h_c_id
                status = st.contest_status
                cf.append((t_name,c_name,time,h_c_id,status,))

    #前端传参，是否点击已结束或进行中
    mywhere = []
    conlist = ct
    status = request.GET.get('status',None)
    if status == 't':
        mywhere.append('status='+status)
        conlist = ct
    elif status == 'f':
        mywhere.append('status='+status)
        conlist = cf
    #分页
    pIndex = int(pIndex)
    page = Paginator(conlist,8)
    plist = page.page_range
    maxpages = page.num_pages
    if pIndex > maxpages:
        pIndex = maxpages
    elif pIndex < 1:
        pIndex = 1
    conlist = page.page(pIndex)
    context = {'pIndex':pIndex,'plist':plist,'maxpages':maxpages,'conlist':conlist,'mywhere':mywhere}


    return render(request,'student/sc_team_list.html',context)



def sc_team_quit(request,h_c_id):
    user_id = request.session.get('user_id')
    print(h_c_id,user_id)
    for i in Team.objects.filter(h_c_id=h_c_id):
        if User.objects.get(id=i.use_id).user_id in user_id:
            Team.objects.get(use_id=i.use_id).delete()
            message = '已退出！'
        else:
            message = '请重试！'
    return render(request,'admin/info.html',locals())




def sc_team_js(request,h_c_id):
    user_id = request.session.get('user_id')
    try:
        for i in Team.objects.filter(h_c_id=h_c_id):
            #验证此人是否在该队伍里
            if User.objects.get(id=i.use_id).user_id in user_id:
                #验证此人是否是队长
                if i.head == True:
                    for k in Team.objects.filter(Q(h_c_id=h_c_id) and Q(head=False)):
                        Team.objects.get(id=k.id).delete()
                    i.delete()
                    message = '已解散团队!'


    except:
        message = '请重试！'

    return render(request,'admin/info.html',locals())





