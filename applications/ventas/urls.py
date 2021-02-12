from django.urls import path , include

from .views import ClienteView ,ClienteNew ,VinoView, ClienteEdit,VentaListView , Ventas ,borrar_detalle_factura
from .reportes import imprimir_factura_recibo ,imprimir_factura_list
urlpatterns = [
    path('clientes/' , ClienteView.as_view() , name='clientes'),
    path('clientes/new/' , ClienteNew.as_view() , name='cliente_new'),
    path('clientes/<int:pk>' , ClienteEdit.as_view() , name='cliente_edit'),
    path('ventas/' , VentaListView.as_view() , name='ventas'),
    path('ventas/ventanew/' ,Ventas , name='ventanew'),
    path('ventas/ventaedit/<int:id>' ,Ventas , name='ventaedit'),
    path('ventas/buscar/' ,VinoView.as_view() , name='buscar'),
    path('ventas/imprimirecibo/<int:id>' , imprimir_factura_recibo ,name='imprimirecibo') ,
    path('ventas/imprimirventas/<str:f1>/<str:f2>/' , imprimir_factura_list , name='imprimirventas'),
    path('ventas/borrar-detalle/<int:id>',borrar_detalle_factura, name="factura_borrar_detalle"),
]