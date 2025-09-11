# modelo.py

from datetime import datetime

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

class Tiquete:
    def __init__(self, id_tiquete, clase, precio_tiquete, asiento_asignado=None):
        self.id_tiquete = id_tiquete
        self.clase = clase
        self.asiento_asignado = asiento_asignado
        self.precio_tiquete = precio_tiquete

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
        
        # Atributos para almacenar los objetos relacionados
        self.pasajeros = []
        self.tripulacion = []
        
        # Atributos para la capacidad, ya que el módulo de gestión ahora lo controlará todo
        self.capacidad_economica_restante = capacidad_economica
        self.capacidad_preferencial_restante = capacidad_preferencial