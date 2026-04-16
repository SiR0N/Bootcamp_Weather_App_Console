from Log_in import menu
from Datos_manuales import leer_registro
from jsonDB import JsonDB
from myLogs import logger

def descripcion_alerta(codigo, tipo):
    if tipo == "temperatura":
        if codigo == 1:
            return "Temperatura muy alta"
        if codigo == 2:
            return "Heladas"
        return "Sin alerta"

    if tipo == "humedad":
        if codigo == 1:
            return "Riesgo de lluvia"
        if codigo == 2:
            return "Riesgo de sequía"
        return "Sin alerta"

    if tipo == "viento":
        if codigo == 1:
            return "Viento muy fuerte"
        return "Sin alerta"

def mostrar_alarma(alarma):
    print(f"\nAlarma ID: {alarma['id']}")
    print(f"  - Temperatura: {descripcion_alerta(alarma['Temperatura (°C)'], 'temperatura')}")
    print(f"  - Humedad: {descripcion_alerta(alarma['Humedad (%)'], 'humedad')}")
    print(f"  - Viento: {descripcion_alerta(alarma['Viento (km/h)'], 'viento')}")
    print(f"  - Registro histórico asociado: {alarma['historico_id']}")

def estadisticas_estacion(registros):
    if not registros:
        return None

    temps = [r["Temperatura (°C)"] for r in registros]
    hums = [r["Humedad (%)"] for r in registros]
    vnts = [r["Viento (km/h)"] for r in registros]

    return {
        "temp_media": sum(temps) / len(temps),
        "temp_max": max(temps),
        "temp_min": min(temps),

        "hum_media": sum(hums) / len(hums),
        "hum_max": max(hums),
        "hum_min": min(hums),

        "vnt_media": sum(vnts) / len(vnts),
        "vnt_max": max(vnts),
        "vnt_min": min(vnts),
    }


def main():
    
    logger.info("Aplicación iniciada")

    resultado_login = menu()
    if resultado_login == True:
        logger.info("Login correcto")

        # Cargar histórico usando la nueva clase
        historico_db = JsonDB("historico.json", default=[])

        estaciones_db = JsonDB("stations.json", default=[])
        
        alarmas_db = JsonDB("alarmas.json", default=[])


        while True:

            # Mostrar últimos 5 registros
            print("\n=== Últimos 5 registros ===")

            ultimos = historico_db.data[-5:]
            if not ultimos:
                print("No hay registros todavía.")
            else:
                for r in ultimos:
                    print(f"ID {r.get('id', '?')} | {r['Fecha']} | {r['Estacion']} | "
                        f"T={r['Temperatura (°C)']}°C | H={r['Humedad (%)']}% | V={r['Viento (km/h)']} km/h")

            print("\n1. Añadir nuevo registro de datos")
            print("2. Mostrar los datos")
            print("3. Mostrar alarmas")
            print("4. Estadísticas por estación")
            print("5. Salir")

            opcion = input("Elige una opción: ")

            if opcion == "1":
                # leer_registro devuelve un diccionario
                registro, alarma = leer_registro()

                # Añadir al JSON
                id = historico_db.append(registro)

                
                

                if alarma != None:
                    alarma["historico_id"] = id

                    # Guardar la alarma en su JSON
                    alarma_id = alarmas_db.append(alarma)

                    print(f"⚠️ Alarma generada con ID {alarma_id} para el registro {id}")
                    logger.warning(f"Alarma {alarma_id} generada para registro {id}: {alarma}")

            elif opcion == "2":
        
                estaciones = estaciones_db.data

                print("\n=== Estaciones disponibles ===")
                for i, est in enumerate(estaciones, start=1):
                    print(f"{i}. {est['name']}")

                try:
                    op = int(input("Elige una opción: "))
                    estacion_seleccionada = estaciones[op - 1]["name"]
                    logger.info(f"Estación seleccionada: {estacion_seleccionada}")
                except Exception as e:
                    logger.warning(f"Opción inválida al seleccionar estación: {e}")
                    print("Opción inválida.")
                    continue

                # Filtrar registros del histórico
                filtrados = [
                    r for r in historico_db.data
                    if r.get("Estacion") == estacion_seleccionada
                ]

                if filtrados:
                    print(f"\n=== Registros para {estacion_seleccionada} ===")
                    for r in filtrados:
                        print(r)
                    logger.info(f"{len(filtrados)} registros mostrados para {estacion_seleccionada}")
                else:
                    print("No hay registros para esa estación.")
                    logger.info(f"No hay registros para {estacion_seleccionada}")

            elif opcion == "3":
                # Mostrar últimas 5 alarmas
                print("\n=== Últimas 5 alarmas ===")

                ultimas = alarmas_db.data[-5:]  # últimas 5
                for a in ultimas:
                    mostrar_alarma(a)

                # Menú de estaciones
                estaciones = estaciones_db.data

                print("\n=== Estaciones disponibles ===")
                for i, est in enumerate(estaciones, start=1):
                    print(f"{i}. {est['name']}")

                try:
                    op = int(input("Elige una estación para ver sus alarmas: "))
                    estacion_seleccionada = estaciones[op - 1]["name"]
                    logger.info(f"Estación seleccionada para alarmas: {estacion_seleccionada}")
                except Exception as e:
                    logger.warning(f"Opción inválida al seleccionar estación: {e}")
                    print("Opción inválida.")
                    continue

                # Filtrar alarmas por estación
                alarmas_filtradas = [
                    a for a in alarmas_db.data
                    if any(
                        r.get("id") == a.get("historico_id") and
                        r.get("Estacion") == estacion_seleccionada
                        for r in historico_db.data
                    )
                ]

                if alarmas_filtradas:
                    print(f"\n=== Alarmas para {estacion_seleccionada} ===")
                    for a in alarmas_filtradas:
                        mostrar_alarma(a)
                    logger.info(f"{len(alarmas_filtradas)} alarmas mostradas para {estacion_seleccionada}")
                else:
                    print("No hay alarmas para esa estación.")
                    logger.info(f"No hay alarmas para {estacion_seleccionada}")

            elif opcion == "4":
                estaciones = estaciones_db.data

                print("\n=== Estaciones disponibles ===")
                for i, est in enumerate(estaciones, start=1):
                    print(f"{i}. {est['name']}")

                try:
                    op = int(input("Elige una estación: "))
                    estacion_sel = estaciones[op - 1]["name"]
                except:
                    print("Opción inválida.")
                    continue

                registros_est = [
                    r for r in historico_db.data
                    if r["Estacion"] == estacion_sel
                ]

                stats = estadisticas_estacion(registros_est)

                if stats is None:
                    print("No hay registros para esta estación.")
                else:
                    print(f"\n=== Estadísticas para {estacion_sel} ===")
                    print(f"Temperatura: media={stats['temp_media']:.1f}°C | "
                        f"max={stats['temp_max']}°C | min={stats['temp_min']}°C")
                    print(f"Humedad: media={stats['hum_media']:.1f}% | "
                        f"max={stats['hum_max']}% | min={stats['hum_min']}%")
                    print(f"Viento: media={stats['vnt_media']:.1f} km/h | "
                        f"max={stats['vnt_max']} km/h | min={stats['vnt_min']} km/h")

            elif opcion == "5":
                logger.info("Aplicación finalizada por el usuario")
                break
            else:
                logger.warning(f"Opción inválida en menú principal: {opcion}")
                print("Opción inválida.")
    else:
        logger.warning("Intento de login fallido")
        return

if __name__ == "__main__":
    main()