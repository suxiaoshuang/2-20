from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.urls import reverse

from ..models import Academy,User
from django.core.paginator import Paginator


def admin_show(request,pIndex):
    if User.objects.get(user_id=request.session.get('user_id')).permissions == 2:
        conlist = User.objects.filter(Q(identify='管理员')&Q(permissions=1))
        pIndex = int(pIndex)
        page = Paginator(conlist,10)
        maxpages = page.num_pages
        plist = page.page_range
        if pIndex > maxpages:
            pIndex = maxpages
        elif pIndex < 1:
            pIndex = 1
        conlist = page.page(pIndex)
        academy = Academy.objects.all()
        context = {'conlist':conlist,'pIndex':pIndex,'plist':plist,'maxpages':maxpages,'academy':academy}
        return render(request,'admin/admin_list.html',context)
    else:
        return redirect(reversed('admin_index'))



def add_admin(request):
    from login_register.views.views import hash_code
    if User.objects.get(user_id=request.session.get('user_id')).permissions == 2:
        if request.method == 'POST':
            try:
                data =  request.POST
                name = data.get('name')
                user_id = data.get('user_id')
                academy = data.get('academy')
                identify = data.get('identify')
                User.objects.create(name=name,user_id=user_id,academy=academy,identify='管理员',has_confirmed=True,permissions=1,password=hash_code('123456'))
                message = '添加成功！'
                return render(request,'admin/info.html',locals())
            except:
                message = '请重新操作！'
                return redirect(reverse(''))
    return redirect(reverse('admin_index'))


def disable(request,use_id):
    user = User.objects.get(id=use_id)
    user.has_confirmed = False
    user.save()
    return redirect(reverse(''))

def on(request,use_id):
    user = User.objects.get(id=use_id)
    user.has_confirmed = True
    user.save()
    return redirect(reverse())

def delete_user(request,use_id):
    User.objects.get(id=use_id).delete()
    return redirect(reverse())

def set_password(request,use_id):
    try:
        user = User.objects.get(id=use_id)
        from login_register.views.views import hash_code
        user.password = hash_code(user.user_id)
        message = '重置密码成功！'
    except:
        message = '服务器错误，请稍后再试。'
    return render(request,'',locals())



