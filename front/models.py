from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=254,unique=True)
    realname = models.CharField(max_length=254,null=True)
    password = models.CharField(max_length=18)
    telephone = models.CharField(max_length=11,null=True)
    signature = models.TextField(null=True)
    avatar = models.CharField(max_length=254,null=True)
    is_admin = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)


class Resources(models.Model):
    name = models.CharField(max_length=254)
    desc = models.TextField()
    img = models.CharField(max_length=254)
    type = models.IntegerField(choices=((1, 'document'), (2, 'media'),(3,'goods')))
    pub_time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('User',on_delete=models.CASCADE)
    is_remove = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)


class Record(models.Model):
    status = models.IntegerField(choices=((1, '进行中'), (0, '已完成')))
    trade_time = models.DateTimeField(auto_now_add=True)
    sender_resources = models.OneToOneField('Resources',null=True,on_delete=models.SET_NULL,related_name='send_record')
    recipient_resources = models.OneToOneField('Resources',null=True,on_delete=models.SET_NULL,related_name='receive_record')


class RecordFinish(models.Model):
    is_success = models.BooleanField(default=False)
    finish_time = models.DateTimeField(auto_now_add=True)
    sender_resources = models.ForeignKey('Resources',null=True,on_delete=models.CASCADE,related_name='send_records')
    recipient_resources = models.ForeignKey('Resources',null=True,on_delete=models.CASCADE,related_name='receive_records')



