import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from clima_app.models import RegistroHorario, RegistroDiario

class Command(BaseCommand):
    help = 'Importa de forma automática los datos de los CSVs horario y diario a la base de datos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('=== Iniciando proceso de importación ==='))

        # -----------------------------------------------------------------
        # 1. IMPORTACIÓN DEL DATASET HORARIO
        # -----------------------------------------------------------------
        try:
            with open('agrodata_horario_completo.csv', mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                registros_horarios = []
                
                # Limpiamos duplicados previos para evitar colisiones
                RegistroHorario.objects.all().delete()
                
                for row in reader:
                    # Convertimos la fecha de texto a un objeto datetime consciente de la zona horaria
                    fecha_dt = datetime.strptime(row['Fecha'], '%Y-%m-%d %H:%M:%S')
                    fecha_consciente = make_aware(fecha_dt)
                    
                    registros_horarios.append(RegistroHorario(
                        fecha=fecha_consciente,
                        humedad_media_global=float(row['Humedad_Media_Global']),
                        temperatura_promedio_global=float(row['Temperatura_Promedio_Global']),
                        bateria_v=float(row['Bateria_V']),
                        panel_solar_v=float(row['Panel_Solar_V']),
                        alerta_sequedad_relativa=int(float(row['alerta_sequedad_relativa'])),
                        alerta_subida_brusca=int(float(row['alerta_subida_brusca'])),
                        alerta_caida_brusca=int(float(row['alerta_caida_brusca'])),
                        alerta_bateria_baja=int(float(row['alerta_bateria_baja'])),
                        alerta_panel_bajo=int(float(row['alerta_panel_bajo'])),
                        alerta_hueco_temporal=int(float(row['alerta_hueco_temporal'])),
                        predic_humedad_futura=float(row['predic_humedad_futura']),
                        predic_sequedad_relativa=int(float(row['predic_sequedad_relativa'])),
                        predic_bateria_baja=int(float(row['predic_bateria_baja'])),
                        predic_panel_bajo=int(float(row['predic_panel_bajo'])),
                        predic_hueco_temporal=int(float(row['predic_hueco_temporal']))
                    ))
                
                # Inyección masiva ultra rápida
                RegistroHorario.objects.bulk_create(registros_horarios)
                self.stdout.write(self.style.SUCCESS(f'Éxito: Se han cargado {len(registros_horarios)} registros horarios.'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Error: No se encontró el archivo "agrodata_horario_completo.csv" en la raíz.'))

        # -----------------------------------------------------------------
        # 2. IMPORTACIÓN DEL DATASET DIARIO
        # -----------------------------------------------------------------
        try:
            with open('agrodata_diario_completo.csv', mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                registros_diarios = []
                
                RegistroDiario.objects.all().delete()
                
                for row in reader:
                    # En el diario la fecha es solo Año-Mes-Día
                    fecha_date = datetime.strptime(row['Fecha'], '%Y-%m-%d').date()
                    
                    registros_diarios.append(RegistroDiario(
                        fecha=fecha_date,
                        humedad_media_global=float(row['Humedad_Media_Global']),
                        temperatura_promedio_global=float(row['Temperatura_Promedio_Global']),
                        bateria_v=float(row['Bateria_V']),
                        panel_solar_v=float(row['Panel_Solar_V']),
                        alerta_sequedad_relativa=int(float(row['alerta_sequedad_relativa'])),
                        alerta_subida_brusca=int(float(row['alerta_subida_brusca'])),
                        alerta_caida_brusca=int(float(row['alerta_caida_brusca'])),
                        alerta_bateria_baja=int(float(row['alerta_bateria_baja'])),
                        alerta_panel_bajo=int(float(row['alerta_panel_bajo'])),
                        alerta_hueco_temporal=int(float(row['alerta_hueco_temporal'])),
                        predic_humedad_futura=float(row['predic_humedad_futura']),
                        predic_sequedad_relativa=int(float(row['predic_sequedad_relativa'])),
                        predic_bateria_baja=int(float(row['predic_bateria_baja'])),
                        predic_panel_bajo=int(float(row['predic_panel_bajo'])),
                        predic_hueco_temporal=int(float(row['predic_hueco_temporal']))
                    ))
                
                RegistroDiario.objects.bulk_create(registros_diarios)
                self.stdout.write(self.style.SUCCESS(f'Éxito: Se han cargado {len(registros_diarios)} registros diarios.'))
                
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Error: No se encontró el archivo "agrodata_diario_completo.csv" en la raíz.'))

        self.stdout.write(self.style.SUCCESS('¡Importación finalizada con éxito!'))