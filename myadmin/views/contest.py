from pathlib import Path

from ..models import Contest, File, Stage, Tyep, Organizer,Registration,User
from django.shortcuts import render,HttpResponse,redirect
from django.db.models import Q, Count
from django.core.paginator import Paginator
from ..forms import PostForm
import os,datetime
from django.conf import settings
from django.urls import reverse

#审核竞赛申报
def audit_clist(request,pIndex):
    user_id = request.session.get('user_id')
    if int(User.objects.get(user_id=user_id).permissions) == 2:
        pIndex = int(pIndex)
        conlist = Contest.objects.filter(audit=False)
        page = Paginator(conlist, 15)
        maxpages = page.num_pages
        plist = page.page_range
        if pIndex > maxpages:
            pIndex = maxpages
        elif pIndex < 1:
            pIndex = 1
        conlist = page.page(pIndex)
        context = {'conlist':conlist,'maxpages':maxpages,'plist':plist,'pIndex':pIndex}
        return render(request,'admin/audit_clist.html',context)

    elif int(User.objects.get(user_id=user_id).permissions) < 2:
        message = '权限不足！不支持访问！'
        return render(request,'admin/info.html',locals())
def audit_con_pass(request,con_id,pIndex):
    con = Contest.objects.get(id=con_id)
    con.audit = True
    con.save()
    return redirect(reverse('audit_clist',args=(pIndex,)))


def audit_con_fail(request,con_id,pIndex):
    Contest.objects.get(id=con_id).delete()
    return redirect(reverse('audit_clist',args=(pIndex,)))


#竞赛列表
def contest_show(request,pIndex=1):
    con = Contest.objects
    mywhere = []
    list = con.filter(Q(contest_status__gte=1) & Q(audit=True))


    kw = request.GET.get('keyword',None)
    status = request.GET.get('status', None)



    if  status:
        list = con.filter(Q(contest_status = 0) & Q(audit=True))
        mywhere.append('status='+status)
        status = 'status='+status

    if kw:
        list = list.filter(Q(Q(contest_name__icontains=kw)|Q(contest_type__icontains=kw)) & Q(audit=True))
        mywhere.append("keyword="+kw)

    pIndex = int(pIndex)
    page = Paginator(list,10)

    maxpages = page.num_pages

    if pIndex <1:
        pIndex = 1

    if pIndex > maxpages:
        pIndex = maxpages

    list2 = page.page(pIndex)
    conlist = []

    for i in list2:
        num = 0
        for k in Registration.objects.filter(Q(con_id=i.id) & Q(status=True)):
            if k !=  None:
                num = num+1
        conlist.append((i,num))
        # print(conlist)


    plist = page.page_range
    context = {'conlist':conlist,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere,'status':status}

    return render(request,'admin/contest_show.html',context)

#竞赛报名列表
def con_open(request,pIndex=1):
    c = Contest.objects.filter(Q(contest_status__gte=1) & Q(audit=True))
    mywhere = []
    keyword = request.GET.get('keyword',None)
    if keyword:
        c = c.filter(Q(contest_name__icontains=keyword) & Q(audit=True))
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
            con.contest_pt = data.get('contest_pt')
            if int(User.objects.get(user_id=request.session.get('user_id')).permissions) == 2:
                con.audit = True
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
    if con.contest_status == 2:
        message = '报名进行中无法删除竞赛！'
        return render(request,'admin/info.html',locals())
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
    # 在竞赛审核通过前，如果是超级管理员就可以查看，否则不予查看
    if int(User.objects.get(user_id=request.session.get('user_id')).permissions) == 2:
        con = Contest.objects.get(Q(id=id) )
        form1 = PostForm()
        c_name = con.contest_name
        c_type = con.contest_type
        form1 = con.contest_info
        c_organizer = con.contest_organizer
        c_stage = con.contest_stage
        c_time = con.contest_time
        c_img = con.contest_img_path
        c_id = id
        c_status = con.contest_status
        permissions = User.objects.get(user_id=request.session.get('user_id')).permissions
        # print(permissions)
        try:
            f_time = con.contest_ctime

            f = File.objects.filter(file_ctime=f_time)

        except:
            print('error')

        return render(request,'admin/super_admin_con_info.html',locals())
    else:
        con = Contest.objects.get(Q(id=id) & Q(audit=True))
        form1 = PostForm()
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
    if con.contest_status == 2:
        message = '报名进行中无法结束竞赛！'
        return render(request,'admin/info.html',locals())
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
            file.file_name = i.name  # 文件名
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

            file.file_size = str(size_format(os.path.getsize(os.path.join(settings.FILE_UPLOAD[0], file_name))))
            file.save()

def admin_registration_audit(request,con_id,pIndex):
    if request.method == 'GET':
        conlist = Registration.objects.filter(Q(con_id=con_id) & Q(status=False))

        page =Paginator(conlist,15)
        pIndex  = int(pIndex)
        plist = page.page_range
        maxpages = page.num_pages
        if pIndex > maxpages:
            pIndex = maxpages
        elif pIndex < 1:
            pIndex = 1
        conlist = page.page(pIndex)
        context = {'conlist':conlist,'plist':plist,'maxpages':maxpages,'pIndex':pIndex}

        return render(request,'',context)
