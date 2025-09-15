# ====================================================================================
# modelos
# ====================================================================================

from datetime import datetime

class Tiquete:
    def __init__(self, id_tiquete, clase, codigo_vuelo):
        self.id_tiquete = id_tiquete
        self.clase = clase
        self.codigo_vuelo = codigo_vuelo

class Pasajero:
    def __init__(self, tipo_documento, id_pasajero, nombre_completo, sexo, fecha_nacimiento, telefono):
        self.tipo_documento = tipo_documento
        self.id_pasajero = id_pasajero
        self.nombre_completo = nombre_completo
        self.sexo = sexo
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono

class Vuelo:
    def __init__(self, codigo_vuelo, ciudad_origen, ciudad_destino, fecha_salida, fecha_llegada, capacidad_economica, capacidad_preferencial, precio_economico, precio_preferencial, tripulacion):
        self.codigo_vuelo = codigo_vuelo
        self.ciudad_origen = ciudad_origen
        self.ciudad_destino = ciudad_destino
        self.fecha_salida = datetime.strptime(fecha_salida, '%Y-%m-%d %H:%M')
        self.fecha_llegada = datetime.strptime(fecha_llegada, '%Y-%m-%d %H:%M')
        self.precio_economica = precio_economico
        self.precio_preferencial = precio_preferencial
        
        # Atributos de capacidad
        self.capacidad_economica = capacidad_economica
        self.capacidad_preferencial = capacidad_preferencial
        
        # Relaciones
        self.tripulacion = tripulacion
        self.pasajeros = []

    def verificarDisponibilidad(self, clase_elegida): # Se utiliza para verifica si hay asientos disponibles en la clase elegida.
        clase_elegida = clase_elegida.lower()
        if clase_elegida == 'economica':
            return self.capacidad_economica > 0
        elif clase_elegida == 'preferencial':
            return self.capacidad_preferencial > 0
        return False
    
 