# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Server(models.Model):
    name = models.CharField(primary_key=True,max_length = 254)
    ram = models.CharField(max_length = 2,blank=True, null=True)
    cpu = models.CharField(max_length = 2,blank=True, null=True)
    storage = models.CharField(max_length = 5,blank=True, null=True)
    status = models.CharField(max_length = 254,blank=True, null=True,default='pending_create')
    host = models.CharField(max_length = 254,blank=True, null=True,default='Not defined') 
