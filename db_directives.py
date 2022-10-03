import sqlite3
from sqlite3 import Error


def dbconnection():
    path = "base.db"
    connection = None

    try:
        connection = sqlite3.connect(path)
        return connection

    except Error as err:
        return err


def insert(sql_directive):
    try:
        connection = dbconnection()
        cursor = connection.cursor()
        cursor.execute(sql_directive)
        connection.commit()
        print('code: 201 - row created')
        connection.close()
    except Error as err:
        print(err)


def create_table(sql_directive):
    try:
        connection = dbconnection()
        cursor = connection.cursor()
        cursor.execute(sql_directive)
        connection.commit()
        print('code: 202 - table created')
        connection.close()
    except Error as err:
        print(err)


def update(sql_directive):
    try:
        connection = dbconnection()
        cursor = connection.cursor()
        cursor.execute(sql_directive)
        connection.commit()
        print('code: 203 - updated')
        connection.close()
    except Error as err:
        print(err)


def delete_from_table(sql_directive):
    try:
        connection = dbconnection()
        cursor = connection.cursor()
        cursor.execute(sql_directive)
        connection.commit()
        print('code: 204 - deleted')
        connection.close()
    except Error as err:
        print(err)


def search(sql_directive):
    try:
        connection = dbconnection()
        cursor = connection.cursor()
        cursor.execute(sql_directive)
        response = cursor.fetchall()
        print('code: 205 - request found')
        connection.close()
        return response
    except Error as err:
        print("no response")
        print(err)

    # sql_delete_table = "DELETE FROM cliente2 WHERE id != 4;"

# sql_update = 'UPDATE cliente2 SET nome="Rogerio" WHERE id=1;'

# RELATED TO THE DATABASE STUFF

# sql_create_table = "CREATE TABLE author (id INTEGER PRIMARY KEY, author_name VARCHAR(60));"
# sql_create_table_genre = "CREATE TABLE genre (id INTEGER PRIMARY KEY, genre_name VARCHAR(60));"
# sql_create_table_disk = "CREATE TABLE disk (id INTEGER PRIMARY KEY, author VARCHAR(60) NOT NULL, genre VARCHAR(20) NOT NULL, year INTEGER NOT NULL, FOREIGN KEY (author) REFERENCES author (author_name), FOREIGN KEY (author) REFERENCES disk (disk_name));"

# create_table(sql_create_table)
# create_table(sql_create_table_genre)
# create_table(sql_create_table_disk)

# sql_create_table = "CREATE TABLE disk (id INTEGER PRIMARY KEY, author VARCHAR(60) NOT NULL, genre VARCHAR(20) NOT NULL);"


# update(sql_update)

# # delete_from_table(sql_delete_table)

# for s in search(sql_request):
#     print(s)



