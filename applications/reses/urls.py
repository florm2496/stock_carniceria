from django.urls import path , include, re_path
from .views import ResCreateView,ResesListView,UpdateResesView

urlpatterns = [
    path('registrares/' , ResCreateView.as_view() , name='registrares'),
    path('listareses/' , ResesListView.as_view() , name='listareses'),
    path('updatereses/<int:pk>' ,UpdateResesView.as_view() , name='updatereses'),
]