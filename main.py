import requests
from datetime import datetime, timedelta
import json
import os

modo_prueba = True  # Cambiar a True para pruebas manuales

API_KEY = os.getenv('CALENDARIFIC_API_KEY')
SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK_URL')
YEAR = datetime.today().year

# Paises del equipo
COUNTRIES = {
    'co': 'Colombia',
    'ar': 'Argentina',
    'mx': 'México',
    'pa': 'Panamá',
    've': 'Venezuela'
}

# Fechas objetivo: dentro de dos días y hoy
TARGET_DATE_2 = (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d')
TARGET_DATE_TODAY = datetime.today().strftime('%Y-%m-%d')

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

    mensaje = ""

    # Feriado dentro de dos días
    feriados_en_2_dias = [f for f in feriados if f['date']['iso'] == TARGET_DATE_2]
    if feriados_en_2_dias:
        mensaje += f"*🔔 En 2 días hay feriado en {pais_nombre}:*\n"
        for f in feriados_en_2_dias:
            mensaje += f"• *{f['name']}*: {f['description']}\n"

    # Feriado hoy
    feriados_hoy = [f for f in feriados if f['date']['iso'] == TARGET_DATE_TODAY]
    if feriados_hoy:
        mensaje += f"\n🎉 *¡Hoy es feriado en {pais_nombre}!* 🎉\n"
        for f in feriados_hoy:
            mensaje += f"• *{f['name']}*: {f['description']}\n"

    if mensaje:
        enviar_a_slack(mensaje)

def enviar_a_slack(mensaje):
    payload = {"text": mensaje}
    headers = {'Content-Type': 'application/json'}
    requests.post(SLACK_WEBHOOK, data=json.dumps(payload), headers=headers)

# Ejecutamos para cada país
for codigo, nombre in COUNTRIES.items():
    obtener_feriados(codigo, nombre)

# Mensaje de test opcional
if modo_prueba:
    enviar_a_slack("🧪 *Modo prueba activado:* Este es un mensaje de test para confirmar que el bot funciona correctamente.")


