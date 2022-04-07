
from django.shortcuts import redirect, render


from django.urls import reverse

import re
from myadmin.models import User

class Middleware(object):
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if re.match(r'[/admin|/student|/teacher]{5,10}.+',path):

            url = re.match(r'[/admin|/student|/teacher]{5,10}.+',path)[0]
            str = re.findall(r'/(.{5,7})/',url)[0]
            # print(str)
            identify = request.session.get('identify')
            dic = {'学生':'student','教师':'teacher','管理员':'admin'}
            identify = dic.get(identify)
            list = ['student','admin','teacher']
            if not request.session.get('is_login',None):
                return redirect(reverse('login'))
            if str in list:
                if str not in identify and int(User.objects.get(user_id=request.session.get('user_id')).permissions) < 1:
                    return redirect(reverse(identify+"_index"))


        response = self.get_response(request)
        return response