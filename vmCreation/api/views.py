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
            print(ip)
            result = subprocess.run(['ssh','192.168.122.119','sudo','./vmCreate.sh',request.data['name'],str(int(request.data['ram']) * 1024),request.data['cpu'],request.data['storage']],stdout=PIPE, stderr=PIPE)
            print(result.stdout.decode())
            return Response(result.stdout.decode(), status=status.HTTP_200_OK)
            

