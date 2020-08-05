from django import forms
from .models import Persona
from django.core.exceptions import ValidationError

class PersonaFormulario(forms.ModelForm):
    # Forma 1: Declarar uno a uno los campos del modelo
    #nombre = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre', 'style': 'font-size:15px;', 'required': "required", 'class'}),                       
    #                        label="Nombre", 
    #                        label_suffix="_core", 
                            #initial="Ej: Diego", 
    #                        help_text="Escriba bien su nombre")
                            #disabled=True)

    class Meta:
        model = Persona
        fields = ('nombre', 'apellido', 'edad', 'photo')

        # Forma 2: Declarar directamente los widgets a traves de un diccionario
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Apellido'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su Edad'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'})
        }

        #help_texts = {
        #    'nombre': 'Ingrese el nombre con la primera Mayuscula'
        #}







        #help_texts = {
         #   'nombre': 'Ingrese nombre bien',
        #}
        #labels = {
            
        #}

    #def clean_edad(self):
    #    edad = self.cleaned_data['edad']
    #    if edad < 18:
    #        raise ValidationError("Tienes que ser mayo de 18 anos")
    #    return edad

    #def clean_nombre(self):
    #    nombre = self.cleaned_data['nombre']
    #    nombre = nombre.capitalize()
    #    return nombre



    #def clean_nombre(self):
    #    nombre = self.cleaned_data['nombre']
    #    if nombre == 'admin':
    #        raise ValidationError("No se permite nombre admin")
    #    nombre_l = nombre.lower()
    #    nombre_c = nombre.capitalize()
    #    return nombre_c

    def clean(self):
        cleaned_data = super(PersonaFormulario, self).clean()
        nombre = cleaned_data.get("nombre")
        apellido = cleaned_data.get("apellido")
        edad = cleaned_data.get("edad")

        if nombre == 'admin':
            raise ValidationError("No se permite nombre admin")
        else:
            nombre_c = nombre.capitalize()
        if edad <= 10:
            raise ValidationError("No se permite menores de 10 anos")
        if apellido is None:
            apellido = "N/A"
        else:
            apellido = apellido.capitalize()

        cleaned_data["nombre"] = nombre_c
        cleaned_data["apellido"] = apellido
        return cleaned_data
