# Proyecto CRUD con Flask y MySQL

## Descripción
Aplicación web en Flask que realiza operaciones CRUD conectándose a una base de datos MySQL. La configuración de la conexión está en `config.py`.

---

## Cómo usar este proyecto

### 1. Clonar el repositorio

```
cmd
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
```

### 2. Crear y activar entorno virtual (recomendado)
```
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```pip install -r requirements.txt```
### 4. Configurar conexión a la base de datos
```
DB_USER = "tu_usuario"
DB_PASSWORD = "tu_contraseña"
DB_HOST = "localhost"
DB_NAME = "tu_basededatos"
```
### 5. Asegúrate que el servidor MySQL esté corriendo (MAMP o similar).

### 6. Ejecutar la app Flask
``` flask run ```
