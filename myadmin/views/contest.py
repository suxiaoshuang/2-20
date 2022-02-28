from ..models import Contest,File
from django.shortcuts import render,HttpResponse,redirect
from django.db.models import Q
from django.core.paginator import Paginator
from ..forms import PostForm
import os,datetime
from django.conf import settings
from django.urls import reverse



def contest_show(request,pIndex=1):
    con = Contest.objects
    mywhere = []
    list = con.filter(contest_status=1)

    kw = request.GET.get('keyword',None)
    status = request.GET.get('status', None)


    if  status:
        list = con.filter(contest_status=0)
        mywhere.append('status='+status)
        status = 'status='+status

    if kw:
        list = list.filter(Q(contest_name__contains=kw)|Q(contest_organizer__contains=kw))
        mywhere.append("keyword="+kw)

    pIndex = int(pIndex)
    try:
        page = Paginator(list,1)
    except :
        pass
    maxpages = page.num_pages

    if pIndex <1:
        pIndex = 1

    if pIndex > maxpages:
        pIndex = maxpages

    list2 = page.page(pIndex)
    plist = page.page_range


    context = {'conlist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere,'status':status}

    return render(request,'admin/contest_show.html',context)


def con_open(request):
    pass


def con_add(request):
    if request.session.get("is_login",None):
        user_name = request.session.get("user_name")
        user_id = request.session.get("user_id")
    if request.method == 'POST':

        form1 = PostForm(request.POST)
        con = Contest()
        data = request.POST
        date_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

        #图片存储
        if request.FILES.get('contest_img',None):
            img = request.FILES.get('contest_img')
            img_name = img.name
            tail = os.path.splitext(img_name)[1]         #
            img_name = ''.join((date_time,tail))                 #
            img_path = os.path.join(settings.IMG_UPLOAD[0],img_name)   #图片的绝对路径
            with open(img_path,'ab') as f:
                for chunk in img.chunks():
                    f.write(chunk)
                f.close()


            #竞赛信息存储
            con.contest_name = data.get('contest_name')
            con.contest_type = data.get('contest_type')
            con.contest_organizer = data.get('contest_organizer')
            con.contest_time = data.get('contest_time')
            con.contest_stage = data.get('contest_stage')
            con.contest_info = data.get('content')
            con.contest_img_path = os.path.join('upload_file/',img_name)    #相对路径
            con.contest_ctime = date_time
            con.save()

        #附件
        if request.FILES.get('files',None):
            files = request.FILES.getlist('files')
            for i in files:
                file = File()
                file.file_name = os.path.splitext(i.name)[0]              #文件名
                print(file.file_name)
                file_tail = os.path.splitext(i.name)[1]                   #文件后缀
                file.file_ctime = date_time
                file.file_user_name = user_name
                file.file_user_id = user_id
                file_name = ''.join((date_time,'-'+os.path.splitext(i.name)[0]+file_tail))   #拼装文件名字
                print(file_name)
                file.file_path = os.path.join('upload/',file_name)          #相对路径

                with open(os.path.join(settings.IMG_UPLOAD[0],file_name),'ab') as f:
                    for chunk in i.chunks():
                        f.write(chunk)
                    f.close()
                file.save()

        return redirect(reverse('admin_contest_show',args=(1,)))

    else:
        form1 = PostForm()
        return render(request, 'admin/contest_add.html', locals())






def con_delete(request,id):
    con = Contest.objects.get(id=id)
    con_time = con.contest_ctime
    file = File.objects.filter(file_ctime=con_time)
    if file:
        file.delete()
    con.delete()

    return redirect(request,reverse('admin_contest_show',args=(1)))




def con_update(request,id):
    if request.method == "GET":
        form1 = PostForm()

        con = Contest.objects.get(id=id)
        c_name = con.contest_name
        c_type = con.contest_type
        form1.content = con.contest_info
        c_organizer = con.contest_organizer
        c_stage = con.contest_stage
        c_time = con.contest_time
        c_img = con.contest_img_path

        return render(request,'admin/contest_update.html',locals())


    elif request.method=="POST":
        con = Contest.objects.get(id=id)
        data = request.POST
        con.contest_time = data.get('c_time')
        con.contest_stage = data.get('c_stage')
        con.contest_name = data.get('c_name')
        con.contest_organizer = data.get('c_organizer')
        con.contest_info = data.get('content')
        con.contest_type = data.get('c_type')

        c_time = con.contest_ctime

        file(request,c_time)
        img_path = img(request)
        if img_path:
            con.contest_img_path = img_path

        return redirect(request,reverse('admin_contest_update',args=(id)))


def con_info(request,id):
    return render(request,'admin/contest_info.html')

def con_close(request,id):
    pass

def img(request):
    if request.FILES.get('img', None):
        img = request.FILES.get('img')
        date_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        img_name = img.name
        tail = os.path.splitext(img_name)[1]  #文件后缀名
        img_name = ''.join((date_time, tail))  #拼接新文件名
        img_path = os.path.join(settings.IMG_UPLOAD[0], img_name)  # 图片的绝对路径
        with open(img_path, 'ab') as f:
            for chunk in img.chunks():
                f.write(chunk)
            f.close()
        img_path = os.path.join('upload_file/',img_name)    #相对路径

    return img_path


def file(request,date_time):
    if request.session.get("is_login",None):
        user_name = request.session.get("user_name")
        user_id = request.session.get("user_id")

    if request.FILES.get('files', None):
        files = request.FILES.getlist('files')
        for i in files:
            file = File()
            file.file_name = os.path.splitext(i.name)[0]  # 文件名
            print(file.file_name)
            file_tail = os.path.splitext(i.name)[1]  # 文件后缀
            file.file_ctime = date_time
            file.file_user_name = user_name
            file.file_user_id = user_id
            file_name = ''.join((date_time, '-' + os.path.splitext(i.name)[0] + file_tail))  # 拼装文件名字
            print(file_name)
            file.file_path = os.path.join('upload/', file_name)  # 相对路径

            with open(os.path.join(settings.IMG_UPLOAD[0], file_name), 'ab') as f:
                for chunk in i.chunks():
                    f.write(chunk)
                f.close()
            file.save()

