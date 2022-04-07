import datetime
import os
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render,redirect,HttpResponse
from django.core.paginator import Paginator

from login import settings
from myadmin.models import Info, Organizer, File, Team, Registration, Contest, User, Match, Works, W_Q


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
            if st.contest_status > 0  and Registration.objects.get(t_id=Team.objects.get(Q(head=True)&Q(h_c_id=t.h_c_id)).id).status == True:
                # if  Registration.objects.get(t_id=Team.objects.get(Q(head=True)&Q(h_c_id=t.h_c_id)).id).status == True:
                t_name = Team.objects.get(id=t.id).t_name
                c_name = Contest.objects.get(team__id=t.id).contest_name
                time = Registration.objects.get(t_id=Team.objects.get(Q(head=True)&Q(h_c_id=t.h_c_id)).id).time
                h_c_id = t.h_c_id
                status = st.contest_status
                match = Match.objects.get(h_c_id=t.h_c_id).id
                # print(Registration.objects.get(t_id=Team.objects.get(Q(head=True)&Q(h_c_id=t.h_c_id)).id).status)
                ct.append((t_name,c_name,time,h_c_id,status,match))

            elif st.contest_status == 0 and Registration.objects.get(t_id=Team.objects.get(Q(head=True)&Q(h_c_id=t.h_c_id)).id).status == True:
                t_name = Team.objects.get(id=t.id).t_name
                c_name = Contest.objects.get(team__id=t.id).contest_name
                time = Registration.objects.get(t_id=Team.objects.get(Q(head=True)&Q(h_c_id=t.h_c_id)).id).time
                h_c_id = t.h_c_id
                status = st.contest_status
                match = Match.objects.get(h_c_id=t.h_c_id).id
                cf.append((t_name,c_name,time,h_c_id,status,match))

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
    if Contest.objects.get(id=Team.objects.filter(h_c_id=h_c_id)[0].con_id).contest_status == 0:
        message = '竞赛已结束，无效操作！'
        return render(request,'admin/info.html',locals())

    for i in Team.objects.filter(h_c_id=h_c_id):
        if User.objects.get(id=i.use_id).user_id in user_id:
            Team.objects.get(use_id=i.use_id).delete()
            message = '已退出！'
        else:
            message = '请重试！'
    return render(request,'admin/info.html',locals())




def sc_team_js(request,h_c_id):
    user_id = request.session.get('user_id')
    #竞赛结束后不能解散队伍，必须在报名中或竞赛进行时解散队伍
    if Contest.objects.get(id=Team.objects.filter(h_c_id=h_c_id)[0].con_id).contest_status == 0:
        message = '竞赛已结束，无效操作！'
        return render(request,'admin/info.html',locals())
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



def sc_upload_works(request,h_c_id):
    if request.method == 'POST':
        data = request.POST
        match =int(data.get('match'))
        stage = int(data.get('stage'))
        name = data.get('work_name')
        file = request.FILES.get('work',None)
        print(match,stage,name)
        if file is None:
            return HttpResponse('你没有提交任何作品！')

        file_name = file.name
        tail = os.path.splitext(file_name)[1]
        date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        #文件在服务器中的真正名字
        url = ''.join((date,'-'+os.path.splitext(file_name)[0]+tail))
        #相对路径
        file_path = os.path.join('work/',url)

        #如果在数据库中找到了这个队伍之前提交的作品，那么将原来的作品从数据库和服务器中移除，并进行更新
        if Works.objects.filter(Q(stage=stage)& Q(match_id=Match.objects.get(h_c_id=h_c_id).id)).exists() :
            work = Works.objects.get(Q(stage=stage)& Q(match_id=Match.objects.get(h_c_id=h_c_id).id))
            #获得原作品在服务器上的路径，并移除该作品
            path = os.path.join(settings.WORK_UPLOAD[0],work.file_path.replace('work/',''))
            os.remove(path)
            #更新服务器上的作品
            with open(os.path.join(settings.WORK_UPLOAD[0], url), 'ab') as f:
                for chunk in file.chunks():
                    f.write(chunk)
                f.close()
            work.name = name
            work.file_path = file_path
            work.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            work.save()
            return HttpResponse('修改成功！')
        #将文件存储到服务器上
        with open(os.path.join(settings.WORK_UPLOAD[0], url), 'ab') as f:
            for chunk in file.chunks():
                f.write(chunk)
            f.close()
        Works.objects.create(stage=stage,file_path=file_path,match_id=match,con_id=Match.objects.get(h_c_id=h_c_id).con_id,team_id=Team.objects.get(Q(head=True)&Q(h_c_id=h_c_id)).id,name=name)
        return HttpResponse('提交成功！')

@csrf_exempt
def match_show(request,match):
    h_c_id = Match.objects.get(id=match).h_c_id
    wq = W_Q.objects.filter(match_id=match).order_by('stage')
    works = Works.objects.filter(match_id=match).order_by('stage')
    # work = None
    st = int(Contest.objects.get(id=Team.objects.filter(h_c_id=h_c_id)[0].con_id).contest_stage)
    # 前端显示作品时，辨识作品属于哪个阶段的产物
    w = []
    for i in works:
        if st == 1:

            if i.stage == 1:
                w.append((i, '决赛'))

        elif st == 2:

            if i.stage == 1:
                w.append((i, '预赛'))
            elif i.stage == 2:
                w.append((i, '决赛'))

        elif st == 3:

            if i.stage == 1:
                w.append((i, '预赛'))
            elif i.stage == 2:
                w.append((i, '复赛'))
            elif i.stage == 3:
                w.append((i, '决赛'))
    works = w

    conlist = list(zip(wq, works))
    # print(conlist)
    context = {'conlist': conlist, 'h_c_id': h_c_id, 'work_data': works}
    return render(request,'student/match_show.html',context)