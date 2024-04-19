from psycopg2 import connect

settings = {
    'host': 'localhost',
    'database': 'Warsztaty2',
    'user': 'postgres',
    'password': 'coderslab',
    'port': '5432'
}


def connect_to_db():
    connection = connect(**settings)
    return connection