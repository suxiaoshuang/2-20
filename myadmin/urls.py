from django.urls import path
from login_register.views.views import index
from .views.contest import con_open,contest_show,con_add,con_delete,con_update,img,con_info,con_close,con_off,con_on
from .views.student import stu_show,stu_add,stu_delete,stu_update

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
    path('contest_update/<int:id>',con_update,name="admin_contest_update"),


    path('student_delete/<int:id>',stu_delete,name="admin_stu_delete"),
    path('student_update/<int:id>',stu_update,name="admin_stu_update"),
    path('student_add/',stu_add,name="admin_stu_add"),
    path('student_show/<int:pIndex>',stu_show,name="admin_stu_show"),



    path('img/',img,name="img"),

]