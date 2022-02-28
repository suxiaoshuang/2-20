from django.shortcuts import redirect
from django.urls import reverse

import re


class Middleware(object):
    def __init__(self,get_response):
        self.get_response = get_response
        print("Middleware")

    def __call__(self, request):
        path = request.path
        if re.match(r'[/admin|/student|/teacher]{5,10}.+',path):
            print(re.match(r'[/admin|/student|/teacher]{5,10}.+',path))
            if not request.session.get('is_login',None):
                return redirect(reverse('login'))

        response = self.get_response(request)
        return response