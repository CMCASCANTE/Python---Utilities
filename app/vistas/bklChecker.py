from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from .formularios.forms import BKLForm
import re
from pydnsbl import DNSBLIpChecker, DNSBLDomainChecker, providers
from pydnsbl.providers import BASE_PROVIDERS, Provider


# Configuramos los providers de listas negras a los que vamos a consultar 
providers = BASE_PROVIDERS # + [Provider('yourprovider1.com'), ...]


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
            # Si coincide con el patron de Dominio
            elif match.group('domain'):
                resultBool, result = checkDomain(valueInput)
        # Si no coincide con ninguno indicamos que no es un valor válido
        else:
            validValue = False


# Tupla de datos que vamos a pasar a la Template HTML
    context = {        
        "formulario": form,
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






