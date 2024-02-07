import datetime




def obtener_hora_actual():
    ahora = datetime.datetime.now()
    hora = ahora.hour
    minutos = ahora.minute
    segundos = ahora.second
    # Formateo con ceros a la izquierda para números menores a 10
    hora_str = str(hora).zfill(2)
    minutos_str = str(minutos).zfill(2)
    segundos_str = str(segundos).zfill(2)
    return f"{hora_str}:{minutos_str}:{segundos_str}"
# obtener la hora actual

