from django.shortcuts import render
from django.http import HttpResponse
import socket
import dns.resolver
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from .personalModules.forms import DNSForm
import re

# Create your views here.
@csrf_protect
def index(request):
    # Variables y recogida de datos
    query = []    
    queryFull = []     
    valueInput = None if request.POST.get("domainValue")==None else request.POST.get("domainValue")
    validValue = True    
    valueSelect = "A" if request.POST.get("selectDNS")==None else request.POST.get("selectDNS")
    form = DNSForm(initial= {"domainValue": valueInput, "selectDNS": valueSelect})  
    error = ""    
    allRecordsData = []
    LISTA_TIPOS = ["NS", "A", "TXT", "MX", "CNAME"]
    
    # Validar datos de input        
    if valueInput:        
        inputValidatePattern = r"\w*[.]{1}\w*([.]{1}\w*)*"
        if re.match(inputValidatePattern, valueInput)== None:            
            validValue = False
    
    # Modulo "dnspython"
    # Busqueda simple
    if validValue and valueInput:
        # creación y configuración del objeto para la consulta
        # objeto que contiene la consulta
        resolver = dns.resolver.Resolver();         
        # configuración de los servidores DNS a consultar
        resolver.nameservers=[socket.gethostbyname('8.8.8.8')]
        def resolveDNS(input, select):
            # lanzamiento de la consulta
            answer = resolver.query(input, select)
            # devolver respuesta
            return answer

        # Convertimos la respuesta en una lista, ya que es un objeto iterable
        # La guardamos en una variable
        # Y gestionando errores para que no salte la excepción y pare el programa
        try:
            query = list(resolveDNS(valueInput, valueSelect))    
        except Exception as err:
            # print(err, file=sys.stderr)
            error = err
      
        # ALL RECORDS
        # Recogemos la lista que esta generada para el select del formulario
        # Filtramos la lista cogiendo los dos valores que tiene por tupla pero solo usamos uno, ya que esta repetido
        for tipo in LISTA_TIPOS:
            try:
                queryFull = list(resolveDNS(valueInput, tipo))    
                for rdata in queryFull:
                    allRecordsData.append({"tipo": tipo, "registro": rdata})
            except Exception as err:
                # print(err, file=sys.stderr)
                error = err
            
      
      
      
                        
    # Tupla de datos que vamos a pasar a la Template HTML
    context = {
        "consulta": query,
        "formulario": form,
        "valueInput": valueInput,
        "selectValue": valueSelect,
        "validValue": validValue,
        "error": error,        
        "todosRegistros": allRecordsData
    }
    # Lanzamiento y paso de datos a la Template HTML
    return HttpResponse(render(request, "../templates/index.html", context))