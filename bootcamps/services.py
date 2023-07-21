from django.shortcuts import get_object_or_404
import requests
from django.contrib.auth.models import User

def enviar_datos_microservicio(estudiante_id, bootcamp):
    estudiante = get_object_or_404(User, pk=estudiante_id)
    url_microservicio = 'https://mockly.app/api/17e8e81a-eb0a-45e3-abd7-1c664dc8864d/bootcampFinalizados'
    data = {
        'id': estudiante_id,
        'estudiante': estudiante.username,
        'bootcamp': bootcamp
    }
    print(data)
    try:
        response = requests.post(url_microservicio, json=data, verify=False)
        response.raise_for_status()
        print('Datos enviados correctamente al microservicio')
    except requests.exceptions.RequestException as e:
        print(f'Error al enviar los datos al microservicio: {str(e)}')

