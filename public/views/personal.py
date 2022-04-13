from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render,redirect
from myadmin.models import Academy,Specialty,User
from myadmin.encryption import PrpCrypt
from django.contrib import messages

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        user_id = request.POST.get('user_id', None)
        try:
            User.objects.get(Q(email=email) & Q(user_id=user_id))
        except:
            return
        from login_register.views.views import mailSocket
        # 对user_id,email进行加密
        pc = PrpCrypt('keyskeyskeyskeys')  # 初始化密钥
        user = pc.encrypt(user_id)
        ema = pc.encrypt(email)

        subject = '修改密码邮件'
        html_content = '''
                            此链接为学科竞赛组织管理平台的修改密码确认链接，如果不是用户本人请忽略。http://{}/public/update_password/{}/{}，
                            请点击站点链接进行密码修改！

                            '''.format('127.0.0.1:8000', user, ema)
        mailSocket('2955978765@qq.com', 'ldbonccetknxdcgb', email, subject, html_content)
        message = '请求已提交，服务器已向注册邮箱发送确认邮件，请至邮箱进行确认！'
        print(user, '\n', ema, '\n', email)
        return render(request,'public/info.html',locals())
    else:
        return render(request,'public/forget_password.html')


#忘记密码后的修改密码
def update_password(request,user_id,email):
    pc = PrpCrypt('keyskeyskeyskeys')  # 初始化密钥
    id = pc.decrypt(user_id)
    ema = pc.decrypt(email)
    print(id,ema)
    user_id = user_id
    if request.method == 'POST':
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        if password == password1:
            from login_register.views.views import hash_code
            user = User.objects.get(Q(user_id=id)&Q(email=ema))
            user.password = hash_code(password)
            user.save()
            messages.success(request,'修改密码成功，请重新登录！')
            return redirect(reverse('login'))
        else:
            messages.error(request,'两次输入的密码不一致！')
            return redirect(reverse('update_password',args=(user_id,email,)))
    return render(request,'public/update_password.html',locals())

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
    return render(request,'public/user.html',locals())

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
        return render(request, 'public/update_user.html', locals())
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