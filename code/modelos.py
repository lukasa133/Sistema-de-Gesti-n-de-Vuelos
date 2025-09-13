# modelos.py

from datetime import datetime

# ====================================================================================
# No se esta utilizando
class Tripulacion:
    def __init__(self, id_tripulante, nombre, rol):
        self.id_tripulante = id_tripulante
        self.nombre = nombre
        self.rol = rol
class Avion:
    def __init__(self, id_avion, modelo, capacidad_total):
        self.id_avion = id_avion
        self.modelo = modelo
        self.capacidad_total = capacidad_total

class Asiento:
    def __init__(self, numero_asiento, clase, disponible=True):
        self.numero_asiento = numero_asiento
        self.clase = clase
        self.disponible = disponible

    def ocupar_asiento(self):
        self.disponible = False
# ====================================================================================

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

    def verificarDisponibilidad(self, clase_elegida):
        """Verifica si hay asientos disponibles en la clase elegida."""
        clase_elegida = clase_elegida.lower()
        if clase_elegida == 'economica':
            return self.capacidad_economica > 0
        elif clase_elegida == 'preferencial':
            return self.capacidad_preferencial > 0
        return False
    
    def reducir_capacidad(self, clase_elegida):
        """Reduce la capacidad disponible de una clase."""
        clase_elegida = clase_elegida.lower()
        if clase_elegida == 'economica':
            self.capacidad_economica -= 1
        elif clase_elegida == 'preferencial':
            self.capacidad_preferencial -= 1