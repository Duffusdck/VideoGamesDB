%pip install bcrypt
import bcrypt
import random
import time

def generar_id():
  tiempo = int(time.time() * 1000)
  random_number = random.randint(100, 999)
  numero = f"{tiempo}{random_number}"
  numero_acortado = numero[10:]
  return int(numero_acortado)


class Usuario:
  def __init__(self, nombre: str, email: str):
    self.id = generar_id()
    self.nombre = nombre
    self.email = email
    self.password = None

  def registrarse(self):
    print(f"Usuario {self.nombre} con correo {self.email} registrado con exito")

  def set_password(self, password:str):
    salt = bcrypt.gensalt()
    self.password = bcrypt.hashpw(password.encode('utf-8'), salt)
    print("Contraseña guardada correctamente.")
  
  def Check_password(self, password:str):
    if bcrypt.checkpw(password.encode('utf-8'), self.password):
      print("Contraseña correcta.")
    else:
      print("Contraseña incorrecta.")

  def __str__(self):
    return f"Usuario: {self.nombre}, Email: {self.email}, ID: {self.id}"

class CuentaBancaria:
  def __init__(self, numero_cuenta: int, usuario: Usuario):
    self.numero_cuenta = numero_cuenta
    self.saldo = 0.0
    self.usuario = usuario
    self.id_usuario = usuario.id
  
  def depositar(self, cantidad):
    self.saldo += cantidad

  def retirar(self, cantidad):
    if self.saldo >= cantidad:
      self.saldo -= cantidad
    else:
      print("Saldo insuficiente")

  def consultar_saldo(self):
    print(f"El saldo de la cuenta {self.numero_cuenta} es: {self.saldo}")
    return self.saldo

  def __str__(self):
    return f"Cuenta: {self.numero_cuenta}, Saldo: {self.saldo}, Usuario: {self.Usuario}"

class Banco:
  def __init__(self,nombre):
    self.nombre = nombre
    self.cuentas = []

  def abrir_cuenta(self, usuario: Usuario):
    nueva_cuenta = CuentaBancaria(generar_id(), usuario)
    self.cuentas.append(nueva_cuenta)
    print(f"Cuenta creada con exito. Numero de cuenta: {nueva_cuenta.numero_cuenta}")
    return nueva_cuenta

  def buscar_cuenta(self, numero_cuenta):
    for cuenta in self.cuentas:
      if cuenta.numero_cuenta == numero_cuenta:
        return cuenta
    print("No se encontro la cuenta")
    return None

  def realizar_transferencia(self, cuenta_origen, cuenta_destino, cantidad):
    if cuenta_origen.saldo >= cantidad:
      cuenta_origen.saldo -= cantidad
      cuenta_destino.saldo += cantidad
      print("Transferencia realizada con exito")
    else:
      print("Saldo insuficiente")

if __name__ == "__main__":
  print("--- Creando banco ---")
  banco = Banco("Banco X")
  print("--- Creando usuario ---")

  for i in range(1, 11):
    nombre_usuario = f"Usuario{i}"
    email_usuario = f"usuario{i}@email.com"

    # Crea el usuario y lo registra
    nuevo_usuario = Usuario(nombre_usuario, email_usuario)
    nuevo_usuario.registrarse()

    # Abre una cuenta para el nuevo usuario
    nueva_cuenta = banco.abrir_cuenta(nuevo_usuario)
  
   # Seccion de 3 transacciones por usuario
  print("\n--- Realizando transacciones de depósito y retiro para cada cuenta ---")
  for i, cuenta in enumerate(banco.cuentas):
    print(f"\nTransacciones para {cuenta.usuario.nombre}:")
    # Transacción 1: Depósito
    deposito1 = random.randint(50, 200)
    cuenta.depositar(deposito1)
    print(f"  - Depósito de ${deposito1}")
    
    # Transacción 2: Depósito
    deposito2 = random.randint(50, 200)
    cuenta.depositar(deposito2)
    print(f"  - Depósito de ${deposito2}")
    
    # Transacción 3: Retiro
    retiro1 = random.randint(20, 100)
    cuenta.retirar(retiro1)
    print(f"  - Retiro de ${retiro1}")
    cuenta.consultar_saldo()

  # 10 transferencias entre las cuentas
  print("\n--- Realizando 10 transferencias entre cuentas ---")
  for i in range(10):
    cuenta_origen_index = random.randint(0, 9)
    cuenta_destino_index = random.randint(0, 9)

    # Confirmacion para no transferir a la misma cuenta
    while cuenta_origen_index == cuenta_destino_index:
      cuenta_destino_index = random.randint(0, 9)

    cuenta_origen = banco.cuentas[cuenta_origen_index]
    cuenta_destino = banco.cuentas[cuenta_destino_index]
    cantidad_transferencia = random.randint(10, 50)
    
    print(f"\nTransferencia #{i+1}:")
    banco.realizar_transferencia(cuenta_origen, cuenta_destino, cantidad_transferencia)
    
  # Consultar saldos finales
  print("\n--- Saldos finales de todas las cuentas ---")
  for cuenta in banco.cuentas:
    cuenta.consultar_saldo()
