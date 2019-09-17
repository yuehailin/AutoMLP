from django.db import models

# Create your models here.

# Create your models here.
class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    c_time = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = ['c_time']
#         verbose_name = '用户'
#         verbose_name_plural = '用户'

class Publisher(models.Model):
         id = models.AutoField(primary_key=True)  # 创建自增的一个主键
         name = models.CharField(null=False, max_length=64, unique=True)  # varchar且不能为空的字段
class Kind(models.Model):

    id = models.IntegerField(primary_key=True)
    kind = models.CharField(null=False, max_length=128, unique=True)
    describe = models.CharField(null=False, max_length=128, unique=True)
    filename = models.CharField(null=False, max_length=128, unique=True)
    filecreatetime = models.DateTimeField(auto_now_add=True)
class Task(models.Model):
    task_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    csv_path = models.CharField(null=False,max_length=512)


    yaml_path = models.CharField(null=False,max_length=512)
    up_time = models.DateTimeField(auto_now_add=True)
class Image(models.Model):
    task_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    csv_path = models.CharField(null=False,max_length=512)

    yaml_path = models.CharField(null=False,max_length=512)
    up_time = models.DateTimeField(auto_now_add=True)