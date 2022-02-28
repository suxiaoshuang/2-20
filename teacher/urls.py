from django.urls import path
from login_register.views.views import index


urlpatterns = [
    path('index/' , index, name='teacher_index'),
]