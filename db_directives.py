import sqlite3
from sqlite3 import Error


def dbconnection():
    path = "/base.db"
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

# # sql_create_table = "CREATE TABLE cliente2 (id INTEGER PRIMARY KEY, nome VARCHAR(60) NOT NULL, cpf VARCHAR(11) NOT NULL);"

# sql_insert1 = "INSERT INTO cliente2 VALUES(1, 'teste', '12345678911');"
# sql_insert2 = "INSERT INTO cliente2 VALUES(2, 'teste', '12345678912');"
# sql_insert3 = "INSERT INTO cliente2 VALUES(3, 'teste3, '12345678917');"
# sql_insert5 = "INSERT INTO cliente2 VALUES(5, 'teste5', '12345678915');"

# sql_request = "SELECT * FROM cliente2"

# # create_table(sql_create_table)

# # insert(sql_insert1)
# # insert(sql_insert2)
# # insert(sql_insert5)
# # insert(sql_insert3)

# # update(sql_update)

# # delete_from_table(sql_delete_table)

# for s in search(sql_request):
#     print(s)



