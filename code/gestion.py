# gestion.py

import modelos # Importamos las clases del módulo modelo

vuelos_disponibles = [] # Una lista global o una estructura de datos para guardar los vuelos
asientos_disponibles = 120
capacidad_preferencial = 80
capacidad_economica = 40


def crear_nuevo_vuelo(vuelos_disponibles, codigo, origen, destino, capacidad_economica, capacidad_preferencial):
    # Verifica si ya existe un vuelo con el mismo código
    if any(v.codigo == codigo for v in vuelos_disponibles):
        raise ValueError(f"El código de vuelo {codigo} ya existe.")
    
    nuevo_vuelo = modelos.Vuelo(codigo, origen, destino, capacidad_economica, capacidad_preferencial)
    vuelos_disponibles.append(nuevo_vuelo)
    return nuevo_vuelo

def buscar_vuelos_por_rango_de_fechas(vuelos_disponibles, fecha_inicio, fecha_fin):
    vuelos_en_rango = []
    
    for vuelo in vuelos_disponibles:
        if fecha_inicio <= vuelo.salida_dt <= fecha_fin:
            vuelos_en_rango.append(vuelo)  # Añadimos el vuelo que cumple con el rango de fechas
    
    return vuelos_en_rango  # Devolvemos los vuelos que cumplen el criterio
    

def vender_tiquete(vuelos_disponibles, codigo_vuelo, pasajero, clase):
    # Buscar el vuelo con el código proporcionado
    vuelo = next((v for v in vuelos_disponibles if v.codigo == codigo_vuelo), None)
    
    if not vuelo:
        raise ValueError(f"Vuelo con código {codigo_vuelo} no encontrado.")
    
    # Verificar la disponibilidad en la clase seleccionada
    if clase == "economica" and vuelo.capacidad_economica > 0:
        vuelo.capacidad_economica -= 1  # Reducir la capacidad económica
        # Aquí se debería agregar al pasajero a una lista de pasajeros
        return f"Tiquete vendido para {pasajero.nombre} en clase económica."
    
    elif clase == "preferencial" and vuelo.capacidad_preferencial > 0:
        vuelo.capacidad_preferencial -= 1  # Reducir la capacidad preferencial
        # Aquí se debería agregar al pasajero a una lista de pasajeros
        return f"Tiquete vendido para {pasajero.nombre} en clase preferencial."
    
    else:
        raise ValueError("No hay capacidad disponible en la clase seleccionada.")

def verificar_asientos_disponibles():
    if

