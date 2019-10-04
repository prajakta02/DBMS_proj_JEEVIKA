from django.db import models
from django.utils import timezone

# Create your models here.

class user(models.Model):
    username=models.CharField(max_length=50,primary_key=True)
    password=models.TextField()
    hname=models.CharField(max_length=50)
    email=models.EmailField()
    address=models.TextField(default='')
    timestamp=models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.username


class blood(models.Model):
    bgroup=models.CharField(max_length=2)
    hname=models.CharField(max_length=50,default='')
    stock=models.IntegerField(default=0)

class medicine(models.Model):
    med_name=models.CharField(max_length=20)
    hname=models.CharField(max_length=50,default='')
    stock=models.IntegerField(default=0)

class req_table(models.Model):
    hname=models.CharField(max_length=50)
    d_hname=models.CharField(max_length=50,default='')
    timestamp=models.DateTimeField(default=timezone.now())
    entity=models.CharField(max_length=20)
    product=models.CharField(max_length=50,default='')
    no_stock=models.IntegerField(default=0)
    delivered_status=models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)+") "+str(self.d_hname)+" by "+str(self.timestamp)
