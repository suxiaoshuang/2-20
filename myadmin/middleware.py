from django.shortcuts import redirect,render
from django.urls import reverse

import re


class Middleware(object):
    def __init__(self,get_response):
        self.get_response = get_response
        print("Middleware")

    def __call__(self, request):
        path = request.path
        if re.match(r'[/admin|/student|/teacher]{5,10}.+',path):
            url = re.match(r'[/admin|/student|/teacher]{5,10}.+',path)[0].replace('/','')[:5]
            identify = request.session.get('identify')
            dic = {'学生':'student','教师':'teacher','管理员':'admin'}
            identify = dic.get(identify)
            if not request.session.get('is_login',None):
                return redirect(reverse('login'))
            elif url not in identify:
                return render(request,identify+'/index.html')

        response = self.get_response(request)
        return response