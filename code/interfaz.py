import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from gestion import vuelos_registrados, obtener_info_vuelo, vender_tiquete
from modelos import Pasajero

ctk.set_appearance_mode("System") # O "Light", o "System"
ctk.set_default_color_theme("dark-blue") # O "blue", "dark-blue", "green"
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Vuelos Disponibles")
        self.current_frame = None
        self.show_frame(FrameBievenida)
        
    def show_frame(self, frame_class, *args, **kwargs):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

    def mostrar_mensaje(self, mensaje, titulo="Notificación"):
        CTkMessagebox(title=titulo, message=mensaje, icon="info")

class FrameBievenida(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Bienvenido a la Agencia de Viajes", font=("Roboto", 24)).pack(pady=20)
        ctk.CTkButton(self, text="Ver Vuelos Disponibles", command=lambda: master.show_frame(FrameVuelos)).pack(pady=10)
        
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

        # Configurar comandos de validación
        self.validar_digitos_cmd = self.register(self.validar_digitos)
        self.validar_letras_cmd = self.register(self.validar_letras)

        # Columna 1
        ctk.CTkLabel(campos_frame, text="Tipo de documento").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.documento_opcion = ctk.CTkOptionMenu(campos_frame, values=["Cédula de Ciudadanía", "Tarjeta de Identidad"])
        self.documento_opcion.grid(row=1, column=0, padx=10, pady=5)
        
        ctk.CTkLabel(campos_frame, text="Número de documento").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.num_doc_entry = ctk.CTkEntry(
            campos_frame, 
            validate="key", 
            validatecommand=(self.validar_digitos_cmd, '%P')
        )
        self.num_doc_entry.grid(row=3, column=0, padx=10, pady=5)

        ctk.CTkLabel(campos_frame, text="Sexo").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.sexo_opcion = ctk.CTkOptionMenu(campos_frame, values=["Femenino", "Masculino"])
        self.sexo_opcion.grid(row=5, column=0, padx=10, pady=5)

        # Columna 2
        ctk.CTkLabel(campos_frame, text="Fecha de nacimiento").grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.fecha_nac_entry = ctk.CTkEntry(campos_frame)
        self.fecha_nac_entry.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(campos_frame, text="Nombre completo").grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.nombre_entry = ctk.CTkEntry(
            campos_frame, 
            validate="key", 
            validatecommand=(self.validar_letras_cmd, '%P')
        )
        self.nombre_entry.grid(row=3, column=1, padx=10, pady=5)

        ctk.CTkLabel(campos_frame, text="Número de teléfono").grid(row=4, column=1, sticky="w", padx=10, pady=5)
        self.telefono_entry = ctk.CTkEntry(
            campos_frame, 
            validate="key", 
            validatecommand=(self.validar_digitos_cmd, '%P')
        )
        self.telefono_entry.grid(row=5, column=1, padx=10, pady=5)

        botones_frame = ctk.CTkFrame(self, fg_color="transparent")
        botones_frame.pack(pady=20)
        ctk.CTkButton(botones_frame, text="COMPRAR CLASE PREFERENCIAL", command=lambda: self.procesar_venta("Preferencial")).pack(side="top", pady=5)
        ctk.CTkButton(botones_frame, text="COMPRAR CLASE ECONOMICA", command=lambda: self.procesar_venta("Economica")).pack(side="top", pady=5)
        ctk.CTkButton(botones_frame, text="VOLVER", command=self.volver).pack(side="top", pady=10)

    def validar_digitos(self, texto_propuesto):
        if texto_propuesto == "" or texto_propuesto.isdigit():
            return True
        else:
            CTkMessagebox(title="Error de Entrada", message="Solo puedes ingresar números en este campo.", icon="warning")
            return False

    def validar_letras(self, texto_propuesto):
        if texto_propuesto == "" or texto_propuesto.replace(" ", "").isalpha():
            return True
        else:
            CTkMessagebox(title="Error de Entrada", message="Solo puedes ingresar letras y espacios en este campo.", icon="warning")
            return False

    def procesar_venta(self, clase_elegida):
        # Esta validación final es la mejor práctica para asegurar que los campos no estén vacíos
        # y para mostrar un error general si algo se pasó por alto.
        pasajero_data = {
            'tipo_documento': self.documento_opcion.get().strip(),
            'id_pasajero': self.num_doc_entry.get().strip(),
            'nombre_completo': self.nombre_entry.get().strip(),
            'sexo': self.sexo_opcion.get().strip(),
            'fecha_nacimiento': self.fecha_nac_entry.get().strip(),
            'telefono': self.telefono_entry.get().strip()
        }
        
        resultado = vender_tiquete(self.codigo_vuelo, pasajero_data, clase_elegida)
        
        if isinstance(resultado, str):
            self.master.mostrar_mensaje(f"{resultado}", "Error en la Venta")
        else:
            vuelo = next((v for v in vuelos_registrados if v.codigo_vuelo == self.codigo_vuelo), None)
            ciudad_origen = vuelo.ciudad_origen if vuelo else ""
            ciudad_destino = vuelo.ciudad_destino if vuelo else ""
            fecha_salida = vuelo.fecha_salida if vuelo else ""
            fecha_llegada = vuelo.fecha_llegada if vuelo else ""
            self.master.mostrar_mensaje(
                f"¡Tiquete comprado con éxito! \nCiudad origen: {ciudad_origen} \nCiudad destino: {ciudad_destino} \nHora y fecha de salida: {fecha_salida} \nHora y fecha de llegada: {fecha_llegada} \nTotal de tiquetes: {resultado.id_tiquete}",
                "Venta Exitosa"
            )

    def volver(self):
        self.master.show_frame(FrameVuelos)

if __name__ == "__main__":
    app = App()
    app.mainloop()