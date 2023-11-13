from ast import get_docstring
from fastapi import Depends, FastAPI, HTTPException, Header, Request
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base  # Importa declarative_base
from enum import Enum as PyEnum
import mysql.connector
import jwt

SECRET_KEY = "abc123"

def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # Imprime un mensaje de registro para verificar que la validación fue exitosa
        print("Token JWT válido:", payload)
        return payload
    except jwt.PyJWTError:
        # Imprime un mensaje de registro para verificar que la validación falló
        print("Error de validación del token JWT")
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


# Define la función de dependencia get_db
def get_db():
    try:
        # Aquí colocarías la lógica para conectarte a la base de datos
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "root",
            "database": "python"
        }
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        yield (connection, cursor)
    finally:
        cursor.close()
        connection.close()



app = FastAPI()

# Configura la conexión a la base de datos
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "python"
}

def create_users_table():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Verifica si la tabla 'users' ya existe
        cursor.execute("SHOW TABLES LIKE 'users'")
        result = cursor.fetchone()

        if result is None:
            # La tabla 'users' no existe, la creamos
            create_table_query = """
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                surname VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                user_level ENUM('admin', 'user', 'guest'),
                password VARCHAR(255)
            );
            """
            cursor.execute(create_table_query)

        connection.commit()
        connection.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la tabla 'users': {str(e)}")

# Llama a la función para crear la tabla 'users' al iniciar la aplicación
create_users_table()

@app.post('/login')
def login(user: dict, db=Depends(get_db)):
    connection, cursor = db

    cursor.execute("SELECT * FROM users WHERE email = %s", (user['email'],))
    user_data = cursor.fetchone()

    if user_data is not None:
        # Accede a la contraseña en el segundo elemento de la tupla
        if user['password'] == user_data[1]:
            token = create_jwt_token({"sub": user['email']})
            return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Credenciales incorrectas")

@app.get('/users')
def get_users(request: Request):
    try:
        token = request.headers.get('Authorization').split(" ")[1]  # Obtener el token del encabezado

        # Verifica el token JWT
        payload = verify_jwt_token(token)

        # Si la verificación es exitosa, obtiene los usuarios.
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        connection.close()
        return users
    except jwt.PyJWTError as e:
        return {" Token JWT inválido: " + str(e)}
 

    
from fastapi import Depends, Security


@app.post('/users')
def create_user(user: dict, request: Request):
    try:
        token = request.headers.get('Authorization').split(" ")[1]  # Obtener el token del encabezado
        print("Token obtenido:", token)  # Impresión para verificar el token

        # Verifica el token JWT
        payload = verify_jwt_token(token)
        print("Token JWT verificado:", payload)  # Impresión para verificar el payload del token

           # Agrega una declaración de impresión para verificar el contenido del objeto 'user'
        print("User:", user)

        # # Verifica si el usuario tiene el nivel de acceso adecuado (por ejemplo, "admin")
        # if payload.get("user_level") != "admin":
        #     raise HTTPException(status_code=403, detail="No tiene permisos para crear usuarios.")

        # Establece la conexión a la base de datos y crea el usuario
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        insert_query = "INSERT INTO users (name, surname, email, user_level, password) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (user['name'], user['surname'], user['email'], user['user_level'], user['password']))
        connection.commit()
        connection.close()
        return user
    except jwt.PyJWTError as e:
        print("Error en PyJWT:", e)
        return {"error": "Token JWT inválido: " + str(e)}
    except HTTPException as e:
        print("Error en HTTPException:", e.detail)
        return {"error": str(e)}
    except Exception as e:
        print("Error general:", e)
        return {"error": f"Error al crear usuario: {str(e)}"}


# Define Base usando declarative_base
Base = declarative_base()

# Define la clase User como subclase de Base
class User(Base):
    # Especificamos el nombre de la tabla en la base de datos
    __tablename__ = "users"

    # Definimos las columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    user_level = Column(Enum("admin", "user", "guest"))
    password = Column(String)


def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # Imprime un mensaje de registro para verificar que la validación fue exitosa
        print("Token JWT válido:", payload)
        return payload
    except jwt.PyJWTError:
        # Imprime un mensaje de registro para verificar que la validación falló
        print("Error de validación del token JWT")
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)