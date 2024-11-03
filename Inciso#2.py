import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox

# Configuración inicial de SymPy
X = sp.symbols('x')

def SolicitarFuncion(EntryFunc):
    Expr = EntryFunc.get()
    if Expr:
        try:
            return sp.sympify(Expr)
        except sp.SympifyError:
            messagebox.showerror("Error", "Función inválida. Inténtalo de nuevo.")
            return None
    else:
        messagebox.showerror("Error", "No se ingresó ninguna función.")
        return None

def SolicitarPunto(EntryX, EntryY):
    try:
        XPunto = float(EntryX.get())
        YPunto = float(EntryY.get())
        return XPunto, YPunto
    except ValueError:
        messagebox.showerror("Error", "Los valores de x e y deben ser numéricos.")
        return None, None

def VerificarPunto(Funcion, XValor, YValor):
    YFuncion = sp.lambdify(X, Funcion, modules=["numpy"])
    return np.isclose(YFuncion(XValor), YValor)

def GraficarFuncionConPunto(Funcion, XPunto, YPunto, Pertenece, FramePlot):
    XVals = np.linspace(-10, 10, 400)
    FLambdified = sp.lambdify(X, Funcion, modules=["numpy"])
    YVals = FLambdified(XVals)
    
    Fig, Ax = plt.subplots(figsize=(10, 6))
    Ax.plot(XVals, YVals, label="Función original", color="blue")
    Ax.plot(XPunto, YPunto, "g*" if Pertenece else "r*", markersize=10, 
            label="Punto en la función" if Pertenece else "Punto fuera de la función")
    
    Ax.axhline(0, color='black', linewidth=0.5)
    Ax.axvline(0, color='black', linewidth=0.5)
    Ax.grid(color='gray', linestyle='--', linewidth=0.5)
    Ax.set_xlabel("X")
    Ax.set_ylabel("f(x)")
    Ax.set_title("Función con el punto indicado")
    Ax.legend()

    for Widget in FramePlot.winfo_children():
        Widget.destroy()

    Canvas = FigureCanvasTkAgg(Fig, master=FramePlot)
    Canvas.draw()
    Canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def GraficarRectaTangente(Funcion, XPunto, FramePlot):
    Derivada = sp.diff(Funcion, X)
    FLambdified = sp.lambdify(X, Funcion, modules=["numpy"])
    FPrimeLambdified = sp.lambdify(X, Derivada, modules=["numpy"])
    
    Pendiente = FPrimeLambdified(XPunto)
    YPunto = FLambdified(XPunto)
    
    XVals = np.linspace(XPunto - 5, XPunto + 5, 400)
    RectaTangente = Pendiente * (XVals - XPunto) + YPunto

    Fig, Ax = plt.subplots(figsize=(10, 6))
    Ax.plot(XVals, FLambdified(XVals), label="Función original", color="blue")
    Ax.plot(XVals, RectaTangente, label="Recta Tangente", color="green")
    Ax.plot(XPunto, YPunto, "r*", markersize=10, label="Punto dado")
    
    Ax.axhline(0, color='black', linewidth=0.5)
    Ax.axvline(0, color='black', linewidth=0.5)
    Ax.grid(color='gray', linestyle='--', linewidth=0.5)
    Ax.set_xlabel("X")
    Ax.set_ylabel("f(x)")
    Ax.set_title("Función y su recta tangente en el punto dado")
    Ax.legend()

    for Widget in FramePlot.winfo_children():
        Widget.destroy()

    Canvas = FigureCanvasTkAgg(Fig, master=FramePlot)
    Canvas.draw()
    Canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def EjecutarGrafico(EntryFunc, EntryX, EntryY, FramePlot, LblVerificacion):
    Funcion = SolicitarFuncion(EntryFunc)
    if Funcion is None:
        return
    
    XPunto, YPunto = SolicitarPunto(EntryX, EntryY)
    if XPunto is None or YPunto is None:
        return
    
    Pertenece = VerificarPunto(Funcion, XPunto, YPunto)
    if Pertenece:
        LblVerificacion.config(text="El punto pertenece a la función.", foreground="green")
    else:
        LblVerificacion.config(text="El punto no pertenece a la función.", foreground="red")

    GraficarFuncionConPunto(Funcion, XPunto, YPunto, Pertenece, FramePlot)
    
    if Pertenece:
        GraficarRectaTangente(Funcion, XPunto, FramePlot)

def Main():
    Root = tk.Tk()
    Root.title("Graficador de Funciones y Derivadas")
    Root.geometry("800x600")

    FrameInput = ttk.Frame(Root, padding="10")
    FrameInput.pack(fill=tk.X, side=tk.TOP)

    ttk.Label(FrameInput, text="Función (en términos de x):").grid(row=0, column=0, sticky=tk.W)
    EntryFunc = ttk.Entry(FrameInput, width=50)
    EntryFunc.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(FrameInput, text="Valor de x del punto:").grid(row=1, column=0, sticky=tk.W)
    EntryX = ttk.Entry(FrameInput, width=20)
    EntryX.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    ttk.Label(FrameInput, text="Valor de y del punto:").grid(row=2, column=0, sticky=tk.W)
    EntryY = ttk.Entry(FrameInput, width=20)
    EntryY.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    # Etiqueta para mostrar el resultado de la verificación
    LblVerificacion = ttk.Label(FrameInput, text="")
    LblVerificacion.grid(row=4, column=1, pady=10)

    BtnGraficar = ttk.Button(FrameInput, text="Graficar", 
                              command=lambda: EjecutarGrafico(EntryFunc, EntryX, EntryY, FramePlot, LblVerificacion))
    BtnGraficar.grid(row=3, column=1, pady=10, sticky=tk.E)

    global FramePlot
    FramePlot = ttk.Frame(Root)
    FramePlot.pack(fill=tk.BOTH, expand=True)

    Root.mainloop()

if __name__ == "__main__":
    Main()
