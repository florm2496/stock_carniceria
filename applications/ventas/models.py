from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
# Create your models here.
from applications.bases.models import ClaseModelo

from django.db.models.signals import post_save ,post_delete
from django.dispatch import receiver
from django.db.models import Sum
from applications.vino.models import Vino

NAT='natural'
JUR='juridica'
TIPO_CLIENTE=[
    (NAT , 'natural'),
    (JUR , 'juridica')
]

class Cliente(ClaseModelo):
    nombre = models.CharField(max_length=50, default='casual')
    tipo = models.CharField(max_length=15, choices=TIPO_CLIENTE,default=NAT )
    numero = models.CharField(blank=True,null=True, max_length=50)
    email = models.CharField(blank=True,null=True, max_length=50)
    direccion = models.CharField(blank=True,null=True, max_length=50)

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name_plural='Clientes'
class FacturaEnc(ClaseModelo):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.id)

    def save(self):
        self.total = self.sub_total - self.descuento
        super(FacturaEnc,self).save()

    class Meta:
        verbose_name_plural = "Encabezado Facturas"
        verbose_name="Encabezado Factura"
    #3    permissions = [
      #      ('sup_caja_facturaenc','Permisos de Supervisor de Caja Encabezado')
       # ]
    

class FacturaDet(ClaseModelo):
    factura = models.ForeignKey(FacturaEnc,on_delete=models.CASCADE)
    vino=models.ForeignKey(Vino,on_delete=models.CASCADE)
    cantidad=models.BigIntegerField(default=0)
    precio=models.FloatField(default=0)
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.vino)

    def save(self):
        self.sub_total = float(float(int(self.cantidad)) * float(self.precio))
        self.total = self.sub_total - float(self.descuento)
        super(FacturaDet, self).save()
    
    class Meta:
        verbose_name_plural = "Detalles Facturas"
        verbose_name="Detalle Factura"
    #    permissions = [
     #       ('sup_caja_facturadet','Permisos de Supervisor de Caja Detalle')
      #  ]


@receiver(post_save, sender=FacturaDet)
def detalle_fac_guardar(sender,instance,**kwargs):
    factura_id = instance.factura.id
    vino_id = instance.vino.id

    enc = FacturaEnc.objects.get(pk=factura_id)
    if enc:
        sub_total = FacturaDet.objects \
            .filter(factura=factura_id) \
            .aggregate(sub_total=Sum('sub_total')) \
            .get('sub_total',0.00)
        
        descuento = FacturaDet.objects \
            .filter(factura=factura_id) \
            .aggregate(descuento=Sum('descuento')) \
            .get('descuento',0.00)
        
        enc.sub_total = sub_total
        enc.descuento = descuento
        enc.save()

    vino=Vino.objects.filter(pk=vino_id).first()
    
    if vino:
        if int(vino.existencia) >= int(instance.cantidad):
            cantidad = int(vino.existencia) - int(instance.cantidad)
            vino.existencia = cantidad
            vino.save()
        else:
            print('no hay stock')
