from .models import Cepa , Bodega,Reserva,Unidad,Vino
from django import forms

class CepaNewForm(forms.ModelForm):
    class Meta:
        model=Cepa
        fields=['nombre','descripcion','estado']
        labels={'nombre':'Nombre','descripcion': 'Descipcion de la cepa' , 'estado':'Estado'}
        widget={'descripcion':forms.TextInput}

def __init__(self, *args, **kwargs): #SE SOBRESCRIBE EL CONSTRUCTOR DEL FORMULARIO
    super().__init__(*args, **kwargs) #SE INVOCA EL CONSTRUCTOR
    for field in iter(self.fields):
        self.fields[field].widget.attrs.update({
            'class':'form-control',
        })


class ReservaNewForm(forms.ModelForm):
    class Meta:
        model=Reserva
        fields=['tipo','descripcion' ,'estado']
        labels={'tipo':'Tipo', 'descripcion':'Descripcion' }
        #widget={'descripcion':forms.TextInput}

    def __init__(self, *args, **kwargs): #SE SOBRESCRIBE EL CONSTRUCTOR DEL FORMULARIO
        super().__init__(*args, **kwargs) #SE INVOCA EL CONSTRUCTOR
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control',
            })
class UnidadNewForm(forms.ModelForm):
    class Meta:
        model=Unidad
        fields=['medida','estado']
        labels={'medida':'Medida'}
        #widget={'descripcion':forms.TextInput}

    def __init__(self, *args, **kwargs): #SE SOBRESCRIBE EL CONSTRUCTOR DEL FORMULARIO
        super().__init__(*args, **kwargs) #SE INVOCA EL CONSTRUCTOR
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control',
            })
class VinoNewForm(forms.ModelForm):
    class Meta:
        model=Vino
        fields=['nombre','descripcion','codigo','precioventa','reserva','bodega','cepa','unidad','existencia','ultimacompra','sm','estado' ]
        #labels={'medida':'Medida'}
        widget={'descripcion':forms.TextInput, 'precioventa':forms.NumberInput(attrs={'required':True})}

    def __init__(self, *args, **kwargs): #SE SOBRESCRIBE EL CONSTRUCTOR DEL FORMULARIO
        super().__init__(*args, **kwargs) #SE INVOCA EL CONSTRUCTOR
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control',
            })
            self.fields['descripcion'].widget.attrs['required']=True
            self.fields['ultimacompra'].widget.attrs['readonly']=True
            self.fields['existencia'].widget.attrs['readonly']=True

    def clean(self):
        try:
            vino=Vino.objects.get(codigo=self.cleaned_data['codigo'])
            if not self.instance.pk:
                raise forms.ValidationError("El registro ya existe")
            elif self.instance.pk!=vino.pk:
                raise forms.ValidationError("Cambio no permitido")
        except Vino.DoesNotExist:
            pass
        return self.cleaned_data



class BodegaNewForm(forms.ModelForm):
    class Meta:
        model=Bodega
        fields=['nombre','numero','email' , 'estado']
        
        #widget={'descripcion':forms.TextInput}

    def __init__(self, *args, **kwargs): #SE SOBRESCRIBE EL CONSTRUCTOR DEL FORMULARIO
        super().__init__(*args, **kwargs) #SE INVOCA EL CONSTRUCTOR
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control',
            })
            self.fields['numero'].widget.attrs['requiered']=False
            self.fields['email'].widget.attrs['requiered']=False