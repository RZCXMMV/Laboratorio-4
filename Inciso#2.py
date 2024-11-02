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

def solicitar_punto():
    # Solicita al usuario el punto en una ventana emergente
    x_punto = simpledialog.askfloat("Entrada de punto", "Introduce el valor de x del punto:")
    y_punto = simpledialog.askfloat("Entrada de punto", "Introduce el valor de y del punto:")
    return x_punto, y_punto

def verificar_punto(funcion, x_valor, y_valor):
    # Verifica si el punto (x_valor, y_valor) pertenece a la función
    y_funcion = sp.lambdify(x, funcion, modules=["numpy"])
    return np.isclose(y_funcion(x_valor), y_valor)

def graficar_funcion_con_punto(funcion, x_punto, y_punto):
    # Define el rango de valores de x para graficar
    x_vals = np.linspace(-10, 10, 400)
    f_lambdified = sp.lambdify(x, funcion, modules=["numpy"])
    y_vals = f_lambdified(x_vals)
    
    # Grafica la función original y el punto indicado
    plt.plot(x_vals, y_vals, label="Función original", color="blue")
    plt.plot(x_punto, y_punto, "r*", markersize=10, label="Punto dado")
    
    # Configuración de cuadrícula, ejes y etiquetas
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Función con el punto indicado")
    plt.legend()
    plt.show()

def graficar_recta_tangente(funcion, x_punto):
    # Calcula la derivada de la función
    derivada = sp.diff(funcion, x)
    f_lambdified = sp.lambdify(x, funcion, modules=["numpy"])
    f_prime_lambdified = sp.lambdify(x, derivada, modules=["numpy"])
    
    # Calcula la pendiente y el valor de la función en el punto
    pendiente = f_prime_lambdified(x_punto)
    y_punto = f_lambdified(x_punto)
    
    # Ecuación de la recta tangente
    x_vals = np.linspace(x_punto - 5, x_punto + 5, 400)
    recta_tangente = pendiente * (x_vals - x_punto) + y_punto

    # Graficar la función, el punto y la recta tangente
    y_vals = f_lambdified(x_vals)
    plt.plot(x_vals, y_vals, label="Función original", color="blue")
    plt.plot(x_vals, recta_tangente, label="Recta Tangente", color="green")
    plt.plot(x_punto, y_punto, "r*", markersize=10, label="Punto dado")
    
    # Configuración de cuadrícula, ejes y etiquetas
    plt.axhline(0, color='black',linewidth=0.5)
    plt.axvline(0, color='black',linewidth=0.5)
    plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    plt.xlabel("Y")
    plt.ylabel("X")
    plt.title("Función y su recta tangente en el punto dado")
    plt.legend()
    plt.show()

def main():
    # Configuración de la ventana principal de Tkinter
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    # Solicita la función y el punto al usuario
    funcion = solicitar_funcion()
    if funcion is None:
        return
    
    x_punto, y_punto = solicitar_punto()
    
    # Verifica si el punto pertenece a la función
    if verificar_punto(funcion, x_punto, y_punto):
        messagebox.showinfo("Verificación", "El punto pertenece a la función.")
        graficar_funcion_con_punto(funcion, x_punto, y_punto)  # Grafica la función con el punto
        graficar_recta_tangente(funcion, x_punto)  # Grafica la recta tangente
    else:
        messagebox.showerror("Error", "El punto no pertenece a la función.")

# Ejecuta el programa principal
if __name__ == "__main__":
    main()
