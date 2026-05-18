from django import forms
from .models import RegistroDiario, RegistroHorario

class RegistroDiarioForm(forms.ModelForm):
    class Meta:
        model = RegistroDiario
        # Excluimos las 6 alertas de la lista para que no se le pidan al usuario
        fields = [
            'fecha', 
            'humedad_media_global', 
            'temperatura_promedio_global', 
            'bateria_v', 
            'panel_solar_v', 
            'predic_humedad_futura'
        ]
        
        # Etiquetas personalizadas para los campos en el formulario HTML
        labels = {
            'fecha': 'Fecha del Resumen',
            'humedad_media_global': 'Humedad Media (%)',
            'temperatura_promedio_global': 'Temperatura Promedio (°C)',
            'bateria_v': 'Voltaje de Batería (V)',
            'panel_solar_v': 'Voltaje de Panel Solar (V)',
            'predic_humedad_futura': 'Humedad Prevista IA (%)',
        }
        
        # Atributos HTML y estilos de Bootstrap para renderizar los inputs
        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control shadow-sm'
            }),
            'humedad_media_global': forms.NumberInput(attrs={
                'class': 'form-control shadow-sm', 
                'step': '0.1', 
                'min': '0', 
                'max': '100',
                'placeholder': 'Ej: 55.4'
            }),
            'temperatura_promedio_global': forms.NumberInput(attrs={
                'class': 'form-control shadow-sm', 
                'step': '0.1',
                'placeholder': 'Ej: 24.5'
            }),
            'bateria_v': forms.NumberInput(attrs={
                'class': 'form-control shadow-sm', 
                'step': '0.01', 
                'min': '0',
                'placeholder': 'Ej: 4.15'
            }),
            'panel_solar_v': forms.NumberInput(attrs={
                'class': 'form-control shadow-sm', 
                'step': '0.01', 
                'min': '0',
                'placeholder': 'Ej: 1.85'
            }),
            'predic_humedad_futura': forms.NumberInput(attrs={
                'class': 'form-control shadow-sm', 
                'step': '0.1', 
                'min': '0', 
                'max': '100',
                'placeholder': 'Ej: 53.0'
            }),
        }


class RegistroHorarioForm(forms.ModelForm):
    class Meta:
        model = RegistroHorario
        fields = [
            'fecha', 
            'humedad_media_global', 
            'temperatura_promedio_global', 
            'bateria_v', 
            'panel_solar_v', 
            'predic_humedad_futura'
        ]
        
        labels = {
            'fecha': 'Fecha y Hora Exacta',
            'humedad_media_global': 'Humedad (%)',
            'temperatura_promedio_global': 'Temperatura (°C)',
            'bateria_v': 'Voltaje de Batería (V)',
            'panel_solar_v': 'Voltaje de Panel Solar (V)',
            'predic_humedad_futura': 'Humedad Prevista IA para Próxima Hora (%)',
        }
        
        widgets = {
            'fecha': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'class': 'form-control shadow-sm'
            }),
            'humedad_media_global': forms.NumberInput(attrs={
                'class': 'form-control shadow-sm', 
                'step': '0.1', 
                'min': '0', 
                'max': '100',
                'placeholder': 'Ej: 62.1'
            }),
            'temperatura_promedio_global': forms.NumberInput(attrs={
                'class': 'form-control shadow-sm', 
                'step': '0.1',
                'placeholder': 'Ej: 18.3'
            }),
            'bateria_v': forms.NumberInput(attrs={
                'class': 'form-control shadow-sm', 
                'step': '0.01', 
                'min': '0',
                'placeholder': 'Ej: 3.98'
            }),
            'panel_solar_v': forms.NumberInput(attrs={
                'class': 'form-control shadow-sm', 
                'step': '0.01', 
                'min': '0',
                'placeholder': 'Ej: 0.00'
            }),
            'predic_humedad_futura': forms.NumberInput(attrs={
                'class': 'form-control shadow-sm', 
                'step': '0.1', 
                'min': '0', 
                'max': '100',
                'placeholder': 'Ej: 61.5'
            }),
        }