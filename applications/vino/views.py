from django.shortcuts import render
from .models import Cepa ,Vino ,Reserva,Bodega ,Unidad
# Create your views here.
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin ,PermissionRequiredMixin
from django.views.generic import ListView ,UpdateView, CreateView ,TemplateView
from .forms import CepaNewForm ,ReservaNewForm,UnidadNewForm,VinoNewForm ,BodegaNewForm
from django.urls import reverse_lazy
#,BodegaNewForm 
from django.http import HttpResponse, JsonResponse
from applications.bases.views import SinPrivilegios


class MixinFormInvalid():
    def form_invalid(self , form):
        response=super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors , status=400)
        else:
            return response 



class CepaView(SinPrivilegios,ListView):
    model=Cepa
    context_object_name='obj'
    template_name='vinos/cepas.html'
    login_url='bases:login'
    permission_required='vino.view_cepa'
    
class CepaNew(SuccessMessageMixin,SinPrivilegios,CreateView):
    model=Cepa
    form_class=CepaNewForm
    template_name='vinos/crearcepa.html'
    context_object_name='obj'
    success_url=reverse_lazy('vino:cepas')
    login_url='bases-login'
    permission_required='vino.add_cepa'
    success_message='Cepa creada satisfactoriamente'
class CepaUpdate(SuccessMessageMixin,SinPrivilegios, UpdateView):
    model=Cepa
    form_class=CepaNewForm
    template_name='vinos/crearcepa.html'
    context_object_name='obj'
    success_url=reverse_lazy('vino:cepas')
    login_url='bases-login'
    permission_required='vino.change_cepa'
    success_message='Cepa actualizada satisfactoriamente'
    #permission_required='vino.delete_cepa'

class BodegaView(SuccessMessageMixin,SinPrivilegios,ListView):
    model=Bodega
    context_object_name='obj'
    template_name='vinos/bodegas.html'
    login_url='bases:login'
    permission_required='vino.view_bodega'
class BodegaNew(SuccessMessageMixin,SinPrivilegios, CreateView):
    model=Bodega
    form_class=BodegaNewForm
    context_object_name='obj'
    template_name='vinos/crearbodega.html'
    login_url='bases:login'
    success_url=reverse_lazy('vino:bodegas')
    permission_required='vino.add_bodega'
    success_message='Bodega creada exitosamente'
class BodegaUpdate(SuccessMessageMixin,SinPrivilegios, UpdateView):
    model=Bodega
    form_class=BodegaNewForm
    context_object_name='obj'
    template_name='vinos/crearbodega.html'
    login_url='bases:login'
    success_url=reverse_lazy('vino:bodegas')   
    permission_required='vino.change_bodega'
    success_message='Bodega editada exitosamente'
class ReservaView(SuccessMessageMixin,SinPrivilegios,ListView):
    model=Reserva
    context_object_name='obj'
    template_name='vinos/reservas.html'
    login_url='bases:login'
    permission_required='vino.view_reserva'
  


    
    
    

class ReservaNew(SinPrivilegios,SuccessMessageMixin,CreateView):
    model=Reserva
    form_class=ReservaNewForm
    context_object_name='obj'
    template_name='vinos/crearreserva.html'
    success_url=reverse_lazy('vino:reservas')
    login_url='bases:login'
    permission_required='vino.add_reserva'
    success_message='Categoria creada exitosamente'
class ReservaUpdate(SuccessMessageMixin,SinPrivilegios,UpdateView):
    model=Reserva
    form_class=ReservaNewForm
    context_object_name='obj'
    template_name='vinos/crearreserva.html'
    success_url=reverse_lazy('vino:reservas')
    login_url='bases:login'
    permission_required='vino.change_reserva'
    success_message='Categoria editada exitosamente'
    #permission_required='vino.delete_reserva'

class UnidadView(SuccessMessageMixin,SinPrivilegios,ListView):
    model=Unidad
    context_object_name='obj'
    template_name='vinos/unidades.html'
    login_url='bases:login'
    permission_required='vino.view_unidad'
    
class UnidadNew(SuccessMessageMixin,SinPrivilegios,CreateView):
    model=Unidad
    form_class=UnidadNewForm
    context_object_name='obj'
    template_name='vinos/crearunidad.html'
    success_url=reverse_lazy('vino:unidades')
   
    permission_required='vino.add_unidad'
    success_message='Unidad creada exitosamente'
class UnidadUpdate(SuccessMessageMixin,SinPrivilegios,UpdateView):
    model=Unidad
    form_class=UnidadNewForm
    context_object_name='obj'
    template_name='vinos/crearunidad.html'
    success_url=reverse_lazy('vino:unidades')

    permission_required='vino.change_unidad'
    success_message='Unidad editada exitosamente'

    

class VinoView(SuccessMessageMixin,SinPrivilegios,ListView): 
    model=Vino
    context_object_name='obj'
    template_name='vinos/vinos.html'
    login_url='bases:login'
    permission_required='vino.view_vino'
class VinoNew(SuccessMessageMixin,MixinFormInvalid,SinPrivilegios,CreateView): 
    model=Vino
    form_class=VinoNewForm
    context_object_name='obj'
    template_name='vinos/modalvino.html'
    success_url=reverse_lazy('vino:vinos')
    login_url='bases:login'
    permission_required='vino.add_vino'
    success_message='Producto creado exitosamente'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

    
    def get_context_data(self , **kwargs):
        context=super(VinoNew , self).get_context_data(**kwargs)
        context['cepa']=Cepa.objects.filter(estado=True)
        context['bodega']=Bodega.objects.filter(estado=True)
        context['unidad']=Unidad.objects.filter(estado=True)
        context['reserva']=Reserva.objects.filter(estado=True)
        print(context)
        return context
class VinoUpdate(SuccessMessageMixin, MixinFormInvalid,SinPrivilegios,UpdateView): 
    model=Vino
    form_class=VinoNewForm
    context_object_name='obj'
    template_name='vinos/modalvino.html'
    success_url=reverse_lazy('vino:vinos')
    login_url='bases:login'
    permission_required='vino.change_vino'
    success_message='Producto editado exitosamente'
    #permission_required='vino.delete_vino'
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context=super(VinoUpdate , self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['cepa']=Cepa.objects.filter(estado=True)
        context['bodega']=Bodega.objects.filter(estado=True)
        context['unidad']=Unidad.objects.filter(estado=True)
        context['reserva']=Reserva.objects.filter(estado=True)
        context["obj"] = Vino.objects.filter(pk=pk).first()
        return context