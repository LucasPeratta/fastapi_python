from fastapi import Depends, FastAPI, HTTPException, Request
import jwt
import mysql.connector
from db_config import db_config, get_db, init_db
from auth import create_jwt_token, verify_jwt_token
from fastapi import Depends
import schedule
import time
import threading




app = FastAPI()

init_db()

contador=0

@app.post('/login')
def login(user: dict, db=Depends(get_db)):
    connection, cursor = db

    cursor.execute("SELECT * FROM users WHERE email = %s", (user['email'],))
    user_data = cursor.fetchone()
    print(user_data)
    if user_data is not None:
        password= user_data[5]
        user_level=user_data[4]
        email= user_data[3]
        if user['password'] == password:
            token = create_jwt_token({"sub": email, "user_level": user_level})
            return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Credenciales incorrectas")

from fastapi import Query

@app.get('/users')
def list_users(
    request: Request,
    name: str = Query(None, description="Filtrar por nombre de usuario"),
    email: str = Query(None, description="Filtrar por dirección de correo electrónico"),
    page: int = Query(1, description="Número de página", gt=0),
    page_size: int = Query(10, description="Tamaño de la página", gt=0, le=100)
):
    global contador
    contador = contador + 1
    try:
        token = request.headers.get('Authorization').split(" ")[1]

        payload = verify_jwt_token(token)

        # Calcular el índice de inicio y fin para la paginación
        start_index = (page - 1) * page_size

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE 1=1"
        params = {}

        if name:
            query += " AND name = %(name)s"
            params["name"] = name

        if email:
            query += " AND email = %(email)s"
            params["email"] = email

        query += " LIMIT %(start_index)s, %(page_size)s"
        params["start_index"] = start_index
        params["page_size"] = page_size

        cursor.execute(query, params)
        users = cursor.fetchall()
        connection.close()
        return users
    except jwt.PyJWTError as e:
        return {"error": "Token JWT inválido: " + str(e)}


@app.post('/users')
def create_user(user: dict, request: Request):
    global contador
    contador = contador + 1
    try:
        token = request.headers.get('Authorization').split(" ")[1]  

        # Verifica el token JWT
        payload = verify_jwt_token(token)

           # Agrega una declaración de impresión para verificar el contenido del objeto 'user'
        print("User:", user)

    except Exception as e:
        print("Error al validar JWT", e)
        return {"error": "Token JWT inválido: " + str(e)}
      
    try:    
        if payload.get("user_level") != "admin":
            raise HTTPException(status_code=403, detail="No tiene permisos para crear usuarios.")
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        insert_query = "INSERT INTO users (name, surname, email, user_level, password) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (user['name'], user['surname'], user['email'], user['user_level'], user['password']))
        connection.commit()
        connection.close()
        return user   
    except Exception as e:
        print("Error general:", e)
        return {"error": f"Error al crear usuario: {str(e)}"}
    

@app.get('/contador')
def get_contador(request: Request):
    try:
        token = request.headers.get('Authorization').split(" ")[1]       
        payload = verify_jwt_token(token)
        return {"contador": contador}
    except jwt.PyJWTError as e:
        return {"error": "Token JWT inválido: " + str(e)}
    
print_lock = threading.Lock()
    
def incrementar_contador():
    global contador
    contador += 1
    with print_lock:
        print(f"Valor actual del contador: {contador}")



schedule.every(5).minutes.do(incrementar_contador)

def programar_tareas():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Iniciar el hilo para programar tareas
tarea_thread = threading.Thread(target=programar_tareas)
tarea_thread.start()


if __name__ == '__main__':
    import uvicorn
    # Resto del código
    uvicorn.run(app, host='0.0.0.0', port=8000)