from django.db import models
from applications.bases.models import ClaseModelo2
# Create your models here.
class Cortes(ClaseModelo2):
    codigo=models.IntegerField(max_length=20 ,unique=True , blank=True , null=True)
    nombre = models.CharField(max_length=50 ,unique=True)
    descripcion = models.CharField(max_length=50 , blank=True , null=True)
    cant_vendida=models.FloatField(default=0)
    precio=models.FloatField(default=0)

    class Meta:
        
        verbose_name = 'CORTE DE CARNE'
        verbose_name_plural = 'CORTES DE CARNE'

    def __str__(self):
        return self.nombre
