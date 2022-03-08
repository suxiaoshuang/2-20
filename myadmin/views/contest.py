from pathlib import Path

from ..models import Contest, File, Stage, Tyep, Organizer
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
    list = con.filter(contest_status__gte=1)

    kw = request.GET.get('keyword',None)
    status = request.GET.get('status', None)


    if  status:
        list = con.filter(contest_status = 0)
        mywhere.append('status='+status)
        status = 'status='+status

    if kw:
        list = list.filter(Q(contest_name__icontains=kw)|Q(contest_type__icontains=kw))
        mywhere.append("keyword="+kw)

    pIndex = int(pIndex)
    page = Paginator(list,10)

    maxpages = page.num_pages

    if pIndex <1:
        pIndex = 1

    if pIndex > maxpages:
        pIndex = maxpages

    list2 = page.page(pIndex)
    plist = page.page_range


    context = {'conlist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere,'status':status}

    return render(request,'admin/contest_show.html',context)


def con_open(request,pIndex=1):
    c = Contest.objects.filter(contest_status__gte=1)
    mywhere = []
    keyword = request.GET.get('keyword',None)
    if keyword:
        c = c.filter(Q(contest_name__icontains=keyword))
        mywhere.append("keyword="+keyword)

    pIndex = int(pIndex)
    page = Paginator(c,5)
    maxpages = page.num_pages

    if pIndex < 1:
        pIndex = 1

    if pIndex > maxpages:
        pIndex = maxpages

    list2 = page.page(pIndex)
    plist = page.page_range
    context = {'conlist':list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    # print(context)
    return render(request,'admin/contest_registration.html',context)


def con_on(request,id):
    c = Contest.objects.get(id=id)
    c.contest_status = 2
    pIndex = request.GET.get('pIndex')
    c.save()

    return redirect(reverse('admin_contest_registration',args=(pIndex)))




def con_off(request,id):
    c = Contest.objects.get(id=id)
    c.contest_status = 1
    pIndex = request.GET.get('pIndex')
    c.save()

    return redirect(reverse('admin_contest_registration',args=(pIndex)))









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

            print(settings.BASE_DIR)
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
            con.contest_img_path = os.path.join('upload_images/',img_name)    #相对路径
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
                file.file_path = os.path.join('upload_file/',file_name)          #相对路径


                with open(os.path.join(settings.FILE_UPLOAD[0],file_name),'ab') as f:
                    for chunk in i.chunks():
                        f.write(chunk)
                    f.close()
                file.file_size = str(size_format(os.path.getsize(os.path.join(settings.FILE_UPLOAD[0],file_name))))
                file.save()

        return redirect(reverse('admin_contest_show',args=(1,)))

    else:
        form1 = PostForm()
        type = Tyep.objects.filter()
        stage = Stage.objects.filter()
        organizer = Organizer.objects.filter()
        return render(request, 'admin/contest_add.html', locals())






def con_delete(request,id):
    con = Contest.objects.get(id=id)
    con_time = con.contest_ctime
    file = File.objects.filter(file_ctime=con_time)
    pIndex = request.GET.get('pIndex')
    if file:                #如果有附件,就把附件delete。
        for i in file:
            url = os.path.join(settings.FILE_UPLOAD[0],i.file_path.replace('upload_file/',''))
            os.remove(url)
            i.delete()
    con.delete()
    status = request.GET.get('mywhere')
    return redirect(reverse('admin_contest_show',args=(1,)),locals())




def con_info(request,id):
    if request.method == "GET":
        form1 = PostForm()

        con = Contest.objects.get(id=id)
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
            print('error')



        return render(request,'admin/contest_info.html',locals())


def size_format(size):
    if size < 1000:
        return '%i' % size + 'size'
    elif 1000 <= size < 1000000:
        return '%.1f' % float(size/1000) + 'KB'
    elif 1000000 <= size < 1000000000:
        return '%.1f' % float(size/1000000) + 'MB'
    elif 1000000000 <= size < 1000000000000:
        return '%.1f' % float(size/1000000000) + 'GB'
    elif 1000000000000 <= size:
        return '%.1f' % float(size/1000000000000) + 'TB'



def con_close(request,id):
    con = Contest.objects.get(id=id)
    con.contest_status = 0
    con.save()
    pIndex = request.GET.get('pIndex')
    return redirect(reverse('admin_contest_show',args=(pIndex,)))

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
        img_path = os.path.join('upload_images/',img_name)    #相对路径

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
            file.file_path = os.path.join('upload_file/', file_name)  # 相对路径

            with open(os.path.join(settings.FILE_UPLOAD[0], file_name), 'ab') as f:
                for chunk in i.chunks():
                    f.write(chunk)
                f.close()
            file.save()

