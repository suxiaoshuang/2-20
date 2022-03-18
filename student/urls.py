from django.urls import path,re_path
from login_register.views.views import index
from .views.enroll import sc_list,sc_enroll,sc_add_team,sc_team_nt,sc_join_team,sc_team_memebers
from .views.team import sc_team_list,sc_team_js,sc_team_quit
urlpatterns = [
    path('index/', index,name='student_index'),
    path('stu_list/<int:pIndex>',sc_list,name="sc_list"),
    path('stu_enroll/',sc_enroll,name="sc_enroll"),
    path('stu_add_team/',sc_add_team,name="sc_add_team"),
    re_path(r'sc_team_nt/(?P<team_id>[0-9].*)/(?P<teacher>.*)/(?P<team_name>.*)',sc_team_nt,name="sc_team_nt"),
    path("stu_join_team/",sc_join_team,name="sc_join_team"),

    re_path('stu_team_members/(?P<h_c_id>[0-9].*)',sc_team_memebers,name="sc_team_members"),
    path('stu_team_list/<int:pIndex>',sc_team_list,name="sc_team_list"),
    path('stu_team_quit/<int:h_c_id>',sc_team_quit,name="sc_team_quit"),
    path('stu_team_js/<int:h_c_id>',sc_team_js,name="sc_team_js"),
]