import customtkinter as ctk
from datetime import datetime, timedelta
from gestion import GestorVuelos

# interfaz.py
import customtkinter as ctk
import gestion # La interfaz interactúa con el módulo de gestión

def crear_ventana_principal():
    ventana = ctk.CTk()
    ventana.title("Sistema de Gestión de Vuelos")

    # Botón para crear un vuelo
    boton_crear_vuelo = ctk.CTkButton(ventana, text="Crear Vuelo", command=mostrar_formulario_crear_vuelo)
    boton_crear_vuelo.pack()

def mostrar_formulario_crear_vuelo():
    # Lógica para mostrar los campos de texto
    # y un botón de "Guardar"
    # Cuando se haga clic en "Guardar", se llamará a la función de gestión:
    # gestion.crear_nuevo_vuelo(datos_del_formulario)
    pass