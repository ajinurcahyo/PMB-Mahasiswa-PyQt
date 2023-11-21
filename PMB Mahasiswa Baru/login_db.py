import sqlite3
def createDatabaseLogin():
    try:
        sqliteConnection = sqlite3.connect('login.db')
        cursor = sqliteConnection.cursor()
        sqlite_create_table_query = '''CREATE TABLE TB_login ( passwd INTEGER PRIMARY KEY UNIQUE, user TEXT NOT NULL, email TEXT NOT NULL);'''

        print("Successfully Connected to SQLite")

        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")
        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite conection is close")

def insertDatatoDB(*data):
    try:
        sqliteConnection = sqlite3.connect('login.db')
        cursor = sqliteConnection.cursor()

        print("Successfully Connected to SQLite")
        cursor.execute("""INSERT INTO TB_login 
                                (passwd, user, email) 
                                VALUES 
                                (?,?,?)""", 
                                (int(data[0]),data[1],data[2]))

        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDB_developers table", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def viewDataFromDB():
    try:
        sqliteConnection = sqlite3.connect('login.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        count = cursor.execute(""" SELECT * FROM TB_login """)
        rows = count.fetchall()

        print("Get data success ", rows)
        cursor.close()
        return rows

    except sqlite3.Error as error:
        print("Failed to get data into sqlite table", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def deleteDataFromDB(passwd):
    try:
        sqliteConnection = sqlite3.connect('login.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite") 

        cursor.execute("DELETE FROM TB_login WHERE passwd={}".format(passwd))
        
        sqliteConnection.commit()
        print("Record delete successfully from SqliteDB_developers table", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")