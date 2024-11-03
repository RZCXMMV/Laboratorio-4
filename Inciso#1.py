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

def SolicitarDerivadas(EntryDerivadas):
    Veces = EntryDerivadas.get()
    try:
        Veces = int(Veces)
        if Veces >= 1:
            return Veces
        else:
            messagebox.showerror("Error", "Introduce un número entero positivo.")
            return None
    except ValueError:
        messagebox.showerror("Error", "Entrada inválida. Inténtalo de nuevo.")
        return None

def DerivarFuncion(Funcion, Veces):
    Derivada = Funcion
    Derivadas = []
    for i in range(Veces):
        Derivada = sp.diff(Derivada, X)
        Derivadas.append(Derivada)
        
        # Validación: Si la derivada es constante, no puede derivarse más veces
        if Derivada.is_constant():
            messagebox.showwarning("Advertencia", f"No se puede derivar {Veces} veces. Se obtuvieron {i} derivadas.")
            break
    return Derivadas

def GraficarFunciones(Funcion, Derivadas, FramePlot):
    XVals = np.linspace(-10, 10, 400)
    FLambdified = sp.lambdify(X, Funcion, modules=["numpy"])
    YVals = FLambdified(XVals)
    
    Fig, Ax = plt.subplots(figsize=(10, 6))
    Ax.plot(XVals, YVals, label=f"Función original: {sp.pretty(Funcion)}", color="blue")
    
    Colores = ["red", "green", "purple", "orange"]
    for i, Deriv in enumerate(Derivadas):
        FDerivLambdified = sp.lambdify(X, Deriv, modules=["numpy"])
        try:
            YDerivVals = FDerivLambdified(XVals)
        except TypeError:
            YDerivVals = np.full_like(XVals, float(Deriv))
        
        Ax.plot(XVals, YDerivVals, label=f"{i+1}ª derivada: {sp.pretty(Deriv)}", color=Colores[i % len(Colores)])
    
    Ax.axhline(0, color='black', linewidth=0.5)
    Ax.axvline(0, color='black', linewidth=0.5)
    Ax.grid(color='gray', linestyle='--', linewidth=0.5)
    Ax.set_xlabel("X")
    Ax.set_ylabel("Y")
    Ax.set_title("Función original y sus derivadas")
    Ax.legend()

    # Eliminar cualquier gráfico previo del FramePlot y agregar el nuevo
    for Widget in FramePlot.winfo_children():
        Widget.destroy()

    Canvas = FigureCanvasTkAgg(Fig, master=FramePlot)
    Canvas.draw()
    Canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def EjecutarGrafico(EntryFunc, EntryDerivadas, FramePlot):
    Funcion = SolicitarFuncion(EntryFunc)
    if Funcion is None:
        return
    
    NumDerivadas = SolicitarDerivadas(EntryDerivadas)
    if NumDerivadas is None:
        return
    
    Derivadas = DerivarFuncion(Funcion, NumDerivadas)
    GraficarFunciones(Funcion, Derivadas, FramePlot)

def Main():
    Root = tk.Tk()
    Root.title("Graficador de Funciones y Derivadas")
    Root.geometry("800x600")

    Style = ttk.Style(Root)
    Style.theme_use("clam")

    FrameInput = ttk.Frame(Root, padding="10")
    FrameInput.pack(fill=tk.X, side=tk.TOP)

    ttk.Label(FrameInput, text="Función (en términos de x):").grid(row=0, column=0, sticky=tk.W)
    EntryFunc = ttk.Entry(FrameInput, width=50)
    EntryFunc.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(FrameInput, text="Número de derivadas:").grid(row=1, column=0, sticky=tk.W)
    EntryDerivadas = ttk.Entry(FrameInput, width=50)
    EntryDerivadas.grid(row=1, column=1, padx=5, pady=5)

    # Botón para graficar la función
    BtnGraficar = ttk.Button(FrameInput, text="Graficar", command=lambda: EjecutarGrafico(EntryFunc, EntryDerivadas, FramePlot))
    BtnGraficar.grid(row=2, column=1, pady=10)

    global FramePlot
    FramePlot = ttk.Frame(Root)
    FramePlot.pack(fill=tk.BOTH, expand=True)

    Root.mainloop()

if __name__ == "__main__":
    Main()
