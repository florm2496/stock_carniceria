from django.shortcuts import render ,redirect
from django.urls import reverse_lazy

# Create your views here.
from .models import Res,Animal,Tropa,VentaReses
from applications.ventas.models import Cliente
from django.views.generic import CreateView , UpdateView,ListView,FormView

from .forms import AnimalForm,EditarRes,VenderRes

'''
class ResCreateView(CreateView):
    model = Res
    fields=('peso_inicial','peso_final','nombre')
    template_name = "reses/creares.html"
    success_url=reverse_lazy('reses:listareses')
'''
    
class ResesListView(ListView):
    model=Res
    context_object_name='obj'
    template_name = "reses/listareses.html"

class UpdateResesView(UpdateView):
    model=Res
    form_class=EditarRes
    template_name = "reses/creares.html"
    success_url=reverse_lazy('reses:listareses')

class CreateTropa(CreateView):
    model=Tropa
    fields='__all__'
    template_name='reses/añadirtropa.html'
    object_name='obj'
    success_url=reverse_lazy('reses:tropas')
class UpdateTropa(UpdateView):
    model=Tropa
    fields='__all__'
    template_name='reses/añadirtropa.html'
    object_name='obj'
    success_url=reverse_lazy('reses:tropas')

class ListTropas(ListView):
    model=Tropa
    context_object_name='obj'
    template_name='reses/tropas.html'


def AñadirAnimal(request,**kwargs):
    template_name='reses/animal.html'
    contexto={}
    
    animal={}
    #OBTENGO EL ID PASADO EN LA URL PARA PODER FILTRAR LA TOPA CORRESPONDIENTE
    ID= kwargs['pk']
    tropa=Tropa.objects.filter(id=ID)
    

    if request.method=='POST':
            #OBTENGO EL ID DEL FORMULARIO
            id_tropa=request.POST.get('tropa')
            #CON ESE ID OBTENGO EL OBJETO,PORQUE SE DEBE GUARDAR UNA INSTANCIA DEL OBJETO , NO SU ID
            tropa=Tropa.objects.get(pk=id_tropa) #USO GET PORQUE OBTENGO DIRECTAMENTE EL OBJETO , SI USO FILTER OBTENGO UN QUERYSET
            peso_animal=request.POST.get('peso_animal')
           
            #obtener el numnero del animal anterior
            anm_ant=Animal.objects.filter(tropa=id_tropa).last()
            print(anm_ant)
            if anm_ant is None:
                num=0
            else:
                num=anm_ant.numero
                

            animal=Animal(
                numero=num+1,
                tropa=tropa,
                peso_animal=peso_animal,

            )  
            animal.save()
            #animal.ident='animal:{}-{}'.format(animal.id , animal.tropa)
            #animal.save()
            #HASTA AQUI ESTA CUBIERTA LA CREACION DEL ANIMAL

            
            return redirect('reses:animales',pk=ID) #se pasa el id  para filtrar el listado de animales segun la tropa


           

    contexto={
        'tropa':tropa,
    }

    return render(request, template_name,contexto)
 
class ListarAnimales(ListView):
    model=Animal 
    template_name='reses/listanimales.html'
    
    
    def get_context_data(self, **kwargs):
        context=super(ListarAnimales , self).get_context_data(**kwargs)
        id=self.kwargs['pk']

        context['lista']=Animal.objects.filter(
            tropa=id
        )
        return context
    
class VentaResesCreate(CreateView):
    form_class=VenderRes
    template_name='reses/venderes.html'
    success_url=reverse_lazy('reses:listaresesvendidas')

    
    def get_context_data(self, **kwargs):
        #SE PASA EL ID DE LA RES QUE SE QUIERE VENDER
        ID=self.kwargs['pk']

        context = super(VentaResesCreate, self).get_context_data(**kwargs)
        context['reses']=Res.objects.filter(id=ID)
        context['clientes']=Cliente.objects.filter(estado=True)
        return context


class VentaResesUpdate(UpdateView):
    model=VentaReses
    form_class=VenderRes
    context_object_name='obj'
    template_name='reses/venderes.html'
    success_url=reverse_lazy('reses:listaresesvendidas')

                 

class VentaResesList(ListView):
    model=VentaReses
    
    template_name='reses/listaventareses.html'
    context_object_name='obj'
    

'''
#class VentaResesEdit()
 def get_queryset(self):
        obj = super(VentaResesList, self).get_queryset()
        
        return obj.filter(vendida=True)
class AñadirAnimal(CreateView):
    model=Animal
    template_name='reses/animal.html'
    fields=('tropa','peso_animal')
    #form_class=AnimalForm
    #context_object_name='obj'
    success_url=reverse_lazy('reses:listareses')

    #esto funciona , pero no guardaba el ID hasta hacerse efectivo el ID en la base de datos. ya se el id definido en los modelos
    #o el que proporciona la ORM.
    #Si funcionaba con los otros campos
    #no se asigna id a un registro hasta que este se guarda con exito en la base de datos


    def form_valid(self,form):
        animal=form.save(commit=False)
        animal.ident='animal:{}-tropa{}'.format(animal.ID, animal.tropa)
        animal.save()

        return super(AñadirAnimal ,self).form_valid(form)

soluciones para crear las reses automaticamente luego de crear el animal:
1-
 
def CrearRes():
    animal=Animal.objects.last()
    res=Res(
        animal=animal,
        peso_inicial=0,
        peso_final=0,
        uc=animal.uc,
        
    )
    res.save()

llamando a la funcion al final de  la vista de añadir animal 
resultado: funcionaba pero la funcion se ejecutaba antes de crear el animal nuevo 
, por lo tanto agarraba el anterior y no el actual

class AñadirAnimal(FormView):
    #en el form view no hace falta asignar un modelo , este ya se asigna en el form relacionado a la vista
    template_name='reses/animal.html'
    form_class=AnimalForm
    context_object_name='obj'
    success_url=reverse_lazy('reses:tropas')
    

    def get_context_data(self, **kwargs):
        #este id lo obtengo de la URL
        ID= self.kwargs['pk']
        print('id',ID)

        context=super(AñadirAnimal , self).get_context_data(**kwargs)
        #HAGO FILTRO POR ID PARA ENVIAR SOLO LA TROPA CORRESPONDIENTE
        context['tropa']=Tropa.objects.filter(id=ID)
        print('----',context['tropa'])
        return context
    

    def form_valid(self,form):
        #de esta forma no se interactua directamente con la ORM de django
        
        animal=Animal(
            tropa=form.cleaned_data['tropa'],
            peso_animal=form.cleaned_data['peso_animal'],
        ) 
        animal.save()
        animal.ident='animal:{}-{}'.format(animal.id , animal.tropa)
        animal.save()
        return super(AñadirAnimal , self).form_valid(form)
'''
