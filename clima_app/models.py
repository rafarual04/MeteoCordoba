from django.db import models

class RegistroHorario(models.Model):
    """
    Modelo para almacenar el histórico detallado hora a hora (agrodata_horario_completo.csv).
    """
    fecha = models.DateTimeField(unique=True, verbose_name="Fecha y Hora")
    
    # Métricas físicas y de entorno (promedios globales)
    humedad_media_global = models.FloatField(verbose_name="Humedad Media Global (%)")
    temperatura_promedio_global = models.FloatField(verbose_name="Temperatura Promedio Global (°C)")
    
    # Métricas energéticas (escaladas a voltios)
    bateria_v = models.FloatField(verbose_name="Voltaje Batería (V)")
    panel_solar_v = models.FloatField(verbose_name="Voltaje Panel Solar (V)")
    
    # Estados actuales de alertas (mapeo binario 0/1)
    alerta_sequedad_relativa = models.IntegerField(default=0, verbose_name="Alerta Sequedad")
    alerta_subida_brusca = models.IntegerField(default=0, verbose_name="Alerta Subida Brusca")
    alerta_caida_brusca = models.IntegerField(default=0, verbose_name="Alerta Caída Brusca")
    alerta_bateria_baja = models.IntegerField(default=0, verbose_name="Alerta Batería Baja")
    alerta_panel_bajo = models.IntegerField(default=0, verbose_name="Alerta Panel Bajo")
    alerta_hueco_temporal = models.IntegerField(default=0, verbose_name="Alerta Hueco Temporal")
    
    # Predicciones de Machine Learning (horizonte t+1)
    predic_humedad_futura = models.FloatField(verbose_name="Predicción Humedad Futura (%)")
    predic_sequedad_relativa = models.IntegerField(default=0, verbose_name="Predicción Sequedad")
    predic_bateria_baja = models.IntegerField(default=0, verbose_name="Predicción Batería Baja")
    predic_panel_bajo = models.IntegerField(default=0, verbose_name="Predicción Panel Bajo")
    predic_hueco_temporal = models.IntegerField(default=0, verbose_name="Predicción Hueco Temporal")

    class Meta:
        ordering = ['-fecha']
        verbose_name = "Registro horario"
        verbose_name = "Registros horarios"

    def __str__(self):
        return f"Horario: {self.fecha.strftime('%Y-%m-%d %H:%M')}"


class RegistroDiario(models.Model):
    """
    Modelo para almacenar el histórico comprimido por días (agrodata_diario_completo.csv).
    """
    fecha = models.DateField(unique=True, verbose_name="Fecha")
    
    # Medias de variables globales
    humedad_media_global = models.FloatField(verbose_name="Humedad Media Diaria (%)")
    temperatura_promedio_global = models.FloatField(verbose_name="Temperatura Media Diaria (°C)")
    bateria_v = models.FloatField(verbose_name="Voltaje Medio Batería (V)")
    panel_solar_v = models.FloatField(verbose_name="Voltaje Medio Panel (V)")
    
    # Alertas consolidadas a nivel diario (0/1)
    alerta_sequedad_relativa = models.IntegerField(default=0)
    alerta_subida_brusca = models.IntegerField(default=0)
    alerta_caida_brusca = models.IntegerField(default=0)
    alerta_bateria_baja = models.IntegerField(default=0)
    alerta_panel_bajo = models.IntegerField(default=0)
    alerta_hueco_temporal = models.IntegerField(default=0)
    
    # Predicciones diarias de la IA (horizonte de mañana t+1)
    predic_humedad_futura = models.FloatField(verbose_name="Predicción Humedad Mañana (%)")
    predic_sequedad_relativa = models.IntegerField(default=0)
    predic_bateria_baja = models.IntegerField(default=0)
    predic_panel_bajo = models.IntegerField(default=0)
    predic_hueco_temporal = models.IntegerField(default=0)

    class Meta:
        ordering = ['-fecha']
        verbose_name = "Registro diario"
        verbose_name = "Registros diarios"

    def __str__(self):
        return f"Diario: {self.fecha.strftime('%Y-%m-%d')}"