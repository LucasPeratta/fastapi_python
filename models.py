from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base  # Importa declarative_base
from enum import Enum as PyEnum

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
