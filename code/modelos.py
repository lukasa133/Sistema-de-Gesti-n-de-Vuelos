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
    
    # Obtenemos la capacidad total que tendrá el avion
    def obtener_capacidad(self):
        return self.capacidad_total

class Asiento:
    def __init__(self, numero_asiento, clase, disponible=True):
        self.numero_asiento = numero_asiento
        self.clase = clase
        self.disponible = disponible
    
    def ocupar_asiento(self):
        """Cambia el estado del asiento a ocupado."""
        self.disponible = False

class Tiquete:
    def __init__(self, id_tiquete, clase, precio_tiquete, asiento_asignado=None):
        self.id_tiquete = id_tiquete
        self.clase = clase
        self.asiento_asignado = asiento_asignado
        self.precio_tiquete = precio_tiquete
    
    def generar_factura(self):
        # La lógica de facturación iría aquí.
        pass

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
        # Atributos de la clase Vuelo
        self.codigo_vuelo = codigo_vuelo
        self.ciudad_origen = ciudad_origen
        self.ciudad_destino = ciudad_destino
        self.fecha_salida = datetime.strptime(fecha_salida, '%Y-%m-%d %H:%M')
        self.fecha_llegada = datetime.strptime(fecha_llegada, '%Y-%m-%d %H:%M')
        
        # Inicialización de listas y creación de asientos
        self.pasajeros = []
        self.tripulacion = []
        self.asientos_economicos = [Asiento(i, 'Economica') for i in range(1, capacidad_economica + 1)]
        self.asientos_preferenciales = [Asiento(i, 'Preferencial') for i in range(1, capacidad_preferencial + 1)]
        
    def obtener_asientos_disponibles(self):
        """Devuelve el número de asientos disponibles por clase."""
        econ_disp = sum(1 for a in self.asientos_economicos if a.disponible)
        pref_disp = sum(1 for a in self.asientos_preferenciales if a.disponible)
        return {'Economica': econ_disp, 'Preferencial': pref_disp}
    
    def asignar_tripulacion(self, tripulacion):
        """Asigna una lista de objetos Tripulacion a este vuelo."""
        self.tripulacion = tripulacion