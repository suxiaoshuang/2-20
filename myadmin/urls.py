from django.urls import path,re_path
from login_register.views.views import index
from .views.contest import con_open,contest_show,con_add,con_delete,img,con_info,con_close,con_off,con_on,admin_registration_audit,audit_clist,audit_con_pass,audit_con_fail
from .views.student import stu_show,stu_add,stu_delete,stu_update
from .views.teacher import tea_add,tea_show,tea_update,tea_delete
from .views.admins import admin_show
from .views.news import admin_news_add,admin_news_show,admin_news_list,admin_news_delete
from .views.notice import n_list,n_show,n_add,n_delete

urlpatterns = [
    path('index/',index,name='admin_index'),
    path('contest_show/<int:pIndex>',contest_show,name="admin_contest_show"),
    path('contest_add/',con_add,name="admin_contest_add"),
    path('contest_info/<int:id>',con_info,name="admin_contest_info"),
    path('contest_registration/<int:pIndex>',con_open,name="admin_contest_registration"),
    path('contest_on/<int:id>',con_on,name="admin_contest_on"),
    path('contest_off/<int:id>',con_off,name="admin_contest_off"),
    path('contest_delete/<int:id>',con_delete,name="admin_contest_delete"),
    path('contest_close/<int:id>',con_close,name="admin_contest_close"),



    path('student_delete/<int:id>',stu_delete,name="admin_stu_delete"),
    path('student_update/<int:id>',stu_update,name="admin_stu_update"),
    path('student_add/',stu_add,name="admin_stu_add"),
    path('student_show/<int:pIndex>',stu_show,name="admin_stu_show"),

    path('teacher_show/<int:pIndex>',tea_show,name="admin_tea_show"),
    path('teacher_update/<int:id>',tea_update,name="admin_tea_update"),
    path('teacher_delete/<int:id>',tea_delete,name="admin_tea_delete"),
    path('teacher_add/',tea_add,name="admin_tea_add"),


    path('admin_show/<int:pIndex>',admin_show,name="admin_admin_show"),

    path('admin_news_add/',admin_news_add,name="admin_news_add"),
    path('admin_news_show/<int:id>',admin_news_show,name="admin_news_show"),
    path('admin_news_list/<int:pIndex>',admin_news_list,name="admin_news_list"),
    path('admin_news_delete/<int:id>',admin_news_delete,name="admin_news_delete"),


    path('admin_notice_add/', n_add, name="notice_add"),
    path('admin_notice_list/<int:pIndex>', n_list, name="notice_list"),
    path('admin_notice_delete/<int:id>', n_delete, name="notice_delete"),
    path('admin_notice_show/<int:id>', n_show, name="notice_show"),

    re_path('admin_registration/(?P<con_id>[0-9].*)/(?P<pIndex>[0-9].*)',admin_registration_audit,name='admin_regristration_audit'),
    path('admin_audit_contest_list/<int:pIndex>',audit_clist,name='audit_clist'),
    path('admin_audit_contest/<int:con_id>/<int:pIndex>',audit_con_pass,name='audit_con_pass'),
    path('admin_audit_contest_fail/<int:con_id>/<int:pIndex>',audit_con_fail,name='audit_con_fail'),
    path('img/',img,name="img"),

]