from django.shortcuts import render, redirect
from django.urls import reverse
from myadmin.models import User,Contest,Info,File
from django.db.models import Q
from django.core.paginator import Paginator

def index(request):
    identify = request.session.get('identify')
    info = Info.objects.all().order_by('-time')[:5]
    con = Contest.objects.filter(Q(audit=True) & Q(contest_status=1)).order_by('-time')[:6]
    news = Info.objects.filter(type='news').order_by('-time')[:6]
    notice = Info.objects.filter(type='notice').order_by('-time')[:6]
    file = File.objects.all().order_by('-id')[:6]
    dic = {'学生': 'student', '教师': 'teacher', '管理员': 'admin'}

    print(info,con)
    return render(request, dic.get(identify)+'/index.html',locals())


def notice_show(request,id):
    if request.method == "GET":
        try:
            info = Info.objects.get(id=id)
            f_time = info.ctime
            file = File.objects.filter(file_ctime=f_time)
            return render(request,'public/notice_show.html',locals())
        except:
            message = "文件不存在！"
            url = request.path_info
            return render(request,'admin/info.html',locals())

def notice_list(request,pIndex):
    if request.method == "GET":
        mywhere = []
        keyword = request.GET.get('keyword',None)
        if keyword:
            list = Info.objects.filter(Q(title__icontains=keyword)&Q(type='notice')).order_by('-time')
            mywhere.append('keyword='+keyword)
        else:
            list = Info.objects.filter(type='notice').order_by('-time')
        pIndex = int(pIndex)
        page = Paginator(list,8)
        maxpages = page.num_pages
        plist = page.page_range
        if pIndex < 1 :
            pIndex = 1
        elif pIndex > maxpages:
            pIndex = maxpages

        list2 = page.page(pIndex)
        context = {'conlist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
        return render(request,'public/notice_list.html',context)



def news_show(request,id):
    if request.method == "GET":
        try:
            info = Info.objects.get(id=id)
            f_time = info.ctime
            file = File.objects.filter(file_ctime=f_time)
            return render(request,'public/news_show.html',locals())
        except:
            message = "文件不存在！"
            url = request.path_info
            return render(request,'admin/info.html',locals())


def news_list(request,pIndex=1):
    if request.method == "GET":
        mywhere = []
        keyword = request.GET.get('keyword',None)
        if keyword:
            list = Info.objects.filter(Q(title__icontains=keyword)&Q(type='news')).order_by('-time')
            mywhere.append('keyword='+keyword)
        else:
            list = Info.objects.filter(type='news').order_by('-time')
        pIndex = int(pIndex)
        page = Paginator(list,8)
        maxpages = page.num_pages
        plist = page.page_range
        if pIndex < 1 :
            pIndex = 1
        elif pIndex > maxpages:
            pIndex = maxpages

        list2 = page.page(pIndex)
        context = {'conlist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
        return render(request,'public/news_list.html',context)


def con_show(request,id):
    con = Contest.objects.get(Q(id=id) & Q(audit=True))
    c_name = con.contest_name
    c_type = con.contest_type
    form1 = con.contest_info
    c_organizer = con.contest_organizer
    c_stage = con.contest_stage
    c_time = con.contest_time
    c_img = con.contest_img_path
    c_id = id
    c_status = con.contest_status
    try:
        f_time = con.contest_ctime
        f = File.objects.filter(file_ctime=f_time)
    except:
        pass
    return render(request,'public/con_show.html',locals())




def file_list(request,pIndex=1):
    pass