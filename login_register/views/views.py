from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse

from myadmin.models import User,ConfirmString,Contest
import hashlib
import datetime
import base64
import socket
import ssl

# Create your views here.
from django.conf import settings


def mailSocket(_username,_password,recver,_subject,text):
    mailserver = ('smtp.qq.com', 465)
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sslclientSocket = ssl.wrap_socket(clientSocket, cert_reqs=ssl.CERT_NONE,
                                      ssl_version=ssl.PROTOCOL_SSLv23)
    print('连接中.........')
    sslclientSocket.connect(mailserver)
    recv = sslclientSocket.recv(1024).decode('utf-8')
    if recv[:3] != '220':
        print('连接失败， 重新连接')
        mailSocket()
    print(recv)  # 220 smtp.qq.com Esmtp QQ Mail Server
    print('连接成功..........')

    # 服务器响应
    sslclientSocket.send(b'HELO qq.com\r\n')
    recv = sslclientSocket.recv(1024).decode()
    print(recv)  # 250 smtp.qq.com
    # 发送登录请求
    sslclientSocket.send(b'AUTH login\r\n')
    recv2 = sslclientSocket.recv(1024).decode('utf-8')
    print(recv2)  # 334 VXNlcm5hbWU6
    # 开始登陆

    username = b'%s\r\n' % base64.b64encode(_username.encode('utf-8'))
    password = b'%s\r\n' % base64.b64encode(_password.encode('utf-8'))
    sslclientSocket.send(username)
    recv = sslclientSocket.recv(1024).decode('utf-8')
    print('username = ', recv)  # 334 UGFzc3dvcmQ6
    sslclientSocket.send(password)
    recv = sslclientSocket.recv(1024).decode()
    print('password = ', recv)  # 235 Authentication successful
    if recv[:3] == '235':
        send(_username,_password,sslclientSocket, recver, _subject, text,)

def send(_username,_password,sslclientSocket, recver, _subject, text):
    mailSender = b'MAIL FROM:<%s>\r\n' % _username.encode('utf-8')
    sslclientSocket.send(mailSender)

    recver = recver
    mailrecv = b'RCPT TO:<%s>\r\n' % recver.encode('utf-8')
    sslclientSocket.send(mailrecv)

    recv = sslclientSocket.recv(1024).decode()
    print(recv)  # 250 OK


    data = b'DATA\r\n'
    sslclientSocket.send(data)
    recv = sslclientSocket.recv(1024).decode()
    print(recv)  # 250 Ok

    # 邮件主题 subject
    _subject = _subject
    subject = b'Subject: %s\r\n' % _subject.encode('utf-8')
    sslclientSocket.send(subject)
    _text = b'%s\r\n' % text.encode('utf-8')
    sslclientSocket.send(_text)


    print('发送结束...')
    sslclientSocket.send(b'\r\n.\r\n')

    sslclientSocket.send(b'QUIT\r\n')

    sslclientSocket.close()




def send_email(email, code):
    subject = '注册邮件'
    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    这里是刘江的博客和教程站点，专注于Python、Django和机器学习技术的分享！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    mailSocket('2955978765@qq.com','ldbonccetknxdcgb',email,subject,html_content)
    # send_mail(subject=subject, message=html_content, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[email])
    # msg.attach_alternative(html_content, 'text/html')
    # msg.send()


def make_confirmed_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    ConfirmString.objects.create(code=code, user=user)
    return code


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def index(request):
    return redirect(reverse('uindex'))


def login(request):
    if request.session.get('is_login', None):
        try:
            identify = request.session.get('identify')
            dic = {'学生':'student','教师':'teacher','管理员':'admin'}

            return redirect(reverse(dic.get(identify)+'_index'))
        except:
            pass

    if request.method == 'POST':
        # login_form = forms.UserForm(request.POST)

        message = '请检查填写的内容！'

        try:
            data = request.POST
            user_id = data['user_id']
            password = data['password']
            user = User.objects.get(user_id=user_id)

        except:
            message = '用户不存在！'
            return render(request, 'login/re.html', locals())

        if user.password == hash_code(password):
            if data['identify'] == user.identify:
                request.session['is_login'] = True
                request.session['user_id'] = user.user_id
                request.session['user_name'] = user.name
                request.session['identify'] = user.identify
                dic = {'学生': 'student', '教师': 'teacher', '管理员': 'admin'}
                return redirect(reverse(dic.get(user.identify)+'_index'),locals())
            else:
                message = '请选择正确的身份进行登录!'
                return render(request,'login/re.html',locals())
        else:
            message = '密码不正确!'
            return render(request, 'login/re.html',locals())
    else:
        return render(request, 'login/re.html',locals())

    # login_form = forms.UserForm()
    # return render(request, 'login/re.html', locals())


def register(request):
    if request.session.get('is_login', None):
        identify = request.session.get('identify')
        dic = {'学生':'student','教师':'teacher','管理员':'admin'}
        return redirect(dic.get(identify)+'_index')

    if request.method == 'POST':

        message = '请检查填写的内容'
        user_id = request.POST.get('user_id')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        # sex = request.POST.get('sex')
        name = request.POST.get('name')
        identify = request.POST.get('identify')
        academy = request.POST.get('academy')
        grade = request.POST.get('grade')
        specialty = request.POST.get('specialty')

        if password1 != password2:
            message = '两次输入的密码不同！'
            return render(request, 'login/re.html', locals())
        else:
            same_name_user = User.objects.filter(name=user_id)
            if same_name_user:
                message = '用户名已存在！'
                return render(request, 'login/re.html', locals())
            same_name_email =User.objects.filter(email=email)
            if same_name_email:
                message = '该邮箱已被注册！'
                return render(request, 'login/re.html', locals())

            new_user = User()
            new_user.name = name
            new_user.password = password1
            new_user.password = hash_code(password1)
            new_user.email = email
            # new_user.sex = sex
            new_user.identify = identify
            new_user.user_id = user_id
            new_user.grade = grade
            new_user.academy =academy
            new_user.specialty = specialty
            new_user.save()
            code = make_confirmed_string(new_user)
            send_email(email, code)

            message = '注册成功，请前往邮箱进行确认！'

            return redirect(reverse('login'))
    else:
        return render(request, 'login/re.html', locals())



def logout(request):
    if not request.session['is_login']:
        identify = request.session.get('identify')
        dic = {'学生':'student','教师':'teacher','管理员':'admin'}
        return redirect(dic.get(identify)+'_index')
    request.session.flush()
    return redirect(reverse('login'))


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求！'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已过期，请重新注册！'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())