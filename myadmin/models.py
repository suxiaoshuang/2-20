from django.db import models

# Create your models here.
from django_summernote.fields import SummernoteTextFormField
class Contest(models.Model):
    contest_name = models.CharField(max_length=200)
    contest_type = models.CharField(max_length=30)
    contest_info = models.TextField()
    contest_status = models.CharField(max_length=10,default=1)
    contest_organizer = models.CharField(max_length=100)
    contest_time = models.CharField(max_length=50)
    contest_stage = models.CharField(max_length=20)
    contest_ctime = models.CharField(max_length=30)
    contest_img_path = models.CharField(max_length=200)
    contest_pt = models.CharField(max_length=10)
    audit = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contest'
        ordering = ['-time']


class User(models.Model):
    identifies = (('student','学生'),('teacher','教师'),('admin','管理员'),)
    gender = (('male', '男'), ('female', '女'),)
    name = models.CharField(max_length=20, unique=False)      #名字
    user_id = models.CharField(max_length=20, unique=True)    #学工号
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # sex = models.CharField(max_length=20, choices=gender)
    identify = models.CharField(max_length=30, choices=identifies, default='学生')
    academy = models.CharField(max_length=30)     #学院
    specialty = models.CharField(max_length=40)   #专业
    grade = models.CharField(max_length=15)  #年级
    c_time = models.DateTimeField(auto_now_add=True)      #注册时间
    has_confirmed = models.BooleanField(default=False)    #认证状态
    permissions = models.CharField(max_length=5,default=0)  #权限
    qualify_apply = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = '用户'
        db_table = 'user'
        ordering = ['-c_time']



class Organizer(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        db_table = 'organizer'


class Info(models.Model):   #新闻
    type = models.CharField(max_length=20,default='news')
    title = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    ctime = models.CharField(max_length=30)
    come_from = models.CharField(max_length=50,null=True,blank=True)
    type = models.CharField(max_length=20)
    img_path = models.CharField(max_length=200)
    class Meta:
        db_table = 'info'
        ordering = ['-time']

class Specialty(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'specialty'


class Tyep(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'type'


class Stage(models.Model):
    stage = models.CharField(max_length=10)

    class Meta:
        db_table = 'stage'

class Team(models.Model):
    h_c_id = models.CharField(max_length=20)
    t_name = models.CharField(max_length=50)
    u_name = models.CharField(max_length=50)
    use = models.ForeignKey(User,on_delete=models.CASCADE)
    head = models.BooleanField(default=False)
    con = models.ForeignKey(Contest,on_delete=models.CASCADE)
    c_name = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'team'
        ordering = ['-time']



class Registration(models.Model):
    t = models.ForeignKey(Team,on_delete=models.CASCADE)
    t_name = models.CharField(max_length=50)
    c_name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    teacher = models.CharField(max_length=30)
    con = models.ForeignKey(to=Contest,on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'registration'
        ordering = ['-time']




class Academy(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'academy'


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






class File(models.Model):
    file_name =  models.CharField(max_length=200)
    file_path = models.CharField(max_length=150)
    file_user_id = models.CharField(max_length=30)
    file_ctime = models.CharField(max_length=30)
    file_user_name = models.CharField(max_length=100)
    file_size = models.CharField(max_length=20,default='0KB')

    class Meta:
        db_table = "file"
        ordering = ['-id']

class Match(models.Model):
    h_c_id = models.CharField(max_length=50)
    tname = models.CharField(max_length=50)
    cname = models.CharField(max_length=50)
    con = models.ForeignKey(Contest,on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team,on_delete=models.CASCADE)

    class Meta:
        db_table = 'match'
        ordering = ['-id']

class W_Q(models.Model):
    match = models.ForeignKey(Match,on_delete=models.CASCADE)
    grade = models.CharField(max_length=30,default=0)
    qualify = models.BooleanField(default=False)
    medal = models.CharField(max_length=50)
    stage = models.IntegerField()
    con = models.ForeignKey(Contest,on_delete=models.CASCADE)
    class Meta:
        db_table = 'wq'
        verbose_name = '获奖、晋级表'


class Works(models.Model):
    con = models.ForeignKey(Contest,on_delete=models.CASCADE)
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    stage = models.IntegerField()
    match = models.ForeignKey(Match,on_delete=models.CASCADE)
    file_path = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'work'


class UWQ(models.Model):
    con = models.ForeignKey(Contest,on_delete=models.CASCADE)
    stage = models.IntegerField(default=1)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'uwq'


class Apply(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    result = models.CharField(max_length=50)

    class Meta:
        db_table = 'apply'
        ordering = ['-time']