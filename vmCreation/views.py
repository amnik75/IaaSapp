# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .updateStates import updateServers
# Create your views here.
from .models import *

def status(request):
    servers = Server.objects
    hosts = Host.objects.all()
    for h in hosts:
        updateServers(servers.filter(host_id = h.id),h.ip)
    servers = Server.objects.all()
    context = {'servers': servers}
    return render(request, 'vmCreation/status.html', context)
