from utilities import borrarPantalla, gotoxy
import time
from datetime import datetime

class Menu:
  def __init__(self,titulo="",opciones=[],col=6,fil=1):
    self.titulo=titulo
    self.opciones=opciones
    self.col=col
    self.fil=fil
      
  def menu(self):
    gotoxy(self.col,self.fil);print(self.titulo)
    self.col-=5

    for opcion in self.opciones:
      self.fil +=1 
      gotoxy(self.col,self.fil);print(opcion)
    gotoxy(self.col+5,self.fil+2)
    opc = input(f"- Ingrese una opcion [1 ... {len(self.opciones)}]: ") 
    return opc   

class Valida:
  def imprimir_error(self, mensaje):
    print(mensaje)
    time.sleep(2)
  
  def solo_numeros(self,mensaje, mensajeError):
    while True:
      try:
        consulta = input(mensaje)
        consulta = int(consulta)
        if consulta > 0:
          break
        else:
          self.imprimir_error(mensajeError)
          continue
      except:
        self.imprimir_error(mensajeError)
    return consulta

  def solo_decimales(self,mensaje,mensajeError):
    while True:
      consulta = str(input(mensaje))
      try: 
        consulta = float(consulta)
        if consulta > float(0):
          break
        else:
          self.imprimir_error(mensajeError)
          continue
      except:
        self.imprimir_error(mensajeError)
    return consulta
  
  def solo_fecha(self, mensaje, mensajeError):
    while True:
      consulta = input(mensaje)
      try:
        if len(consulta) == 10 and consulta[4] == consulta[7] == '-' and consulta[:4].isdigit() and consulta[5:7].isdigit() and consulta[8:].isdigit():
          datetime.strptime(consulta, '%Y-%m-%d')
          break
        else:
          self.imprimir_error(mensajeError)
          continue
      except:
        self.imprimir_error(mensajeError)
    return consulta
      
  def cedula(self, mensaje):
    mensajeError = 'El DNI debe tener al menos 10 dígitos'
    while True:
      consulta = str(input(mensaje))
      try:
        if len(consulta) >= 10:
          break
        else:
          self.imprimir_error(mensajeError)
          continue
      except:
        self.imprimir_error(mensajeError)
    return consulta
  
if __name__ == '__main__':
  # instanciar el menu
  opciones_menu = ["1. Entero", "2. Letra", "3. Decimal"]
  menu = Menu(titulo="-- Mi Menú --", opciones=opciones_menu, col=10, fil=5)
  # llamada al menu
  opcion_elegida = menu.menu()
  print("Opción escogida:", opcion_elegida)
  valida = Valida()
  if(opciones_menu==1):
    numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
    print("Número validado:", numero_validado)
  
  numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
  print("Número validado:", numero_validado)
  
  letra_validada = valida.solo_letras("Ingrese una letra:", "Mensaje de error")
  print("Letra validada:", letra_validada)
  
  decimal_validado = valida.solo_decimales("Ingrese un decimal:", "Mensaje de error")
  print("Decimal validado:", decimal_validado)