import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox

X = sp.symbols('x')  # Define la variable simbólica x

def SolicitarFuncion(EntryFunc):
    Expr = EntryFunc.get()  # Obtiene el texto de la entrada de función
    if Expr:
        try:
            Funcion = sp.sympify(Expr)  # Convierte la cadena de texto en una expresión simbólica
            # Validación adicional para funciones racionales (con denominadores)
            numerador, denominador = Funcion.as_numer_denom()  # Separa la función en numerador y denominador
            if not denominador.is_constant():  # Verifica si el denominador no es constante
                messagebox.showinfo("Aviso", "La función tiene un denominador. Se aplicará la regla del cociente.")
            return Funcion  # Devuelve la función simbólica
        except sp.SympifyError:
            messagebox.showerror("Error", "Función inválida. Inténtalo de nuevo.")  # Manejo de errores si la función es inválida
            return None
    else:
        messagebox.showerror("Error", "No se ingresó ninguna función.")  # Mensaje si no se ingresó nada
        return None  # Devuelve None

def SolicitarDerivadas(EntryDerivadas):
    Veces = EntryDerivadas.get()  # Obtiene el texto de la entrada de número de derivadas
    try:
        Veces = int(Veces)  # Intenta convertir la entrada a un entero
        if Veces >= 1:  # Verifica que el número de derivadas sea al menos 1
            return Veces  # Devuelve el número de derivadas
        else:
            messagebox.showerror("Error", "Introduce un número entero positivo.")  # Mensaje de error si el número es inválido
            return None
    except ValueError:
        messagebox.showerror("Error", "Entrada inválida. Inténtalo de nuevo.")  # Manejo de errores si la conversión falla
        return None

def DerivarFuncion(Funcion, Veces):
    Derivada = Funcion  # Inicializa la derivada como la función original
    Derivadas = []  # Lista para almacenar las derivadas
    for i in range(Veces):  # Itera el número de veces que se debe derivar
        Derivada = sp.diff(Derivada, X)  # Calcula la derivada respecto a X
        Derivadas.append(Derivada)  # Agrega la derivada a la lista
        
        # Validación: Si la derivada es constante, no puede derivarse más veces
        if Derivada.is_constant():
            messagebox.showwarning("Advertencia", f"No se puede derivar {Veces} veces. Se obtuvieron {i + 1} derivadas.")
            break  # Sale del bucle si se encuentra una derivada constante
    return Derivadas  # Devuelve la lista de derivadas calculadas

def GraficarFunciones(Funcion, Derivadas, FramePlot):
    XVals = np.linspace(-10, 10, 400)  # Crea un rango de valores para X
    FLambdified = sp.lambdify(X, Funcion, modules=["numpy"])  # Convierte la función simbólica en una función numérica
    YVals = FLambdified(XVals)  # Evalúa la función en los valores de X
    
    Fig, Ax = plt.subplots(figsize=(10, 6))  # Crea una figura y un eje para el gráfico
    Ax.plot(XVals, YVals, label=f"Función original: {sp.pretty(Funcion)}", color="blue")  # Grafica la función original
    
    Colores = ["red", "green", "purple", "orange"]  # Define una lista de colores para las derivadas
    for i, Deriv in enumerate(Derivadas):  # Itera sobre las derivadas calculadas
        FDerivLambdified = sp.lambdify(X, Deriv, modules=["numpy"])  # Convierte la derivada en una función numérica
        try:
            YDerivVals = FDerivLambdified(XVals)  # Evalúa la derivada en los valores de X
        except TypeError:
            YDerivVals = np.full_like(XVals, float(Deriv))  # Maneja el caso donde la derivada es constante
        
        Ax.plot(XVals, YDerivVals, label=f"{i + 1}ª derivada: {sp.pretty(Deriv)}", color=Colores[i % len(Colores)])  # Grafica cada derivada
    
    # Dibuja líneas de referencia en el gráfico
    Ax.axhline(0, color='black', linewidth=0.5)  # Línea horizontal en Y=0
    Ax.axvline(0, color='black', linewidth=0.5)  # Línea vertical en X=0
    Ax.grid(color='gray', linestyle='--', linewidth=0.5)  # Añade una cuadrícula al gráfico
    Ax.set_xlabel("X")  # Etiqueta del eje X
    Ax.set_ylabel("Y")  # Etiqueta del eje Y
    Ax.set_title("Función original y sus derivadas")  # Título del gráfico
    Ax.legend(fontsize=12)  # Aumenta el tamaño de la fuente de la leyenda

    # Eliminar cualquier gráfico previo del FramePlot y agregar el nuevo
    for Widget in FramePlot.winfo_children():
        Widget.destroy()  # Destruye widgets existentes en el marco del gráfico

    Canvas = FigureCanvasTkAgg(Fig, master=FramePlot)  # Crea un lienzo para el gráfico
    Canvas.draw()  # Dibuja el gráfico
    Canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Agrega el lienzo al marco de la interfaz gráfica

def EjecutarGrafico(EntryFunc, EntryDerivadas, FramePlot):
    # Función principal para ejecutar el proceso de graficación.
    Funcion = SolicitarFuncion(EntryFunc)  # Solicita la función al usuario
    if Funcion is None:  # Verifica si la función es válida
        return
    
    NumDerivadas = SolicitarDerivadas(EntryDerivadas)  # Solicita el número de derivadas
    if NumDerivadas is None:  # Verifica si el número de derivadas es válido
        return
    
    Derivadas = DerivarFuncion(Funcion, NumDerivadas)  # Calcula las derivadas de la función
    GraficarFunciones(Funcion, Derivadas, FramePlot)  # Grafica la función y sus derivadas

def Main():
    # Función principal para configurar la interfaz gráfica.
    Root = tk.Tk()  # Crea la ventana principal
    Root.title("Graficador de Funciones y Derivadas")  # Establece el título de la ventana
    Root.geometry("800x600")  # Establece el tamaño de la ventana

    Style = ttk.Style(Root)  # Crea un estilo para la interfaz
    Style.theme_use("clam")  # Usa un tema predefinido

    FrameInput = ttk.Frame(Root, padding="10")  # Crea un marco para la entrada
    FrameInput.pack(fill=tk.X, side=tk.TOP)  # Agrega el marco a la ventana

    # Etiqueta y entrada para la función
    ttk.Label(FrameInput, text="Función (en términos de x):").grid(row=0, column=0, sticky=tk.W)
    EntryFunc = ttk.Entry(FrameInput, width=50)  # Campo de entrada para la función
    EntryFunc.grid(row=0, column=1, padx=5, pady=5)

    # Etiqueta y entrada para el número de derivadas
    ttk.Label(FrameInput, text="Número de derivadas:").grid(row=1, column=0, sticky=tk.W)
    EntryDerivadas = ttk.Entry(FrameInput, width=50)  # Campo de entrada para el número de derivadas
    EntryDerivadas.grid(row=1, column=1, padx=5, pady=5)

    # Botón para graficar la función
    BtnGraficar = ttk.Button(FrameInput, text="Graficar", command=lambda: EjecutarGrafico(EntryFunc, EntryDerivadas, FramePlot))
    BtnGraficar.grid(row=2, column=1, pady=10)

    global FramePlot  # Define FramePlot como global para su acceso en otras funciones
    FramePlot = ttk.Frame(Root)  # Crea un marco para los gráficos
    FramePlot.pack(fill=tk.BOTH, expand=True)  # Agrega el marco a la ventana

    Root.mainloop()  # Inicia el bucle principal de la interfaz gráfica

if __name__ == "__main__":
    Main()  # Ejecuta la función principal al iniciar el programa
