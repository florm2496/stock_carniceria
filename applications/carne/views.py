from django.shortcuts import render
from .models import Cortes
from django.views.generic import CreateView,ListView,UpdateView
from django.urls import reverse_lazy
from .forms import CrearCorteForm


class CrearCorte(CreateView):
    form_class=CrearCorteForm
    template_name = "carne/crearcorte.html"
    success_url=reverse_lazy('carne:listacortes')


class ListaCortes(ListView):
    model = Cortes
    template_name = "carne/listacortes.html"
    context_object_name='obj'

class ActualizarCorte(UpdateView):
    model=Cortes
    form_class=CrearCorteForm
    context_object_name='obj'
    template_name = "carne/crearcorte.html"
    success_url=reverse_lazy('carne:listacortes')


