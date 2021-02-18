from django.db import models
from applications.bases.models import ClaseModelo2

# Create your models here.
class Res(ClaseModelo2):
    id = models.AutoField(primary_key=True)
    nombre=models.CharField(default='Res' ,max_length=10)
    peso_inicial = models.FloatField(max_length=7 , default=0)
    ingreso = models.DateTimeField(auto_now_add=True)
    peso_final=models.FloatField(blank=True , null=True , default=0)
    
   

    class Meta:
        """Meta definition for MODELNAME."""

        verbose_name = 'Res'
        verbose_name_plural = 'Reses'

    def __str__(self):
        return self.nombre + str(self.id)
