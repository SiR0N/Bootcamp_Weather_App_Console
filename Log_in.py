import hashlib
from jsonDB import JsonDB   # importa la clase
from getpass import getpass

ARCHIVO_USUARIOS = "usuarios.json"

# Base de datos de usuarios en disco
usuarios_db = JsonDB(ARCHIVO_USUARIOS, default={})

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def registrar_interno(usuario, password):
    if usuarios_db.exists(usuario):
        return False

    usuarios_db.set(usuario, hash_password(password))
    return True

def registrar():
    print("\n=== REGISTRO ===")
    usuario = input("Usuario: ")
    password = getpass("Contraseña: ")

    resultado = registrar_interno(usuario, password)
    if resultado:
        print("Usuario registrado correctamente.")
    else:
        print("Ese usuario ya existe.")
    return resultado

def login_interno(usuario, password):
    if not usuarios_db.exists(usuario):
        return False

    return usuarios_db.get(usuario) == hash_password(password)
    
def login():
    print("\n=== LOGIN ===")
    usuario = input("Usuario: ")
    password = getpass("Contraseña: ")

    resultado = login_interno(usuario,password)
    if resultado:
        print("Login exitoso 🎉")
    else:
        print("Usuario o contraseña incorrectos.")
    return resultado

def menu():
    while True:
        print("\n1. Registrar")
        print("2. Login")
        print("3. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            registrar()
        elif opcion == "2":
            if login():
                return True
        elif opcion == "3":
            print("¡Hasta pronto! 👋")
            return False
        else:
            print("Opción inválida")

if __name__ =="__main__":
    menu()
