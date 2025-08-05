from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from .formularios.forms import BKLForm
import re
from pydnsbl import DNSBLIpChecker, DNSBLDomainChecker, providers
from pydnsbl.providers import BASE_PROVIDERS, Provider
from django.conf import settings


# Lista de providers custom
customProvidersList = [
    'zen.spamhaus.org', # Una de las más completas y reputadas (ZEN consolida SBL, XBL, PBL).
    'sbl.spamhaus.org', # Spamhaus SBL (Spamhaus Block List).
    'xbl.spamhaus.org', # Spamhaus XBL (Exploits Block List - botnets, proxies abiertos).
    'pbl.spamhaus.org', # Spamhaus PBL (Policy Block List - IPs que no deberían enviar directamente a servidores de correo).
    'b.barracudacentral.org', # Barracuda Reputation Block List.
    'bl.spamcop.net', # SpamCop Blocking List.
    'cbl.abuseat.org', # Composite Blocking List (similar a XBL).
    'dnsbl.sorbs.net', # SORBS (muchas listas dentro de una, puede ser ruidosa si no se filtran las sublistas).
    'dul.dnsbl.sorbs.net', # SORBS DUL (Dynamic User List).
    'http.dnsbl.sorbs.net', # SORBS HTTP (servidores HTTP abiertos).
    'socks.dnsbl.sorbs.net', # SORBS SOCKS (proxies SOCKS abiertos).
    'misc.dnsbl.sorbs.net', # SORBS MISC (varios problemas).
    'spam.dnsbl.sorbs.net', # SORBS SPAM (spam reportado).
    'psbl.surbl.org', # Passive Spam Block List (basada en spam detectado).        
    'web.dnsbl.sorbs.net', # SORBS WEB (servidores web comprometidos).
    'safe.dnsbl.sorbs.net', # SORBS SAFE.
    'dnsbl.dronebl.org', # DroneBL (para sistemas comprometidos).
    'opm.tornevall.org', # Open Proxy Monitor.    
    'combined.rbl.msrbl.net', # MSRBL Combined (varias listas).
    'hostkarma.junkemailfilter.com', # HostKarma.
    'rbl.interserver.net', # InterServer RBL.
    'all.s5h.net', # S5H.
    'dnsbl-1.uceprotect.net', # UCEPROTECT Level 1 (puede ser controvertida por su agresividad).
    'dnsbl-2.uceprotect.net', # UCEPROTECT Level 2.
    'dnsbl-3.uceprotect.net', # UCEPROTECT Level 3.
    'b.cbl.abuseat.org', # CBL (variación de abuse.at).
    'access.redhawk.org', # Redhawk (para IRC).    
    'all.rbl.cluecentral.net', # ClueCentral.
]  
# Convertimos la lista a objetos Provider 
customProviders = [Provider(p) for p in customProvidersList]
# Configuramos los providers de listas negras a los que vamos a consultar 
providers = BASE_PROVIDERS + customProviders


# Create your views here.
@csrf_protect
def bklChecker(request):
    # Variables
    resultBool = False    
    result = ""
    
    # Obtenemos los datos del formulario (una IP o un Dominio)  
    valueInput = None if request.POST.get("inputValue")==None else request.POST.get("inputValue").strip()
    validValue = True   
        
    # creamos el formulario 
    form = BKLForm(initial= {"inputValue": valueInput})  

    
















    # Validar datos de input        
    if valueInput:        
        # Creación del pattern para comprobar si se introduce una IP o un Dominio 
        inputValidatePattern = re.compile(
            r"^(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$|"
            r"^(?P<domain>(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6})$"
        )
        match = inputValidatePattern.match(valueInput)
              

        # Si son datos validos lanzamos la request  
        if match:            
            # Si coincide con el patron de IP 
            if match.group('ip'):
                resultBool, result = checkIP(valueInput)
                print(result.providers)
            # Si coincide con el patron de Dominio
            # elif match.group('domain'):
                # resultBool, result = checkDomain(valueInput)
            else:
                validValue = False  
        # Si no coincide con ninguno indicamos que no es un valor válido
        else:
            validValue = False






    # Contador de visitas 
    total_visits = 0
    # Lee el contador directamente del archivo
    with settings.VISIT_COUNTER_LOCK: # Usa el mismo bloqueo para leer el archivo
        try:
            with open(settings.VISIT_COUNTER_FILE_BKL, 'r') as f:
                total_visits_str = f.read().strip()
                try:
                    total_visits = int(total_visits_str)
                except ValueError:
                    total_visits = 0 # Si el archivo está corrupto
        except FileNotFoundError:
            total_visits = 0 # Si el archivo aún no existe (aunque el middleware lo crea)
        except IOError as e:
            print(f"Error al leer el archivo del contador en la vista: {e}")

    










# Tupla de datos que vamos a pasar a la Template HTML
    context = {        
        "formulario": form,
        'total_visits': total_visits,
        "valueInput": valueInput,        
        "validValue": validValue,
        "resultadoBool": resultBool,         
        "isListed": result.blacklisted if validValue and valueInput else None,
        "resultado": result if validValue and valueInput else None     
    }
    # Lanzamiento y paso de datos a la Template HTML
    return HttpResponse(render(request, "../templates/bklChecker.html", context))




















# Funcion para consultar las listas negras de un dominio 
def checkDomain(dominio):
    # Creamos el objeto de pydnsbl que va a realizar la consulta    
    checker = DNSBLDomainChecker(providers=providers)
    
    # Lanzamos la consulta con manejo de excepciones 
    try:
        result = checker.check(dominio)
        print(result)
        return True, result
        
    except Exception as e:
         return False, f"Ha ocurrido un error: {e}"


# Funcion para consultar las listas negras de una IP
def checkIP(ip):
    # Creamos el objeto de pydnsbl que va a realizar la consulta
    checker = DNSBLIpChecker(providers=providers)
    
    # Lanzamos la consulta con manejo de excepciones
    try:
        result = checker.check(ip)
        return True, result
    except Exception as e:
         return False, f"Ha ocurrido un error {e}"






