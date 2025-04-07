import requests
from datetime import datetime, timedelta
import json
import os

API_KEY = os.getenv('CALENDARIFIC_API_KEY')
SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK_URL')
YEAR = datetime.today().year

# paises del equipo
COUNTRIES = {
    'co': 'Colombia',
    'ar': 'Argentina',
    'mx': 'México',
    'pa': 'Panamá',
    've': 'Venezuela'
}

# Fecha objetivo: feriados que ocurren dentro de dos días
TARGET_DATE = (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d')

def obtener_feriados(pais_codigo, pais_nombre):
    url = "https://calendarific.com/api/v2/holidays"
    params = {
        'api_key': API_KEY,
        'country': pais_codigo,
        'year': YEAR,
        'type': 'national'
    }
    response = requests.get(url, params=params).json()
    feriados = response['response']['holidays']
    
    # Filtramos los feriados que ocurren exactamente en la fecha objetivo
    encontrados = [f for f in feriados if f['date']['iso'] == TARGET_DATE]
    
    if encontrados:
        mensaje = f"*¡Atención!* En 2 días hay feriado en *{pais_nombre}*:\n"
        for f in encontrados:
            mensaje += f"• *{f['name']}*: {f['description']}\n"
        enviar_a_slack(mensaje)

def enviar_a_slack(mensaje):
    payload = {"text": mensaje}
    headers = {'Content-Type': 'application/json'}
    requests.post(SLACK_WEBHOOK, data=json.dumps(payload), headers=headers)

# Ejecutamos para cada país
for codigo, nombre in COUNTRIES.items():
    obtener_feriados(codigo, nombre)
