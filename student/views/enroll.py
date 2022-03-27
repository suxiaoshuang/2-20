from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render,redirect,HttpResponse
from django.core.paginator import Paginator
from myadmin.models import Info, Organizer, File, Team, Registration, Contest, User, Stage, Match,UWQ


def sc_list(request,pIndex=1):
    if request.method == "GET":
        con = Contest.objects.filter(Q(contest_status=2) & Q(audit=True))
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
        df = []
        jk = []
        for r_id in conlist:
            tf = 0
            st = False
            sc_en = Registration.objects.filter(con_id=r_id.id)   #拿到所有该比赛的参赛记录  r_id是比赛记录
            for team_id in sc_en:
                team = Team.objects.filter(registration__id=team_id.id)   #拿到各参赛队伍的队长记录  team_id是各队伍的报名记录
                # print(team)     #一条报名记录对应一个队伍，一对一
                for user in team:   #user.use_id  Team里的use_id
                    h_c_id = user.h_c_id
                    for i in Team.objects.filter(h_c_id=h_c_id):   #找所有h_c_id=xxxx的队伍
                        if us_id in User.objects.get(id=i.use_id).user_id:     #用户判断是否在参赛队伍里
                            tf = r_id.id
                            # team_id = user.id
                            if Registration.objects.get(id=team_id.id).t_name:
                                st = True


            df.append(tf)
            jk.append(st)
        # print(df)
        conlist = list(zip(df,jk,conlist))
        print(conlist)
        context = {'conlist':conlist,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'df':df}
        return render(request,'student/sc_list.html',context)


def sc_enroll(request):
    if request.method == "GET":
        id = request.GET.get('id')
        name = Contest.objects.get(id=id).contest_name
        user = User.objects.get(user_id=request.session.get('user_id'))
        try:
            team = Team.objects.create(head=True,con_id=id,use_id=user.id,u_name=request.session.get('user_name'),c_name=name,h_c_id=user.user_id[:2]+user.user_id[4:]+id)
            Registration.objects.create(c_name=name,type=Contest.objects.get(id=id).contest_type,status=False,con_id=id,t_id=team.id)
        except:
            return HttpResponse("出了点错误，请重试！")
    return HttpResponse("报名成功！")


def sc_add_team(request):
    if request.method == "GET":
        con_id = request.GET.get('con_id')
        team_id,reg_id,status= team_id_reg_id(request,con_id)

        teacher = User.objects.filter(identify='教师')
        if status == True :
            teacher = Registration.objects.get(id=reg_id).teacher
            team_name = Registration.objects.get(id=reg_id).t_name
            return redirect(reverse('sc_team_nt', args=(team_id,teacher,team_name,)))

        team_id = Team.objects.get(id=team_id).h_c_id
        return render(request,'student/sc_enroll.html',locals())

    if request.method == "POST":

        teacher = request.POST.get('teacher')
        team_name = request.POST.get('team')
        con_id = request.POST.get("con_id")

        team_id,reg_id,status = team_id_reg_id(request,con_id)
        print(team_id,reg_id,status)
        team = Team.objects.get(id=team_id)
        team.t_name = team_name

        reg = Registration.objects.get(id=reg_id)
        reg.t_name = team_name
        reg.teacher = teacher
        team.save()
        reg.save()

        return redirect(reverse('sc_team_nt', args=(team_id,teacher,team_name,)))


def sc_team_nt(request,team_id,teacher,team_name):
    team_id = team_id
    team_id = Team.objects.get(id=team_id).h_c_id

    teacher = teacher
    team_name = team_name
    print(team_id,teacher,team_name)
    return render(request,'student/team_n_t.html',locals())


def sc_join_team(request):
    if request.method == 'GET':
        return render(request,'student/join_team.html')

    if request.method == "POST":
        h_c_id = request.POST.get('h_c_id')
        user_id = request.session.get("user_id")
        user_name = request.session.get("user_name")
        con_id = request.POST.get('con_id')
        # print(con_id,h_c_id)
        #不能让队长再加入自己的队伍
        if Team.objects.filter(Q(head=True) & Q(use_id=User.objects.get(user_id=user_id).id) & Q(h_c_id=h_c_id)):
            message = "您已是队伍队长，不能再加入该队伍！"
            return render(request,'admin/info.html',locals())

        # 验证用户是否已加入队伍，否则不予加入，跳转至队伍详情页面
        team_id,reg_id,status = team_id_reg_id(request,con_id)
        if team_id:
            message = '您已加入一个队伍，请先退出原队伍再进行操作！'
            return render(request,'admin/info.html',locals())

        # 验证所填写的队伍id和竞赛id是否存在，否则重新填写队伍h_c_id和竞赛id
        try:
            team = Team.objects.get(Q(h_c_id=h_c_id) & Q(con_id=con_id))
            # print(team)
        except:
            message = "填写的队伍id或竞赛id错误，请重新核对填写！"
            return render(request,'admin/info.html',locals())

        #加入队伍
        t = Team()
        t.h_c_id = team.h_c_id
        t.c_name = team.c_name
        t.use_id = User.objects.get(user_id=user_id).id
        t.u_name = user_name
        t.con_id = team.con_id
        t.head = False
        t.t_name = team.t_name
        t.save()
        #跳转至队伍详情页面
        # return render(request,'student/team_members.html',locals())
        return redirect(reverse('sc_team_members',args=(h_c_id,)))

#团队
def sc_team_memebers(request,h_c_id):
    conlist = []
    h_uid = None
    team = Team.objects.filter(h_c_id=h_c_id)
    match = Match.objects.get(h_c_id=h_c_id).id
    # stage = Stage.objects.all()
    con_status = True
    #提交作品的相应阶段的权限
    # st = None
    uwq = UWQ.objects.filter(con_id=Team.objects.filter(h_c_id=h_c_id)[0].con_id)[0]
    stage = uwq.stage
    status = uwq.status

    for members in team:
        #队长用户名

        name = members.u_name
        user_id = User.objects.get(team__id=members.id).user_id
        head = members.head
        if head == True:
            h_uid = user_id
            head = '是'
        elif head == False:
            head = '否'
        h_c_id = h_c_id

        c_name = members.c_name
        c_status = Contest.objects.get(team__id=members.id).contest_status
        if c_status == 0:
            c_status = '竞赛已结束'
            con_status = False
        elif c_status == 1:
            c_status = '竞赛进行中'
        elif c_status == 2:
            c_status = '竞赛开启报名中'

        lt = (name,user_id,head,h_c_id,c_name,c_status)
        conlist.append(lt)
    user = request.session.get('user_id')
    # print(h_uid,user)
    return render(request,'student/team_members.html',{"conlist":conlist,'user':user,'h_uid':h_uid,'h_c_id':h_c_id,'stage':stage,'match':match,'con_status':con_status,'status':status})


def team_id_reg_id(request,con_id):
    sc_en = Registration.objects.filter(con_id=con_id)  # 拿到所有该比赛的参赛记录
    us_id = request.session.get('user_id')
    status = False
    tea_id = None
    registration_id = None
    for team_id in sc_en:
        team = Team.objects.filter(registration__id=team_id.id)  # 拿到各参赛队伍的队长的报名记录
        # print(team)
        for user in team:    #队长team记录
            h_c_id = user.h_c_id
            for i in Team.objects.filter(h_c_id=h_c_id):
                u = User.objects.get(team__id=i.id)
                if us_id in u.user_id:
                    tea_id = user.id
                    registration_id = team_id.id
                    if user.t_name:
                        status = True  # 是否已填写团队信息

    return tea_id,registration_id,status