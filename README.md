# Bootcamp_Weather_App_Console

Aplicación de consola en Python para la gestión de estaciones meteorológicas, usuarios, alarmas, logs y estadísticas.  
Incluye persistencia en ficheros JSON, logging profesional y tests unitarios.

---

## Características principales

- Sistema de **login** con usuarios almacenados en JSON  
- Gestión de **estaciones meteorológicas**  
- Registro de **histórico de mediciones**  
- Sistema de **alarmas** configurable  
- **Logs** automáticos con `logging`  
- **Estadísticas** por estación  
- Tests unitarios con `pytest`

- ---

## Requisitos

- Python **3.10+**
- pip (gestor de paquetes)
- pytest

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/SiR0N/Bootcamp_Weather_App_Console.git
cd Bootcamp_Weather_App_Console
```
### 2. Entorno Virtual
#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```
#### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```
## Ejecutar la aplicacion

```bash
python app_consola.py
```

## Estructura del proyecto

```bash
Bootcamp_Weather_App_Console/
│
├── app_consola.py        # Punto de entrada de la aplicación
├── Log_in.py             # Gestión de usuarios y login
├── jsonDB.py             # Acceso y manipulación de ficheros JSON
├── myLogs.py             # Configuración del logger
├── Datos_manuales.py     # Datos de ejemplo / carga manual
│
├── alarmas.json          # Configuración de alarmas
├── historico.json        # Histórico de mediciones
├── stations.json         # Estaciones meteorológicas
├── usuarios.json         # Usuarios registrados
│
├── test_Log_in.py        # Tests unitarios
├── test_jsondb.py        # Tests unitarios
│
├── requirements.txt
└── README.md
