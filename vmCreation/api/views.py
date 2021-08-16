from vmCreation.models import *
from vmCreation.api.serializers import ServerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from random import randrange
import subprocess
from subprocess import PIPE
from vmCreation.updateStates import updateServers

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
            r = randrange(2)
            ip = virtips[r]
            host = ids[r]
            serializer.save()
            result = subprocess.run(['ssh',ip,'sudo','./vmCreate.sh',request.data['name'],str(int(request.data['ram']) * 1024),request.data['cpu'],request.data['storage']],stdout=PIPE, stderr=PIPE)
            s = Server.objects.filter(name = request.data['name']).first()
            h = Host.objects.filter(id = host).first()
            s.status = "Active"
            s.host = h
            s.save()
            return Response(result.stdout.decode(), status=status.HTTP_200_OK)
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
                result = subprocess.run(['ssh',ip,'sudo','./vmCreate.sh',request.data['name'],str(int(request.data['ram']) * 1024),request.data['cpu'],request.data['storage']],stdout=PIPE, stderr=PIPE)
                s = Server.objects.filter(name = request.data['name']).first()
                h = Host.objects.filter(id = host).first()
                s.status = "Active"
                s.host = h
                s.save()
                return Response(result.stdout.decode(), status=status.HTTP_200_OK)
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
