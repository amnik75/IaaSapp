# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Server(models.Model):
    name = models.CharField(max_length = 254,blank=True, null=True)
    ram = models.CharField(max_length = 2,blank=True, null=True)
    cpu = models.CharField(max_length = 2,blank=True, null=True)
    storage = models.CharField(max_length = 5,blank=True, null=True)
