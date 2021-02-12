from django.db import models
from applications.bases.models import ClaseModelo2 , ClaseModelo


class Unidad(ClaseModelo2):
    medida=models.CharField(max_length=10)
    def __str__(self):
         return self.medida
class Bodega(ClaseModelo2):
    nombre=models.CharField(max_length=30)
    numero=models.CharField(max_length=30, blank=True ,null=True)
    email=models.CharField(max_length=30 ,blank=True ,null=True)
    def __str__(self):
        return self.nombre
class Reserva(ClaseModelo2):
    tipo=models.CharField(max_length=20)
    descripcion=models.CharField(max_length=50, blank=True ,null=True)
    def __str__(self):
        return self.tipo

class Cepa(ClaseModelo2):
    nombre=models.CharField(max_length=30)
    descripcion=models.CharField(max_length=100 , blank=True ,null=True)
    estado=models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
# Create your models here.
class Vino(ClaseModelo2):
    nombre=models.CharField(max_length=40)
    descripcion=models.CharField(max_length=100 , blank=True ,null=True)
    codigo=models.CharField(max_length=30 ,unique=True)
    precioventa=models.FloatField()
    reserva=models.ForeignKey(Reserva , on_delete=models.CASCADE)
    bodega=models.ForeignKey(Bodega ,blank=True,null=True, on_delete=models.CASCADE)
    cepa=models.ForeignKey(Cepa,blank=True,null=True,  on_delete=models.CASCADE)
    unidad=models.ForeignKey(Unidad, on_delete=models.CASCADE)
    existencia=models.IntegerField(default=0)
    ultimacompra=models.DateField(blank=True , null=True)
    sm=models.IntegerField(blank=True , null=True)
    

    def __str__(self):
            return '{}'.format(self.nombre)
class Meta:
        verbose_name_plural = "Productos"

  
