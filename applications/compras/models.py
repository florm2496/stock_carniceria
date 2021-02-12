from django.db import models



#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

from applications.bases.models import ClaseModelo
from applications.vino.models import Vino



class ComprasEnc(ClaseModelo):
    fecha_compra=models.DateField(null=True,blank=True)
    observacion=models.TextField(blank=True,null=True)
    total=models.FloatField(default=0)

   
    
    def __str__(self):
        return '{}'.format(self.observacion)
    def save(self):
        self.observacion = self.observacion.upper()
        super(ComprasEnc,self).save()

    class Meta:
        verbose_name_plural = "Encabezado Compras"
        verbose_name="Encabezado Compra"

class ComprasDet(ClaseModelo):
    compra=models.ForeignKey(ComprasEnc,on_delete=models.CASCADE)
    vino=models.ForeignKey(Vino,on_delete=models.CASCADE)
    cantidad=models.BigIntegerField(default=0)
    sub_total=models.FloatField(default=0)
    precio=models.FloatField(default=0)
   
    

    def __str__(self):
        return '{}'.format(self.vino)

    def save(self):
        self.sub_total = float(float(int(self.cantidad)) * float(self.precio))
        super(ComprasDet, self).save()
    
    class Mega:
        verbose_name_plural = "Detalles Compras"
        verbose_name="Detalle Compra"


@receiver(post_save, sender=ComprasDet)
def detalle_compra_guardar(sender,instance,**kwargs):
    id_vino = instance.vino.id
    fecha_compra=instance.compra.fecha_compra
    print(fecha_compra)

    vino=Vino.objects.filter(pk=id_vino).first()
    if vino:
        cantidad = int(vino.existencia) + int(instance.cantidad)
        vino.existencia = cantidad
        vino.ultimacompra=fecha_compra
        print(vino.ultimacompra)
        vino.save()


@receiver(post_delete, sender=ComprasDet)
def detalle_compra_borrar(sender,instance, **kwargs):
    id_vino = instance.vino.id
    id_compra = instance.compra.id
    fecha_compra=instance.compra.fecha_compra

    enc = ComprasEnc.objects.filter(pk=id_compra).first()
    if enc:
        sub_total = ComprasDet.objects.filter(compra=id_compra).aggregate(Sum('sub_total'))
        print('--------------------' ,sub_total['sub_total__sum']) 
        if  sub_total['sub_total__sum'] is None or sub_total['sub_total__sum']==0:
            enc.total=0  
            print('!!!!!!!1funciona',enc.total) 
            enc.save()
        else:
            enc.total=sub_total['sub_total__sum']
            enc.save()
    
    vino=Vino.objects.filter(pk=id_vino).first()
    if vino:
        cant=int(instance.cantidad)
        ex=int(vino.existencia)
        if cant>ex:
            print('no se puede hacer')
        elif cant<=ex:
            cantidad = ex - cant
            vino.existencia = cantidad
            vino.ultimacompra=fecha_compra
            vino.save()




