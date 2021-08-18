from vmCreation.models import *
from vmCreation.api.serializers import ServerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from random import randrange
import subprocess
from subprocess import PIPE
from vmCreation.updateStates import updateServers
import random

class Create(APIView):
    def post(self, request, format= None):
        serializer = ServerSerializer(data=request.data)
        virtips = []
        ids = []
        hosts =  Host.objects.order_by('id')
        for host in hosts:
            virtips.append(host.ip)
            ids.append(host.id)
        if serializer.is_valid():
            r = randrange(len(virtips))
            hip = virtips[r]
            host = ids[r]
            serializer.save()
            ips = Server.objects.values('ip').distinct()
            found = False
            while not found:
                oct = random.randint(2, 254)
                ip = "192.168.123." + str(oct)
                if ip not in ips:
                    found = True
            mac = "52:54:00:%02x:%02x:%02x" % (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
            result = subprocess.run(['ssh',hip,'sudo','./vmCreate.sh',request.data['name'],str(int(request.data['ram']) * 1024),request.data['cpu'],request.data['storage'],ip,mac],stdout=PIPE, stderr=PIPE)
            s = Server.objects.filter(name = request.data['name']).first()
            h = Host.objects.filter(id = host).first()
            s.status = "Active"
            s.host = h
            s.ip = ip
            s.mac = mac
            s.save()
            return Response(ip, status=status.HTTP_200_OK)
        elif isRepeating(request.data):
            servers = Server.objects
            hosts = Host.objects.all()
            for h in hosts:
                updateServers(servers.filter(host_id = h.id),h.ip)
            server = Server.objects.filter(name = request.data["name"]).first()
            if server.status == "Error":
                for i in range(len(virtips)):
                    if virtips[i] != server.host.ip:
                        ip = virtips[i]
                        host = ids[i]
                        break
                server.status = "pending_create"
                server.host = None
                server.save()
                result = subprocess.run(['ssh',ip,'sudo','./vmEvacuate.sh',request.data['name'],str(int(request.data['ram']) * 1024),request.data['cpu'],server.mac],stdout=PIPE, stderr=PIPE)
                s = Server.objects.filter(name = request.data['name']).first()
                h = Host.objects.filter(id = host).first()
                s.status = "Active"
                s.host = h
                s.save()
                return Response("Server created on new host successfully!", status=status.HTTP_200_OK)
            else:
                return Response("The name is used by an other customer", status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_200_OK)

def isRepeating(data):
    if "name" in data:
        name = data["name"]
        servers = Server.objects.all()
        for server in servers:
            if server.name == name:
                return True
    return False
