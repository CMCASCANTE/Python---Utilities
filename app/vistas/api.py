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
                #################
                ## Test Values ##
                #################
                # url3 = "https://api.ionos.com/auth/v1/tokens/generate"
                # url2 = "https://api.ionos.com/cloudapi/v6/datacenters"
                # token="eyJ0eXAiOiJKV1QiLCJraWQiOiIyYzMwY2FmYi03ZjY3LTRhOWEtYjk2MS1kNjQyMDBjMjg4NTIiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJBcnN5cyIsImlhdCI6MTczNzU3MDMxNCwiY2xpZW50IjoiVVNFUiIsImlkZW50aXR5Ijp7InByaXZpbGVnZXMiOlsiREFUQV9DRU5URVJfQ1JFQVRFIiwiU05BUFNIT1RfQ1JFQVRFIiwiSVBfQkxPQ0tfUkVTRVJWRSIsIk1BTkFHRV9EQVRBUExBVEZPUk0iLCJBQ0NFU1NfQUNUSVZJVFlfTE9HIiwiUENDX0NSRUFURSIsIkFDQ0VTU19TM19PQkpFQ1RfU1RPUkFHRSIsIkJBQ0tVUF9VTklUX0NSRUFURSIsIkNSRUFURV9JTlRFUk5FVF9BQ0NFU1MiLCJLOFNfQ0xVU1RFUl9DUkVBVEUiLCJGTE9XX0xPR19DUkVBVEUiLCJBQ0NFU1NfQU5EX01BTkFHRV9NT05JVE9SSU5HIiwiQUNDRVNTX0FORF9NQU5BR0VfQ0VSVElGSUNBVEVTIiwiQUNDRVNTX0FORF9NQU5BR0VfTE9HR0lORyIsIk1BTkFHRV9EQkFBUyIsIkFDQ0VTU19BTkRfTUFOQUdFX0ROUyIsIk1BTkFHRV9SRUdJU1RSWSIsIkFDQ0VTU19BTkRfTUFOQUdFX0NETiIsIkFDQ0VTU19BTkRfTUFOQUdFX1ZQTiIsIkFDQ0VTU19BTkRfTUFOQUdFX0FQSV9HQVRFV0FZIiwiQUNDRVNTX0FORF9NQU5BR0VfTkdTIiwiQUNDRVNTX0FORF9NQU5BR0VfS0FBUyIsIkFDQ0VTU19BTkRfTUFOQUdFX05FVFdPUktfRklMRV9TVE9SQUdFIiwiQUNDRVNTX0FORF9NQU5BR0VfQUlfTU9ERUxfSFVCIiwiQ1JFQVRFX05FVFdPUktfU0VDVVJJVFlfR1JPVVBTIiwiQUNDRVNTX0FORF9NQU5BR0VfSUFNX1JFU09VUkNFUyJdLCJ1dWlkIjoiN2EyMDc5MzctNjA0Mi00Nzg1LWI4NmEtMDQ1ZjI1YTI0MWVhIiwicmVzZWxsZXJJZCI6ODI4NjI3NCwicmVnRG9tYWluIjoiaW9ub3MuZGUiLCJyb2xlIjoiYWRtaW4iLCJjb250cmFjdE51bWJlciI6MzE5Mzk1OTcsImlzUGFyZW50IjpmYWxzZX0sImV4cCI6MTc2OTEyNzkxNH0.U4_wA4t7blAHvg6bFNgAslvuJReBfS0akGkqS2ZsVL0c01rqa5pKouXxR6X2FSN2Ir2QxrzsRSUVDlSPADmhYMd_y_QvrojcZS7at6dWd6wJf_TgbMpRLmOpuDZGTnuDg-tYowzWdNSOn6ZoexyJIE99KourM0BSd819A1E-8rgS6hf_ndiJ06IHoUAbjl9boW3er14Ha_GYE0ULSonAEcaylFeABpwP-ENkyEbbIWaaefKWF7_AmvLqSX0gajrM1XPqIh3bv8I91vocgHoxrUwi74aUvJjxiu47o8cUYXSD6DllWXIBOQU-VACfBz2oJnoHnBxTEsbQYpJoH4sKtg"
                # # Adding a payload
                # payload = {"id": [1, 2, 3], "userId":1}
                # response = requests.get(url, params=payload)


                # The API endpoint
                url = valueInput
                # Auth Variables
                basicHeaders = HTTPBasicAuth(basicUserValue, basicPassValue)
                tokenAuth = {'Authorization': f'{tokenKeyValue} {tokenValueValue}'}
                # A GET request to the API
                if authValue == "Token":
                    print("test3")
                    response = requests.get(url, headers=tokenAuth)
                elif authValue == "Basic":
                    print("test2")
                    response = requests.get(url, auth=basicHeaders)
                else:
                    print("test4")
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


    
    def testing():
        print("no java")
    
    context = {       
        "testing": testing,
        "respuesta": respuesta,  
        "formulario": form,
        "formularioAuth" : formAuth,
        "formularioAuthBasic": formAuthBasic,
        "formularioAuthToken": formAuthToken,
        "valueSelect": valueSelect
    }
    return HttpResponse(render(request, "../templates/apiReq.html", context))