from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .formularios.forms import ApiForm
from .formularios.forms import ApiFormAuthBasic
from .formularios.forms import ApiFormAuthToken
from .formularios.forms import ApiFormAuth
from .formularios.forms import ApiFormReqBodySelect
from .formularios.forms import ApiFormReqBody
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

    # Valores para el formulario par los campos de los parametros
    formFieldsSelectValue = "None" if request.POST.get("bodyFieldSelect")==None else request.POST.get("bodyFieldSelect")
    basicBodyKey =[] 
    basicBodyValue =[] 
    for i in range(1, 11):
        basicBodyKey.append(None if request.POST.get(f"key{i}")==None else request.POST.get(f"key{i}").strip())
        basicBodyValue.append(None if request.POST.get(f"value{i}")==None else request.POST.get(f"value{i}").strip())
    # Formulario par los campos de los parametros
    # Pasamos un dict con los campos que recogerá el objeto del formulario 
    fields ={'key1':'value1',
             'key2':'value2',
             'key3':'value3',
             'key4':'value4',
             'key5':'value5',
             'key6':'value6',
             'key7':'value7',
             'key8':'value8',
             'key9':'value9',
             'key10':'value10',
             } 
    paramFields = ApiFormReqBody(fields, 
                           initial= {"key1": basicBodyKey[0], "value1": basicBodyValue[0],
                                     "key2": basicBodyKey[1], "value2": basicBodyValue[1],
                                     "key3": basicBodyKey[2], "value3": basicBodyValue[2],                                     
                                     "key4": basicBodyKey[3], "value4": basicBodyValue[3],
                                     "key5": basicBodyKey[4], "value5": basicBodyValue[4],
                                     "key6": basicBodyKey[5], "value6": basicBodyValue[5],
                                     "key7": basicBodyKey[6], "value7": basicBodyValue[6],
                                     "key8": basicBodyKey[7], "value8": basicBodyValue[7],
                                     "key9": basicBodyKey[8], "value9": basicBodyValue[8],
                                     "key10": basicBodyKey[9], "value10": basicBodyValue[9]
                                    }
                          )
    formFieldsSelect = ApiFormReqBodySelect(initial= {"bodyFieldSelect": formFieldsSelectValue})  
    # Convertimos los resultados en un diccionario para enviar con la request 
    # params = dict(zip(basicBodyKey, basicBodyValue))
    params = dict()
    if formFieldsSelectValue != "None":
        for i in range(int(formFieldsSelectValue)):
            params.update({basicBodyKey[i]: basicBodyValue[i]})

    

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
                    response = requests.get(url, auth=basicHeaders, params = params )
                else:                    
                    response = requests.get(url)
            
            # POST
            elif valueSelect == "POST":
                ###################
                # EN CONSTRUCCION #
                ###################
                pass
            
            respuesta = response.text
        except Exception as err:
                # print(f"Error: {err}")
                respuesta = err

    context = {       
        "respuesta": respuesta,  
        "formulario": form,
        "formularioAuth": formAuth,
        "formularioAuthBasic": formAuthBasic,
        "formularioAuthToken": formAuthToken,
        "valueSelect": valueSelect, 
        "formfieldSelect": formFieldsSelect,       
        "formFields": paramFields,
        "test": params     
    }
    return HttpResponse(render(request, "../templates/apiReq.html", context))
