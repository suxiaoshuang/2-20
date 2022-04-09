from django.urls import reverse
from myadmin.models import User,Team,Match,Registration,Works,W_Q
from django.db.models import Q, Count
from django.shortcuts import render,HttpResponse,redirect
import random
list1 = ['佛山', '南宁', '北海', '杭州', '南昌', '厦门', '温州','虞美人','合欢花','杏花','蜡梅','玉兰','兰花','青囊','芙蓉','青鸾花','杜鹃','紫薇','玉簪','玉蕊','凌霄','秋海棠']
def te(request):
    user = User.objects.filter(Q(identify='学生') & ~Q(name='su'))
    teacher = User.objects.filter((Q(identify='教师')))
    user1,user2 = user[:20],user[20:]
    print(user1,user2)
    con_id = 14
    c_name = '大学生程序设计大赛'
    type = '信息技术'
    medal = ['无','银奖','金奖']

    k = 0
    for i in user1:

        Team.objects.create(u_name=i.name,c_name=c_name,con_id=con_id,h_c_id=i.user_id+str(con_id),use_id=i.id,head=True,t_name=list1[random.randrange(0,len(list1)-1)])
        team = Team.objects.get(Q(use_id=i.id) & Q(c_name=c_name))
        Registration.objects.create(c_name=c_name,type=type,con_id=con_id,t_id=team.id,t_name=team.t_name,teacher=random.choice(teacher).name,status=True)
        Match.objects.create(h_c_id=team.h_c_id,tname=team.t_name,cname=team.c_name,status=True,con_id=con_id,team_id=team.id)
        match = Match.objects.get(team_id=team.id)
        for m in range(1,4):
            if m >1 and W_Q.objects.filter(Q(match_id=match.id)& Q(stage=m-1)) and W_Q.objects.get(Q(match_id=match.id)& Q(stage=m-1)).qualify:
                Works.objects.create(stage=m,file_path='xx',con_id=con_id,match_id=match.id,team_id=team.id,name=random.choice(list1[:-1]))
                if m == 3:
                    grade = random.randrange(50, 100)
                    if grade >= 80 and grade < 90:
                        W_Q.objects.create(grade=grade, qualify=True, stage=m, match_id=match.id, medal='银奖',
                                           con_id=con_id)
                    elif grade >= 90:
                        W_Q.objects.create(grade=grade, qualify=True, stage=m, match_id=match.id, medal='金奖',
                                           con_id=con_id)
                    elif grade >= 60 and grade < 80:
                        W_Q.objects.create(grade=grade, qualify=True, stage=m, match_id=match.id, medal='铜奖',
                                           con_id=con_id)
                    else:
                        W_Q.objects.create(grade=grade, qualify=False, stage=m, match_id=match.id, medal='无',
                                           con_id=con_id)
                elif m ==2:
                    grade = random.randrange(50, 100)
                    if grade >= 60:
                        W_Q.objects.create(grade=grade, qualify=True, stage=m, match_id=match.id, medal='无',
                                           con_id=con_id)
                    else:
                        W_Q.objects.create(grade=grade, qualify=False, stage=m, match_id=match.id, medal='无',
                                           con_id=con_id)
            if m ==1:
                Works.objects.create(stage=m, file_path='xx', con_id=con_id, match_id=match.id, team_id=team.id,
                                     name=random.choice(list1[:-1]))
                grade = random.randrange(40,100)
                if grade >= 60 :
                    W_Q.objects.create(grade=grade,qualify=True,stage=m,match_id=match.id,medal='无',con_id=con_id)
                else:
                    W_Q.objects.create(grade=grade, qualify=False, stage=m, match_id=match.id, medal='无', con_id=con_id)
        for j in range(len(user2)):
            # print(k)
            if k >=3:
                k = 0
                user2 = user2[3:]
                # print(user2)
                break
            Team.objects.create(u_name=user2[j].name,c_name=c_name,con_id=con_id,h_c_id=i.user_id+str(con_id),use_id=user2[j].id,head=False,t_name=team.t_name)
            k = k + 1

    return redirect(reverse('admin_index'))


