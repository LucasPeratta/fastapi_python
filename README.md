# FastAPI + MySQL Starter

Este es un proyecto de inicio para crear una aplicación web con FastAPI y MySQL en Windows.

## Requisitos Previos

- Python 3.x instalado. Puedes descargarlo desde [Python Official Website](https://www.python.org/downloads/).
- MySQL Server instalado. Puedes descargarlo desde [MySQL Community Downloads](https://dev.mysql.com/downloads/installer/).

## Configuración del Entorno

1. **Instalación de MySQL:**

   - Descarga e instala MySQL Server.
   - Configura una contraseña para el usuario root durante la instalación.

2. **Creación de la Base de Datos y Usuario en MySQL:**
   - Abre una ventana de comandos de MySQL (`mysql -u root -p`) e ingresa la contraseña.
   - Ejecuta los siguientes comandos SQL para crear la base de datos y el usuario:
     ```sql
     CREATE DATABASE python;
     CREATE USER 'tu_usuario'@'localhost' IDENTIFIED BY 'tu_contraseña';
     GRANT ALL PRIVILEGES ON python.* TO 'tu_usuario'@'localhost';
     FLUSH PRIVILEGES;
     EXIT;
     ```
3. **Instalación de Dependencias de Python:**  
   -Ejecuta el siguiente comando para instalar las dependencias necesarias dentro del entorno virtual: pip install fastapi uvicorn mysql-connector-python[mysqlclient] schedule pyjwt

4. **Inicialización de la Base de Datos:**
   -Ejecuta el siguiente comando para crear la tabla de usuarios: python main.py

5. **Ejecución de la Aplicació**
   -Finalmente, inicia el servidor FastAPI con el siguiente comando: uvicorn main:app --reload

6. **Acceso a la Aplicación:**
   -Abre tu navegador o pruebalo en Postman y visita http://localhost:8000.
