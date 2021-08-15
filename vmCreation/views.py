# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import libvirt,sys,os

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

def updateServers(servers,ip):
    conn = None
    libres = True
    try:
        conn = libvirt.open("qemu+ssh://" + ip + "/system")
    except libvirt.libvirtError as e:
        libres = False
    
    if not libres:
        response = os.system("ping -c 1 " + ip)
        if response == 0:
            for server in servers:
                server.status = "Unknown"
                server.save()
        else:
            for server in servers:
                server.status = "Error"
                server.save()

    else:
        for server in servers: 
            dom = conn.lookupByName(server.name)
            state, reason = dom.state()
            if state == libvirt.VIR_DOMAIN_NOSTATE:
                state = "NOSTATE"
            elif state == libvirt.VIR_DOMAIN_RUNNING:
                state = "Active"
            elif state == libvirt.VIR_DOMAIN_BLOCKED:
                state = "BLOCKED"
            elif state == libvirt.VIR_DOMAIN_PAUSED:
                state = "BLOCKED"
            elif state == libvirt.VIR_DOMAIN_SHUTDOWN:
                state = "SHUTDOWN"
            elif state == libvirt.VIR_DOMAIN_SHUTOFF:
                state = "SHUTOFF"
            elif state == libvirt.VIR_DOMAIN_CRASHED:
                state = "CRASHED"
            elif state == libvirt.VIR_DOMAIN_PMSUSPENDED:
                state = "PMSUSPENDED"
            else:
                state = "Unknown"
            server.status = state
            server.save()
        conn.close()
