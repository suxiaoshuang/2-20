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
    stage = Stage.objects.all()
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

    # return render(request,'admin/layui.html',context)
    # return render(request,'admin/modal.html',context)

def match_wq(request,match):

    grade = request.POST.get('grade')
    stag = request.POST.get('stag')
    qualify = request.POST.get('qualify')
    medal = request.POST.get('medal')

    stage = request.GET.get('stage')
    con_id = request.GET.get('con_id')
    pIndex = request.GET.get('pIndex')
    print(stage,con_id,pIndex)
    try:
        wq = W_Q.objects.get(Q(match_id=match) & Q(stage=stag))
        if wq :
            wq.grade = grade
            wq.qualify = qualify
            wq.medal = medal
            wq.save()
    except:
        W_Q.objects.create(grade=grade, stage=stag, qualify=qualify, medal=medal, match_id=match)
    # reverse('match_team_list' + '?stage=' + stage, args=(pIndex, con_id,))
    if stage:
        return redirect('/admin/match_team_list/'+pIndex+'/'+con_id+'?stage='+stage)
    else:
        return redirect(reverse('match_team_list' , args=(pIndex, con_id,)))


def match_stu(request,match):
    wq = W_Q.objects.filter(match_id=match).order_by('stage')
    work = Works.objects.filter(match_id=match).order_by('stage')
    h_c_id = Match.objects.get(id=match).h_c_id

    # for i in wq:
    #     if int(i.stage) == 1:
    #         conlist[0] = i
    #     elif int(i.stage) == 2:
    #         conlist[1] = i
    #     elif int(i.stage) == 3:
    #         conlist[2] = i
    # for k in work:
    #     if int(k.stage) == 1:
    #         data[0] = k
    #     elif int(k.stage) ==2:
    #         data[1] = k
    #     elif int(k.stage) == 3:
    #         data[2] = k
    conlist = list(zip(wq,work))
    context = {'conlist':conlist,'h_c_id':h_c_id,'work_data':work}

    return render(request,'admin/match_stu.html',context)