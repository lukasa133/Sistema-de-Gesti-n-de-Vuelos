# gestion.py

from modelos import Vuelo, Pasajero, Tiquete
from datetime import datetime

# Listas globales para almacenar todos los objetos creados
vuelos_registrados = []
pasajeros_registrados = []
tiquetes_vendidos = []

def crear_nuevo_vuelo(codigo, origen, destino, salida, llegada, cap_economica, cap_preferencial):
    """
    Crea una instancia de Vuelo y la añade a la lista de vuelos.
    
    Args:
        codigo (str): Código único del vuelo.
        origen (str): Ciudad de origen.
        destino (str): Ciudad de destino.
        salida (str): Fecha y hora de salida ('YYYY-MM-DD HH:MM').
        llegada (str): Fecha y hora de llegada ('YYYY-MM-DD HH:MM').
        cap_economica (int): Capacidad de asientos económicos.
        cap_preferencial (int): Capacidad de asientos preferenciales.
    
    Returns:
        Vuelo: El objeto Vuelo creado.
    """
    
    # Verificación de que el código de vuelo sea único
    if any(v.codigo_vuelo == codigo for v in vuelos_registrados):
        raise ValueError(f"El código de vuelo {codigo} ya existe.")
    
    # Creación del objeto Vuelo y adición a la lista de registros
    nuevo_vuelo = Vuelo(codigo, origen, destino, salida, llegada, cap_economica, cap_preferencial)
    vuelos_registrados.append(nuevo_vuelo)
    return nuevo_vuelo

def registrar_pasajero(tipo_doc, id_pasajero, nombre, sexo, fecha_nacimiento, telefono):
    """
    Crea y registra un nuevo pasajero.
    
    Returns:
        Pasajero: El objeto Pasajero creado.
    """
    nuevo_pasajero = Pasajero(tipo_doc, id_pasajero, nombre, sexo, fecha_nacimiento, telefono)
    pasajeros_registrados.append(nuevo_pasajero)
    return nuevo_pasajero

def vender_tiquete(codigo_vuelo, pasajero, clase):
    """
    Vende un tiquete a un pasajero para un vuelo específico.
    
    Args:
        codigo_vuelo (str): Código del vuelo.
        pasajero (Pasajero): Objeto Pasajero.
        clase (str): Clase del tiquete ('Economica' o 'Preferencial').
    
    Returns:
        Tiquete: El objeto Tiquete vendido.
    """
    # 1. Buscar el vuelo
    vuelo = next((v for v in vuelos_registrados if v.codigo_vuelo == codigo_vuelo), None)
    if not vuelo:
        raise ValueError(f"Vuelo con código {codigo_vuelo} no encontrado.")

    # 2. Verificar la disponibilidad y reducir la capacidad
    if clase == 'Economica':
        if vuelo.capacidad_economica_restante <= 0:
            raise ValueError("No hay asientos disponibles en clase económica.")
        vuelo.capacidad_economica_restante -= 1
        precio = 100
    elif clase == 'Preferencial':
        if vuelo.capacidad_preferencial_restante <= 0:
            raise ValueError("No hay asientos disponibles en clase preferencial.")
        vuelo.capacidad_preferencial_restante -= 1
        precio = 250
    else:
        raise ValueError("Clase de tiquete no válida.")
        
    # 3. Crear el tiquete y asignarlo al pasajero y al vuelo
    id_tiquete = len(tiquetes_vendidos) + 1 # Generar un ID simple
    nuevo_tiquete = Tiquete(id_tiquete, clase, precio)
    tiquetes_vendidos.append(nuevo_tiquete)
    vuelo.pasajeros.append(pasajero)

    return nuevo_tiquete

def consultar_vuelos_disponibles_en_rango(fecha_inicio_str, fecha_fin_str):
    """
    Busca vuelos programados en un rango de fechas.
    
    Returns:
        list: Lista de objetos Vuelo.
    """
    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d %H:%M')
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError("Formato de fecha y hora inválido. Use 'YYYY-MM-DD HH:MM'.")
    
    vuelos_en_rango = [
        v for v in vuelos_registrados 
        if fecha_inicio <= v.fecha_salida <= fecha_fin
    ]
    return vuelos_en_rango

def obtener_info_vuelo(codigo_vuelo):
    vuelo = next((v for v in vuelos_registrados if v.codigo_vuelo == codigo_vuelo), None)
    if not vuelo:
        raise ValueError(f"Vuelo con código {codigo_vuelo} no encontrado.")

    # El número de asientos ocupados es simplemente el número de pasajeros.
    asientos_ocupados = len(vuelo.pasajeros)

    # El número de asientos disponibles es la suma de los asientos restantes en ambas clases.
    asientos_disponibles = vuelo.capacidad_economica_restante + vuelo.capacidad_preferencial_restante

    # El total de asientos es la suma de los ocupados más los disponibles.
    total_asientos = asientos_ocupados + asientos_disponibles
    
    return {
        'codigo': vuelo.codigo_vuelo,
        'origen': vuelo.ciudad_origen,
        'destino': vuelo.ciudad_destino,
        'pasajeros_registrados': len(vuelo.pasajeros),
        'asientos_ocupados': asientos_ocupados,
        'asientos_disponibles': asientos_disponibles
    }


