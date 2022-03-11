from django.urls import path
from login_register.views.views import index
from .views.enroll import sc_list,sc_enroll
urlpatterns = [
    path('index/', index,name='student_index'),
    path('stu_list/<int:pIndex>',sc_list,name="sc_list"),
    path('stu_enroll/<int:id>',sc_enroll,name="sc_enroll"),
]