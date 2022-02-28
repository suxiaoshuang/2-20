from django.db import models

# Create your models here.


class User(models.Model):
    identifies = (('student','学生'),('teacher','教师'),('admin','管理员'),)
    gender = (('male', '男'), ('female', '女'),)
    name = models.CharField(max_length=20, unique=False)      #名字
    user_id = models.CharField(max_length=20, unique=True)    #学工号
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=20, choices=gender, default='男')
    identify = models.CharField(max_length=30, choices=identifies, default='学生')
    academy = models.CharField(max_length=30, default='计算机')     #学院
    specialty = models.CharField(max_length=40,default='软件工程')   #专业
    grade = models.CharField(max_length=15,default='2018')  #年级
    c_time = models.DateTimeField(auto_now_add=True)      #注册时间
    has_confirmed = models.BooleanField(default=False)    #认证状态

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = '用户'
        db_table = 'user'


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name+":"+self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = '确认码'
        db_table = 'confirmstring'




class Contest(models.Model):
    contest_name = models.CharField(max_length=200)
    contest_type = models.CharField(max_length=30)
    contest_info = models.TextField()
    contest_status = models.BooleanField(default=True)
    contest_organizer = models.CharField(max_length=100)
    contest_time = models.CharField(max_length=50)
    contest_stage = models.CharField(max_length=20)
    contest_ctime = models.CharField(max_length=30)
    contest_img_path = models.CharField(max_length=200)

    class Meta:
        db_table = 'contest'


class File(models.Model):
    file_name =  models.CharField(max_length=200)
    file_path = models.CharField(max_length=150)
    file_user_id = models.CharField(max_length=30)
    file_ctime = models.CharField(max_length=30)
    file_user_name = models.CharField(max_length=100)

    class Meta:
        db_table = "file"