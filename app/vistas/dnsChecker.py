from django.shortcuts import render
from django.http import HttpResponse
import socket
import dns.resolver
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from .formularios.forms import DNSForm
import re
from django.conf import settings

# Create your views here.
@csrf_protect
def dnsChecker(request):
    # Variables y recogida de datos
    query = []    
    queryFull = []     
    valueInput = None if request.POST.get("domainValue")==None else request.POST.get("domainValue").strip()
    validValue = True    
    valueSelect = "ALL" if request.POST.get("selectDNS")==None else request.POST.get("selectDNS")
    valueNameserver = "8.8.8.8" if request.POST.get("nameServer")==None else request.POST.get("nameServer")
    form = DNSForm(initial= {"domainValue": valueInput, "selectDNS": valueSelect, "nameServer": valueNameserver})  
    error = ""    
    allRecordsData = []    
    allRecordsCname = False
    LISTA_TIPOS = ["NS", "A", "AAAA", "TXT", "SPF", "MX", "CNAME", "CAA", "SRV"]
    
    # Validar datos de input        
    if valueInput:        
        inputValidatePattern = r"(\w|-)*[.]{1}\w*([.]{1}\w*)*"
        if re.match(inputValidatePattern, valueInput)== None:            
            validValue = False
    
    # Modulo "dnspython"
    # Busqueda simple
    if validValue and valueInput:
        # creación y configuración del objeto para la consulta
        # objeto que contiene la consulta
        resolver = dns.resolver.Resolver()        
        # configuración de los servidores DNS a consultar
        resolver.nameservers=[socket.gethostbyname(valueNameserver)]
        def resolveDNS(input, select):
            # lanzamiento de la consulta
            answer = resolver.resolve(input, select)
            # devolver respuesta
            return answer

        # Convertimos la respuesta en una lista, ya que es un objeto iterable
        # La guardamos en una variable
        # Y gestionando errores para que no salte la excepción y pare el programa
        try:
            query = list(resolveDNS(valueInput, valueSelect))    
            print(query)
        except Exception as err:
            # print(err, file=sys.stderr)
            error = err
      
        # ALL RECORDS        
        # Listamos los tipos de registros predefinidos en la lista y lanzamos una consula por cada uno
        for tipo in LISTA_TIPOS:
            try:
                queryFull = list(resolveDNS(valueInput, tipo))    
                for rdata in queryFull:
                    if tipo == "CNAME" and rdata: 
                        allRecordsData.clear()
                        allRecordsData.append({"tipo": tipo, "registro": rdata})  
                        allRecordsCname = True                  
                        break
                    else:    
                        allRecordsData.append({"tipo": tipo, "registro": rdata})                    
            except Exception as err:
                # print(err, file=sys.stderr)
                error = err
            
      




    # Contador de visitas 
        total_visits = 0
    # Lee el contador directamente del archivo
    with settings.VISIT_COUNTER_LOCK: # Usa el mismo bloqueo para leer el archivo
        
        try:
            with open(settings.VISIT_COUNTER_FILE_DNS, 'r') as f:
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
        "consulta": query,
        'total_visits': total_visits,
        "formulario": form,
        "valueInput": valueInput,
        "selectValue": valueSelect,
        "validValue": validValue,
        "error": error,        
        "todosRegistros": allRecordsData,
        "todosRegistrosCname": allRecordsCname
    }
    # Lanzamiento y paso de datos a la Template HTML
    return HttpResponse(render(request, "../templates/dnsChecker.html", context))