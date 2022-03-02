from django.shortcuts import render,HttpResponse,redirect
from django.db.models import Q
from django.core.paginator import Paginator
import os,datetime
from django.conf import settings
from django.urls import reverse
from ..models import User
from django.views.decorators.csrf import csrf_exempt

def stu_show(request,pIndex=1):
    stu = User.objects.filter(identify='学生')
    mywhere = []
    keyword = request.GET.get('keyword',None)
    if keyword:
        stu = stu.filter(Q(user_id=keyword)|Q(name__icontains=keyword))
        mywhere.append("keyword="+keyword)

    pIndex = int(pIndex)
    page = Paginator(stu,10)
    maxpages = page.num_pages
    if pIndex < 1:
        pIndex = 1
    elif pIndex > maxpages:
        pIndex = maxpages

    data = page.page(pIndex)
    plist = page.page_range
    context = {'conlist':data,'plist':plist,'maxpages':maxpages,'pIndex':pIndex,'mywhere':mywhere}

    return render(request,'admin/student_show.html',context)


def stu_delete(request,id):
    stu = User.objects.get(id=id)
    stu.delete()
    pIndex = request.GET.get('pIndex')

    return redirect(reverse('admin_stu_show',args=(pIndex,)))

def stu_update(request,id):
    if request.method == "GET":
        stu = User.objects.get(id=id)
        id = id
        s_id = stu.user_id
        s_name = stu.name
        s_email = stu.email
        s_academy = stu.academy
        s_specialty = stu.specialty
        s_grade = stu.grade

        return render(request,'admin/student_update.html',locals())
    elif request.method == "POST":
        data = request.POST
        stu = User.objects.get(id=id)
        stu.user_id = data.get('s_id')
        stu.name = data.get('s_name')
        stu.grade = data.get('s_grade')
        stu.specialty = data.get("s_specialty")
        stu.academy = data.get("s_academy")
        stu.email = data.get("s_email")
        stu.save()

        return redirect(reverse('admin_stu_update',args=(id,)))


import pandas as pd
from login_register.views.views import hash_code
@csrf_exempt

def stu_add(request):
    if request.method == "POST":
        data = request.FILES.items()
        for i,ob in data:
            name = ob.name
            tail = os.path.splitext(name)[1]
            name = ''.join((datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),tail))
            url = os.path.join(settings.FILE_UPLOAD[0],name)
            print(url)
            with open(url,'ab')as f:
                for chunk in ob.chunks():
                 f.write(chunk)
            f.close()
            ds = pd.read_excel(url,error_bad_lines=False)
            try:
                for index, row in ds.iterrows():
                    user = User()
                    user.name = row['name']
                    user.user_id = row.user_id
                    user.email = str(row.email)
                    user.grade = row.grade
                    user.academy = row.academy
                    user.specialty = row.specialty
                    user.identify = '学生'
                    user.c_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    user.has_confirmed = True
                    user.password = hash_code('123456')
                    user.save()
            except:
                print('error')

    return redirect(reverse('admin_stu_show',args=(1,)))