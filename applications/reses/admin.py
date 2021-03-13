from django.contrib import admin

# Register your models here.
from .models import Res,Tropa,Animal,VentaReses

admin.site.register(Res)
admin.site.register(Tropa)
admin.site.register(Animal)
admin.site.register(VentaReses)