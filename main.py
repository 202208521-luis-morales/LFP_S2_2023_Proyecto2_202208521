import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog

from AFDAnalizer import ADFAnalizer

texto_prueba_1 = """
Claves = ["codigo", "producto", "precio_compra", "precio_venta", "stock"]

Registros = [
  {1, "Barbacoa", 10.50, 20.00, 6}
  {2, "Salsa", 13.00, 16.00, 7}
  {3, "Mayonesa", 15.00, 18.00, 8}
  {4, "Mostaza", 14.00, 16.00, 4}
]

# Comentarios

'''
comentario multilinea
'''

imprimir("1. Reporte de");
imprimir("Abarroteria");

imprimirln("2. Reporte de");
imprimirln("Abarroteria");

conteo();

promedio("stock");

contarsi("stock", 0);

datos();

sumar("stock");

max("campo");

min("campo");

exportarReporte("titulo");
"""

class ViewMethod:
  def __init__(self) -> None:
    self.ventana = tk.Tk()
    self.ventana.title("Proyecto 2 - 202208521")

    self.titulo = tk.Label(self.ventana, text="Proyecto 2 - 202208521", padx=10)
    self.boton1 = tk.Button(self.ventana, text="Abrir", command=self.boton1_clicado)
    self.boton2 = tk.Button(self.ventana, text="Analizar", command=self.boton2_clicado)
    self.boton3 = tk.Button(self.ventana, text="Reportes", command=self.boton3_clicado)

    self.titulo.grid(row=0, column=0, columnspan=2)
    self.boton1.grid(row=0, column=3)
    self.boton2.grid(row=0, column=4)
    self.boton3.grid(row=0, column=5)

    self.texto_editable = scrolledtext.ScrolledText(self.ventana, wrap=tk.WORD, width=50, height=30)
    self.texto_editable.grid(row=1, column=0, columnspan=3)

    self.texto_no_editable = scrolledtext.ScrolledText(self.ventana, wrap=tk.WORD, width=60, height=30, bg='black', fg='white')
    self.texto_no_editable.config(state='disabled')
    self.texto_no_editable.grid(row=1, column=3, columnspan=3)
  
  def exec(self):
    self.ventana.mainloop()

  def boton1_clicado(self):
    archivo = filedialog.askopenfilename(filetypes=[("Archivos .bizdata", "*.bizdata")])
    if archivo:
      with open(archivo, "r") as file:
        contenido = file.read()
        self.texto_editable.delete(1.0, tk.END)
        self.texto_editable.insert(tk.END, contenido)

  def boton2_clicado(self):
    [self.prompt_text(txt) for txt in ADFAnalizer(self.get_edible_text() + "\n").analize()]
    self.prompt_text(">>> EJECUCIÓN FINALIZADA\n\n")

  def boton3_clicado(self):
    print("Botón 3 clicado!")

  def prompt_text(self, text_to_prompt):
    self.texto_no_editable.config(state=tk.NORMAL)
    self.texto_no_editable.insert(tk.END, text_to_prompt)
    self.texto_no_editable.config(state=tk.DISABLED)

  def get_edible_text(self):
    return self.texto_editable.get("1.0", "end-1c")

if __name__ == '__main__':
  ViewMethod().exec()
      
"""
texto_prueba_2 = 
Claves = ["codigo", "producto", "precio_compra", "precio_venta", "stock"]

Registros = [
  {1, "Barbacoa", 10.50, 20.00, 6}
  {2, "Salsa", 13.00, 16.00, 7}
  {3, "Mayonesa", 15.00, 18.00, 8}
  {4, "Mostaza", 14.00, 16.00, 4}
]

# Comentarios

'''
comentario multilinea
'''

conteo();

contarsi("stock", 0);

datos();

exportarReporte("titulo");

imprimir("1. Reporte de");
imprimir("Abarroteria");

imprimirln("2. Reporte de");
imprimirln("Abarroteria");

max("campo");
min("campo");

promedio("stock");

sumar("stock");
"""