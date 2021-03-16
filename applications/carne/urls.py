from django.urls import path

from .views import CrearCorte , ListaCortes,ActualizarCorte
urlpatterns = [
    path('crearcorte' , CrearCorte.as_view() ,name='crearcorte'),
    path('listacortes' , ListaCortes.as_view() , name='listacortes'),
    path('actualizarcorte/<int:pk>' , ActualizarCorte.as_view() , name='actualizarcorte')
    
]