# gestion.py

from modelos import Vuelo, Pasajero, Tiquete
from datetime import datetime

# ====================================================================================
# Datos iniciales (actúan como la base de datos pre-cargada)
# ====================================================================================

# Registros globales
vuelos_registrados = []
tiquetes_vendidos = []

# Vuelos pre-existentes con sus capacidades
vuelo1 = Vuelo(
    codigo_vuelo="AV101",
    ciudad_origen="Medellín",
    ciudad_destino="Bogotá",
    fecha_salida="2025-12-25 08:00",
    fecha_llegada="2025-12-25 09:00",
    capacidad_economica=150,
    capacidad_preferencial=20
)

vuelo2 = Vuelo(
    codigo_vuelo="LA202",
    ciudad_origen="Bogotá",
    ciudad_destino="Cartagena",
    fecha_salida="2025-12-26 12:00",
    fecha_llegada="2025-12-26 13:30",
    capacidad_economica=80,
    capacidad_preferencial=15
)

vuelo3 = Vuelo(
    codigo_vuelo="SK303",
    ciudad_origen="Cali",
    ciudad_destino="Medellín",
    fecha_salida="2025-12-27 15:00",
    fecha_llegada="2025-12-27 16:00",
    capacidad_economica=100,
    capacidad_preferencial=10
)

# Añadir los vuelos a la lista de registros
vuelos_registrados.extend([vuelo1, vuelo2, vuelo3])

# ====================================================================================
# Funciones de gestión (acciones)
# ====================================================================================

def vender_tiquete(codigo_vuelo, pasajero_dict, clase_elegida):
    if not all(pasajero_dict.values()):
        return "¡ERROR! Todos los campos deben estar completos."
    
"""
    nombre_completo = pasajero_dict.get("nombre_completo", "")
    if not nombre_completo.replace(" ", "").isalpha():
        return "¡ERROR! El espacio de nombre completo debe de contener solo texto."
    
    telefono = pasajero_dict.get("telefono", "")
    if not telefono.isdigit():
        return "¡ERROR! El número de teléfono debe contener solo dígitos."
    
    numero_documento = pasajero_dict.get("id_pasajero", "")
    if not numero_documento.isdigit():
        return "¡ERROR! El número de documento debe contener solo dígitos."
"""

    vuelo = next((v for v in vuelos_registrados if v.codigo_vuelo == codigo_vuelo), None)

    if not vuelo.verificarDisponibilidad(clase_elegida):
        return f"¡ERROR! No hay asientos disponibles en la clase {clase_elegida} para el vuelo {codigo_vuelo}."

    pasajero = Pasajero(**pasajero_dict)

    id_tiquete = len(tiquetes_vendidos) + 1

"""
    if clase_elegida.lower() == 'economica':
        precio = 120000 
    elif clase_elegida.lower() == 'preferencial':
        precio = 750000
    else:
        return f"¡ERROR! La clase {clase_elegida} no es valida."
"""
        
    nuevo_tiquete = Tiquete(id_tiquete, clase_elegida, precio, codigo_vuelo) # Aquí pasas el código de vuelo.
    tiquetes_vendidos.append(nuevo_tiquete)
    vuelo.pasajeros.append(pasajero) # Agregas el pasajero al vuelo.
    vuelo.reducir_capacidad(clase_elegida) # Reduces la capacidad disponible.
    
    return nuevo_tiquete

def obtener_info_vuelo(codigo_vuelo):
    """
    Devuelve la información detallada de un vuelo: pasajeros, asientos ocupados y disponibles.
    Retorna un diccionario con la información.
    """
    vuelo = next((v for v in vuelos_registrados if v.codigo_vuelo == codigo_vuelo), None)
    if not vuelo:
        return f"Error: Vuelo con código '{codigo_vuelo}' no encontrado."
    
    asientos_economicos_ocupados = vuelo.capacidad_economica - sum(1 for t in tiquetes_vendidos if t.codigo_vuelo == codigo_vuelo and t.clase.lower() == 'economica')
    asientos_preferenciales_ocupados = vuelo.capacidad_preferencial - sum(1 for t in tiquetes_vendidos if t.codigo_vuelo == codigo_vuelo and t.clase.lower() == 'preferencial')
    
    total_asientos_ocupados = asientos_economicos_ocupados + asientos_preferenciales_ocupados
    total_asientos_disponibles = vuelo.capacidad_economica + vuelo.capacidad_preferencial - total_asientos_ocupados
    
    return {
        'codigo': vuelo.codigo_vuelo,
        'pasajeros_registrados': len(vuelo.pasajeros),
        'asientos_ocupados': total_asientos_ocupados,
        'asientos_disponibles': total_asientos_disponibles,
        'info_por_clase': {
            'Economica': {'ocupados': asientos_economicos_ocupados, 'disponibles': vuelo.capacidad_economica - asientos_economicos_ocupados},
            'Preferencial': {'ocupados': asientos_preferenciales_ocupados, 'disponibles': vuelo.capacidad_preferencial - asientos_preferenciales_ocupados}
        }
    }