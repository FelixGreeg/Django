from django import forms
from .models import Pregunta, Opcion

class PreguntaFormulario(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['texto_pregunta']  # Elimina 'fecha_publicacion'
    
class OpcionFormulario(forms.ModelForm):
    class Meta:
        model = Opcion
        fields = ['texto_opcion']