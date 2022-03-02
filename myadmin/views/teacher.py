import pandas as pd
from django.shortcuts import render,HttpResponse,redirect
from django.db.models import Q
from django.core.paginator import Paginator
import os,datetime
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from login_register.views.views import hash_code
from ..models import User


@csrf_exempt
def tea_add(request):
    if request.method == "POST":
        data = request.FILES.items()
        for i, ob in data:
            name = ob.name
            tail = os.path.splitext(name)[1]
            name = ''.join((datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), tail))
            url = os.path.join(settings.FILE_UPLOAD[0], name)
            print(url)
            with open(url, 'ab')as f:
                for chunk in ob.chunks():
                    f.write(chunk)
            f.close()
            ds = pd.read_excel(url, error_bad_lines=False)

            for index, row in ds.iterrows():
                user = User()
                user.name = row['name']
                user.user_id = row.user_id
                user.email = str(row.email)
                user.specialty = row.specialty
                user.identify = '教师'
                user.c_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                user.has_confirmed = True
                user.password = hash_code('123456')
                user.save()


    return redirect(reverse('admin_tea_show', args=(1,)))

def tea_show(request,pIndex=1):
    stu = User.objects.filter(identify='教师')
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

    return render(request,'admin/teacher_show.html',context)

def tea_update(request,id):
    if request.method == "GET":
        stu = User.objects.get(id=id)
        id = id
        s_id = stu.user_id
        s_name = stu.name
        s_email = stu.email
        s_specialty = stu.specialty


        return render(request,'admin/teacher_update.html',locals())
    elif request.method == "POST":
        data = request.POST
        stu = User.objects.get(id=id)
        stu.user_id = data.get('s_id')
        stu.name = data.get('s_name')
        stu.specialty = data.get("s_specialty")

        stu.email = data.get("s_email")
        stu.save()

        return redirect(reverse('admin_tea_update',args=(id,)))

def tea_delete(request,id):
    stu = User.objects.get(id=id)
    stu.delete()
    pIndex = request.GET.get('pIndex')

    return redirect(reverse('admin_tea_show',args=(pIndex,)))