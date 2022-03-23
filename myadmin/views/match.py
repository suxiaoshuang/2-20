from ..models import Contest, File, Stage, Tyep, Organizer, Registration, User, Match, Team,Match,W_Q
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
        if  Match.objects.filter(con_id=i.id):
            conlist.append(i)

    pIndex = int(pIndex)
    page = Paginator(10,conlist)
    maxpages = page.num_pages
    plist = page.page_range
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    pdata = page.page(pIndex)

    context = {'conlist':pdata,'plist':plist,'pIndex':pIndex,'maxpages':maxpages}

    return render(request,'admin/match_show.html',context)


def match_team_list(request,pIndex,con_id):
    mteam = Match.objects.filter(Q(status=True) & Q(con_id=con_id))
    pIndex = int(pIndex)
    page = Paginator(10,mteam)
    maxpages = page.num_pages
    plist = page.page_range
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    pdata = page.page(pIndex)
    context = {'conlist': pdata, 'plist': plist, 'pIndex': pIndex, 'maxpages': maxpages,'con_id':con_id}

    return render(request,'admin/match_tlist.html',context)


def match_wq(request,match):
    if request.method == 'POST':
        grade = request.POST.get('grade')
        stage = request.POST.get('stage')
        qualify = request.POST.get('qualify')
        medal = request.POST.get('medal')
        W_Q.objects.create(grade=grade,stage=stage,qualify=qualify,medal=medal,match_id=match)
        return
    else:
        stage = Stage.objects.all()

        return 
