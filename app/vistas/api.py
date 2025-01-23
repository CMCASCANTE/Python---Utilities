from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .formularios.forms import ApiForm
from .formularios.forms import ApiFormAuthBasic
from .formularios.forms import ApiFormAuthToken
from .formularios.forms import ApiFormAuth
import requests
from requests.auth import HTTPBasicAuth

# Create your views here.
@csrf_protect
def api(request):
    # Variables
    response = ""
    respuesta = ""
    # Valores del formulario
    valueInput = None if request.POST.get("urlValue")==None else request.POST.get("urlValue").strip()
    valueSelect = "GET" if request.POST.get("apiRequestType")==None else request.POST.get("apiRequestType")
    # Formulario
    form = ApiForm(initial= {"urlValue": valueInput, "apiRequestType": valueSelect})  

    # Valores del formulario Auth
    basicUserValue = None if request.POST.get("basicUser")==None else request.POST.get("basicUser").strip()
    basicPassValue = None if request.POST.get("basicPass")==None else request.POST.get("basicPass").strip()
    tokenKeyValue = "Bearer" if request.POST.get("tokenKey")==None else request.POST.get("tokenKey").strip()
    tokenValueValue = None if request.POST.get("tokenValue")==None else request.POST.get("tokenValue").strip()
    authValue = "None" if request.POST.get("apiAuthType")==None else request.POST.get("apiAuthType")
    # Formulario Auth
    formAuth = ApiFormAuth(initial= {"apiAuthType": authValue})  
    formAuthBasic = ApiFormAuthBasic(initial= {"basicUser": basicUserValue, "basicPass": basicPassValue})  
    formAuthToken = ApiFormAuthToken(initial= {"tokenKey": tokenKeyValue, "tokenValue": tokenValueValue})  

    # Peticion
    if valueInput:
        try:
            # GET
            if valueSelect == "GET":
                # The API endpoint
                url = valueInput
                # Auth Variables
                basicHeaders = HTTPBasicAuth(basicUserValue, basicPassValue)
                tokenAuth = {'Authorization': f'{tokenKeyValue} {tokenValueValue}'}
                # A GET request to the API
                if authValue == "Token":                    
                    response = requests.get(url, headers=tokenAuth)
                elif authValue == "Basic":                    
                    response = requests.get(url, auth=basicHeaders)
                else:                    
                    response = requests.get(url)
            
            # POST
            elif valueSelect == "POST":
                ###################
                # EN CONSTRUCCION #
                ###################
                # The API endpoint
                url = "https://api.ionos.com/auth/v1/tokens/generate"

                # Data to be sent
                data = {
                    "userID": 1,
                    "title": "Making a POST request",
                    "body": "This is the data we created."
                }

                # A POST request to the API
                response = requests.post(url, json=data)
            
            respuesta = response.text
        except Exception as err:
                # print(f"Error: {err}")
                respuesta = err

    context = {       
        "respuesta": respuesta,  
        "formulario": form,
        "formularioAuth" : formAuth,
        "formularioAuthBasic": formAuthBasic,
        "formularioAuthToken": formAuthToken,
        "valueSelect": valueSelect
    }
    return HttpResponse(render(request, "../templates/apiReq.html", context))