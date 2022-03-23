from django.shortcuts import render

from ..models import Academy,User



def admin_show(request,pIndex):
    pass



def add_admin(request):
    from login_register.views.views import hash_code
    if request.method == 'GET':
        academy = Academy.objects.all()

        context = {'academy':academy}
        return render()

    if request.method == 'POST':
        data =  request.POST
        name = data.get('name')
        user_id = data.get('user_id')
        academy = data.get('academy')
        identify = data.get('identify')
        User.objects.create(name=name,user_id=user_id,academy=academy,identify='管理员',has_confirmed=True,permissions=1,password=hash_code('123456'))
        message = '添加成功！'
        return render(request,'admin/info.html',locals())