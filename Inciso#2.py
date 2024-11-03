import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox

# Configuración inicial de SymPy
x = sp.symbols('x')

def solicitar_funcion(entry_func):
    expr = entry_func.get()
    if expr:
        try:
            return sp.sympify(expr)
        except sp.SympifyError:
            messagebox.showerror("Error", "Función inválida. Inténtalo de nuevo.")
            return None
    else:
        messagebox.showerror("Error", "No se ingresó ninguna función.")
        return None

def solicitar_punto(entry_x, entry_y):
    try:
        x_punto = float(entry_x.get())
        y_punto = float(entry_y.get())
        return x_punto, y_punto
    except ValueError:
        messagebox.showerror("Error", "Los valores de x e y deben ser numéricos.")
        return None, None

def verificar_punto(funcion, x_valor, y_valor):
    y_funcion = sp.lambdify(x, funcion, modules=["numpy"])
    return np.isclose(y_funcion(x_valor), y_valor)

def graficar_funcion_con_punto(funcion, x_punto, y_punto, pertenece, frame_plot):
    x_vals = np.linspace(-10, 10, 400)
    f_lambdified = sp.lambdify(x, funcion, modules=["numpy"])
    y_vals = f_lambdified(x_vals)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_vals, y_vals, label="Función original", color="blue")
    ax.plot(x_punto, y_punto, "r*" if pertenece else "g*", markersize=10, 
            label="Punto en la función" if pertenece else "Punto fuera de la función")
    
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    ax.set_xlabel("X")
    ax.set_ylabel("f(x)")
    ax.set_title("Función con el punto indicado")
    ax.legend()

    for widget in frame_plot.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def graficar_recta_tangente(funcion, x_punto, frame_plot):
    derivada = sp.diff(funcion, x)
    f_lambdified = sp.lambdify(x, funcion, modules=["numpy"])
    f_prime_lambdified = sp.lambdify(x, derivada, modules=["numpy"])
    
    pendiente = f_prime_lambdified(x_punto)
    y_punto = f_lambdified(x_punto)
    
    x_vals = np.linspace(x_punto - 5, x_punto + 5, 400)
    recta_tangente = pendiente * (x_vals - x_punto) + y_punto

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_vals, f_lambdified(x_vals), label="Función original", color="blue")
    ax.plot(x_vals, recta_tangente, label="Recta Tangente", color="green")
    ax.plot(x_punto, y_punto, "r*", markersize=10, label="Punto dado")
    
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    ax.set_xlabel("X")
    ax.set_ylabel("f(x)")
    ax.set_title("Función y su recta tangente en el punto dado")
    ax.legend()

    for widget in frame_plot.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def ejecutar_grafico(entry_func, entry_x, entry_y, frame_plot, lbl_verificacion):
    funcion = solicitar_funcion(entry_func)
    if funcion is None:
        return
    
    x_punto, y_punto = solicitar_punto(entry_x, entry_y)
    if x_punto is None or y_punto is None:
        return
    
    pertenece = verificar_punto(funcion, x_punto, y_punto)
    if pertenece:
        lbl_verificacion.config(text="El punto pertenece a la función.", foreground="green")
    else:
        lbl_verificacion.config(text="El punto no pertenece a la función.", foreground="red")

    graficar_funcion_con_punto(funcion, x_punto, y_punto, pertenece, frame_plot)
    
    if pertenece:
        graficar_recta_tangente(funcion, x_punto, frame_plot)

def main():
    root = tk.Tk()
    root.title("Graficador de Funciones y Derivadas")
    root.geometry("800x600")

    frame_input = ttk.Frame(root, padding="10")
    frame_input.pack(fill=tk.X, side=tk.TOP)

    ttk.Label(frame_input, text="Función (en términos de x):").grid(row=0, column=0, sticky=tk.W)
    entry_func = ttk.Entry(frame_input, width=50)
    entry_func.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_input, text="Valor de x del punto:").grid(row=1, column=0, sticky=tk.W)
    entry_x = ttk.Entry(frame_input, width=20)
    entry_x.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    ttk.Label(frame_input, text="Valor de y del punto:").grid(row=2, column=0, sticky=tk.W)
    entry_y = ttk.Entry(frame_input, width=20)
    entry_y.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    # Etiqueta para mostrar el resultado de la verificación
    lbl_verificacion = ttk.Label(frame_input, text="")
    lbl_verificacion.grid(row=4, column=1, pady=10)

    btn_graficar = ttk.Button(frame_input, text="Graficar", 
                              command=lambda: ejecutar_grafico(entry_func, entry_x, entry_y, frame_plot, lbl_verificacion))
    btn_graficar.grid(row=3, column=1, pady=10, sticky=tk.E)

    global frame_plot
    frame_plot = ttk.Frame(root)
    frame_plot.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
