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
            return sp.sympify(Expr)  # Convierte la cadena de texto en una expresión simbólica
        except sp.SympifyError:
            messagebox.showerror("Error", "Función inválida. Inténtalo de nuevo.")  # Manejo de errores si la función es inválida
            return None
    else:
        messagebox.showerror("Error", "No se ingresó ninguna función.")  # Mensaje si no se ingresó nada
        return None

def SolicitarPunto(EntryX, EntryY):
    try:
        XPunto = float(EntryX.get())  # Convierte el valor de X a float
        YPunto = float(EntryY.get())  # Convierte el valor de Y a float
        return XPunto, YPunto  # Devuelve las coordenadas del punto
    except ValueError:
        messagebox.showerror("Error", "Los valores de x e y deben ser numéricos.")  # Mensaje si la conversión falla
        return None, None

def VerificarPunto(Funcion, XValor, YValor):
    # Verifica si el punto pertenece a la función.
    YFuncion = sp.lambdify(X, Funcion, modules=["numpy"])  # Convierte la función simbólica en una función numérica
    return np.isclose(YFuncion(XValor), YValor)  # Compara si el valor de la función en XValor es cercano a YValor

def GraficarFuncionConPunto(Funcion, XPunto, YPunto, Pertenece, FramePlot):
    XVals = np.linspace(-10, 10, 400)  # Crea un rango de valores para X
    FLambdified = sp.lambdify(X, Funcion, modules=["numpy"])  # Convierte la función simbólica en una función numérica
    YVals = FLambdified(XVals)  # Evalúa la función en los valores de X
    
    Fig, Ax = plt.subplots(figsize=(10, 6))  # Crea una figura y un eje para el gráfico
    Ax.plot(XVals, YVals, label="Función original", color="blue")  # Grafica la función original
    Ax.plot(XPunto, YPunto, "g*" if Pertenece else "r*", markersize=10, 
            label="Punto en la función" if Pertenece else "Punto fuera de la función")  # Grafica el punto

    # Dibuja líneas de referencia en el gráfico
    Ax.axhline(0, color='black', linewidth=0.5)  # Línea horizontal en Y=0
    Ax.axvline(0, color='black', linewidth=0.5)  # Línea vertical en X=0
    Ax.grid(color='gray', linestyle='--', linewidth=0.5)  # Añade una cuadrícula al gráfico
    Ax.set_xlabel("X")  # Etiqueta del eje X
    Ax.set_ylabel("f(x)")  # Etiqueta del eje Y
    Ax.set_title("Función con el punto indicado")  # Título del gráfico
    Ax.legend()  # Muestra la leyenda

    # Eliminar cualquier gráfico previo del FramePlot y agregar el nuevo
    for Widget in FramePlot.winfo_children():
        Widget.destroy()  # Destruye widgets existentes en el marco del gráfico

    Canvas = FigureCanvasTkAgg(Fig, master=FramePlot)  # Crea un lienzo para el gráfico
    Canvas.draw()  # Dibuja el gráfico
    Canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Agrega el lienzo al marco de la interfaz gráfica

def GraficarRectaTangente(Funcion, XPunto, FramePlot):
    # Grafica la recta tangente a la función en el punto dado.
    Derivada = sp.diff(Funcion, X)  # Calcula la derivada de la función
    FLambdified = sp.lambdify(X, Funcion, modules=["numpy"])  # Convierte la función simbólica en una función numérica
    FPrimeLambdified = sp.lambdify(X, Derivada, modules=["numpy"])  # Convierte la derivada en una función numérica
    
    Pendiente = FPrimeLambdified(XPunto)  # Evalúa la pendiente de la tangente en el punto dado
    YPunto = FLambdified(XPunto)  # Evalúa el valor de la función en el punto dado
    
    XVals = np.linspace(XPunto - 5, XPunto + 5, 400)  # Crea un rango de valores para X alrededor del punto
    RectaTangente = Pendiente * (XVals - XPunto) + YPunto  # Ecuación de la recta tangente

    Fig, Ax = plt.subplots(figsize=(10, 6))  # Crea una figura y un eje para el gráfico
    Ax.plot(XVals, FLambdified(XVals), label="Función original", color="blue")  # Grafica la función original
    Ax.plot(XVals, RectaTangente, label="Recta Tangente", color="green")  # Grafica la recta tangente
    Ax.plot(XPunto, YPunto, "r*", markersize=10, label="Punto dado")  # Marca el punto dado
    
    # Dibuja líneas de referencia en el gráfico
    Ax.axhline(0, color='black', linewidth=0.5)  # Línea horizontal en Y=0
    Ax.axvline(0, color='black', linewidth=0.5)  # Línea vertical en X=0
    Ax.grid(color='gray', linestyle='--', linewidth=0.5)  # Añade una cuadrícula al gráfico
    Ax.set_xlabel("X")  # Etiqueta del eje X
    Ax.set_ylabel("f(x)")  # Etiqueta del eje Y
    Ax.set_title("Función y su recta tangente en el punto dado")  # Título del gráfico
    Ax.legend()  # Muestra la leyenda

    # Eliminar cualquier gráfico previo del FramePlot y agregar el nuevo
    for Widget in FramePlot.winfo_children():
        Widget.destroy()  # Destruye widgets existentes en el marco del gráfico

    Canvas = FigureCanvasTkAgg(Fig, master=FramePlot)  # Crea un lienzo para el gráfico
    Canvas.draw()  # Dibuja el gráfico
    Canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Agrega el lienzo al marco de la interfaz gráfica

def EjecutarGrafico(EntryFunc, EntryX, EntryY, FramePlot, LblVerificacion):
    # Función principal para ejecutar el proceso de graficación.
    Funcion = SolicitarFuncion(EntryFunc)  # Solicita la función al usuario
    if Funcion is None:  # Verifica si la función es válida
        return
    
    XPunto, YPunto = SolicitarPunto(EntryX, EntryY)  # Solicita las coordenadas del punto
    if XPunto is None or YPunto is None:  # Verifica si las coordenadas son válidas
        return
    
    Pertenece = VerificarPunto(Funcion, XPunto, YPunto)  # Verifica si el punto pertenece a la función
    # Actualiza la etiqueta de verificación con el resultado
    if Pertenece:
        LblVerificacion.config(text="El punto pertenece a la función.", foreground="green")
    else:
        LblVerificacion.config(text="El punto no pertenece a la función.", foreground="red")

    GraficarFuncionConPunto(Funcion, XPunto, YPunto, Pertenece, FramePlot)  # Grafica la función y el punto
    
    if Pertenece:  # Si el punto pertenece a la función, grafica la recta tangente
        GraficarRectaTangente(Funcion, XPunto, FramePlot)

def Main():
    # Función principal para configurar la interfaz gráfica.
    Root = tk.Tk()  # Crea la ventana principal
    Root.title("Graficador de Funciones y Derivadas")  # Establece el título de la ventana
    Root.geometry("800x600")  # Establece el tamaño de la ventana

    FrameInput = ttk.Frame(Root, padding="10")  # Crea un marco para la entrada de datos
    FrameInput.pack(fill=tk.X, side=tk.TOP)  # Agrega el marco a la parte superior

    # Etiqueta y entrada para la función
    ttk.Label(FrameInput, text="Función (en términos de x):").grid(row=0, column=0, sticky=tk.W)
    EntryFunc = ttk.Entry(FrameInput, width=50)
    EntryFunc.grid(row=0, column=1, padx=5, pady=5)

    # Etiqueta y entrada para el valor de x del punto
    ttk.Label(FrameInput, text="Valor de x del punto:").grid(row=1, column=0, sticky=tk.W)
    EntryX = ttk.Entry(FrameInput, width=20)
    EntryX.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    # Etiqueta y entrada para el valor de y del punto
    ttk.Label(FrameInput, text="Valor de y del punto:").grid(row=2, column=0, sticky=tk.W)
    EntryY = ttk.Entry(FrameInput, width=20)
    EntryY.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    # Etiqueta para mostrar el resultado de la verificación
    LblVerificacion = ttk.Label(FrameInput, text="")
    LblVerificacion.grid(row=4, column=1, pady=10)

    # Botón para graficar
    BtnGraficar = ttk.Button(FrameInput, text="Graficar", 
                              command=lambda: EjecutarGrafico(EntryFunc, EntryX, EntryY, FramePlot, LblVerificacion))
    BtnGraficar.grid(row=3, column=1, pady=10, sticky=tk.E)

    global FramePlot  # Declara FramePlot como global para acceso en otras funciones
    FramePlot = ttk.Frame(Root)  # Crea un marco para los gráficos
    FramePlot.pack(fill=tk.BOTH, expand=True)  # Agrega el marco a la ventana

    Root.mainloop()  # Inicia el bucle principal de la interfaz gráfica

if __name__ == "__main__":
    Main()  # Ejecuta la función principal al iniciar el programa
