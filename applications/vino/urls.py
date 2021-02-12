from django.urls import path , include 
from .views import CepaView ,CepaUpdate, UnidadView,UnidadNew,UnidadUpdate , BodegaView , ReservaView , VinoView,VinoNew,VinoUpdate ,CepaNew,BodegaNew,ReservaNew,BodegaUpdate,ReservaUpdate
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('cepas/',CepaView.as_view(),name='cepas'),
     path('cepas/new/',CepaNew.as_view(),name='cepanew'),
     path('cepas/cepaupdate/<int:pk>',CepaUpdate.as_view(),name='cepaupdate'),
    path('unidades/',UnidadView.as_view(),name='unidades'),
    path('unidades/unidadnew',UnidadNew.as_view(),name='crearunidad'),
    path('unidades/unidadupdate/<int:pk>/',UnidadUpdate.as_view(),name='unidadupdate'),
    path('reservas/',ReservaView.as_view(),name='reservas'),
    path('reservas/creareserva/',ReservaNew.as_view(),name='creareserva'),
     path('reservas/update/<int:pk>/',ReservaUpdate.as_view(),name='reservaupdate'),
    path('bodegas/',BodegaView.as_view(),name='bodegas'),
    path('bodegas/new/',BodegaNew.as_view(),name='crearbodega'),
    path('bodegas/update/<int:pk>/',BodegaUpdate.as_view(),name='bodegaupdate'),
    path('vinos/',VinoView.as_view(),name='vinos'),
    path('vinos/new/',VinoNew.as_view(),name='crearvino'),
    path('vinos/update/<int:pk>/',VinoUpdate.as_view(),name='vinoupdate'),
    
]