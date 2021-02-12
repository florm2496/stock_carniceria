from django.shortcuts import render

# SE ULTILIZAN LAS API VIEWS .

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from .serializers import VinoSerializer
from applications.vino.models import Vino

class VinoList(APIView):
    def get(self,request):
        vino=Vino.objects.all()
        data=VinoSerializer(vino,many=True).data

        return Response(data)

class VinoDetalle(APIView):
    def get(self, request , codigo):
        vino=get_object_or_404(Vino,codigo=codigo)
        data=VinoSerializer(vino).data
        return Response(data)