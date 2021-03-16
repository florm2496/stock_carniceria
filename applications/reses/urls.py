from django.urls import path , include, re_path
from .views import ResesListView,UpdateResesView,AñadirAnimal,ListTropas,CreateTropa,UpdateTropa,ListarAnimales,VentaResesCreate,VentaResesUpdate,VentaResesList

urlpatterns = [
    #path('registrares/' , ResCreateView.as_view() , name='registrares'),
    path('listareses/' , ResesListView.as_view() , name='listareses'),
    path('updatereses/<int:pk>' ,UpdateResesView.as_view() , name='updatereses'),

    #path('animal/<int:pk>' ,AñadirAnimal.as_view() , name='animal'),
    path('animal/<int:pk>' ,AñadirAnimal , name='animal'),
    path('animales/<int:pk>' ,ListarAnimales.as_view() , name='animales'),

    path('tropas/' ,ListTropas.as_view() , name='tropas'),
    path('añadirtropa/' ,CreateTropa.as_view() , name='añadirtropa'),
    path('editartropa/<int:pk>' ,UpdateTropa.as_view() , name='editartropa'),

    path('venderes/<int:pk>' ,VentaResesCreate.as_view() , name='venderes'),
    path('listaresesvendidas' ,VentaResesList.as_view(), name='listaresesvendidas' ),
    path('vendereseditar/<int:pk>' ,VentaResesUpdate.as_view() , name='vendereseditar'),
]