from  django.urls import path , include
from .views import VinoList , VinoDetalle

urlpatterns=[
    path('v1/productos/' ,VinoList.as_view() , name='vinolista'),
    path('v1/productos/<str:codigo>', VinoDetalle.as_view(),name='vinodetalle')

]