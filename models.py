# Importamos las clases y módulos necesarios de SQLAlchemy
from sqlalchemy import Column, Integer, String, Enum


# Definimos la clase User que representa el modelo de la tabla de la base de datos
class User:
    # Especificamos el nombre de la tabla en la base de datos
    __tablename__ = "users"

    # Definimos las columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    # La columna 'id' es de tipo entero, clave primaria y es un índice
    name = Column(String, index=True)
    # La columna 'name' es de tipo cadena y es un índice
    surname = Column(String, index=True)
    # La columna 'surname' es de tipo cadena y es un índice
    email = Column(String, unique=True, index=True)
    # La columna 'email' es de tipo cadena, única y es un índice
    user_level = Column(Enum("admin", "user", "guest"))
    # La columna 'user_level' es de tipo Enum con opciones "admin", "user" y "guest"
    password = Column(String)
    # La columna 'password' es de tipo cadena
