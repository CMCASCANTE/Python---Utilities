from django.http import HttpResponse
from django.shortcuts import render
import os
from django.shortcuts import render
from django.conf import settings

def index(request):

    # Contador de visitas 
    total_visits = 0
    # Lee el contador directamente del archivo
    with settings.VISIT_COUNTER_LOCK: # Usa el mismo bloqueo para leer el archivo
        try:
            with open(settings.VISIT_COUNTER_FILE, 'r') as f:
                total_visits_str = f.read().strip()
                try:
                    total_visits = int(total_visits_str)
                except ValueError:
                    total_visits = 0 # Si el archivo está corrupto
        except FileNotFoundError:
            total_visits = 0 # Si el archivo aún no existe (aunque el middleware lo crea)
        except IOError as e:
            print(f"Error al leer el archivo del contador en la vista: {e}")

    context = {
        'total_visits': total_visits,
    }





    return HttpResponse(render(request, "../templates/index.html", context))