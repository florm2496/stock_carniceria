from django.shortcuts import render 
from django.urls import reverse_lazy

# Create your views here.
from .models import Res

from django.views.generic import CreateView , UpdateView,ListView




class ResCreateView(CreateView):
    model = Res
    fields='__all__'
    template_name = "reses/creares.html"
    success_url=reverse_lazy('reses:listareses')

    
class ResesListView(ListView):
    model=Res
    context_object_name='obj'
    template_name = "reses/listareses.html"

class UpdateResesView(UpdateView):
    model=Res
    fields='__all__'
    template_name = "reses/creares.html"
    success_url=reverse_lazy('reses:listareses')