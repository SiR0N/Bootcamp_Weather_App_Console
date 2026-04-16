from datetime import datetime
from jsonDB import JsonDB

def leer_registro():

    print("=== Registro Meteorológico ===")

    # Validar fecha
    while True:
        fecha_texto = input("Introduce la fecha y hora (DD/MM/AAAA HH:MM): ")
        try:
            fecha = datetime.strptime(fecha_texto, "%d/%m/%Y %H:%M")
            break
        except ValueError:
            print("Formato incorrecto. Usa DD/MM/AAAA HH:MM")

    # -----------------------------
    # MENÚ DE ESTACIONES
    # -----------------------------
    estaciones_db = JsonDB("stations.json", default=[])
    estaciones = estaciones_db.data

    print("\n=== Estaciones disponibles ===")
    for i, est in enumerate(estaciones, start=1):
        print(f"{i}. {est['name']}")

    while True:
        try:
            op = int(input("Elige una estación: "))
            estacion = estaciones[op - 1]["name"]
            break
        except:
            print("Opción inválida. Intenta de nuevo.")

    # Validar temperatura
    while True:
        try:
            temperatura = float(input("Temperatura (°C): "))
            if -10 <= temperatura <= 42:
                break
            else:
                print("La temperatura debe estar entre -10 y 42")
        except ValueError:
            print("Introduce un número válido")

    # Validar humedad
    while True:
        try:
            humedad = float(input("Humedad (%): "))
            if 0 <= humedad <= 100:
                break
            else:
                print("La humedad debe estar entre 0 y 100")
        except ValueError:
            print("Introduce un número válido")

    # Validar viento
    while True:
        try:
            viento = float(input("Viento (km/h): "))
            break
        except ValueError:
            print("Introduce un número válido")

    registro = {
        "Fecha": fecha.strftime("%d/%m/%Y %H:%M"),
        "Estacion": estacion,
        "Temperatura (°C)": temperatura,
        "Humedad (%)": humedad,
        "Viento (km/h)": viento
    }

    # Alertas
    print("\n--- ALERTAS ---")

    temperatura_a = 0
    viento_a = 0
    humedad_a = 0

    if temperatura > 35:
        print("Alerta: Temperatura muy alta")
        temperatura_a = 1
    if temperatura < 0:
        print("Alerta: Heladas")
        temperatura_a = 2

    if viento > 70:
        print("Alerta: Viento muy fuerte")
        viento_a = 1

    if humedad > 70:
        print("Alerta: riesgo lluvia")
        humedad_a = 1 
    if humedad < 10:
        print("Alerta: riesgo sequia")
        humedad_a = 2

    # Mostrar registro
    print("\n--- Registro a procesar ---")
    for clave, valor in registro.items():
        print(f"{clave}: {valor}")
    
    alarma = None
    if temperatura_a + viento_a + humedad_a > 0:
        alarma = {
            
            "Temperatura (°C)": temperatura_a,
            "Humedad (%)": humedad_a,
            "Viento (km/h)": viento_a
        }

    return registro, alarma
