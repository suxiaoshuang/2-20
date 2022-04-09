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
            if W_Q.objects.get(Q(match_id=i.id) & Q(stage=1)).grade:
                # print('yes')
                data.append((i, Works.objects.get(Q(match_id=i.id) & Q(stage=1)).name,'已提交'))
            else:
                data.append((i, Works.objects.get(Q(match_id=i.id) & Q(stage=1)).name, '未提交'))
        except:
            # print('no')
            # if W_Q.objects.get(match_id=i.id).grade:
            #     data.append((i,'','已提交'))
            # else:
            data.append((i, '', '未提交'))
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
            for i,k,j in conlist:
                try:
                    if W_Q.objects.filter(Q(stage=cst) & Q(qualify=True) &Q(match_id=i.id)):
                        if W_Q.objects.get(Q(match_id=i.id) & Q(stage=cst)).grade:
                            mteam.append((i,Works.objects.get(Q(stage=cst+1) & Q(match_id=i.id)).name,'已提交'))
                        else:
                            mteam.append((i, Works.objects.get(Q(stage=cst + 1) & Q(match_id=i.id)).name, '未提交'))
                except:
                    if W_Q.objects.filter(Q(stage=cst) & Q(qualify=True) & Q(match_id=i.id)):
                        # if W_Q.objects.get(match_id=i.id).grade:
                        #     mteam.append((i,'','已提交'))
                        # else:
                        mteam.append((i, '', '未提交'))



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
    con_id = Match.objects.get(id=match).con_id
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
        W_Q.objects.create(grade=grade, stage=stag, qualify=qualify, medal=medal, match_id=match,con_id=con_id)

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


def count(request,con_id):
    grade1,grade2,grade3 = [],[],[]
    stage,stage2,stage3 = None,None,None
    con_stage = int(Contest.objects.get(id=con_id).contest_stage)
    if con_stage == 3:
        stage = '初赛'
        stage2 = '复赛'
        stage3 = '决赛'
        for match in Match.objects.filter(con_id=con_id):
            for wq in W_Q.objects.filter(Q(match_id=match.id) & Q(stage=1)):
                grade1.append(wq.grade)
            for wq in W_Q.objects.filter(Q(match_id=match.id) & Q(stage=2)):
                grade2.append(wq.grade)
            for wq in W_Q.objects.filter(Q(match_id=match.id) & Q(stage=3)):
                grade3.append(wq.grade)

    elif con_stage == 2:
        stage = '初赛'
        stage2 = '决赛'
        for match in Match.objects.filter(con_id=con_id):
            for wq in W_Q.objects.filter(Q(match_id=match.id) & Q(stage=1)):
                grade1.append(wq.grade)
            for wq in W_Q.objects.filter(Q(match_id=match.id) & Q(stage=2)):
                grade2.append(wq.grade)

    elif con_stage ==1:
        stage = '比赛'
        for match in Match.objects.filter(con_id=con_id):
            for wq in W_Q.objects.filter(Q(match_id=match.id) & Q(stage=1)):
                grade1.append(wq.grade)

        # temp = W_Q.objects.filter(con_id=con_id).count()
    f1,f2,f3 = [],[],[]
    f1x,f1y,f2x,f2y,f3x,f3y = [],[],[],[],[],[]
    if grade1:
        f1x,f1y = [],[]
        d1 = sorted(set(grade1))
        # print(d1)
        for d in d1:
            # f1.append((d, grade1.count(d)))
            f1x.append(int(d))
            f1y.append(grade1.count(d))
    if grade2:
        f2x,f2y = [],[]
        d2 = sorted(set(grade2))
        print(d2)
        for d in d2:
            # f2.append((d,grade2.count(d)))
            f2x.append(int(d))
            f2y.append(grade2.count(d))
    if grade3:
        f3x,f3y = [],[]
        d3 = sorted(set(grade3))
        for d in d3:
            # f3.append((d,grade3.count(d)))
            f3x.append(int(d))
            f3y.append(grade3.count(d))
    cname = Contest.objects.get(id=con_id).contest_name





    result = {'f1x':f1x,'f1y':f1y,'f2x':f2x,'f2y':f2y,'f3x':f3x,'f3y':f3y,'cname':cname,'con_stage':con_stage,
              'stage':stage,'stage2':stage2,'stage3':stage3,
            }
    print(result)
    # print(W_Q.objects.filter(Q(con_id=con_id)&Q(stage=1)).values('grade').annotate(Count('match_id')))
    # print(f1,'\n',f2,'\n',f3)

    return render(request,'admin/match_count.html',result)

#竞赛数据统计----报名人数、获奖情况
def match_con_count_list(request,pIndex=1):
    con = Contest.objects.filter(Q(contest_status=1) | Q(contest_status=0))
    conlist = []
    rt,rnum,mj,my,mt = 0,0,0,0,0
    for con_ in con:
        #如果该项目进入比赛阶段
        if Match.objects.filter(con_id=con_.id):
            for reg in Registration.objects.filter(con_id=con_.id):
                #队伍数量
                rt = rt+1
                for t in Team.objects.filter(h_c_id=Team.objects.get(id=reg.t_id).h_c_id):
                    if t:
                        #报名人数
                        rnum = rnum+1

            #如果项目进入评审阶段
            if W_Q.objects.filter(con_id=con_.id):
                #my、mj、mt分别是获得银、金、铜奖的的队伍数量
                my = W_Q.objects.filter(Q(con_id=con_.id)&Q(medal='银奖')).count()
                mj = W_Q.objects.filter(Q(con_id=con_.id) & Q(medal='金奖')).count()
                mt = W_Q.objects.filter(Q(con_id=con_.id)&Q(medal='铜奖')).count()

        conlist.append((con_,rt,rnum,mj,my,mt,))
    pIndex = int(pIndex)
    page = Paginator(conlist,8)
    maxpages = page.num_pages
    plist = page.page_range
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    pdata = page.page(pIndex)
    context = {'conlist':pdata,'pIndex':pIndex,'maxpages':maxpages,'plist':plist}
    return render(request,'admin/match_con_count_list.html',context)

def match_con_team(request,con_id,pIndex=1):
    team = Registration.objects.filter(con_id=con_id)
    head = None
    conlist = []
    for reg in team:
        medal = '无'
        head = User.objects.get(team=reg.t_id).name
        for wq in W_Q.objects.filter(match_id=Match.objects.get(team_id=reg.t_id).id):
            if wq.medal != '无':
                medal = wq.medal
        conlist.append((reg,head,medal,Match.objects.get(team_id=reg.t_id).id))


    pIndex = int(pIndex)
    page = Paginator(conlist,10)
    maxpages = page.num_pages
    plist = page.page_range
    if pIndex > maxpages:
        pIndex = maxpages
    elif pIndex < 1:
        pIndex = 1
    pdata = page.page(pIndex)
    context = {'conlist':pdata,'maxpages':maxpages,'plist':plist,'pIndex':pIndex,'con_id':con_id}
    return render(request,'admin/match_team_l.html',context)

