import ast
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .formularios.forms import ApiForm
from .formularios.forms import ApiFormAuthBasic
from .formularios.forms import ApiFormAuthToken
from .formularios.forms import ApiFormAuth
from .formularios.forms import ApiFormReqBodySelect
from .formularios.forms import ApiFormReqBody
from .formularios.forms import ApiFormReqBodyTextarea
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
           




    # Valores para formulario Textarea que recoge los datos de body para POST
    formFieldsTextareaValue = None if request.POST.get("bodyTextarea")==None else request.POST.get("bodyTextarea").strip()
    # Formulario Textarea que recoge los datos de body para POST
    formFieldsTextarea = ApiFormReqBodyTextarea(initial= {"bodyTextarea": formFieldsTextareaValue})  












  

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
                    response = requests.get(url, headers=tokenAuth, params = params)
                elif authValue == "Basic":                    
                    response = requests.get(url, auth=basicHeaders, params = params)
                else:                    
                    response = requests.get(url, params = params)
            



            # POST
            elif valueSelect == "POST":
                # Iniciación de variables
                bodyParams : dict = ""
                # The API endpoint
                url = valueInput
                # Auth Variables                        
                basicHeaders = HTTPBasicAuth(basicUserValue, basicPassValue)
                tokenAuth = {'Authorization': f'{tokenKeyValue} {tokenValueValue}'}                
                # A POST request to the API            
                # Convertimos la string del textarea a un dict para poder recoger los parámetros 
                if formFieldsTextareaValue: 
                    try:
                        bodyParams = ast.literal_eval(formFieldsTextareaValue)
                    except:
                        respuesta = "Introduce los parámetros en formato JSON"
                else:
                    bodyParams = ""
                # Lanzamos la request 
                # Si has introducido parámetros pero no tienen el formato correcto no haces nada
                if respuesta:
                    pass
                else: 
                    if authValue == "Token":
                        response = requests.post(url, headers=tokenAuth, json = bodyParams)
                    elif authValue == "Basic":                    
                        response = requests.post(url, auth=basicHeaders, json = bodyParams) # data=json.dumps(data)) #  json = params)
                    else:
                        response = requests.post(url, data = bodyParams)

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
        "formfieldTextarea" : formFieldsTextarea,
        "formfieldTextareaValue" : formFieldsTextarea
    }
    return HttpResponse(render(request, "../templates/apiReq.html", context))
