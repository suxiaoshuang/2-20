from myadmin.models import User,Apply
from django.urls import reverse
from django.shortcuts import render,HttpResponse,redirect


def apply(request):
    user = User.objects.get(user_id=request.session.get('user_id'))
    if user.qualify_apply !=1:
        user.qualify_apply = 1
        Apply.objects.create(user_id=User.objects.get(user_id=request.session.get('user_id')).id,result='申请中')
        permissions = int(User.objects.get(user_id=request.session.get('user_id')).permissions)
        user.save()
    return redirect(reverse('apply_list'))


def apply_list(request):
    conlist = []
    if Apply.objects.filter(user_id=User.objects.get(user_id=request.session.get('user_id')).id).exists():
        for i in Apply.objects.filter(user_id=User.objects.get(user_id=request.session.get('user_id')).id):
            conlist.append((i,request.session.get('user_id'),request.session.get('user_name'),))


        # conlist = [(Apply.objects.filter(user_id=User.objects.get(user_id=request.session.get('user_id')).id),request.session.get('user_id'),request.session.get('user_name'),)]
    permissions = int(User.objects.get(user_id=request.session.get('user_id')).permissions)

    # print(conlist)
    return render(request,'teacher/qualify_apply.html',locals())
