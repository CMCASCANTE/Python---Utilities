from django.http import HttpResponse
from django.shortcuts import render
from .formularios.forms import PortForm
import socket
import re
import asyncio
from django.conf import settings

def telnet(request):
    # Variables de la aplicación
    datos =[]
    ipInput = None if request.POST.get("ipValue")==None else request.POST.get("ipValue").strip()
    validIPValue = True    
    validPortValue = True    
    portInput = None if request.POST.get("portValue")==None else request.POST.get("portValue").strip()
    form = PortForm(initial= {"ipValue": ipInput, "portValue": portInput})  
    respuesta = ""
 
    
    # Validar datos de input        
    if ipInput:        
        inputValidatePattern = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        if re.match(inputValidatePattern, ipInput)== None:            
            validIPValue = False
          
    if portInput:        
        inputValidatePattern = r"^\d{1,5}$"        
        if re.match(inputValidatePattern, portInput)== None:   
            validPortValue = False


    # Si los datos son correctos, lanzamos la comprobación de puertos abiertos    
    if validIPValue and validPortValue and ipInput and portInput:
        # Si se cierra sin conectar o da error devolvemos False, en caso de que conecte devolvemos True
        async def isOpen(ip,port):            
            request = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:          
                # programamos un cierre en 10 segundos si no conecta      
                request.settimeout(10)
                request.connect((ip, int(port)))                
                return 1
            except Exception as err: 
                return err
       
        # Lanzamos 
        respuesta=asyncio.run(isOpen(ipInput, portInput))






    # Contador de visitas 
    total_visits = 0
    # Lee el contador directamente del archivo
    with settings.VISIT_COUNTER_LOCK: # Usa el mismo bloqueo para leer el archivo
        try:
            with open(settings.VISIT_COUNTER_FILE_TELNET, 'r') as f:
                total_visits_str = f.read().strip()
                try:
                    total_visits = int(total_visits_str)
                except ValueError:
                    total_visits = 0 # Si el archivo está corrupto
        except FileNotFoundError:
            total_visits = 0 # Si el archivo aún no existe (aunque el middleware lo crea)
        except IOError as e:
            print(f"Error al leer el archivo del contador en la vista: {e}")


    





    # Dict con datos para pasar a la Template
    datos = {
        "respuesta": respuesta,
        'total_visits': total_visits,
        "formulario": form,
        "ipInput": ipInput,
        "portInput": portInput,
        "validIPValue": validIPValue,
        "validPortValue": validPortValue
    }
    return HttpResponse(render(request, "../templates/telnet.html", datos))