import sys,libvirt,os

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
            hupdate = False
            for server in servers:
                server.status = "Error"
                server.save()
                if not hupdate:
                    host = server.host
                    host.status = "Down"
                    host.save()
                    hupdate = True

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

