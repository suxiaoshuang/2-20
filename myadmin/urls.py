from django.urls import path,re_path
from login_register.views.views import index
from .views.contest import con_open,contest_show,con_add,con_delete,img,con_info,con_close,con_off,con_on,admin_registration_audit,audit_clist,audit_con_pass,audit_con_fail,audit_registration_list,admin_registration_audit,reg_audit_fail,reg_audit_pass
from .views.student import stu_show,stu_add,stu_delete,stu_update
from .views.teacher import tea_add,tea_show,tea_update,tea_delete
from .views.admins import admin_show
from .views.news import admin_news_add,admin_news_show,admin_news_list,admin_news_delete
from .views.notice import n_list,n_show,n_add,n_delete
from .views.match import match_con_show,match_team_list,match_wq,match_stu,count,match_con_count_list,match_con_team\
,match_result_export
from .views.work import f_down,f_up,s_down,s_up,t_down,t_up
from .views.teacher_qualify import tea_qualify_apply,tea_qualify_apply_list
from .views.temp import te
from .views.person import update_user,user,delete_user

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

    path('admin_audit_reg_list/<int:pIndex>',audit_registration_list,name='audit_reg_list'),
    path('admin_registration_audit/<int:con_id>',admin_registration_audit,name="reg_audit"),

    path('reg_audit_pass/<int:t_id>',reg_audit_pass,name='reg_audit_pass'),
    path('reg_audit_fail/<int:t_id>',reg_audit_fail,name='reg_audit_fail'),
#竞赛相关
    path('match_con_show/<int:pIndex>',match_con_show,name="match_con_show"),
    path('match_team_list/<int:pIndex>/<int:con_id>',match_team_list,name="match_team_list"),
    path('match_wq/<int:match>',match_wq,name='match_wq'),
    path('match_stu/<int:match>',match_stu,name='match_stu_admin'),
    path('match_count/<int:con_id>',count,name='count'),
    path('mcclist/<int:pIndex>',match_con_count_list,name='mcclist'),
    path('match_con_tteam/<int:con_id>/<int:pIndex>',match_con_team,name='mteam'),
    path('match_result_export/<int:con_id>',match_result_export,name='match_result_export'),



    #作品上传权限控制
    path('work_f_up/<int:pIndex>/<int:con_id>',f_up,name='f_up'),
    path('work_f_down/<int:pIndex>/<int:con_id>',f_down,name='f_down'),
    path('work_s_up/<int:pIndex>/<int:con_id>',s_up,name='s_up'),
    path('work_s_down/<int:pIndex>/<int:con_id>',s_down,name='s_down'),
    path('work_t_up/<int:pIndex>/<int:con_id>',t_up,name='t_up'),
    path('work_t_down/<int:pIndex>/<int:con_id>',t_down,name='t_down'),

    #教师申请临时管理员权限
    path('tea_qualify_apply_list/<int:pIndex>',tea_qualify_apply_list,name='tea_qualify_apply_list'),
    path('tea_qualify_apply/<int:user_id>/<int:qualify>/<int:pIndex>',tea_qualify_apply,name='tea_qualify_apply'),

    path('test/',te,name='test'),
    path('img/',img,name="img"),


    path('user/',user,name='admin_user'),
    path('update_user/',update_user,name='admin_update_user'),
    path('delete)_user/',delete_user,name='admin_delete_user'),

]