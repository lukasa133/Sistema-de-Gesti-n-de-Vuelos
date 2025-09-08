import customtkinter as ctk
import tkinter as tk2


ctk.set_appearance_mode("light")  # modos: "system" (default), "dark", "light"
ctk.set_default_color_theme("green")  # temas: "blue" (default), "dark-blue", "green"

app = ctk.CTk() # Crea una ventana CTk como lo haces con la ventana Tk.

app.geometry("500x340")
def button_function():
    print("boton presionado")

# usa CTkButton en lugar de tkinter Button


button = ctk.CTkButton(master=app, text="CTkButton", command=button_function)
button.place(relx=0.25, rely=0.25, anchor=ctk.CENTER)



app.mainloop() # este es para se muestre y se mantenga la ventana principal abierta