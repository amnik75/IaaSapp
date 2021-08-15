# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from .models import Server

def status(request):
    servers = Server.objects.all()
    context = {'servers': servers}
    return render(request, 'vmCreation/status.html', context)
