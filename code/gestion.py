#gestion.py

from modelos import Vuelo, Pasajero, Tiquete
from datetime import datetime

# ====================================================================================
# Datos iniciales (actúan como la base de datos pre-cargada)
# ====================================================================================

# Registros globales
vuelos_registrados = []
pasajeros_registrados = []
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
    """
    Vende un tiquete a un pasajero para un vuelo específico.
    Retorna el Tiquete vendido si la operación es exitosa.
    """
    vuelo = next((v for v in vuelos_registrados if v.codigo_vuelo == codigo_vuelo), None)
    if not vuelo:
        raise ValueError("Error: Vuelo no encontrado.")
    
    asientos_ocupados_en_clase = sum(1 for t in tiquetes_vendidos if t.codigo_vuelo == codigo_vuelo and t.clase == clase_elegida)
    
    if clase_elegida == 'Economica':
        capacidad_maxima = vuelo.capacidad_economica
        precio = 120.000 
    elif clase_elegida == 'Preferencial':
        capacidad_maxima = vuelo.capacidad_preferencial
        precio = 750.000
    else:
        raise ValueError("Error: Clase de tiquete no válida.")
    
    if asientos_ocupados_en_clase >= capacidad_maxima:
        raise ValueError("Error: No hay asientos disponibles en la clase seleccionada.")

    pasajero = Pasajero(**pasajero_dict)
    pasajeros_registrados.append(pasajero)
    vuelo.pasajeros.append(pasajero)

    id_tiquete = len(tiquetes_vendidos) + 1
    nuevo_tiquete = Tiquete(id_tiquete, clase_elegida, precio, codigo_vuelo=codigo_vuelo)
    tiquetes_vendidos.append(nuevo_tiquete)

    if not all(pasajero_dict.values()):
        raise ValueError("Error: Todos los campos del pasajero deben ser diligenciados.")
    
    pasajero = Pasajero(**pasajero_dict)
    pasajeros_registrados.append(pasajero)
    vuelo.pasajeros.append(pasajero)
    
    return nuevo_tiquete

def consultar_vuelos_en_rango(fecha_inicio_str, fecha_fin_str):
    """
    Busca vuelos programados en un rango de fechas.
    Retorna una lista de vuelos que cumplen con el criterio.
    """
    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d %H:%M')
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError("Error: Formato de fecha y hora inválido. Use 'YYYY-MM-DD HH:MM'.")

    vuelos_en_rango = [
        v for v in vuelos_registrados 
        if fecha_inicio <= v.fecha_salida <= fecha_fin
    ]
    return vuelos_en_rango

def obtener_info_vuelo(codigo_vuelo):
    """
    Devuelve la información detallada de un vuelo: pasajeros, asientos ocupados y disponibles.
    Retorna un diccionario con la información.
    """
    vuelo = next((v for v in vuelos_registrados if v.codigo_vuelo == codigo_vuelo), None)
    if not vuelo:
        raise ValueError(f"Error: Vuelo con código '{codigo_vuelo}' no encontrado.")
    
    asientos_economicos_ocupados = sum(1 for t in tiquetes_vendidos if t.codigo_vuelo == codigo_vuelo and t.clase == 'Economica')
    asientos_preferenciales_ocupados = sum(1 for t in tiquetes_vendidos if t.codigo_vuelo == codigo_vuelo and t.clase == 'Preferencial')
    
    asientos_economicos_disponibles = vuelo.capacidad_economica - asientos_economicos_ocupados
    asientos_preferenciales_disponibles = vuelo.capacidad_preferencial - asientos_preferenciales_ocupados
    
    total_asientos_ocupados = asientos_economicos_ocupados + asientos_preferenciales_ocupados
    total_asientos_disponibles = asientos_economicos_disponibles + asientos_preferenciales_disponibles

    return {
        'codigo': vuelo.codigo_vuelo,
        'pasajeros_registrados': len(vuelo.pasajeros),
        'asientos_ocupados': total_asientos_ocupados,
        'asientos_disponibles': total_asientos_disponibles,
        'info_por_clase': {
            'Economica': {'ocupados': asientos_economicos_ocupados, 'disponibles': asientos_economicos_disponibles},
            'Preferencial': {'ocupados': asientos_preferenciales_ocupados, 'disponibles': asientos_preferenciales_disponibles}
        }
    }