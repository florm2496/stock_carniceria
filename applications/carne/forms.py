from django import forms
from .models import Cortes

class CrearCorteForm(forms.ModelForm):
    class Meta:
        model=Cortes
        fields=('__all__')
        #labels={'medida':'Medida'}
        widget={'descripcion':forms.TextInput, 'precio':forms.NumberInput(attrs={'required':True})}

    def __init__(self, *args, **kwargs): #SE SOBRESCRIBE EL CONSTRUCTOR DEL FORMULARIO
        super().__init__(*args, **kwargs) #SE INVOCA EL CONSTRUCTOR
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control',
            })
            self.fields['cant_vendida'].widget.attrs['readonly']=True