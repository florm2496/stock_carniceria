from django.db import models
from applications.bases.models import ClaseModelo2
from django.db.models.signals import post_save
from django.dispatch import receiver
from applications.ventas.models import Cliente
# Create your models here.
class Tropa(ClaseModelo2):
    cant_animales = models.IntegerField()


    def __str__(self):
        return 'Tropa numero'+str(self.id)

class Animal(ClaseModelo2):
    numero=models.IntegerField(default=0)
    ident=models.CharField(max_length=50,blank=True, null=True)
    tropa = models.ForeignKey(Tropa, on_delete=models.CASCADE)
    peso_animal=models.FloatField(default=0)

    #def save(self):
        #self.ident='animal:{}-tropa:{}'.format(self.id ,self.tropa)
     #   super(Animal , self).save()

    def __str__(self):
        
        return str(self.numero) +'-'+ str(self.tropa)
    



class Res(ClaseModelo2):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    nombre=models.CharField(default='Res' ,max_length=10)
    peso_inicial = models.FloatField(max_length=7 , default=0)
    ingreso = models.DateTimeField(auto_now_add=True)
    peso_final=models.FloatField(blank=True , null=True , default=0)
    vendida=models.BooleanField(default=False)
    
   

    class Meta:
        """Meta definition for MODELNAME."""

        verbose_name = 'Res'
        verbose_name_plural = 'Reses'

    def __str__(self):
        return self.nombre 

TB='transferencia bancaria'
MP='mercado pago'
EF='efectivo'
TJ='tarjeta'
MEDIO_PAGO=[
    ('TB' ,'TRANSFERENCIA BANCARIA'),
    ('MP' ,'MERCADO PAGO'),
    ('EF' ,'EFECTIVO'),
    ('TJ' ,'TARJETA')
]
class VentaReses(ClaseModelo2):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    res=models.ForeignKey(Res, on_delete=models.CASCADE)
    precio=models.FloatField(default=0)
    medio_pago = models.CharField(max_length=15, choices=MEDIO_PAGO,default=EF )

    def __str__(self):
        return str(self.id)+'-'+str(self.precio)
    class Meta:
        """Meta definition for MODELNAME."""

        verbose_name = 'VentaRes'
        verbose_name_plural = 'VentaReses'


@receiver(post_save, sender=Animal)
def CrearResesDeUnAnimal(sender, instance,**kwargs):
    tropa=instance.tropa
    id_animal=instance.id
   
    animal=Animal.objects.filter(id=id_animal).update(
        ident='animal{}-{}'.format(id_animal,tropa),
    )
   
    #print('desde el signal',animal) la variable animal devuelve 1 , esto quiere decir que el update fue exitoso
   
    #PROCESO PARA CREAR LAS DOS MEDIA RESES PERTENECIENTES  AL ANIMAL EN CUESTION
    reses=[]
    anm=Animal.objects.get(id=id_animal)
    for num in range(2):
        res =Res(
            animal=anm,
            nombre='res{}-anm{}'.format(num,anm.id),
        )
        reses.append(res)
    Res.objects.bulk_create(reses)

#este metodo luego de realizar una venta de reses , cambia el estado de la res vendida a True
@receiver(post_save, sender=VentaReses)
def vender_reses(sender , instance,**kwargs):
    #obtener id de la res vendida
    id_res=instance.res.id
    #obtener la instancia de la res
    res=Res.objects.get(pk=id_res)
    #cambiar estado de la res
    res.vendida=True
    res.save()
