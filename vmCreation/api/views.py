from vmCreation.models import Server
from vmCreation.api.serializers import ServerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from random import randrange
import subprocess
from subprocess import PIPE

class Create(APIView):
    def post(self, request, format= None):
        serializer = ServerSerializer(data=request.data)
        virtips = ['192.168.122.104','192.168.122.119']
        if serializer.is_valid():
            ip = virtips[randrange(2)]
            result = subprocess.run(['ssh',ip,'sudo','./vmCreate.sh',request.data['name'],str(int(request.data['ram']) * 1024),request.data['cpu'],request.data['storage']],stdout=PIPE, stderr=PIPE)
            serializer.save()
            return Response(result.stdout.decode(), status=status.HTTP_200_OK)
        elif isRepeating(request.data) :
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
