from django import forms

from .models import Animal,Res,VentaReses



class AnimalForm(forms.ModelForm):
    class Meta:
        model=Animal
        fields=(
            'tropa',
            'peso_animal'
        )
class EditarRes(forms.ModelForm):
    class Meta:
        model=Res
        fields=('__all__')
        
        #METODO 1
        widgets = {
                'nombre': forms.TextInput(attrs={'disabled':'disabled'}),
               # 'nombre': forms.TextInput(attrs={'readonly':'True'}),
                
            }   
    #METODO 2
    def __init__(self, *args, **kwargs):
        super(EditarRes, self).__init__(*args, **kwargs)
        self.fields['animal'].widget.attrs['disabled']='disabled'
        #self.fields['nombre'].widget.attrs['disabled']='disabled'

class VenderRes(forms.ModelForm):
    class Meta:
        model=VentaReses
        fields=('res' ,'cliente' ,'precio' ,'medio_pago','estado')