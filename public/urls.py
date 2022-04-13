from django.urls import path,re_path
from .views.index import index,news_list,news_show,notice_list,notice_show,con_show,file_list
from .views.download import work,file
from .views.personal import forget_password,user,update_password,update_user,delete_user
urlpatterns = [
    path('index/',index,name='uindex'),
    path('news_show/<int:id>',news_show,name='n_show'),
    path('news_list/<int:pIndex>',news_list,name='n_list'),
    path('notice_show/<int:id>',notice_show,name='nt_show'),
    path('notice_list/<int:pIndex>',notice_list,name="nt_list"),
    path('con_show/<int:id>',con_show,name='c_show'),
    re_path('work/(?P<url>.*)',work,name='dwork'),
    re_path('file/(?P<url>.*)',work,name='dfile'),

    path('forget_password/',forget_password,name='forget_password'),
    re_path('update_password/(?P<user_id>.*)/(?P<email>.*)',update_password,name='update_password'),
    path('user/',user,name='user'),
    path('delete_user/',delete_user,name='delete_user'),
    path('update_user/',update_user,name='update_user'),
]