import tkinter as tk
from tkinter import ttk

def set_progress(percentage):
    progress_bar["value"] = percentage

# Crear la ventana principal
root = tk.Tk()
root.title("Barra de Carga Determinada")

# Obtener el ancho y alto de la pantalla
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()

# Calcular las coordenadas x e y para que la ventana esté centrada
x = (ancho_pantalla - 400) / 2
y = (alto_pantalla - 200) / 2

# Establecer la geometría de la ventana
root.geometry(f'400x200+{int(x)}+{int(y)}')

# Crear un marco para organizar los elementos
frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, padx=50, pady=50)

# Crear la barra de carga determinada
progress_bar = ttk.Progressbar(frame, mode="determinate", length=200)
progress_bar.grid(row=0, column=0, columnspan=2, pady=10)

# Entrada para establecer el porcentaje
percentage_entry = ttk.Entry(frame)
percentage_entry.grid(row=1, column=0, pady=10)

# Botón para establecer el porcentaje
set_percentage_button = ttk.Button(frame, text="Establecer Porcentaje", command=lambda: set_progress(float(percentage_entry.get())))
set_percentage_button.grid(row=1, column=1, pady=10)

# Iniciar la aplicación
root.mainloop()