from django.shortcuts import render
from myadmin.models import User,Contest,Info,File
from django.db.models import Q
from django.core.paginator import Paginator



def notice_show(request,id):
    if request.method == "GET":
        permissions = int(User.objects.get(user_id=request.session.get('user_id')).permissions)
        try:
            info = Info.objects.get(id=id)
            f_time = info.ctime
            file = File.objects.filter(file_ctime=f_time)
            return render(request,'teacher/notice_show.html',locals())
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
        context = {'conlist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere,'permissions':int(User.objects.get(user_id=request.session.get('user_id')).permissions)}
        return render(request,'teacher/notice_list.html',context)



def news_show(request,id):
    if request.method == "GET":
        permissions = int(User.objects.get(user_id=request.session.get('user_id')).permissions)
        try:
            info = Info.objects.get(id=id)
            f_time = info.ctime
            file = File.objects.filter(file_ctime=f_time)
            return render(request,'teacher/news_show.html',locals())
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
        context = {'conlist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere,'permissions': int(User.objects.get(user_id=request.session.get('user_id')).permissions)}
        return render(request,'teacher/news_list.html',context)


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
    permissions = int(User.objects.get(user_id=request.session.get('user_id')).permissions)
    try:
        f_time = con.contest_ctime
        f = File.objects.filter(file_ctime=f_time)
    except:
        pass
    return render(request,'teacher/con_show.html',locals())

