from django.contrib import admin

# Register your models here.
from .models import Caja,MovimientosCaja
#,CierreCaja

admin.site.register(Caja)
admin.site.register(MovimientosCaja)
#admin.site.register(CierreCaja)