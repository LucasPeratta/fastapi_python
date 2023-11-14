import mysql.connector

# Configura la conexión a la base de datos
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "python"
}

def create_users_table():  
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    cursor.execute("SHOW TABLES LIKE 'users'")
    result = cursor.fetchone()

    if result is None:
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


def get_db():
    try:       
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        yield (connection, cursor)
    finally:
        cursor.close()
        connection.close()



def init_db():
    create_users_table()