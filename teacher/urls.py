from django.urls import path
from login_register.views.views import index
from .views.qualify_apply import apply,apply_list
from .views.comment import news_list,news_show,notice_list,notice_show,con_show


urlpatterns = [
    path('index/' , index, name='teacher_index'),
    path('apply/',apply,name='apply'),
    path('apply_list/',apply_list,name='apply_list'),

    path('tnews_show/<int:id>', news_show, name='tn_show'),
    path('tnews_list/<int:pIndex>', news_list, name='tn_list'),
    path('tnotice_show/<int:id>', notice_show, name='tnt_show'),
    path('tnotice_list/<int:pIndex>', notice_list, name="tnt_list"),
    path('tcon_show/<int:id>', con_show, name='tc_show'),
]