import database


def menu():
    connection = database.connect()
    database.create_tables(connection)