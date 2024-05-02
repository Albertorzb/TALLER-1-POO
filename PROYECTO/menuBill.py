from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient
from sales import Sale
from product  import Product
from iCrud import ICrud
from datetime import datetime
import time,os
from functools import reduce
validar = Valida()
path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
  def create(self):
    borrarPantalla()
    while True:
      print('AGREGAR CLIENTES')
      new_client_data = {}
      json_file = JsonFile(path+'/archivos/clients.json')
      clients_data = json_file.read()
      dni = validar.cedula("Ingrese DNI del cliente: ")
      client = json_file.find("dni",dni)
      if client:
        print("El DNI ya existe");time.sleep(2)
        borrarPantalla()
        continue
      new_client_data['dni'] = dni
      new_client_data['nombre'] = input("Ingrese nombre del cliente: ").strip()
      new_client_data['apellido'] = input("Ingrese el apellido del cliente: ")
      new_client_data['valor'] = validar.solo_decimales("Ingrese el valor del cliente: ", "ERROR​")
      option = input('Guardar cambios (s/n)')
      if option.lower() == 's':
        clients_data.append(new_client_data)
        json_file.save(clients_data)
        print('Cliente agregado con éxito.')
        borrarPantalla()
        break
      elif option.lower() == 'n':
        borrarPantalla()
        break
  borrarPantalla()

  def consult(self):
    while True:
      borrarPantalla()
      print('INFORMACION DE CLIENTES')
      dni = input('Ingrese DNI del cliente: ')
      json_file = JsonFile(path+'/archivos/clients.json')
      cli_data = json_file.read()
      found_client = None
      for client in cli_data:
        if client['dni'] == dni:
          found_client = client
          break
      if found_client:
        print(f"Nombre: {found_client['nombre']}")
        print(f"Apellido: {found_client['apellido']}")
        print(f"Valor: {found_client['valor']}")
        option=input(f"Ingrese 's' para volver a consultar / Presione 'n' para salir ")
        if option == "s":
          borrarPantalla()
          continue
        else:
          borrarPantalla()
        break
      else:
        print("Sin busqueda. Inténtelo nuevamente.");time.sleep(2)
        borrarPantalla()
      break
  borrarPantalla()

  def delete(self):
    while True:
      borrarPantalla()
      print('ELIMINAR CLIENTE')
      delete_client = input('Ingrese DNI: ')
      json_file = JsonFile(path+'/archivos/clients.json')
      clients_data = json_file.read()
      found_client = None
      for client in clients_data:
        if client['dni'] == delete_client:
          found_client = client
          break
      if found_client:
        print(f"Nombre: {found_client['nombre']}")
        print(f"Apellido: {found_client['apellido']}")
        print(f"Valor: {found_client['valor']}")
        option = input("Ingrese 's' para eliminar cliente / Ingrese 'n' para salir ") 
        if option  == "s":
          clients_data.remove(found_client)
          json_file.save(clients_data)
          print("​​​Cliente eliminado")
          time.sleep(3)
          borrarPantalla()
          break
        else:
          borrarPantalla()
        break
      else:
        print("No hay resultados de busqueda.")
        time.sleep(2)
        borrarPantalla()
      break
  borrarPantalla()

  def update(self):
    while True:
      borrarPantalla()
      print('ACTUALIZAR CLIENTE')
      dni = input(f"Ingrese DNI del cliente: ")
      json_file = JsonFile(path+'/archivos/clients.json')
      clients_data = json_file.read()
      found_client = None
      for client in clients_data:
        if client['dni'] == dni:
          found_client = client
          break
      if found_client:
        print(f"Datos actuales")
        print(f"DNI:      {found_client['dni']}")
        print(f"Nombre:   {found_client['nombre']}")
        print(f"Apellido: {found_client['apellido']}")
        option = input(f"Ingrese 's' para actualizar / Ingrese 'n' para salir ")    
        if option == "s":
          while True:
            print("Actualizar datos")
            nuevo_dni = validar.cedula("DNI:      ")
            nuevo_nombre = input("Nombre:   ")
            nuevo_apellido = input(f"Apellido: ")
            found_client['dni'] = nuevo_dni
            found_client['nombre'] = nuevo_nombre
            found_client['apellido'] = nuevo_apellido
            option_2 = input("Ingrese 's' para guardar cambios / Ingrese 'n para cancelar y salir ") 
            if option_2 == "s":
              json_file.save(clients_data)
              time.sleep(2)
              break
            else:
              break
        
        break
      else:
        print(red_color + "Sin resultados de busqueda. ")
        time.sleep(2)
        borrarPantalla()
      break
  borrarPantalla()

class CrudProducts(ICrud):
  def create(self):
    while True:
      borrarPantalla()
      print('AGREGAR PRODUCTOS')
      new_product_data = {}
      json_file = JsonFile(path+'/archivos/products.json')
      product_data = json_file.read()
      max_id = max(product_data, key=lambda x: x['id'])['id']
      new_product_data['id'] = max_id + 1
      while True:
        try:
          new_product_data['descripcion'] = input("Ingrese nombre del producto: ")
          if any(product['descripcion'] == new_product_data['descripcion'] for product in product_data):
            raise ValueError("El producto ya existe.")
          break
        except ValueError as e:
          print(f"{e}")
          time.sleep(3)
          continue
      new_product_data['precio'] = validar.solo_decimales("Ingrese precio del producto: ","El precio debe ser positivo.")
      new_product_data['stock'] = validar.solo_numeros("Ingrese stock del producto: ","El stock debe ser un número entero.")
      option = input('Guardar cambios? {s/n}')
      if option.lower() == 's':
        product_data.append(new_product_data)
        json_file.save(product_data)
        print('Producto agregado con exito.')
        time.sleep(2)
        borrarPantalla()
        break
      else:
        borrarPantalla()
        break
  borrarPantalla()
  
  def update(self):
    while True:
      borrarPantalla()
      print('ACTUALIZAR PRODUCTO')
      try:
        product_id = int(input("Ingrese ID de producto:"))
        json_file = JsonFile(path+'/archivos/products.json')
        products_data = json_file.read()
        found_product = None
        for product in products_data:
          if product['id'] == product_id:
            found_product = product
            break
      except: 
        print('Sin resultados de busqueda.​')
        time.sleep(2)
        break
      if found_product:
        print("Informacion actual:")
        print(f"Nombre: {found_product['descripcion']}")
        print(f"Precio: {found_product['precio']}")
        print(f"Stock: {found_product['stock']}")
        option = input("Ingrese 's' para actualizar datos / Ingrese 'n' para salir")    
        if option == "s":
          while True:
            print("Actualizar informacion:")
            nuevo_producto = input("Nombre:  ")
            found_product['descripcion'] = nuevo_producto
            while True:
              try: 
                nuevo_precio = float(input("Precio: "))
                if nuevo_precio <= 0:
                  raise ValueError("El precio debe ser positivo.")
                else:
                  found_product['precio'] = nuevo_precio
                nuevo_stock = int(input("Stock: "))
                if nuevo_stock <= 0:
                  raise ValueError("El stock debe ser entero.")
                else:
                  found_product['stock'] = nuevo_stock
                break
              except ValueError as e:
                print(e)
                time.sleep(2)
                continue
            confirm = input("Guardar cambios? (s/n)") 
            if confirm == "s":
              json_file.save(products_data)
              print('Datos guardados.')
              time.sleep(2)
              break
            else:
              break
        else:
          break
      else:
        print("Sin resultados.​​​")
        time.sleep(2)
        borrarPantalla()
      break
  borrarPantalla()

  def delete(self):
    while True:
      borrarPantalla()
      print('ELIMINAR PRODUCTOS')
      option = input("Ingrese 's' para eliminar un producto / Ingrese 'n' para salir ")
      if option == "s":
        try:
          id_product = int(input("Ingrese ID del producto: "))
          json_file = JsonFile(path+'/archivos/products.json')
          product_data = json_file.read()
          found_product = None
          for product in product_data:
            if product['id'] == id_product:
              found_product = product
              break
        except:
          print("Sin resultados. ")
          time.sleep(2)
          continue
        if found_product:
          print(f"Nombre: {found_product['descripcion']}")
          print(f"Precio: {found_product['precio']}")
          print(f"Stock: {found_product['stock']}")
          confirm = input("Eliminar producto? (s/n)") 
          if confirm.lower() == "s":
            product_data.remove(found_product)
            json_file.save(product_data)
            print('Producto eliminado. ')
            time.sleep(2)
            borrarPantalla()
          else:
            borrarPantalla()
            continue
          break
        else:
          print('Sin resultados. ')
          break
      else:
        break
  borrarPantalla()
  
  def consult(self):
    while True:
      borrarPantalla()
      print('CONSULTAR PRODUCTOS')
      try:
        id_producto = int(input('Ingrese ID del producto: '))
        json_file = JsonFile(path+'/archivos/products.json')
        products_data = json_file.read()
        found_product = None
        for product in products_data:
          if product['id'] == id_producto:
            found_product = product
            break
      except:
        print("Sin resultados. ");
        time.sleep(2)
        break
      if found_product:
        print(f"Nombre: {found_product['descripcion']}")
        print(f"Precio: {found_product['precio']}")
        print(f"Stock: {found_product['stock']}")
        option = input("Volver a consultar? (s/n)")
        if option == "s":
          borrarPantalla()
          continue
        else:
          borrarPantalla()
        break
      else:
        print("Sin resultados de busqueda.")
        time.sleep(2)
        borrarPantalla()
      break
  borrarPantalla()

class CrudSales(ICrud):
  def create(self):
    while True:
      print('\033c', end='')
      validar = Valida()
      gotoxy(2,1);print(blue_color+"----------------------"*4)
      gotoxy(30,3);print(purple_color+"VENTAS")
      gotoxy(17,5);print(Company.get_business_name())
      json_file = JsonFile(path+'/archivos/invoices.json')
      invoices = json_file.read()
      next_invoice_number = len(invoices) + 1
      gotoxy(5,7);print(f"{purple_color}Factura: {red_color}{next_invoice_number}")
      gotoxy(5,8);dni = input(purple_color+f"Cédula: {yellow_color}")
      json_file = JsonFile(path+'/archivos/clients.json')
      client = json_file.find("dni",dni)
      if not client:
        gotoxy(13,8);print(f"{red_color}El cliente no existe. 😡​");time.sleep(2)
        gotoxy(13,8);print(' '*25)
        continue
      gotoxy(5,9);print(f"{purple_color}Fecha: {cyan_color}{datetime.now()}")
      gotoxy(56,7);print(purple_color+"Subtotal : ")
      gotoxy(56,8);print(purple_color+"Descuento: ")
      gotoxy(76,7);print(purple_color+"Iva      : ")
      gotoxy(76,8);print(purple_color+"Total    : ")
      client = client[0]
      cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True)
      sale = Sale(cli)
      gotoxy(5,8);print(f'{purple_color}Usuario: {yellow_color}{cli.fullName()}')
      gotoxy(2,10);print(red_color+"--"*64+reset_color) 
      gotoxy(5,11);print(purple_color+"Línea"+blue_color) 
      gotoxy(12,11);print(purple_color+"ID_Artículo"+blue_color) 
      gotoxy(24,11);print(purple_color+"Descripción"+blue_color) 
      gotoxy(38,11);print(purple_color+"Precio"+blue_color) 
      gotoxy(48,11);print(purple_color+"Cantidad"+blue_color) 
      gotoxy(58,11);print(purple_color+"Subtotal"+blue_color)
      gotoxy(68,11);print(red_color +"| Finaliar Venta (n) | Continuar (ENTER) | Reingresar (z) | " +blue_color)
      loop_principal = True
      default = 1
      while loop_principal:
        line = 12 + default
        gotoxy(7,line);print(default)
        gotoxy(15,line);
        id = validar.solo_numeros('', f"{red_color}ERROR: Solo números. ")
        json_file = JsonFile(path+'/archivos/products.json')
        prods = json_file.find("id",id)
        if not prods:
          gotoxy(15,line);print("El producto no existe. 🥶​");time.sleep(2)
          gotoxy(15,line);print(' ' * 120)
          continue
        prods = prods[0]
        product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
        gotoxy(24,line);print(product.descrip)
        gotoxy(38,line);print(product.preci)
        qyt = validar.solo_numeros('',f"{red_color}ERROR: Solo números. ​{reset_color}")
        gotoxy(59,line);print(product.preci*qyt)
        gotoxy(77,line);key_pressed = input().lower()
        if key_pressed == "z": 
          gotoxy(15,line);print(' ' * 140)
          continue
        else:
          sale.add_detail(product,qyt)
          gotoxy(67,7);print(round(sale.subtotal,2))
          gotoxy(67,8);print(round(sale.discount,2))
          gotoxy(87,7);print(round(sale.iva,2))
          gotoxy(87,8);print(round(sale.total,2))
          gotoxy(76,line);print(green_color+"Well Done ✔"+blue_color) 
          default += 1
          line += 1
          if key_pressed == "n":        
            line += 1
            while True:
              gotoxy(5,line);print(cyan_color + f"| ¿Está seguro de grabar la venta? (s/n) | - Ingresar más productos: (z) |")
              gotoxy(82,line);procesar = input().lower()
              gotoxy(5,line);print(' '*120)
              if procesar == "s":
                gotoxy(25,line+1);print(yellow_color + "Venta realizada exitosamente. 😊");time.sleep(2)
                # print(sale.getJson())
                json_file = JsonFile(path+'/archivos/invoices.json')
                invoices = json_file.read()
                ult_invoices = invoices[-1]["factura"]+1
                data = sale.getJson()
                data["factura"]=ult_invoices
                invoices.append(data)
                json_file = JsonFile(path+'/archivos/invoices.json')
                json_file.save(invoices)
                time.sleep(3)
                loop_principal = False
                break
              elif procesar =="n":
                gotoxy(25,line);print(red_color + "🤣 Venta Cancelada 🤣")    
                time.sleep(2)
                loop_principal = False
                break
              elif procesar =="z":
                gotoxy(25,line);print(green_color + "🤑​ Ingrese Productos Nuevamente 🤑​" + blue_color);time.sleep(2)
                gotoxy(25,line);print(' ' * 120)
                break
              else:
                gotoxy(90,line);print(red_color + '😤​ ¡Ingrese una opción valida! 😤​');time.sleep(2)
                gotoxy(90,line);print(' ' * 80)
      if not loop_principal:
        break 
  borrarPantalla()

  def update(self):
    while True:
      borrarPantalla()
      print('ACTUALIZAR FACTURA')
      invoice = validar.solo_numeros("Ingrese Factura: ",'ERROR​ ​')
      json_file = JsonFile(path+'/archivos/invoices.json')
      invoices = json_file.find("factura",invoice)
      if not invoices:
        print('La factura no existe.​​')
        time.sleep(2)
        borrarPantalla()
        break
      for invoice_data in invoices:
        print(f'Número de factura: {invoice}')
        print(f"Fecha: {invoice_data['Fecha']}")
        print(f"Cliente: {invoice_data['cliente']}")
        print(f'Actualizar:')
        new_date = validar.solo_fecha('Nueva fecha (YYYY-MM-DD): ','Ingrese en el formato correcto. ')
        invoice_data['Fecha'] = new_date
        while True:
          json_file = JsonFile(path+'/archivos/clients.json')
          new_client = validar.cedula("DNI: ")
          client = json_file.find("dni",new_client)
          if client:
            invoice_data['cliente'] = f"{client[0]['nombre']} {client[0]['apellido']}"
            print(f'{cyan_color}- Cliente: {yellow_color}{invoice_data['cliente']}')
            break
          else:
            print("Usuario no encontrado")
            time.sleep(2)
            continue
      gotoxy(2, 11);print(f"{'ID Producto':<15} {'Descripcion':<15} {'Precio':<10} {'Cantidad':<10} {'Finalizar (n)  / Continuar (ENTER)'}{yellow_color}")
      line=12
      invoice_data['detalle'] = []
      while True:
        try:
          gotoxy(2,line);new_product = int(input())
          json_file = JsonFile(path+'/archivos/products.json')
          prods = json_file.find("id",new_product)
          if not prods:
            gotoxy(15,line);print("Producto no existe")
            gotoxy(15,line);print(' ' * 20)
            continue
          prods = prods[0]
          product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
          gotoxy(18,line);print(product.descrip)
          gotoxy(34,line);print(product.preci)
          new_quantity = validar.solo_numeros('',"Solo números positivos.")
          gotoxy(62,line);option_x = input()
          gotoxy(62, line);print(' '*120)
          if option_x == "n":
            if prods:
              gotoxy(76,line);print("✔") 
              invoice_data['detalle'].append({'producto': prods['descripcion'], 'precio': prods['precio'], 'cantidad': new_quantity})
              gotoxy(60, line);print('✔️')
              gotoxy(10, line + 1);option_z = input('Guardar cambios? (s/n)')
              gotoxy(10, line + 1);print(' '*120)
              if option_z.lower() == 's':
                json_file.update_invoice(invoice_data)
                json_file.replace(path + '/archivos/invoices.json', invoices)
                line += 1
                gotoxy(10, line);print('Cambios actualizados correctamente.​')
                borrarPantalla()
                break
              else:
                line += 1
                gotoxy(10, line);print('No se realizaron cambios')
                borrarPantalla()
                break
            else:
              gotoxy(2, line);print('​ERROR: No existe esa ID. Intentelo de nuevo. 🤥​');time.sleep(3)
              gotoxy(2, line);print(" "*120)
            break
          else:
            if product:
              invoice_data['detalle'].append({'producto': prods['descripcion'], 'precio': prods['precio'], 'cantidad': new_quantity})
              gotoxy(60, line);print('✔️')
              line += 1
            else:
              gotoxy(2, line);print('No existe esa ID.​');time.sleep(2)
              gotoxy(2, line);print(" "*120)
              continue
        except ValueError:
          gotoxy(12, line);print('Ingrese opciones validas..​');time.sleep(1)
          gotoxy(12, line);print(" "*80)  
      break
  borrarPantalla()
    
  def delete(self):
    while True:
      borrarPantalla()
      print('ELIMINAR FACTURAS')
      while True:
        invoice= int(input(f"Ingrese número de factura: "))
        json_file = JsonFile(path+'/archivos/invoices.json')
        invoices = json_file.find("factura",invoice)
        if not invoices:
          print('Busqueda sin éxito.​')
          time.sleep(2)
        break
      print(f"Número de Factura: {invoice}")
      for invoice_data in invoices:
        gotoxy(20,7);print(f"{purple_color}- Fecha: {blue_color}{invoice_data['Fecha']:<15}{purple_color}- Cliente: {blue_color}{invoice_data['cliente']}")
        gotoxy(15,8);print(f"{purple_color}Subtotal: {yellow_color}{invoice_data['subtotal']:<10}{purple_color}Descuento: {yellow_color}{invoice_data['descuento']:<10}{purple_color}IVA: {yellow_color}{invoice_data['iva']:<10}{purple_color}Total: {red_color}{invoice_data['total']:<10}")
        gotoxy(20,10);print(f"{purple_color}{'Productos':<15} {'Precio':<10} {'Cantidad':<10} {'Subtotal':<10}")
        line = 11
        for detail in invoice_data['detalle']:
          precio = float(detail['precio'])  
          cantidad = int(detail['cantidad']) 
          subtotal = precio * cantidad
          gotoxy(20, line); print(blue_color + f"{detail['producto']:<15} {detail['precio']:<10} {detail['cantidad']:<10} {subtotal:<10}")
          line += 1
        gotoxy(10,line+1); confirm = input("Eliminar factura? (s/n)")
        if confirm.lower() == 's':
          json_file = JsonFile(path+'/archivos/invoices.json')
          json_file.delete("factura", invoice)
          print(' '*190)
          print("Factura eliminada​")
          time.sleep(2)
          borrarPantalla()
          break
        else:
          borrarPantalla()
          continue
      break
  borrarPantalla()

  def consult(self):
    while True:
      borrarPantalla()
      print("INFORMACION DE VENTAS")
      option = input("Ingrese 'a' para buscar una factura / Ingrese 'b' para mostrar todas las facturas / Ingrese 'c' para informacion general / 'Ingrese 'd' para salir ")
      if option == "a":
        while True:
          invoice = validar.solo_numeros("Ingrese Factura: ",'Debe ingresar solo números.​')
          json_file = JsonFile(path+'/archivos/invoices.json')
          invoices = json_file.find("factura",invoice)
          if not invoices:
            print('Busqueda sin éxito.​')
            time.sleep(2)
          else:
            borrarPantalla()
            json_file.print_all_invoices(invoices)
            break
      elif option == "b":
        while True:
          json_file = JsonFile(path+'/archivos/invoices.json')
          invoices = json_file.read()
          if not invoices:
            gotoxy(10, 5);print(f"{red_color}No hay facturas disponibles.")
            input(f"{blue_color}Presione ENTER para salir. 😵​​​​")
            borrarPantalla()
            break
          else:
            borrarPantalla()
            json_file.print_all_invoices(invoices)
            break
      elif option == "c":
        borrarPantalla()
        json_file = JsonFile(path+'/archivos/invoices.json')
        invoices = json_file.read()
        gotoxy(15,5);print(f"{cyan_color}Información general de ventas: {yellow_color}")
        total_clientes = len(set([i["cliente"] for i in invoices]));
        gotoxy(10,7);print(f'{yellow_color}- Total de clientes: {green_color}{total_clientes}')
        suma = reduce(lambda total, invoice: round(total+ invoice["total"],2), invoices,0)
        gotoxy(10,9);print(f'{yellow_color}- Suma total de ventas: {green_color}{suma}')
        totales_map = list(map(lambda invoice: invoice["total"], invoices))
        max_invoice = max(totales_map)
        gotoxy(10,11);print(f'{yellow_color}- Máximo total de una factura: {green_color}{max_invoice}')
        min_invoice = min(totales_map)
        gotoxy(10,13);print(f'{yellow_color}- Mínimo total de una factura: {green_color}{min_invoice}')
        gotoxy(10,15);print(f'{yellow_color}- Lista de totales de todas las facturas:')
        line = 16
        for i in totales_map:
          gotoxy(10,line);print(green_color, i)
          line += 1
        line += 1
        gotoxy(8,line+1);input(f"{yellow_color}Presione ENTER para regresar al menú principal.​");borrarPantalla()
      else:
        break
  borrarPantalla()
      
      
#Menu Proceso Principal
opc=''
while opc !='4':  
  borrarPantalla()
  message = 'Sistema de facturas'
  menu_main = Menu(message,[f"1) Clientes​",f"2) Productos",f"3) Ventas",f"4) Sali"],20,10)
  opc = menu_main.menu()
  options = [f"1) Ingresar",f"2) Actualizar ​",f"3) Eliminar",f"4) Consultar​",f"5) Salir​"]
  if opc == "1":
    opc1 = ''
    while opc1 !='5':
      borrarPantalla()
      clients = CrudClients()
      message = 'Menu clientes'
      menu_clients = Menu(message,options,20,10)
      opc1 = menu_clients.menu()
      if opc1 == "1":
        clients.create();time.sleep(1)
      elif opc1 == "2":
        clients.update();time.sleep(1)
      elif opc1 == "3":
        clients.delete();time.sleep(1)
      elif opc1 == "4":
        clients.consult();time.sleep(1)
      print("Regresando al menu Clientes...")
      # time.sleep(2)            
  elif opc == "2":
    opc2 = ''
    while opc2 !='5':
      borrarPantalla()    
      message = 'Menu productos'
      product = CrudProducts()
      menu_products = Menu(message,options,20,10)
      opc2 = menu_products.menu()
      if opc2 == "1":
        product.create();time.sleep(1)
      elif opc2 == "2":
        product.update();time.sleep(1)
      elif opc2 == "3":
        product.delete();time.sleep(1)
      elif opc2 == "4":
        product.consult();time.sleep(1)

  elif opc == "3":
    opc3 =''
    while opc3 !='5':
      borrarPantalla()
      message = 'Menu ventas'
      sales = CrudSales()
      menu_sales = Menu(message,options,20,10)
      opc3 = menu_sales.menu()
      if opc3 == "1":
        sales.create();time.sleep(1)
      elif opc3 == "2":
        sales.update();time.sleep(1)
      elif opc3 == "3":
        sales.delete();time.sleep(1)
      elif opc3 == "4":
        sales.consult();time.sleep(1)
  print("Regresando al menu Principal...")
  # time.sleep(2)            

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()
