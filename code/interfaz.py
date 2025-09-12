import customtkinter as ctk 
from CTkMessagebox import CTkMessagebox 
from gestion import vuelos_registrados, obtener_info_vuelo, vender_tiquete
from modelos import Pasajero

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.geometry("800x600")
        self.title("Vuelos Disponibles")
        
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(self.main_frame, text="Vuelos Disponibles", font=("Roboto", 24)).pack(pady=10)
        
        self.vuelos_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.vuelos_frame.pack(fill="both", expand=True)

        self.mostrar_vuelos()

    def mostrar_vuelos(self):
        # Limpiar cualquier contenido anterior
        for widget in self.vuelos_frame.winfo_children():
            widget.destroy()

        for vuelo in vuelos_registrados:
            self.crear_tarjeta_vuelo(self.vuelos_frame, vuelo)

    def crear_tarjeta_vuelo(self, parent_frame, vuelo):
        vuelo_info = obtener_info_vuelo(vuelo.codigo_vuelo)

        tarjeta = ctk.CTkFrame(parent_frame, corner_radius=10, border_width=2)
        tarjeta.pack(pady=10, padx=10, fill="x")

        # Frame principal de la tarjeta (siempre visible)
        info_basica_frame = ctk.CTkFrame(tarjeta, fg_color="transparent")
        info_basica_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(info_basica_frame, text=f"Ciudad origen: {vuelo.ciudad_origen} - Ciudad destino: {vuelo.ciudad_destino}", font=("Roboto", 14)).grid(row=0, column=0, sticky="w", columnspan=2)
        ctk.CTkLabel(info_basica_frame, text=f"Fecha: {vuelo.fecha_salida.strftime('%d/%m/%Y')}").grid(row=1, column=0, sticky="w", columnspan=2)
        ctk.CTkLabel(info_basica_frame, text=f"Cupo total: {vuelo.capacidad_economica + vuelo.capacidad_preferencial}").grid(row=2, column=0, sticky="w", columnspan=2)
        ctk.CTkLabel(info_basica_frame, text=f"Cupos preferenciales disponibles: {vuelo_info['info_por_clase']['Preferencial']['disponibles']}").grid(row=3, column=0, sticky="w", columnspan=2)
        ctk.CTkLabel(info_basica_frame, text=f"Cupos económicos disponibles: {vuelo_info['info_por_clase']['Economica']['disponibles']}").grid(row=4, column=0, sticky="w", columnspan=2)

        # Frame de detalles expandidos (inicialmente oculto)
        detalles_frame = ctk.CTkFrame(tarjeta, fg_color="transparent")
        
        ctk.CTkLabel(detalles_frame, text=f"Piloto: Juan", font=("Roboto", 12)).pack(anchor="w", pady=2)
        ctk.CTkLabel(detalles_frame, text=f"Copiloto: Daniel", font=("Roboto", 12)).pack(anchor="w", pady=2)
        ctk.CTkLabel(detalles_frame, text=f"Personal de cabina: Brayan - Martin", font=("Roboto", 12)).pack(anchor="w", pady=2)

        def toggle_detalles():
            if detalles_frame.winfo_ismapped():
                detalles_frame.pack_forget()
            else:
                detalles_frame.pack(fill="x", padx=10, pady=(0, 10))

        boton_frame = ctk.CTkFrame(tarjeta, fg_color="transparent")
        boton_frame.pack(fill="x", padx=10, pady=5)

        btn_mostrar_mas = ctk.CTkButton(boton_frame, text="MOSTRAR MÁS", command=toggle_detalles)
        btn_mostrar_mas.pack(side="left", padx=(0, 5))
        
        btn_comprar = ctk.CTkButton(boton_frame, text="COMPRAR BOLETO", command=lambda: TiqueteCompraDialog(self, vuelo.codigo_vuelo, self.mostrar_vuelos))
        btn_comprar.pack(side="left")

# ================================================
# Ventana emergente para la compra de tiquetes
# ================================================

class TiqueteCompraDialog(ctk.CTkToplevel):
    def __init__(self, master, codigo_vuelo, refresh_callback):
        super().__init__(master)
        self.master = master
        self.codigo_vuelo = codigo_vuelo
        self.refresh_callback = refresh_callback
        
        self.title("Datos")
        self.geometry("450x450")
        
        ctk.CTkLabel(self, text="Datos del Pasajero", font=("Roboto", 24)).pack(pady=20)
        
        campos_frame = ctk.CTkFrame(self, fg_color="transparent")
        campos_frame.pack(pady=10, padx=10)

        # Columna 1
        ctk.CTkLabel(campos_frame, text="Tipo de documento").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.tipo_doc_entry = ctk.CTkEntry(campos_frame)
        self.tipo_doc_entry.grid(row=1, column=0, padx=10, pady=5)

        ctk.CTkLabel(campos_frame, text="Número de documento").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.num_doc_entry = ctk.CTkEntry(campos_frame)
        self.num_doc_entry.grid(row=3, column=0, padx=10, pady=5)

        ctk.CTkLabel(campos_frame, text="Sexo").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.sexo_entry = ctk.CTkEntry(campos_frame)
        self.sexo_entry.grid(row=5, column=0, padx=10, pady=5)

        # Columna 2
        ctk.CTkLabel(campos_frame, text="Fecha de nacimiento").grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.fecha_nac_entry = ctk.CTkEntry(campos_frame)
        self.fecha_nac_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(campos_frame, text="Nombre completo").grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.nombre_entry = ctk.CTkEntry(campos_frame)
        self.nombre_entry.grid(row=3, column=1, padx=10, pady=5)

        ctk.CTkLabel(campos_frame, text="Número de teléfono").grid(row=4, column=1, sticky="w", padx=10, pady=5)
        self.telefono_entry = ctk.CTkEntry(campos_frame)
        self.telefono_entry.grid(row=5, column=1, padx=10, pady=5)

        botones_frame = ctk.CTkFrame(self, fg_color="transparent")
        botones_frame.pack(pady=20)
        
        ctk.CTkButton(botones_frame, text="COMPRAR CLASE PREFERENCIAL", command=lambda: self.procesar_venta("Preferencial")).pack(side="top", pady=5)
        ctk.CTkButton(botones_frame, text="COMPRAR CLASE ECONOMICA", command=lambda: self.procesar_venta("Economica")).pack(side="top", pady=5)
        
    def procesar_venta(self, clase_elegida):
        try:
            pasajero_data = {
                'tipo_documento': self.tipo_doc_entry.get(),
                'id_pasajero': self.num_doc_entry.get(),
                'nombre_completo': self.nombre_entry.get(),
                'sexo': self.sexo_entry.get(),
                'fecha_nacimiento': self.fecha_nac_entry.get(),
                'telefono': self.telefono_entry.get()
            }
            
            vender_tiquete(self.codigo_vuelo, pasajero_data, clase_elegida)

            if not self.tipo_doc_entry.get().strip() or not self.num_doc_entry.get()() or not self.nombre_entry.get().strip() or not self.sexo_entry.get().strip() or not self.fecha_nac_entry.get().strip() or not self.telefono_entry.get().strip():
                texto_a_mostrar = "Por favor, completa todos los campos."
            else:
            # Línea corregida
                CTkMessagebox(title="Éxito", message="¡Tiquete comprado con éxito!") 
                self.refresh_callback() 
                self.destroy() 
            
        except ValueError as e:
            # Línea corregida
            CTkMessagebox(title="Error", message=str(e))

if __name__ == "__main__":
    app = App()
    app.mainloop()