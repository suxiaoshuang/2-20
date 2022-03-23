from django.urls import path,re_path
from .views.index import index,news_list,news_show,notice_list,notice_show,con_show,file_list

urlpatterns = [
    path('index/',index,name='uindex'),
    path('news_show/<int:id>',news_show,name='n_show'),
    path('news_list/<int:pIndex>',news_list,name='n_list'),
    path('notice_show/<int:id>',notice_show,name='nt_show'),
    path('notice_list/<int:pIndex>',notice_list,name="nt_list"),
    path('con_show/<int:id>',con_show,name='c_show'),
]