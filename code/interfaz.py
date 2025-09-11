# vista.py

import customtkinter as ctk
from gestion import (
    crear_nuevo_vuelo,
    registrar_pasajero,
    vender_tiquete,
    consultar_vuelos_disponibles_en_rango,
    obtener_info_vuelo
)
from datetime import datetime

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración principal de la ventana
        self.geometry("600x400")
        self.title("Sistema de Gestión de Vuelos")
        
        # Atributos para los frames de cada "pantalla"
        self.frame_menu_principal = None
        self.frame_crear_vuelo = None
        self.frame_vender_tiquete = None
        self.frame_consultar_vuelo = None
        self.frame_resultado = None

        self.mostrar_menu_principal()

    def limpiar_interfaz(self):
        """Oculta todos los frames para poder mostrar uno nuevo."""
        for widget in self.winfo_children():
            widget.pack_forget()

    def mostrar_menu_principal(self):
        """Crea la pantalla inicial con las opciones principales."""
        self.limpiar_interfaz()
        self.frame_menu_principal = ctk.CTkFrame(self)
        self.frame_menu_principal.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(self.frame_menu_principal, text="Menú Principal", font=("Roboto", 24)).pack(pady=20)
        
        ctk.CTkButton(self.frame_menu_principal, text="1. Crear Nuevo Vuelo", command=self.mostrar_crear_vuelo).pack(pady=10)
        ctk.CTkButton(self.frame_menu_principal, text="2. Vender Tiquete", command=self.mostrar_vender_tiquete).pack(pady=10)
        ctk.CTkButton(self.frame_menu_principal, text="3. Consultar Vuelos", command=self.mostrar_consultar_vuelos).pack(pady=10)

    def mostrar_crear_vuelo(self):
        """Crea la interfaz para la funcionalidad 'Crear Vuelo'."""
        self.limpiar_interfaz()
        self.frame_crear_vuelo = ctk.CTkFrame(self)
        self.frame_crear_vuelo.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(self.frame_crear_vuelo, text="Crear Nuevo Vuelo", font=("Roboto", 20)).pack(pady=10)
        
        # Campos de entrada de datos (Entry widgets)
        self.codigo_vuelo_entry = ctk.CTkEntry(self.frame_crear_vuelo, placeholder_text="Código de vuelo")
        self.codigo_vuelo_entry.pack(pady=5)
        # ... agregar más campos para origen, destino, fechas, etc.

        ctk.CTkButton(self.frame_crear_vuelo, text="Guardar Vuelo", command=self.procesar_crear_vuelo).pack(pady=10)
        ctk.CTkButton(self.frame_crear_vuelo, text="Volver", command=self.mostrar_menu_principal).pack(pady=5)
    
    def procesar_crear_vuelo(self):
        """Llama al gestor para crear el vuelo y muestra el resultado."""
        try:
            # Obtener datos de los campos de entrada
            codigo = self.codigo_vuelo_entry.get()
            # ... obtener el resto de los datos
            origen = "Medellin"  # Ejemplo de datos
            destino = "Bogota"
            salida = datetime.now().strftime('%Y-%m-%d %H:%M')
            llegada = datetime.now().strftime('%Y-%m-%d %H:%M')
            cap_econ = 100
            cap_pref = 50

            # Llamar a la función del gestor
            nuevo_vuelo = crear_nuevo_vuelo(codigo, origen, destino, salida, llegada, cap_econ, cap_pref)
            
            # Mostrar resultado en la interfaz
            self.mostrar_resultado(f"Vuelo '{nuevo_vuelo.codigo_vuelo}' creado con éxito.", True)
        except ValueError as e:
            self.mostrar_resultado(str(e), False)
    
    # Agregar aquí los métodos para las otras funcionalidades (vender tiquete, consultar, etc.)
    def mostrar_vender_tiquete(self):
         self.limpiar_interfaz()
         self.frame_vender_tiquete = ctk.CTkFrame(self)
         self.frame_crear_vuelo.pack(pady=20, padx=20, fill="both", expand=True)
         

    def mostrar_consultar_vuelos(self):
         self.limpiar_interfaz()
         
    #     # ... crear widgets para esta pantalla

    def mostrar_resultado(self, mensaje, exito=True):
        """Muestra un mensaje al usuario después de una operación."""
        self.limpiar_interfaz()
        self.frame_resultado = ctk.CTkFrame(self)
        self.frame_resultado.pack(pady=20, padx=20, fill="both", expand=True)
        
        color = "green" if exito else "red"
        ctk.CTkLabel(self.frame_resultado, text=mensaje, text_color=color, font=("Roboto", 16)).pack(pady=20)
        ctk.CTkButton(self.frame_resultado, text="Volver al Menú", command=self.mostrar_menu_principal).pack(pady=10)

# Iniciar la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()