from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum
# Create your models here.
from applications.bases.models import ClaseModelo
from applications.caja.models import Caja
from django.db.models.signals import post_save ,post_delete
from django.dispatch import receiver
from django.db.models import Sum
from applications.vino.models import Vino
from applications.ventas.managers import FacturaDetManager,FacturaEncManager




NAT='natural'
JUR='juridica'
TIPO_CLIENTE=[
    (NAT , 'natural'),
    (JUR , 'juridica')
]

class Cliente(ClaseModelo):
    nombre = models.CharField(max_length=50, default='casual')
    tipo = models.CharField(max_length=15, choices=TIPO_CLIENTE ,blank=True , null=True )
    saldo=models.FloatField(default=0)
    numero = models.CharField(blank=True,null=True, max_length=50)
    email = models.CharField(blank=True,null=True, max_length=50)
    direccion = models.CharField(blank=True,null=True, max_length=50)

    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name_plural='Clientes'


class Pago(ClaseModelo):
    monto=models.FloatField(default=0)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return self.id + self.cliente

    class Meta:
        verbose_name_plural='Pagos'

class FacturaEnc(ClaseModelo):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)
    cerrada=models.BooleanField(default=False)
    objects=FacturaEncManager()

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
    
#venta anulada= es aquella venta que se cancela
#venta cerrada=es aquella venta que se cierra en un cierre de caja 

class FacturaDet(ClaseModelo):
    factura = models.ForeignKey(FacturaEnc,on_delete=models.CASCADE)
    vino=models.ForeignKey(Vino,on_delete=models.CASCADE)
    cantidad=models.BigIntegerField(default=0)
    precio=models.FloatField(default=0)
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)
    anulada=models.BooleanField(default=False)
    objects=FacturaDetManager()

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
    
    detalle=FacturaDet.objects.get(pk=instance.id)
    subtotal=detalle.sub_total
    #print('detalle del subtotal',detalle.sub_total)

    if enc:
        sub_total = FacturaDet.objects.filter(factura=factura_id).aggregate(sub_total=Sum('sub_total')).get('sub_total',0.00)

        print(FacturaDet.objects.filter(factura=factura_id))

        descuento = FacturaDet.objects \
            .filter(factura=factura_id) \
            .aggregate(descuento=Sum('descuento')) \
            .get('descuento',0.00)
        

        enc.sub_total = sub_total
        #print('///////////////////',enc.sub_total)
        enc.descuento = descuento

        enc.save()

        cliente=enc.cliente
        saldo=cliente.saldo
        if subtotal>=0:
            cliente.saldo=saldo + subtotal
            cliente.save()
            print('saldo del cliente positivo')
        elif subtotal<0:
            print('saldo cliente ngativo',cliente.saldo)
        
        

    vino=Vino.objects.filter(pk=vino_id).first()
    
    if vino:
        if int(vino.existencia) >= int(instance.cantidad):
            cantidad = int(vino.existencia) - int(instance.cantidad)
            vino.existencia = cantidad
            vino.save()
            print('vinoooooooooooooooooooooo')
        else:
            print('no hay stock')




@receiver(post_save, sender=FacturaDet)

def ventas_caja(sender ,instance , **kwargs):
    ultima_venta=FacturaDet.objects.last()
    ultimo_total=ultima_venta.total
    caja=Caja.objects.last()
    monto_actual_caja=caja.monto_actual
    #print('caja ahora' , monto_actual_caja)
    caja.monto_actual=monto_actual_caja+ultimo_total
    caja.save()
    #print('caja luego de sumar',ultimo_total,':',caja.monto_actual)


'''
@receiver(post_save, sender=Pago)
def realizar_pago(sender,instance,**kwargs):
    
    
    
      #se obtiene el cliente que relacionado a la venta(o el que realizo la compra)
        cliente_id=enc.cliente.id
        #se obtiene la instancia de ese cliente
        cliente=Cliente.objects.get(pk=cliente_id)
        #se obtiene el saldo que tenia el cliente antes de realizar la compra
        saldo=cliente.saldo
        print('desde el borrado',enc.sub_total)
        #se actualiza su saldo con el monto de la compra que realizo
        cliente.saldo=saldo + enc.sub_total
        #se guarda la actualizacion en la base de datos
        cliente.save()

    
    
    
    
    
    
    
    '''