
from django.urls import reverse
from django.shortcuts import render,redirect
from myadmin.models import Academy,Specialty,User
from django.contrib import messages

#用户个人页面
def user(request):
    user = User.objects.get(user_id=request.session.get('user_id'))
    name = user.name
    user_id = user.user_id
    academy = user.academy
    if user.identify == '学生':
        specialty = user.specialty
        grade = user.grade
    identify = user.identify
    email = user.email
    time = user.c_time
    return render(request,'admin/user.html',locals())

#注销账户
def delete_user(request):
    user = User.objects.get(user_id=request.session.get('user_id'))
    user.has_confirmed = False
    return redirect(reverse('logout'))


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def update_user(request):
    if request.method == 'GET':
        user = User.objects.get(user_id=request.session.get('user_id'))
        name = user.name
        user_id = user.user_id
        academy = Academy.objects.all()
        aca = user.academy
        if user.identify == '学生':
            specialty = Specialty.objects.all()
            spe = user.specialty
            grade = user.grade
        identify = user.identify
        email = user.email
        time = user.c_time
        return render(request, 'admin/update_user.html', locals())
    else:
        user = User.objects.get(user_id=request.session.get('user_id'))
        user.name = request.POST.get('name')
        # user.user_id = request.POST.get('user_id')
        user.academy = request.POST.get('academy')
        user.specialty = request.POST.get('specialty')
        user.grade = request.POST.get('grade')
        user.email = request.POST.get('email')
        # request.session['user_id'] = user.user_id
        # request.session['user_name'] = user.name
        print(user.name,user.user_id,user.academy,user.specialty,user.grade,user.email)
        user.save()
        messages.success(request,'修改成功！')
        return redirect(reverse('user'))