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
        raise Exception(status_code=401, detail="Token inválido o expirado")