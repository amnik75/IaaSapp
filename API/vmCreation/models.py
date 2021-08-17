# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Host(models.Model):
    id = models.IntegerField(primary_key=True,blank = False,null = False)
    ip = models.CharField(max_length = 15,blank=True, null=True)
    status = models.CharField(max_length = 254,blank=True, null=True,default='Up')

class Server(models.Model):
    name = models.CharField(primary_key=True,max_length = 254)
    ram = models.CharField(max_length = 2,blank=True, null=True)
    cpu = models.CharField(max_length = 2,blank=True, null=True)
    storage = models.CharField(max_length = 5,blank=True, null=True)
    status = models.CharField(max_length = 254,blank=True, null=True,default='pending_create')
    ip = models.CharField(max_length = 15,blank=True, null=True,unique=True)
    host = models.ForeignKey(Host,on_delete=models.CASCADE,null = True,blank=True)
    mac = models.CharField(max_length = 17,blank=True, null=True,unique=True)

