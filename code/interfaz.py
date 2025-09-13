import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from gestion import vuelos_registrados, obtener_info_vuelo, vender_tiquete
from modelos import Pasajero

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Vuelos Disponibles")
        self.current_frame = None
        self.show_frame(FrameVuelos)

    def show_frame(self, frame_class, *args, **kwargs):
        # Elimina el frame actual si existe
        if self.current_frame is not None:
            self.current_frame.destroy()
        # Crea y muestra el nuevo frame
        self.current_frame = frame_class(self, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

class FrameVuelos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Vuelos Disponibles", font=("Roboto", 24)).pack(pady=10)
        self.vuelos_frame = ctk.CTkScrollableFrame(self)
        self.vuelos_frame.pack(fill="both", expand=True)
        self.mostrar_vuelos()

    def mostrar_vuelos(self):
        for widget in self.vuelos_frame.winfo_children():
            widget.destroy()
        for vuelo in vuelos_registrados:
            self.crear_tarjeta_vuelo(self.vuelos_frame, vuelo)

    def crear_tarjeta_vuelo(self, parent_frame, vuelo):
        vuelo_info = obtener_info_vuelo(vuelo.codigo_vuelo)
        tarjeta = ctk.CTkFrame(parent_frame, corner_radius=10, border_width=2)
        tarjeta.pack(pady=10, padx=10, fill="x")

        info_basica_frame = ctk.CTkFrame(tarjeta, fg_color="transparent")
        info_basica_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(info_basica_frame, text=f"Ciudad origen: {vuelo.ciudad_origen} - Ciudad destino: {vuelo.ciudad_destino}", font=("Roboto", 14)).grid(row=0, column=0, sticky="w", columnspan=2)
        ctk.CTkLabel(info_basica_frame, text=f"Fecha: {vuelo.fecha_salida.strftime('%d/%m/%Y')}").grid(row=1, column=0, sticky="w", columnspan=2)
        ctk.CTkLabel(info_basica_frame, text=f"Cupo total: {vuelo.capacidad_economica + vuelo.capacidad_preferencial}").grid(row=2, column=0, sticky="w", columnspan=2)
        ctk.CTkLabel(info_basica_frame, text=f"Cupos preferenciales disponibles: {vuelo_info['info_por_clase']['Preferencial']['disponibles']}").grid(row=3, column=0, sticky="w", columnspan=2)
        ctk.CTkLabel(info_basica_frame, text=f"Cupos económicos disponibles: {vuelo_info['info_por_clase']['Economica']['disponibles']}").grid(row=4, column=0, sticky="w", columnspan=2)

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
        btn_comprar = ctk.CTkButton(
            boton_frame, 
            text="COMPRAR BOLETO", 
            command=lambda: self.master.show_frame(FrameCompraTiquete, vuelo.codigo_vuelo)
        )
        btn_comprar.pack(side="left")

class FrameCompraTiquete(ctk.CTkFrame):
    def __init__(self, master, codigo_vuelo):
        super().__init__(master)
        self.master = master
        self.codigo_vuelo = codigo_vuelo
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
        ctk.CTkButton(botones_frame, text="VOLVER", command=self.volver).pack(side="top", pady=10)

    def procesar_venta(self, clase_elegida):
        # Validar primero
        if (not self.tipo_doc_entry.get().strip() or
            not self.num_doc_entry.get().strip() or
            not self.nombre_entry.get().strip() or
            not self.sexo_entry.get().strip() or
            not self.fecha_nac_entry.get().strip() or
            not self.telefono_entry.get().strip()):
            CTkMessagebox(title="Error", message="Por favor, completa todos los campos.")
            return
        pasajero_data = {
            'tipo_documento': self.tipo_doc_entry.get().strip(),
            'id_pasajero': self.num_doc_entry.get().strip(),
            'nombre_completo': self.nombre_entry.get().strip(),
            'sexo': self.sexo_entry.get().strip(),
            'fecha_nacimiento': self.fecha_nac_entry.get().strip(),
            'telefono': self.telefono_entry.get().strip()
        }
        try:
            vender_tiquete(self.codigo_vuelo, pasajero_data, clase_elegida)
            CTkMessagebox(title="Éxito", message="¡Tiquete comprado con éxito!")
            self.volver()
        except ValueError as e:
            CTkMessagebox(title="Error", message=str(e))

    def volver(self):
        self.master.show_frame(FrameVuelos)

if __name__ == "__main__":
    app = App()
    app.mainloop()