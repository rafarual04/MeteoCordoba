from django.shortcuts import redirect, render, get_object_or_404
from .models import RegistroHorario, RegistroDiario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import F, Q, Avg, Sum
from .forms import RegistroDiarioForm, RegistroHorarioForm

# ==========================================
# HELPERS Y DECORADORES DE SEGURIDAD
# ==========================================
def _obtener_entorno_crud(escala):
    """Retorna el Modelo y el Formulario correspondiente según la escala."""
    if escala == 'diario':
        return RegistroDiario, RegistroDiarioForm
    return RegistroHorario, RegistroHorarioForm

def es_administrador(user):
    """Verifica si el usuario está autenticado y pertenece al staff."""
    return user.is_authenticated and user.is_staff

# ==========================================
# VISTAS PRINCIPALES DE LA WEB
# ==========================================
def index(request):
    """Página de inicio con el estado actual del sistema"""
    total_horas = RegistroHorario.objects.count()
    total_dias = RegistroDiario.objects.count()
    context = {
        'total_horas': total_horas,
        'total_dias': total_dias,
    }
    return render(request, 'index.html', context)

@login_required
def vista_datos(request):
    tipo_vista = request.GET.get('tipo', 'diario') # 'diario' por defecto
    page_number = request.GET.get('page')
    
    # 1. Filtramos según el tipo
    if tipo_vista == 'horario':
        queryset = RegistroHorario.objects.all().order_by('-fecha')
        titulo = "Detalle de Registros Horarios"
    else:
        # Aquí iría tu lógica de promedios diarios o el modelo de medias
        queryset = RegistroDiario.objects.all().order_by('-fecha') 
        titulo = "Resumen de Medias Diarias"

    # 2. Paginación: 10 registros por página
    paginator = Paginator(queryset, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'registros': page_obj,
        'tipo_vista': tipo_vista,
        'titulo': titulo,
    }
    return render(request, 'datos.html', context)

@login_required
def panel_alertas(request):
    """Vista de gestión de alertas con paginación y filtrado por escala"""
    tipo_vista = request.GET.get('tipo', 'diario')
    page_number = request.GET.get('page')
    
    # 1. Selección de QuerySet según el parámetro 'tipo'
    if tipo_vista == 'diario':
        queryset = RegistroDiario.objects.filter(
            Q(alerta_sequedad_relativa=1) | 
            Q(alerta_bateria_baja=1) | 
            Q(alerta_panel_bajo=1)
        ).order_by('-fecha')
    else:
        # Escala horaria incluye alertas de red y cambios bruscos
        queryset = RegistroHorario.objects.filter(
            Q(alerta_sequedad_relativa=1) | 
            Q(alerta_bateria_baja=1) | 
            Q(alerta_panel_bajo=1) | 
            Q(alerta_subida_brusca=1) | 
            Q(alerta_caida_brusca=1) | 
            Q(alerta_hueco_temporal=1)
        ).order_by('-fecha')

    # 2. Configuración del Paginator (10 elementos para el grid 2x5)
    paginator = Paginator(queryset, 10)
    page_obj = paginator.get_page(page_number)

    # 3. Cálculo del rango de páginas para evitar desbordamiento en el UI
    # (Esto permite que el HTML itere sobre un rango controlado)
    index = page_obj.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    context = {
        'registros': page_obj,
        'tipo_vista': tipo_vista,
        'page_range': page_range, # Pasamos el rango calculado
    }
    return render(request, 'alertas.html', context)

@login_required
def dashboard(request):
    # 1. Históricos
    historico_diario = RegistroDiario.objects.all().order_by('fecha')
    historico_horario = RegistroHorario.objects.all().order_by('fecha')
    
    # 2. Datos Escala DIARIA (Promedios globales y sumas totales)
    data_diaria = {
        'hum': RegistroDiario.objects.aggregate(a=Avg('humedad_media_global'))['a'],
        'temp': RegistroDiario.objects.aggregate(a=Avg('temperatura_promedio_global'))['a'],
        'bat': RegistroDiario.objects.aggregate(a=Avg('bateria_v'))['a'],
        'predic': RegistroDiario.objects.all().order_by('-fecha').first().predic_humedad_futura if RegistroDiario.objects.exists() else 0,
        'seq': RegistroDiario.objects.aggregate(s=Sum('alerta_sequedad_relativa'))['s'],
        'ene': RegistroDiario.objects.aggregate(s=Sum(F('alerta_bateria_baja') + F('alerta_panel_bajo')))['s'],
        'tem': RegistroDiario.objects.aggregate(s=Sum(F('alerta_subida_brusca') + F('alerta_caida_brusca')))['s'],
    }

    # 3. Datos Escala HORARIA (Promedios y sumas de los últimos 200 registros)
    data_horaria = {
        'hum': RegistroHorario.objects.aggregate(a=Avg('humedad_media_global'))['a'],
        'temp': RegistroHorario.objects.aggregate(a=Avg('temperatura_promedio_global'))['a'],
        'bat': RegistroHorario.objects.aggregate(a=Avg('bateria_v'))['a'],
        'predic': RegistroHorario.objects.all().order_by('-fecha').first().predic_humedad_futura if RegistroHorario.objects.exists() else 0,
        'seq': RegistroHorario.objects.aggregate(s=Sum('alerta_sequedad_relativa'))['s'],
        'ene': RegistroHorario.objects.aggregate(s=Sum(F('alerta_bateria_baja') + F('alerta_panel_bajo')))['s'],
        'tem': RegistroHorario.objects.aggregate(s=Sum(F('alerta_subida_brusca') + F('alerta_caida_brusca')))['s'],
    }

    return render(request, 'dashboard.html', {
        'historico_diario': historico_diario,
        'historico_horario': historico_horario,
        'd': data_diaria,
        'h': data_horaria
    })

    
def registro_usuario(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            usuario.is_staff = False 
            usuario.save()
            messages.success(request, '¡Cuenta creada con éxito! Ya puedes iniciar sesión.')
            return redirect('login')
        else:
            # Capturamos los errores en inglés de Django y los traducimos al vuelo
            for field in form:
                for error in field.errors: 
                    error_str = str(error).lower()
                    
                    # Traducción de errores de contraseña
                    if "too common" in error_str:
                        messages.error(request, "La contraseña es demasiado común. Elige otra más segura.")
                    elif "entirely numeric" in error_str:
                        messages.error(request, "La contraseña no puede contener solo números.")
                    elif "too short" in error_str:
                        messages.error(request, "La contraseña es demasiado corta (debe tener mínimo 8 caracteres).")
                    elif "mismatch" in error_str or "didn't match" in error_str:
                        messages.error(request, "Las contraseñas introducidas no coinciden.")
                    
                    # Traducción de errores de nombre de usuario
                    elif "already exists" in error_str:
                        messages.error(request, "Este nombre de usuario ya está registrado. Elige otro.")
                    elif "letters, digits" in error_str:
                        messages.error(request, "El nombre de usuario solo puede contener letras, números y los caracteres @/./+/-/_")
                    elif "max_length" in error_str or "at most" in error_str:
                        messages.error(request, f"El campo {field.label} es demasiado largo.")
                        
                    # Por si se nos escapa alguno muy raro, lo cubrimos elegantemente en español
                    else:
                        messages.error(request, f"El dato introducido en el campo de usuario o contraseña no es válido.")
    else:
        form = UserCreationForm()
        
    return render(request, 'registration/registro.html', {'form': form})

# ==========================================
# CONTROLADORES CRUD (SOLO PARA ADMINISTRADORES)
# ==========================================
@login_required
@user_passes_test(es_administrador)
def crear_registro(request, escala):
    Modelo, Formulario = _obtener_entorno_crud(escala)
    
    if request.method == 'POST':
        form = Formulario(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            
            # Cálculo de percentiles del histórico de datos
            valores_historicos = Modelo.objects.all()
            total_registros = valores_historicos.count()
            
            # Valores por defecto si la base de datos está vacía
            p20_humedad = 20.0
            p80_temp = 30.0
            p10_bateria = 3.4
            
            if total_registros > 0:
                # Consultas optimizadas a la base de datos
                humedades = valores_historicos.order_by('humedad_media_global').values_list('humedad_media_global', flat=True)
                temps = valores_historicos.order_by('temperatura_promedio_global').values_list('temperatura_promedio_global', flat=True)
                baterias = valores_historicos.order_by('bateria_v').values_list('bateria_v', flat=True)
                
                p20_humedad = humedades[max(0, int(total_registros * 0.20) - 1)]
                p80_temp = temps[max(0, int(total_registros * 0.80) - 1)]
                p10_bateria = baterias[max(0, int(total_registros * 0.10) - 1)]

            # Aplicación de las condiciones de alertas de la tabla
            
            # 1. Sequedad relativa (Nivel Alto)
            registro.alerta_sequedad_relativa = (
                registro.humedad_media_global < p20_humedad and 
                registro.temperatura_promedio_global > p80_temp
            )
            
            # 4. Batería baja (Nivel Medio)
            registro.alerta_bateria_baja = registro.bateria_v < p10_bateria
            
            # 5. Panel solar bajo en horario diurno (Nivel Medio: de 10:00h a 17:00h)
            hora_registro = registro.fecha.hour if hasattr(registro.fecha, 'hour') else 12
            if 10 <= hora_registro <= 17:
                registro.alerta_panel_bajo = registro.panel_solar_v < 1.5
            else:
                registro.alerta_panel_bajo = False

            # Búsqueda del último registro para deltas y huecos temporales
            ultimo_registro = Modelo.objects.all().order_by('-fecha').first()
            if ultimo_registro:
                dif_humedad = registro.humedad_media_global - ultimo_registro.humedad_media_global
                horas_desfase = (registro.fecha - ultimo_registro.fecha).total_seconds() / 3600.0
                
                if escala == 'horario':
                    # 2. Subida brusca de humedad (> 5% en una hora)
                    registro.alerta_subida_brusca = dif_humedad > 5.0
                    # 3. Caída brusca de humedad (< -5% en una hora)
                    registro.alerta_caida_brusca = dif_humedad < -5.0
                    # 6. Hueco temporal (Más de una hora)
                    registro.alerta_hueco_temporal = horas_desfase > 1.05
                else:
                    registro.alerta_subida_brusca = dif_humedad > 10.0
                    registro.alerta_caida_brusca = dif_humedad < -10.0
                    registro.alerta_hueco_temporal = horas_desfase > 26.0
            else:
                registro.alerta_subida_brusca = False
                registro.alerta_caida_brusca = False
                registro.alerta_hueco_temporal = False

            registro.save()
            messages.success(request, f"Registro {escala} guardado con las nuevas reglas analizadas.")
            return redirect(f"/datos/?tipo={escala}")
        else:
            messages.error(request, "Error en los datos introducidos.")
    else:
        form = Formulario()
        
    return render(request, 'crud/form_registro.html', {'form': form, 'escala': escala, 'accion': 'Crear'})

@login_required
@user_passes_test(es_administrador)
def editar_registro(request, escala, pk):
    Modelo, Formulario = _obtener_entorno_crud(escala)
    registro = get_object_or_404(Modelo, pk=pk)
    
    if request.method == 'POST':
        form = Formulario(request.POST, instance=registro)
        if form.is_valid():
            registro = form.save(commit=False)
            
            # Recalcular percentiles del histórico excluyendo el registro que se edita
            valores_historicos = Modelo.objects.exclude(pk=pk)
            total_registros = valores_historicos.count()
            
            p20_humedad = 20.0
            p80_temp = 30.0
            p10_bateria = 3.4
            
            if total_registros > 0:
                humedades = valores_historicos.order_by('humedad_media_global').values_list('humedad_media_global', flat=True)
                temps = valores_historicos.order_by('temperatura_promedio_global').values_list('temperatura_promedio_global', flat=True)
                baterias = valores_historicos.order_by('bateria_v').values_list('bateria_v', flat=True)
                
                p20_humedad = humedades[max(0, int(total_registros * 0.20) - 1)]
                p80_temp = temps[max(0, int(total_registros * 0.80) - 1)]
                p10_bateria = baterias[max(0, int(total_registros * 0.10) - 1)]

            # Revaluación de condiciones al editar
            registro.alerta_sequedad_relativa = (
                registro.humedad_media_global < p20_humedad and 
                registro.temperatura_promedio_global > p80_temp
            )
            registro.alerta_bateria_baja = registro.bateria_v < p10_bateria
            
            hora_registro = registro.fecha.hour if hasattr(registro.fecha, 'hour') else 12
            if 10 <= hora_registro <= 17:
                registro.alerta_panel_bajo = registro.panel_solar_v < 1.5
            else:
                registro.alerta_panel_bajo = False

            # Búsqueda del registro cronológicamente anterior al editado
            registro_previo = Modelo.objects.filter(fecha__lt=registro.fecha).order_by('-fecha').first()
            if registro_previo:
                dif_humedad = registro.humedad_media_global - registro_previo.humedad_media_global
                horas_desfase = (registro.fecha - registro_previo.fecha).total_seconds() / 3600.0
                
                if escala == 'horario':
                    registro.alerta_subida_brusca = dif_humedad > 5.0
                    registro.alerta_caida_brusca = dif_humedad < -5.0
                    registro.alerta_hueco_temporal = horas_desfase > 1.05
                else:
                    registro.alerta_subida_brusca = dif_humedad > 10.0
                    registro.alerta_caida_brusca = dif_humedad < -10.0
                    registro.alerta_hueco_temporal = horas_desfase > 26.0
            
            registro.save()
            messages.success(request, f"Registro {escala} actualizado y alertas recalculadas según normativa.")
            return redirect(f"/datos/?tipo={escala}")
        else:
            messages.error(request, "Error al actualizar el registro.")
    else:
        form = Formulario(instance=registro)
        
    return render(request, 'crud/form_registro.html', {'form': form, 'escala': escala, 'accion': 'Editar', 'registro': registro})

@login_required
@user_passes_test(es_administrador)
def eliminar_registro(request, escala, pk):
    Modelo, _ = _obtener_entorno_crud(escala)
    registro = get_object_or_404(Modelo, pk=pk)
    
    if request.method == 'POST':
        registro.delete()
        messages.success(request, f"Registro eliminado correctamente de la escala {escala}.")
        return redirect(f"/datos/?tipo={escala}")
        
    return render(request, 'crud/confirmar_eliminar.html', {'registro': registro, 'escala': escala})