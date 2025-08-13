# app/middleware.py
import os
from django.conf import settings
from django.http import HttpResponseForbidden

# Usamos el bloqueo definido en settings.py para asegurar la seguridad en la escritura del archivo
# Asegúrate de que VISIT_COUNTER_LOCK se inicialice en settings.py
# (No podemos importar directamente threading.Lock aquí porque cada import crearía un nuevo lock)
_visit_counter_lock = settings.VISIT_COUNTER_LOCK

class FileVisitCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Asegúrate de que el archivo exista e inicializa el contador si es la primera vez
        if not os.path.exists(settings.VISIT_COUNTER_FILE):
            with _visit_counter_lock: # Bloquea para la inicialización inicial
                try:
                    with open(settings.VISIT_COUNTER_FILE, 'w') as f:
                        f.write('0')
                except IOError as e:
                    print(f"Error al crear o inicializar el archivo del contador: {e}")




        # Versión para un archivo contador en cada apartado de la APP
        if not os.path.exists(settings.VISIT_COUNTER_FILE_DNS):
            with _visit_counter_lock: # Bloquea para la inicialización inicial
                try:
                    with open(settings.VISIT_COUNTER_FILE_DNS, 'w') as f:
                        f.write('0')
                except IOError as e:
                    print(f"Error al crear o inicializar el archivo del contador: {e}")

        if not os.path.exists(settings.VISIT_COUNTER_FILE_TELNET):
            with _visit_counter_lock: # Bloquea para la inicialización inicial
                try:
                    with open(settings.VISIT_COUNTER_FILE_TELNET, 'w') as f:
                        f.write('0')
                except IOError as e:
                    print(f"Error al crear o inicializar el archivo del contador: {e}")

        if not os.path.exists(settings.VISIT_COUNTER_FILE_BKL):
            with _visit_counter_lock: # Bloquea para la inicialización inicial
                try:
                    with open(settings.VISIT_COUNTER_FILE_BKL, 'w') as f:
                        f.write('0')
                except IOError as e:
                    print(f"Error al crear o inicializar el archivo del contador: {e}")
        







    def __call__(self, request):
        # Este código se ejecuta en cada request antes de que la vista sea llamada.

        # No queremos contar requests de admin, estáticos, media o favicons
        if (not request.path.startswith('/admin/') and
            not request.path.startswith('/static/') and
            not request.path.startswith('/media/') and
            not request.path == '/favicon.ico'): # Es común que los navegadores pidan favicon

            try:
                # Bloquea el acceso al archivo mientras se lee y escribe
                with _visit_counter_lock:
                    with open(settings.VISIT_COUNTER_FILE, 'r') as f:
                        current_count_str = f.read().strip()
                        try:
                            current_count = int(current_count_str)
                        except ValueError:
                            # Si el archivo está corrupto o vacío, reinicia a 0
                            current_count = 0
                    
                    new_count = current_count + 1

                    with open(settings.VISIT_COUNTER_FILE, 'w') as f:
                        f.write(str(new_count))




                # Versión para un archivo contador en cada apartado de la APP
                if request.path.startswith('/dns'):                    
                    with _visit_counter_lock:
                        with open(settings.VISIT_COUNTER_FILE_DNS, 'r') as f:
                            current_count_str = f.read().strip()
                            try:
                                current_count = int(current_count_str)
                            except ValueError:
                                # Si el archivo está corrupto o vacío, reinicia a 0
                                current_count = 0
                        
                        new_count = current_count + 1

                        with open(settings.VISIT_COUNTER_FILE_DNS, 'w') as f:
                            f.write(str(new_count))

                if request.path.startswith('/telnet'):
                    with _visit_counter_lock:
                        with open(settings.VISIT_COUNTER_FILE_TELNET, 'r') as f:
                            current_count_str = f.read().strip()
                            try:
                                current_count = int(current_count_str)
                            except ValueError:
                                # Si el archivo está corrupto o vacío, reinicia a 0
                                current_count = 0
                        
                        new_count = current_count + 1

                        with open(settings.VISIT_COUNTER_FILE_TELNET, 'w') as f:
                            f.write(str(new_count))

                if request.path.startswith('/bkl'):
                    with _visit_counter_lock:
                        with open(settings.VISIT_COUNTER_FILE_BKL, 'r') as f:
                            current_count_str = f.read().strip()
                            try:
                                current_count = int(current_count_str)
                            except ValueError:
                                # Si el archivo está corrupto o vacío, reinicia a 0
                                current_count = 0
                        
                        new_count = current_count + 1

                        with open(settings.VISIT_COUNTER_FILE_BKL, 'w') as f:
                            f.write(str(new_count))



                        
            except IOError as e:
                print(f"Error al leer o escribir en el archivo del contador: {e}")
            except Exception as e:
                print(f"Un error inesperado ocurrió en el middleware del contador: {e}")

        response = self.get_response(request)
        return response






# Middleware para prohibir el acceso a todo lo que no sea necesario 
class PermisoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_urls = [
            '/',
            '/dns',
            '/telnet',
            '/bkl',
            '/static/CSS/general.css',
            '/favicon.ico'
        ]

    def __call__(self, request):
        if request.path not in self.allowed_urls:
            return HttpResponseForbidden("Acceso Denegado")

        response = self.get_response(request)
        return response