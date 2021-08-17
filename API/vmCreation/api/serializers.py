from rest_framework import serializers
from vmCreation.models import Server

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ('name','ram','cpu','storage')
