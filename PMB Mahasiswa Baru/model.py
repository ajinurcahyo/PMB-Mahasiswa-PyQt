import sqlite3
def createDatabase():
    try:
        sqliteConnection = sqlite3.connect('pendaftaran.db')
        cursor = sqliteConnection.cursor()
        sqlite_create_table_query = '''CREATE TABLE TB_Pendaftaran ( nisn INTEGER PRIMARY KEY UNIQUE,
        nama TEXT NOT NULL, asalSekolah TEXT NOT NULL, tempatTglLahir TEXT NOT NULL, agama TEXT NOT NULL, alamat TEXT NOT NULL, nomorHp TEXT NOT NULL, prodi TEXT NOT NULL);'''

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
        sqliteConnection = sqlite3.connect('pendaftaran.db')
        cursor = sqliteConnection.cursor()

        print("Successfully Connected to SQLite")
        cursor.execute("""INSERT INTO TB_Pendaftaran 
                                (nisn, nama, asalSekolah, tempatTglLahir, agama, alamat, nomorHp, prodi) 
                                VALUES 
                                (?,?,?,?,?,?,?,?)""", 
                                (int(data[0]),data[1],data[2],data[3],data[4],data[5],data[6],data[7]))

        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDB_developers table", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def deleteDataFromDB(nisn):
    try:
        sqliteConnection = sqlite3.connect('pendaftaran.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite") 

        cursor.execute("DELETE FROM TB_Pendaftaran WHERE nisn={}".format(nisn))
        
        sqliteConnection.commit()
        print("Record delete successfully from SqliteDB_developers table", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def viewDataFromDB():
    try:
        sqliteConnection = sqlite3.connect('pendaftaran.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        count = cursor.execute(""" SELECT * FROM TB_Pendaftaran """)
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


# ================= INFO PENDAFTARAN =========================
def createDatabasePendaftaran():
    try:
        sqliteConnectionInfoPendaftaran = sqlite3.connect('pendaftaran.db')
        cursor = sqliteConnectionInfoPendaftaran.cursor()
        # print("Successfully Connected to SQLite")

        sqlite_create_table_info_pendaftaran = '''CREATE TABLE TB_InfoPendaftaran ( gelombang INTEGER PRIMARY KEY UNIQUE,
        periodeGelombang TEXT NOT NULL, fakultas TEXT NOT NULL, prodi TEXT NOT NULL, keteranganInfo TEXT NOT NULL);'''

        print("Successfully Connected to SQLite")

        cursor.execute(sqlite_create_table_info_pendaftaran)
        sqliteConnectionInfoPendaftaran.commit()
        print("SQLite table created")
        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if sqliteConnectionInfoPendaftaran:
            sqliteConnectionInfoPendaftaran.close()
            print("sqlite conection is close")

def insertDataInfoPendaftaran(*data):
    try:
        sqliteConnectionInfoPendaftaran = sqlite3.connect('pendaftaran.db')
        cursor = sqliteConnectionInfoPendaftaran.cursor()

        print("Successfully Connected to SQLite")
        cursor.execute("""INSERT INTO TB_InfoPendaftaran 
                                (gelombang, periodeGelombang, fakultas, prodi, keteranganInfo) 
                                VALUES 
                                (?,?,?,?,?)""", 
                                (int(data[0]),data[1],data[2],data[3],data[4]))
        sqliteConnectionInfoPendaftaran.commit()
        print("Record inserted successfully into SqliteDB_developers table", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)

    finally:
        if sqliteConnectionInfoPendaftaran:
            sqliteConnectionInfoPendaftaran.close()
            print("The SQLite connection is closed")

def deleteDataInfoPendaftaran(gelombang):
    try:
        sqliteConnectionInfoPendaftaran = sqlite3.connect('pendaftaran.db')
        cursor = sqliteConnectionInfoPendaftaran.cursor()
        print("Successfully Connected to SQLite") 

        cursor.execute("DELETE FROM TB_InfoPendaftaran WHERE gelombang={}".format(gelombang))
        
        sqliteConnectionInfoPendaftaran.commit()
        print("Record delete successfully from SqliteDB_developers table", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table", error)

    finally:
        if sqliteConnectionInfoPendaftaran:
            sqliteConnectionInfoPendaftaran.close()
            print("The SQLite connection is closed")

def viewDataInfoPendaftaran():
    try:
        sqliteConnectionInfoPendaftaran = sqlite3.connect('pendaftaran.db')
        cursor = sqliteConnectionInfoPendaftaran.cursor()
        print("Successfully Connected to SQLite")

        count = cursor.execute(""" SELECT * FROM TB_InfoPendaftaran """)
        rows = count.fetchall()

        print("Get data success ", rows)
        cursor.close()
        return rows

    except sqlite3.Error as error:
        print("Failed to get data into sqlite table", error)

    finally:
        if sqliteConnectionInfoPendaftaran:
            sqliteConnectionInfoPendaftaran.close()
            print("The SQLite connection is closed")