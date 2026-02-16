import sqlite3

GET_NOODLES_BY_NAME = "SELECT * FROM noodles WHERE name = ?;"
GET_ALL_NOODLES = "SELECT * FROM noodles;"
GET_NOODLES_BY_RATING = "SELECT * FROM noodles WHERE rating BETWEEN ? and ?;"
GET_BEST_PREPARATION_FOR_NOODLE = """
SELECT * FROM noodles
WHERE name = ?
ORDER BY rating DESC
LIMIT 1;"""
DELETE_NOODLE = "DELETE FROM noodles WHERE name = ? and ID = ?;"

def get_noodles_by_name(connection, name):
    with connection:
        return connection.execute(GET_NOODLES_BY_NAME, (name,)).fetchall()

def get_all_noodles(connection):
    with connection:
        return connection.execute(GET_ALL_NOODLES).fetchall()

def get_noodles_by_rating(connection, min_rating, max_rating):
    with connection:
        return connection.execute(GET_NOODLES_BY_RATING, (min_rating, max_rating,)).fetchall()

def get_best_preparation_for_noodle(connection, name):
    with connection:
        return connection.execute(GET_BEST_PREPARATION_FOR_NOODLE, (name,)).fetchone()

def delete_noodle(connection, name, noodle_id):
    with connection:
        connection.execute(DELETE_NOODLE, (name, noodle_id))