# ====================================================================================
# modelos
# ====================================================================================

from datetime import datetime

class Tiquete:
    def __init__(self, id_tiquete, clase, precio_tiquete, codigo_vuelo):
        self.id_tiquete = id_tiquete
        self.clase = clase
        self.precio_tiquete = precio_tiquete
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
    def __init__(self, codigo_vuelo, ciudad_origen, ciudad_destino, fecha_salida, fecha_llegada, capacidad_economica, capacidad_preferencial):
        self.codigo_vuelo = codigo_vuelo
        self.ciudad_origen = ciudad_origen
        self.ciudad_destino = ciudad_destino
        self.fecha_salida = datetime.strptime(fecha_salida, '%Y-%m-%d %H:%M')
        self.fecha_llegada = datetime.strptime(fecha_llegada, '%Y-%m-%d %H:%M')
        
        # Atributos de capacidad
        self.capacidad_economica = capacidad_economica
        self.capacidad_preferencial = capacidad_preferencial
        
        # Relaciones
        self.pasajeros = []
        self.tripulacion = []

    def verificarDisponibilidad(self, clase_elegida): # Se utiliza para verifica si hay asientos disponibles en la clase elegida.
        clase_elegida = clase_elegida.lower()
        if clase_elegida == 'economica':
            return self.capacidad_economica > 0
        elif clase_elegida == 'preferencial':
            return self.capacidad_preferencial > 0
        return False
    
    def reducir_capacidad(self, clase_elegida): # Función para reducir la capacidad disponible de una clase.
        clase_elegida = clase_elegida.lower()
        if clase_elegida == 'economica':
            self.capacidad_economica -= 1
        elif clase_elegida == 'preferencial':
            self.capacidad_preferencial -= 1