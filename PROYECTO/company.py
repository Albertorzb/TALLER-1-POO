from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color

class Company:
  next = 0  # Variable de clase(estatica) para almacenar el próximo ID disponible
  # meetodo constructor que s eejecuta cuando se instancia la clase
  def __init__(self, name="SuperMaxi", ruc="0943213456001"):
    # Incrementa el contador de ID para cada nueva instancia
    Company.next += 1
    # variables de instancias
    self.__id = Company.next  # Asigna el ID único a la instancia actual privada
    self.business_name = name  # Asigna el nombre de la empresa a la instancia actual
    self.ruc = ruc  # Asigna el RUC de la empresa a la instancia actual
        
  # metodo de usuario que muestra la información de la empresa (ID, nombre y RUC)
  def show(self):
    print(f"ID: {self.__id} EMPRESA: {self.business_name} RUC: {self.ruc}")
      
  def getJson(self):
    return {"ID": self.__id, "RAZONSOCIAL": self.business_name, "RUC": self.ruc}
  
  @staticmethod
  def get_business_name():
    return f"{purple_color}EMPRESA: {cyan_color}Corporación El DORADO {red_color}| {purple_color}RUC: {cyan_color}0876543294001"
        
if __name__ == '__main__':
    # Se ejecuta solo si este script es el principal
    print("***********************************************************")
    # Crea dos instancias(objetos) de la clase Company con nombres diferentes
    comp1 = Company("SuperMaxi")
    comp2 = Company(ruc="9999999999001")
    # Muestra la información de la primera empresa
    comp1.show()
    print("-----------------------------------------------------------")
    # Muestra la información de la segunda empresa
    comp2.show()
    print("-----------------------------------------------------------")
    # print(comp2.__id)
    print(Company.next)
    print(comp1.getJson())
    print(comp2.getJson())
    compa = (comp1, comp2)
    for comp in compa: print(comp.getJson())
    
