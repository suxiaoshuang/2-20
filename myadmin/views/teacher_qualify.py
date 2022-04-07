from django.shortcuts import render,HttpResponse,redirect
from django.db.models import Q
from django.core.paginator import Paginator
import os,datetime
from django.conf import settings
from django.urls import reverse
from ..models import User,Apply
from django.views.decorators.csrf import csrf_exempt

def tea_qualify_apply_list(request,pIndex):
    data = []
    if int(User.objects.get(user_id=request.session.get('user_id')).permissions) == 2:
        user = User.objects.filter((Q(identify='教师') & Q(qualify_apply=1)) | (Q(permissions=1) & Q(identify='教师')))
        print(user)
        for i in user:
            data.append((i,Apply.objects.filter(user_id=i.id)[0].time,))
        pIndex = int(pIndex)

        page = Paginator(data, 5)
        plist = page.page_range
        maxpages = page.num_pages
        if pIndex > maxpages:
            pIndex = maxpages
        elif pIndex < 1:
            pIndex = 1
        conlist = page.page(pIndex)
        context = {'conlist': conlist, 'maxpages': maxpages, 'plist': plist, 'pIndex': pIndex}

        return render(request, 'admin/tea_qualify_apply.html', context)
    else:
        message = '权限不足'
        return render(request,'admin/info.html',locals())


def tea_qualify_apply(request,user_id,qualify,pIndex):
    if int(qualify) == 1:
        user = User.objects.get(user_id=user_id)
        user.permissions = 1
        apply = Apply.objects.filter(user_id=User.objects.get(user_id=user_id).id)[0]
        apply.result = '申请已同意'
        user.save()
        apply.save()
    elif int(qualify) == 0:
        user = User.objects.get(user_id=user_id)
        user.qualify_apply = 0
        user.permissions = 0
        apply = Apply.objects.filter(user_id=User.objects.get(user_id=user_id).id)[0]
        apply.result = '权限已取消'
        user.save()
        apply.save()

    user = User.objects.get(user_id=user_id)
    user.qualify_apply = 0
    user.save()

    return redirect(reverse('tea_qualify_apply_list',args=(pIndex,)))







