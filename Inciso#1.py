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

def solicitar_derivadas(entry_derivadas):
    veces = entry_derivadas.get()
    try:
        veces = int(veces)
        if veces >= 1:
            return veces
        else:
            messagebox.showerror("Error", "Introduce un número entero positivo.")
            return None
    except ValueError:
        messagebox.showerror("Error", "Entrada inválida. Inténtalo de nuevo.")
        return None

def derivar_funcion(funcion, veces):
    derivada = funcion
    for _ in range(veces):
        derivada = sp.diff(derivada, x)
    return derivada

def graficar_funciones(funcion, derivadas, frame_plot):
    x_vals = np.linspace(-10, 10, 400)
    f_lambdified = sp.lambdify(x, funcion, modules=["numpy"])
    y_vals = np.linspace(-10, 10, 400)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_vals, y_vals, label=f"Función original: {sp.pretty(funcion)}", color="blue")
    
    colores = ["red", "green", "purple", "orange"]
    for i, deriv in enumerate(derivadas):
        f_deriv_lambdified = sp.lambdify(x, deriv, modules=["numpy"])
        try:
            y_deriv_vals = f_deriv_lambdified(x_vals)
        except TypeError:
            y_deriv_vals = np.full_like(x_vals, float(deriv))
        
        ax.plot(x_vals, y_deriv_vals, label=f"{i+1}ª derivada: {sp.pretty(deriv)}", color=colores[i % len(colores)])
    
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(color='gray', linestyle='--', linewidth=0.5)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Función original y sus derivadas")
    ax.legend()

    # Eliminar cualquier gráfico previo del frame_plot y agregar el nuevo
    for widget in frame_plot.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def ejecutar_grafico(entry_func, entry_derivadas, frame_plot):
    funcion = solicitar_funcion(entry_func)
    if funcion is None:
        return
    
    num_derivadas = solicitar_derivadas(entry_derivadas)
    if num_derivadas is None:
        return
    
    derivadas = [derivar_funcion(funcion, i + 1) for i in range(num_derivadas)]
    graficar_funciones(funcion, derivadas, frame_plot)

def main():
    root = tk.Tk()
    root.title("Graficador de Funciones y Derivadas")
    root.geometry("800x600")

    style = ttk.Style(root)
    style.theme_use("clam")

    frame_input = ttk.Frame(root, padding="10")
    frame_input.pack(fill=tk.X, side=tk.TOP)

    ttk.Label(frame_input, text="Función (en términos de x):").grid(row=0, column=0, sticky=tk.W)
    entry_func = ttk.Entry(frame_input, width=50)
    entry_func.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_input, text="Número de derivadas:").grid(row=1, column=0, sticky=tk.W)
    entry_derivadas = ttk.Entry(frame_input, width=50)
    entry_derivadas.grid(row=1, column=1, padx=5, pady=5)

    # Botón para graficar la función
    btn_graficar = ttk.Button(frame_input, text="Graficar", command=lambda: ejecutar_grafico(entry_func, entry_derivadas, frame_plot))
    btn_graficar.grid(row=2, column=1, pady=10)

    global frame_plot
    frame_plot = ttk.Frame(root)
    frame_plot.pack(fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()
