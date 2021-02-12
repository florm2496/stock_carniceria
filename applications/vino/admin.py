from django.contrib import admin
from .models import Bodega ,Cepa,Unidad,Reserva,Vino
# Register your models here.
admin.site.register(Bodega)
admin.site.register(Cepa)
admin.site.register(Unidad)
admin.site.register(Reserva)
admin.site.register(Vino)