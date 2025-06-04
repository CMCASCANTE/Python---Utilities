import requests
import json

# Define la URL a la que se enviará la solicitud POST
url = 'https://example.com/api/pipelines'

# Define el cuerpo de la solicitud como un diccionario Python
pipeline_data = {
    "name": "MiPipeline",  # Nombre del pipeline, no debe exceder los 20 caracteres
    "logs": [
        # Array de objetos, cada uno representará una entrada de log
        {"source": "app_server", "type": "access_log", "level": "info", "message": "User logged in"},
        {"source": "database", "type": "error_log", "level": "error", "message": "Connection error"}
    ]
}

# Configura las cabeceras para enviar datos en formato JSON
headers = {
    'Content-Type': 'application/json'
}

# Realiza la solicitud POST enviando los datos en formato JSON
response = requests.post(url, headers=headers, data=json.dumps(pipeline_data))
print(json.dumps(pipeline_data))
# Muestra el código de estado de la respuesta
print('Código de estado:', response.status_code)

# Muestra la respuesta del servidor
print('Respuesta del servidor:', response.text)