from django.urls import reverse
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from ..models import Info
import datetime

def admin_news_add(request):
    if request.method == "GET":
        info = Info()
        information = info.text
        return render(request,'news_info.html',locals())

    elif request.method == "POST":
        info = Info()
        df = request.POST
        info.title = df.get('title')
        info.text = df.get('information')
        info.ctime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        info.save()
        from ..views.contest import file
        file(request,info.ctime)

        return redirect(reverse('admin_news_list',args=(1)))

def admin_news_list(request,pIndex=1):
    if request.method == "GET":
        list = Info.objects.filter()
        pIndex = int(pIndex)
        page = Paginator.page(list,8)
        maxpages = page.num_pages
        plist = page.page_ranage
        if pIndex < 1 :
            pIndex = 1
        elif pIndex > maxpages:
            pIndex = maxpages

        list2 = page.page(pIndex)
        context = {'conlist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages}
        return render(request,'admin_news_list.html',context)


def admin_news_show(request,id):
    if request.method == "GET":
        try:
            info = Info.objects.get(id=id)
            return render(request,'admin_news_show.html',info)
        except:
            message = "文件不存在！"

