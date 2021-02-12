from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.views import generic
from django.urls import reverse_lazy
import datetime
from django.http import HttpResponse, JsonResponse

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin ,PermissionRequiredMixin
from django.http import HttpResponse
import json
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, permission_required
from applications.bases.views import SinPrivilegios
from .models import ComprasEnc, ComprasDet
from .forms import ComprasEncForm
#from bases.views import SinPrivilegios
from applications.vino.models import Vino




class ComprasView(SinPrivilegios,generic.ListView):
    model = ComprasEnc
    template_name = "compras/listacompras.html"
    context_object_name = "obj"
    permission_required='compras.view_comprasenc'
    


@login_required(login_url='/login/')
@permission_required('cmp.view_comprasenc', login_url='bases:sin_privilegios')
def compras(request,compra_id=None):
    template_name="compras/from2.html"
    vino=Vino.objects.filter(estado=True)
    print(vino)
    form_compras={}
    contexto={}

    if request.method=='GET':
        form_compras=ComprasEncForm()
        enc = ComprasEnc.objects.filter(pk=compra_id).first()

        if enc:
            det = ComprasDet.objects.filter(compra=enc)
            fecha_compra = datetime.date.isoformat(enc.fecha_compra)
            e = {
                'fecha_compra':fecha_compra,
                'observacion': enc.observacion,
                'total':enc.total
            }
            form_compras = ComprasEncForm(e)
        else:
            det=None
        
        contexto={'productos':vino,'encabezado':enc,'detalle':det,'form_enc':form_compras}

#METODO POST
    if request.method=='POST':
        fecha_compra = request.POST.get("fecha_compra")
        observacion = request.POST.get("observacion")
        total = 0

        if not compra_id:

            enc = ComprasEnc(
                fecha_compra=fecha_compra,
                observacion=observacion,
                uc = request.user 
            )
            if enc:
                enc.save()
                compra_id=enc.id
        else:
            enc=ComprasEnc.objects.filter(pk=compra_id).first()
            if enc:
                enc.fecha_compra = fecha_compra
                enc.observacion = observacion
                enc.um=request.user.id
                enc.save()

        if not compra_id:
            return redirect("compras:listacompras")
        
        producto = request.POST.get("id_codigo")
        cantidad = request.POST.get("id_cantidad_detalle")
        precio = request.POST.get("id_precio_detalle")
        sub_total_detalle = request.POST.get("id_sub_total_detalle")
        

        prod = Vino.objects.get(codigo=producto)
        print('producto',prod.id)
     
        det = ComprasDet(
            compra=enc,
            vino=prod,
            cantidad=cantidad,
            precio=precio,
            uc = request.user

        )

        if det:
            det.save()

            sub_total=ComprasDet.objects.filter(compra=compra_id).aggregate(Sum('sub_total'))
            enc.total = sub_total["sub_total__sum"]
            enc.save()

        return redirect("compras:editarcompra",compra_id=compra_id)


    return render(request, template_name, contexto)


class CompraDetDelete(PermissionRequiredMixin, generic.DeleteView):
    
    model = ComprasDet
    template_name = "compras/delete_detcompra.html"
    context_object_name = 'obj'
    permission_required = "compras.delete_comprasdet"
    def get_success_url(self):
          compra_id=self.kwargs['compra_id']
          return reverse_lazy('compras:editarcompra', kwargs={'compra_id': compra_id})