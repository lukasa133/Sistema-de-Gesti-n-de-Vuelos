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

    vuelo = next((v for v in vuelos_registrados if v.codigo_vuelo == codigo_vuelo), None) # Usa 'next' para encontrar el primer vuelo que coincida con el código_vuelo, si no lo encuentra devuelve 'None'.

    if not vuelo.verificarDisponibilidad(clase_elegida): # Condicional para mostrar mensabe si no se encuentran asientos disponibles para la clase.
        return f"¡ERROR! No hay asientos disponibles en la clase {clase_elegida} para el vuelo {codigo_vuelo}."

    pasajero = Pasajero(**pasajero_data) # Separa los valores del diccionario pasajero_dict para tomarlo como atributos y crear un objeto.

    id_tiquete = len(tiquetes_vendidos) + 1
        
    nuevo_tiquete = Tiquete(id_tiquete, clase_elegida, codigo_vuelo) # Crea un objeto para oa clase tiquete.
    tiquetes_vendidos.append(nuevo_tiquete)
    vuelo.pasajeros.append(pasajero) # Agregas el pasajero a la lista de la clase vuelo.
    # vuelo.tripulacion.append()
    
    return nuevo_tiquete

def obtener_info_vuelo(codigo_vuelo): # Función para detallar la  información de un vuelo: pasajeros, asientos ocupados y disponibles.
    
    vuelo = next((v for v in vuelos_registrados 
    if v.codigo_vuelo == codigo_vuelo), 
    None) # Usa 'next' para encontrar el primer vuelo que coincida con el código_vuelo, si no lo encuentra devuelve 'None'.
    
    if not vuelo:
        return f"Error: Vuelo con código '{codigo_vuelo}' no encontrado."
    
     # 1. Contar los tiquetes vendidos por clase
    asientos_economicos_vendidos = sum(1 for t in tiquetes_vendidos 
    if t.codigo_vuelo == codigo_vuelo 
    and t.clase.lower() == 'economica') # Calcula los asientos ocupados restando los tiquetes vendidos en capacidad_economica. El generador (1 for ...) cuenta cada uno de los tiquetes vendidos para la clase económica.
    
    asientos_preferenciales_vendidos = sum(1 for t in tiquetes_vendidos 
    if t.codigo_vuelo == codigo_vuelo 
    and t.clase.lower() == 'preferencial') # Calcula los asientos ocupados restando los tiquetes vendidos en capacidad_preferencial. El generador (1 for ...) cuenta cada uno de los tiquetes vendidos para la clase preferencial.
    
    
    # 2. Calcular los cupos disponibles
    asientos_economicos_disponibles = vuelo.capacidad_economica - asientos_economicos_vendidos
    asientos_preferenciales_disponibles = vuelo.capacidad_preferencial - asientos_preferenciales_vendidos
    
    # El resto de tus cálculos...
    total_asientos_ocupados = asientos_economicos_vendidos + asientos_preferenciales_vendidos
    total_asientos_disponibles = asientos_economicos_disponibles + asientos_preferenciales_disponibles
    
    return {
        'codigo': vuelo.codigo_vuelo,
        'pasajeros_registrados': len(vuelo.pasajeros),
        'asientos_ocupados': total_asientos_ocupados,
        'asientos_disponibles': total_asientos_disponibles,
        'info_por_clase': {
            'Economica': {'ocupados': asientos_economicos_vendidos, 'disponibles': asientos_economicos_disponibles},
            'Preferencial': {'ocupados': asientos_preferenciales_vendidos, 'disponibles': asientos_preferenciales_disponibles}
        }
    }