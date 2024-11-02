import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox

# Configuración inicial de SymPy
x = sp.symbols('x')

def solicitar_funcion():
    # Solicita al usuario una función en una ventana emergente
    expr = simpledialog.askstring("Entrada de función", "Introduce la función en términos de x (ejemplo: sin(x) o x**2):")
    if expr:
        return sp.sympify(expr)
    else:
        messagebox.showerror("Error", "No se ingresó ninguna función.")
        return None

def solicitar_derivadas():
    # Solicita al usuario el número de derivadas
    while True:
        try:
            veces = simpledialog.askinteger("Número de derivadas", "¿Cuántas veces deseas derivar la función?", minvalue=1)
            if veces is not None:
                return veces
            else:
                messagebox.showerror("Error", "Por favor, introduce un número entero positivo.")
        except ValueError:
            messagebox.showerror("Error", "Entrada inválida. Inténtalo de nuevo.")

def derivar_funcion(funcion, veces):
    # Calcula la derivada de la función la cantidad de veces indicada
    derivada = funcion
    for _ in range(veces):
        derivada = sp.diff(derivada, x)
    return derivada

def graficar_funciones(funcion, derivadas):
    # Define el rango de valores de x para graficar
    x_vals = np.linspace(-10, 10, 400)
    f_lambdified = sp.lambdify(x, funcion, modules=["numpy"])
    y_vals = f_lambdified(x_vals)
    
    # Grafica la función original con su expresión en la leyenda
    plt.plot(x_vals, y_vals, label=f"Función original: {sp.pretty(funcion)}", color="blue")
    
    # Colores para las derivadas
    colores = ["red", "green", "purple", "orange"]
    for i, deriv in enumerate(derivadas):
        f_deriv_lambdified = sp.lambdify(x, deriv, modules=["numpy"])
        
        # Verifica si la derivada es una constante y crea un array con el mismo tamaño de x_vals
        try:
            y_deriv_vals = f_deriv_lambdified(x_vals)
        except TypeError:
            y_deriv_vals = np.full_like(x_vals, float(deriv))
        
        # Muestra la expresión de cada derivada en la leyenda
        plt.plot(x_vals, y_deriv_vals, label=f"{i+1}ª derivada: {sp.pretty(deriv)}", color=colores[i % len(colores)])
    
    # Configuración de la cuadrícula, los ejes y el título
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.xlabel("Y")
    plt.ylabel("X")
    plt.title("Función original y sus derivadas")
    plt.legend()
    plt.show()

def main():
    # Configuración de la ventana principal de Tkinter
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    # Solicita la función y el número de derivadas a través de ventanas emergentes
    funcion = solicitar_funcion()
    if funcion is None:
        return
    
    num_derivadas = solicitar_derivadas()
    if num_derivadas is None:
        return
    
    # Calcula las derivadas y grafica
    derivadas = [derivar_funcion(funcion, i + 1) for i in range(num_derivadas)]
    graficar_funciones(funcion, derivadas)

# Ejecuta el programa principal
if __name__ == "__main__":
    main()

