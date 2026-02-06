import sqlite3

CREATE_BEANS_TABLE = "CREATE TABLE IF NOT EXISTS beans (ID INTEGER PRIMARY KEY, Name TEXT, Method TEXT, Rating INTEGER);"

INSERT_BEAN = "INSERT INTO beans (name, method, rating) VALUES (?, ?, ?);"
GET_BEANS_BY_NAME = "SELECT * FROM beans WHERE name = ?;"
GET_ALL_BEANS = "SELECT * FROM beans;"
GET_BEANS_BY_RATING = "SELECT * FROM beans WHERE rating BETWEEN ? and ?;"
GET_BEST_PREPARATION_FOR_BEAN = """
SELECT * FROM beans
WHERE name = ?
ORDER BY rating DESC
LIMIT 1;"""
DELETE_BEAN = "DELETE FROM beans WHERE name = ? and ID = ?;"

def connect():
    return sqlite3.connect("data.db")

def create_tables(connection):
    with connection:
        connection.execute(CREATE_BEANS_TABLE)

def add_bean(connection, name, method, rating):
    with connection:
        connection.execute(INSERT_BEAN, (name, method, rating))

def get_beans_by_name(connection, name):
    with connection:
        return connection.execute(GET_BEANS_BY_NAME, (name,)).fetchall()

def get_all_beans(connection):
    with connection:
        return connection.execute(GET_ALL_BEANS).fetchall()

def get_beans_by_rating(connection, min_rating, max_rating):
    with connection:
        return connection.execute(GET_BEANS_BY_RATING , (min_rating, max_rating,)).fetchall()

def get_best_preparation_for_bean(connection, name):
    with connection:
        return connection.execute(GET_BEST_PREPARATION_FOR_BEAN, (name,)).fetchone()

def delete_bean(connection, name, bean_id):
    with connection:
        connection.execute(DELETE_BEAN, (name, bean_id))