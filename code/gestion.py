# ====================================================================================
# gestión
# ====================================================================================

from modelos import Vuelo, Pasajero, Tiquete

# Listas para registrar.
vuelos_registrados = []
tiquetes_vendidos = []


# Se establecen vuelos por defecto.
vuelo1 = Vuelo(
    codigo_vuelo="AV101",
    ciudad_origen="Medellín",
    ciudad_destino="Bogotá",
    fecha_salida="2025-12-25 08:00",
    fecha_llegada="2025-12-25 09:00",
    precio_economico="100.000",
    precio_preferencial="300.000",
    capacidad_economica=150,
    capacidad_preferencial=20,
    tripulacion = {"Piloto": "Juan", "Copiloto": "Martin", "personal_de_cabina": ["Sara", "Esthefany"]}
    
)

vuelo2 = Vuelo(
    codigo_vuelo="LA202",
    ciudad_origen="Bogotá",
    ciudad_destino="Cartagena",
    fecha_salida="2025-12-26 12:00",
    fecha_llegada="2025-12-26 13:30",
    precio_economico="300.000",
    precio_preferencial="750.000",
    capacidad_economica=80,
    capacidad_preferencial=15,
    tripulacion = {"Piloto": "Carlos", "Copiloto": "Alejandro", "personal_de_cabina": ["Maria", "Dayana"]}
)

vuelo3 = Vuelo(
    codigo_vuelo="SK303",
    ciudad_origen="Cali",
    ciudad_destino="Medellín",
    fecha_salida="2025-12-27 15:00",
    fecha_llegada="2025-12-27 16:00",
    precio_economico="200.000",
    precio_preferencial="500.000",
    capacidad_economica=100,
    capacidad_preferencial=10,
    tripulacion = {"Piloto": "James", "Copiloto": "Oscar", "personal_de_cabina": ["Sarah", "Ana"]}
)

# Añadir los vuelos a la lista de registros.
vuelos_registrados.extend([vuelo1, vuelo2, vuelo3])



def vender_tiquete(codigo_vuelo, pasajero_data, clase_elegida): # Función encargada de realizar la venta de los tiquetes.

    if not all(pasajero_data.values()): # Condicional para mostrar mensaje al dejar algún espacio vacio.
        return "¡ERROR! Todos los campos deben estar completos."

    vuelo = None
    for v in vuelos_registrados: 
        if v.codigo_vuelo == codigo_vuelo: # Evalua si el código del vuelo registrado coincide
            vuelo = v
            break
        
    # Calcular asientos disponibles antes de vender
    asientos_economicos_vendidos = sum(1 for t in tiquetes_vendidos 
                                       if t.codigo_vuelo == codigo_vuelo and t.clase.lower() == 'economica')
    
    asientos_preferenciales_vendidos = sum(1 for t in tiquetes_vendidos 
                                           if t.codigo_vuelo == codigo_vuelo and t.clase.lower() == 'preferencial')
    
    # Evalua la disponibilidad del asiento 
    asientos_economicos_disponibles = vuelo.capacidad_economica - asientos_economicos_vendidos 
    asientos_preferenciales_disponibles = vuelo.capacidad_preferencial - asientos_preferenciales_vendidos

    # Condicional para evaluar si los asientos llegó a su cupo maximo.
    if clase_elegida.lower() == 'economica' and asientos_economicos_disponibles <= 0:
        return f"¡ERROR! No hay asientos disponibles en la clase Economica para el vuelo {codigo_vuelo}."
    
    if clase_elegida.lower() == 'preferencial' and asientos_preferenciales_disponibles <= 0:
        return f"¡ERROR! No hay asientos disponibles en la clase Preferencial para el vuelo {codigo_vuelo}."

    pasajero = Pasajero(**pasajero_data) # Desempaqueta el diccionario pasajero_data y crea un objeto. 
    id_tiquete = len(tiquetes_vendidos) + 1
    nuevo_tiquete = Tiquete(id_tiquete, clase_elegida, codigo_vuelo)
    
    tiquetes_vendidos.append(nuevo_tiquete)
    vuelo.pasajeros.append(pasajero)
    
    return nuevo_tiquete 

def obtener_info_vuelo(codigo_vuelo): # Función para detallar la  información de un vuelo: pasajeros, asientos ocupados y disponibles.
    
    vuelo = None
    for v in vuelos_registrados:
        if v.codigo_vuelo == codigo_vuelo:
            vuelo = v
            break
    # Se asume que el código siempre existe por la interfaz
    asientos_economicos_vendidos = sum(1 for t in tiquetes_vendidos if t.codigo_vuelo == codigo_vuelo and t.clase.lower() == 'economica')
    asientos_preferenciales_vendidos = sum(1 for t in tiquetes_vendidos if t.codigo_vuelo == codigo_vuelo and t.clase.lower() == 'preferencial')
    
    # Evalua la disponibilidad del asiento para la interfaz.
    asientos_economicos_disponibles = vuelo.capacidad_economica - asientos_economicos_vendidos
    asientos_preferenciales_disponibles = vuelo.capacidad_preferencial - asientos_preferenciales_vendidos
    
    return {
        'info_por_clase': {
            'Economica': {'disponibles': asientos_economicos_disponibles},
            'Preferencial': {'disponibles': asientos_preferenciales_disponibles}
        }
    }