from django.db import models
import datetime
# Create your models here.



class IP(models.Model):
    IP_id = models.AutoField(primary_key=True)
    vlan = models.CharField(max_length=20,null=False)
    host = models.CharField(max_length=40,null=False)
    name = models.CharField(max_length=40,null=True)
    thing = models.CharField(max_length=80,null=True)
    domain = models.CharField(max_length=40,null=True)
    person_name = models.CharField(max_length=20,null=True)
    person_tel = models.CharField(max_length=30,null=True)
    admin_name = models.CharField(max_length=20,null=True)
    admin_tel = models.CharField(max_length=30,null=True)
    bbs_admin_name = models.CharField(max_length=20,null=True)
    bbs_admin_tel = models.CharField(max_length=30,null=True)
    blj_user = models.CharField(max_length=20,null=True)
    blj_password = models.CharField(max_length=40,null=True)
    system_type = models.CharField(max_length=20,null=True)
    cpu = models.CharField(max_length=20,null=True)
    momory = models.CharField(max_length=20,null=True)
    storage = models.CharField(max_length=20,null=True)
    assistance = models.CharField(max_length=40,null=True)
    ssh = models.CharField(max_length=40,null=True)
    telnet = models.CharField(max_length=30,null=True)
    host_user = models.CharField(max_length=40,null=True)
    host_password = models.CharField(max_length=40,null=True)
    host_manage_type = models.CharField(max_length=20,null=True)
    sql_type = models.CharField(max_length=20,null=True)
    is_post = models.CharField(max_length=20,null=True)
    post = models.CharField(max_length=200,null=True)
    remark = models.CharField(max_length=400,null=True)
    colony = models.CharField(max_length=20,null=True)
    status = models.CharField(max_length=10,null=True)
    times = models.CharField(max_length=20,null=True)
    ms = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.host

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_number = models.CharField(max_length=40,null=False)
    user_password = models.CharField(max_length=40,null=False)
    user_mail = models.CharField(max_length=20,default='0') #用户的qq邮箱
    user_type = models.CharField(max_length=20,null=False,default='0') #用户权限，默认是0

    def __str__(self):
        return self.user_number


class Time(models.Model):
    time_id = models.AutoField(primary_key=True)
    times = models.CharField(max_length=30,null=True)
    time = models.CharField(max_length=50, default=datetime.datetime.now())
    list1 = models.CharField(max_length=8000,null=True) #可以ping同的网站列表
    list0 = models.CharField(max_length=8000,null=True) #不可以ping同的网站列表
    count1 = models.CharField(max_length=20,default='0')
    count0 = models.CharField(max_length=20,default='0')

    def __str__(self):
        return self.times

class Error(models.Model):
    error_id = models.AutoField(primary_key=True)
    host = models.CharField(max_length=20,null=False) #主机ip
    time = models.CharField(max_length=20,null=False) #发生异常的时间
    text = models.CharField(max_length=1000,null=True)  #发生异常的内容
    msg = models.CharField(max_length=2000,null=True)  #处理异常的备注
    status = models.CharField(max_length=10,default='1')  #异常的状态，默认为 1 0 表示异常已经处理
    mail = models.CharField(max_length=10,null=True)  #是否发送过邮件
    distribution = models.CharField(max_length=10,null=True)  #是否被分配
    run = models.CharField(max_length=10,null=True)  #是否在运行

    def __str__(self):
        return self.host





