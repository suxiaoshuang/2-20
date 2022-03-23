from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from ..models import Info, Organizer, File
import datetime
from ..forms import PostForm

def admin_news_add(request):
    if request.method == "GET":
        organizer = Organizer.objects.filter()
        information = PostForm()
        return render(request,'admin/admin_news_add.html',locals())

    elif request.method == "POST":
        info = Info()
        df = request.POST
        info.title = df.get('title')
        info.text = df.get('content')
        info.ctime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        info.come_from = df.get('come_from')

        from ..views.contest import file,img
        file(request,info.ctime)
        info.img_path = img(request)
        info.type = 'news'
        info.save()

        return redirect(reverse('admin_news_list',args=(1,)))

def admin_news_list(request,pIndex=1):
    if request.method == "GET":
        mywhere = []
        keyword = request.GET.get('keyword',None)
        if keyword:
            list = Info.objects.filter(Q(title__icontains=keyword)&Q(type='news'))
            mywhere.append('keyword='+keyword)
        else:
            list = Info.objects.filter(type='news')
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
        return render(request,'admin/admin_news_list.html',context)



def admin_news_show(request,id):
    if request.method == "GET":
        try:
            info = Info.objects.get(id=id)
            f_time = info.ctime
            file = File.objects.filter(file_ctime=f_time)
            return render(request,'admin/admin_news_show.html',locals())
        except:
            message = "文件不存在！"
            url = request.path_info
            return render(request,'admin/info.html',locals())


def admin_news_delete(request,id):
    if request.method == "GET":
        try:
            news = Info.objects.get(id=id)
            f_time = news.ctime
            file = File.objects.filter(file_ctime=f_time)
            if file:
                file.delete()
            news.delete()
            pIndex = request.GET.get('pIndex')
            return redirect(reverse('admin_news_list',args=(pIndex,)))
        except:
            message = '删除文件不存在'
            return render(request,'admin/info.html')