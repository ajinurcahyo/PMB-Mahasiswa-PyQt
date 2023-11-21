import sys
import model
import sqlite3
import login_db
from PyQt5 import QtWidgets
from login_window import Ui_Form as login_window
from main_window import Ui_Form as main_window
from admin import Ui_Form as admin_window
from PyQt5.QtWidgets import (QFileDialog)
from PyQt5.QtGui import QPixmap

class ProgramPendaftaran(login_window): # saat pertama running akan menampilkan layout login window
    def __init__(self, dialog):
        login_window.__init__(self)
        self.setupUi(dialog)

        model.createDatabase() # pemanggilan dari modul model fungsi create database
        model.createDatabasePendaftaran() # pemanggilan dari modul model fungsi create database pendaftaran
        login_db.createDatabaseLogin() # pemanggilan dari modul login-db fungsi create database login
        
        self.QpushButton_login.clicked.connect(self.login) 
        # button login apabila di klik akan mengeksekusi ( menjalankan ) fungsi login
        self.QpushButton_addUser.clicked.connect(self.buatUser)
        # button add user  apabila di klik akan mengeksekusi ( menjalankan ) fungsi buatUser
#-------------------- MAIN WINDOW PESERTA ------------------------#
    def login(self): # fungsi login
        username = self.QLineEdit_username.text() # line username
        password = self.QLineEdit_password.text() # line password 
        # baris 27 - 28 digunakan untuk menarik data (username dan password )
        cur = sqlite3.connect("login.db") # KONEKSI KE DATABASE , login.db adalah nama database
        result = cur.execute("SELECT * FROM TB_login WHERE user = ? AND passwd = ?", (username, password)).fetchall()
                # SELECT( perintah yg digunakan untuk memilih dari database)
                # FROM TB_login ( FROM digunakan untuk menginisialisasi nama tabel, diikuti nama tabel dibelakangnya ( TB_login))
                # WHERE user, AND passwd ( digunakan untuk memfilter hasil pemilihan, berupa user dan password)
                # fetchall digunakan untuk pemanggilan data
        cur.commit() # commit digunakan untuk mengakhiri semua transaksi 
        cur.close() # menutup koneksi database

        if result: # intinya jika hasil ( username dan password ) ditemukan maka :
            print("User Found !") # print User Found! pada terminal

            self.mainWindow = QtWidgets.QDialog()
            self.mainUI = main_window()
            self.mainUI.setupUi(self.mainWindow)
            # baris 42 - 44 digunakan untuk pemanggilan main window ( peserta ), jika tidak dipanggil maka tidak dapat terhubung ke main window ( peserta )
            loginWindow.show() # menampilkan login window
            self.mainWindow.show() # menampilkan main window ( peserta )

            self.mainUI.label_gagal.hide() # menyembunyikan label gagal
            self.mainUI.label_lulus.hide() # menyembunyikan label lulus
            self.mainUI.label_13.hide() # menyembunyikan label berikut data lengkap anda pada menu pengumuman
            self.mainUI.tableWidget_pengumuman.hide() # menyembunyikan tabel data peserta pada menu pengumuman 

            self.mainUI.pushButtonViewInfoPendaftaran.clicked.connect(self.viewDataInfoPendaftaranUser)
            # button view info Pendaftaran apabila di klik akan mengeksekusi ( menjalankan ) fungsi viewDataInforPendaftaranUser
            self.mainUI.pushButton_tambah.clicked.connect(self.simpanData)
            self.mainUI.pushButton_clear1.clicked.connect(self.clearData1)
            self.mainUI.pushButton_clear2.clicked.connect(self.clearData2)
            self.mainUI.pushButton_cek.clicked.connect(self.cekData) 
            self.mainUI.pushButton_ubah.clicked.connect(self.ubahData)
            self.mainUI.pushButton_view.clicked.connect(self.viewData)
            self.mainUI.pushButton_pengumuman.clicked.connect(self.cekDataPengumuman)
            self.mainUI.pushButton_clearPengumuman.clicked.connect(self.clearDataPengumuman)
            self.mainUI.pushButtonPasFoto.clicked.connect(self.get_image)
            self.mainUI.pushButtonIjazah.clicked.connect(self.get_file_ijazah)  
            self.mainUI.pushButtonKartuKeluarga.clicked.connect(self.get_file_kk) 

        elif(username == "admin" and password == "admin"): # jika username = admin dan password = admin maka:
            print("User Found !") # print User Found pada terminal

            self.mainWindow2 = QtWidgets.QDialog()
            self.mainUI = admin_window()
            self.mainUI.setupUi(self.mainWindow2)
            # baris 71 - 73 digunakan untuk pemanggilan admin window, jika tidak dipanggil maka tidak dapat terhubung ke admin window
            loginWindow.show() # menampilkan login window
            self.mainWindow2.show() # menampilkan admin window

            #self.viewData2()
            self.viewData3() # memanggil fungsi viewData3
            self.viewDataUser() # memanggil fungsi viewDataUser 
            self.mainUI.BtnHome.clicked.connect(lambda: self.mainUI.stackedWidget.setCurrentWidget(self.mainUI.homePage))
            # button home apabila di klik akan terkoneksi dengan stackedwiget homePage
            self.mainUI.BtnDataMhs.clicked.connect(lambda: self.mainUI.stackedWidget.setCurrentWidget(self.mainUI.dataPage))
            self.mainUI.BtnBerkas.clicked.connect(lambda: self.mainUI.stackedWidget.setCurrentWidget(self.mainUI.berkasPage))
            self.mainUI.BtnUser.clicked.connect(lambda: self.mainUI.stackedWidget.setCurrentWidget(self.mainUI.userPage))
            self.mainUI.simpanInfoPendaftaran.clicked.connect(self.simpanDataInfoPendaftaran)
            self.mainUI.HapusInfoPendaftaran.clicked.connect(self.hapusDataPendaftaran)
            self.mainUI.pushButtonLihatInfoPendaftaran.clicked.connect(self.viewDataInfoPendaftaranAdmin)
            self.mainUI.pushButton_hapus.clicked.connect(self.hapusData)
            self.mainUI.HapusUser.clicked.connect(self.hapusDataUser)

        else: # jika user dan password tidak ditemukan maka:
            print("User Not Found !") # print User Not Found pada terminal
            self.messagebox("INFO", "User Not Found !") # notifikasi user not found

    # MEMBUAT USER
    def buatUser(self): # fungsi buat user
        username = self.lineEdit_buatUser.text() # line username
        password = self.lineEdit_buatPass.text() # line password
        email = self.lineEdit_buatEmail.text() # line email
        # baris 98 - 100 digunakan untuk menarik data ( username, password dan email)
        
        login_db.insertDatatoDB(password, username, email) # pemanggilan dari modul login_db fungsi insert data toDB
        self.messagebox("INFO", "Success Add User") # notifikasi success add user

    # MESSAGEBOX ( Pesan notifikasi )
    def messagebox(self, title, message): # fungsi pesan notifikasi
        mess = QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec_()

    # MENAMPILKAN INFO PENDAFTARAN PADA PESERTA
    def viewDataInfoPendaftaranUser(self): # fungsi view info pendaftaram
        data = model.viewDataInfoPendaftaran() # memanggil dari modul model, fungsi view data info pendaftaran 

        for info in data:
            rowPosition = self.mainUI.tableWidgetViewInfoPendaftaran.rowCount()
            self.mainUI.tableWidgetViewInfoPendaftaran.insertRow(rowPosition)
            self.mainUI.tableWidgetViewInfoPendaftaran.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(info[0])))
                # pada tabel widget info pendaftaran baris ke 0 akan di isi oleh data index ke 0 yaitu gelombang, diambil dari tabel TB_InfoPendaftaran pada database
            self.mainUI.tableWidgetViewInfoPendaftaran.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(info[1]))
                # pada tabel widget info pendaftaran baris ke 1 akan di isi oleh data index ke 1 yaitu periode gelombang, diambil dari tabel TB_InfoPendaftaran pada database
            self.mainUI.tableWidgetViewInfoPendaftaran.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(info[2]))
                # pada tabel widget info pendaftaran baris ke 2 akan di isi oleh data index ke 2 yaitu fakultas, diambil dari tabel TB_InfoPendaftaran pada database
            self.mainUI.tableWidgetViewInfoPendaftaran.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(info[3]))
                # pada tabel widget info pendaftaran baris ke 3 akan di isi oleh data index ke 3 yaitu prodi, diambil dari tabel TB_InfoPendaftaran pada database
            self.mainUI.tableWidgetViewInfoPendaftaran.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(info[4]))
                # pada tabel widget info pendaftaran baris ke 4 akan di isi oleh data index ke 4 yaitu keterangan info, diambil dari tabel TB_InfoPendaftaran pada database
            # baris 119 - 129 adalah proses plotting ( penempatan ) data pada tabel widget view info pendaftaran

    # SIMPAN DATA PESERTA 
    def simpanData(self): # fungsi simpan data peserta
        nama = self.mainUI.lineEdit_nama.text() # line nama
        nisn = self.mainUI.lineEdit_nisn.text() # line nisn
        asalSekolah = self.mainUI.lineEdit_sekolah.text() # line asal sekolah
        tempatTglLahir = self.mainUI.lineEdit_ttl.text() # lint tmpat tgl lahir
        agama = self.mainUI.lineEdit_agama.text() # line agama
        alamat = self.mainUI.lineEdit_alamat.text() # line alamat
        nomorHp= self.mainUI.lineEdit_nomor.text() # line nomor hp
        prodi = self.mainUI.comboBox_prodi.currentText() # line prodi
        # baris 135 - 142 digunakan untuk menarik data 
        
        model.insertDatatoDB(nisn, nama, asalSekolah, tempatTglLahir, agama, alamat, nomorHp, prodi) # memanggil dari modul model, fungsi insert data to db

        self.messagebox("INFO","Data Peserta {} Berhasil Disimpan".format(nama)) # menampilkan notif data peserta berhasil disimpan

    # CEK DATA PESERTA ( Pencarian dengan memasukkan nama lengkap )
    def cekData(self): # fungsi cek data
        nama = self.mainUI.lineEdit_cariNama.text() # line nama
        db = sqlite3.connect('pendaftaran.db') # koneksi ke database
        cursor = db.cursor() 
        cursor.execute("SELECT * FROM TB_Pendaftaran WHERE nama= '" + str(nama) + "'") 
        data = cursor.fetchall() # memanggil data
        db.commit()
        db.close()

        if(data): # jika data ditemukan maka:
            for tp in data: # hanya sebagai alias
                self.mainUI.LineEdit_nama.setText(""+tp[1])
                self.mainUI.LineEdit_nisn.setText(""+str(tp[0]))
                self.mainUI.LineEdit_sekolah.setText(""+tp[2])
                self.mainUI.LineEdit_ttl.setText(""+tp[3])
                self.mainUI.LineEdit_agama.setText(""+tp[4])
                self.mainUI.LineEdit_alamat.setText(""+tp[5])
                self.mainUI.LineEdit_nomor.setText(""+tp[6])
                self.mainUI.LineEdit_prodi.setText(""+tp[7])

                self.messagebox("INFO", "Data Peserta {} Ditemukan".format(nama))
        else:
            self.messagebox("INFO", "Mohon Maaf Data Peserta {} Tidak Ditemukan".format(nama))

    # UBAH DATA PESERTA ( Syarat, data peserta harus ditemukan)
    def ubahData(self): # fungsi ubah data
        nama = self.mainUI.LineEdit_nama.text()
        nisn = self.mainUI.LineEdit_nisn.text()
        asalSekolah = self.mainUI.LineEdit_sekolah.text()
        tempatTglLahir = self.mainUI.LineEdit_ttl.text()
        agama = self.mainUI.LineEdit_agama.text()
        alamat = self.mainUI.LineEdit_alamat.text()
        nomorHp = self.mainUI.LineEdit_nomor.text()
        prodi = self.mainUI.comboBox_prodi_2.currentText()

        db = sqlite3.connect('pendaftaran.db')
        cursor = db.cursor()
        sqlite = "UPDATE TB_Pendaftaran SET nisn= ?, asalSekolah= ?, tempatTglLahir= ?, agama= ?, alamat= ?, nomorHp= ?, prodi= ? WHERE nama= ?"
        data = cursor.execute(sqlite, (nisn, asalSekolah,  tempatTglLahir, agama, alamat, nomorHp, prodi, nama))
        db.commit()
        db.close()

        if(data):
            self.messagebox("INFO", "Data Peserta {} Berhasil Diubah".format(nama))
        else:
            self.messagebox("INFO", "Data Peserta {} Gagal Diubah".format(nama))

    # MENAMPILKAN DATA PENDAFTAR ( Hanya dapat menampilkan nama lengkap, asal sekolah dan prodi )
    def viewData(self): # fungsi view data
        data = model.viewDataFromDB() # memanggil data dari modul ( file ) model, fungsi view data from db

        for biodata in data:
            rowPosition = self.mainUI.tableWidget_data.rowCount()
            self.mainUI.tableWidget_data.insertRow(rowPosition)
            self.mainUI.tableWidget_data.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(biodata[1]))
            self.mainUI.tableWidget_data.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(biodata[2]))
            self.mainUI.tableWidget_data.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(biodata[7]))

    # -- UPLOAD BERKAS --

    # UPLOAD PAS FOTO ( jpg , jpeg, gif)
    def get_image(self): # fungsi get image
        fname= QFileDialog.getOpenFileName(None, 'Open File', r"<Default dir>", "All files (*.jpg *.jpeg *.gif)")
            # r ( read/ membaca) pada default direktori, all files ( semua file ) dengan format jpg, jpeg dan gif
        self.pixmap =QPixmap(fname[0])
        self.mainUI.labelImage.setPixmap(self.pixmap) # gambar akan ditampilkan pada laebl image

    # FILE IJAZAH ( PDF )
    def get_file_ijazah(self): # fungsi get file ijazah
        fname= QFileDialog.getOpenFileName(None, 'Select File', r"<Default dir>", "All files (*.pdf)")
            # r ( read/ membaca) pada default direktori, all files ( semua file ) dengan format pdf
        self.mainUI.lineEditIjazah.setText(fname[0])

    # FILE KK ( PDF )
    def get_file_kk(self): # fungsi get file kk
        fname= QFileDialog.getOpenFileName(None, 'Select File', r"<Default dir>", "All files (*.pdf)")
            # r ( read/ membaca) pada default direktori, all files ( semua file ) dengan format pdf
        self.mainUI.lineEditKartuKeluarga.setText(fname[0])

    # LIHAT HASIL KELULUSAN ( Pencarian dengan nisn, jika data dengan pencarian nisn tersebut ada dalam database maka dinyatakan diterima, jika tidak maka dinyatakan tidak diterima )
    def cekDataPengumuman(self): # fungsi cek data pengumuman
        nisn = int(self.mainUI.lineEdit_pengumuman.text()) # line nisn , dalam memasukkan nisn harus berupa integer ( angka )
        db = sqlite3.connect('pendaftaran.db') # koneksi ke database, pendaftaran.db adalah nama databasenya
        cursor = db.cursor() 
        cursor.execute("SELECT * FROM TB_Pendaftaran WHERE nisn= '" + str(nisn) + "'") # eksekusi memilih dari TB_Pendaftaran ( nama tabel) dengan format pencarian nisn
        data = cursor.fetchall() # memanggil data
        db.commit()
        db.close()

        if(data): # intinya jika data ditemukan maka: 
            for biodata in data:
                rowPosition = self.mainUI.tableWidget_pengumuman.rowCount()
                self.mainUI.tableWidget_pengumuman.insertRow(rowPosition)
                self.mainUI.tableWidget_pengumuman.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(biodata[1]))
                    #pada tabel pengumuman baris ke 0 akan di isi oleh data index ke 1 yaitu nama, yang diambil dari tabel TB_Pendaftaran pada database
                self.mainUI.tableWidget_pengumuman.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(biodata[0])))
                    #pada tabel pengumuman baris ke 1 akan di isi oleh data index ke 0 yaitu nisn, yang diambil dari tabel TB_Pendaftaran pada database
                self.mainUI.tableWidget_pengumuman.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(biodata[2]))
                    #pada tabel pengumuman baris ke 2 akan di isi oleh data index ke 2 yaitu asal sekolah, yang diambil dari tabel TB_Pendaftaran pada database
                self.mainUI.tableWidget_pengumuman.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(biodata[3]))
                    #pada tabel pengumuman baris ke 3 akan di isi oleh data index ke 3 yaitu tempat tgl lahir, yang diambil dari tabel TB_Pendaftaran pada database
                self.mainUI.tableWidget_pengumuman.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(biodata[4]))
                    #pada tabel pengumuman baris ke 4 akan di isi oleh data index ke 4 yaitu agama, yang diambil dari tabel TB_Pendaftaran pada database
                self.mainUI.tableWidget_pengumuman.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(biodata[5]))
                    #pada tabel pengumuman baris ke 5 akan di isi oleh data index ke 5 yaitu alamat, yang diambil dari tabel TB_Pendaftaran pada database
                self.mainUI.tableWidget_pengumuman.setItem(rowPosition, 6, QtWidgets.QTableWidgetItem(biodata[6]))
                    #pada tabel pengumuman baris ke 6 akan di isi oleh data index ke 6 yaitu nomor hp, yang diambil dari tabel TB_Pendaftaran pada database
                self.mainUI.tableWidget_pengumuman.setItem(rowPosition, 7, QtWidgets.QTableWidgetItem(biodata[7]))
                    #pada tabel pengumuman baris ke 7 akan di isi oleh data index ke 7 yaitu prodi, yang diambil dari tabel TB_Pendaftaran pada database
                # baris 241 - 257 adalah proses plotting ( penempatan ) data pada tabel widget pengumuman

                self.messagebox("INFO", "Peserta Dengan NISN {} Dinyatakan Diterima Di Universitas Jenderal Achmad Yani Yogyakarta".format(nisn)) # muncul notif diterima
                self.mainUI.label_lulus.setText("SELAMAT! ANDA DINYATAKAN LULUS") # label selamat
                self.mainUI.label_lulus.show() # menampilkan label selamat
                self.mainUI.label_13.show() # menampilkan label berikut data lengkap anda
                self.mainUI.tableWidget_pengumuman.show() # menampilkan tabel widget pengumuman

        else: # jika data tidak ditemukan
            self.messagebox("INFO", "Peserta Dengan NISN {} Dinyatakan Tidak Diterima Di Universitas Jenderal Achmad Yani Yogyakarta".format(nisn)) # muncul notif tidak diterima
            self.mainUI.label_gagal.setText("JANGAN PUTUS ASA DAN TETAP SEMANGAT !") # label jangan putus asa
            self.mainUI.label_gagal.show() # menampilkan label jangan putus asa
            self.mainUI.label_lulus.hide() # label selamat disembunyikan
            self.mainUI.label_13.hide() # label berikut data lengkap anda disembunyikan
            self.mainUI.tableWidget_pengumuman.hide() # tabel widget pengumuman disembunyikan

#------------------------ ADMIN -------------------------#

    # SIMPAN INFO PENDAFTARAN
    def simpanDataInfoPendaftaran(self): # fungsi simpan data info pendaftaran
        gelombang = self.mainUI.gelombangLineEdit.text() # line gelombang
        periodeGelombang = self.mainUI.periodeGelombangLineEdit.text() # line periode gelombang
        fakultas = self.mainUI.fakultasLineEdit.text() # line fakultas
        prodi = self.mainUI.prodiLineEdit.text() # line prodi
        keteranganInfo = self.mainUI.keteranganInfoLineEdit.text() #line keterangan info
        # baris 279-283 digunakan untuk penarikan data , yang nantinya akan di tempatkan pada tabel info pendaftaran

        model.insertDataInfoPendaftaran(gelombang, periodeGelombang, fakultas, prodi, keteranganInfo) 
        # memanggil dari modul ( file ) model, fungsi insert data info pendaftaran

        rowPosition = self.mainUI.tableWidgetInfoPendaftaran.rowCount() # rowCount digunakan untuk menambahkan baris baru

        self.mainUI.tableWidgetInfoPendaftaran.insertRow(rowPosition)
        self.mainUI.tableWidgetInfoPendaftaran.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(periodeGelombang))
            # pada tabel widget info pendaftaran pada baris ke 0 akan di isi oleh periode gelombang
        self.mainUI.tableWidgetInfoPendaftaran.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(gelombang))
            # pada tabel widget info pendaftaran pada baris ke 1 akan di isi oleh gelombang
        self.mainUI.tableWidgetInfoPendaftaran.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(fakultas))
            # pada tabel widget info pendaftaran pada baris ke 2 akan di isi oleh fakultas
        self.mainUI.tableWidgetInfoPendaftaran.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(prodi))
            # pada tabel widget info pendaftaran pada baris ke 3 akan di isi oleh prodi
        self.mainUI.tableWidgetInfoPendaftaran.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(keteranganInfo))
            # pada tabel widget info pendaftaran pada baris ke 4 akan di isi oleh keterangan info
        # baris 291 - 300 adalah proses plotting ( penempatan ) data, kedalam tabel widget info pendaftaran

        self.messagebox("INFO","Info Pendaftaran Berhasil Disimpan") # menampilkan notif info berhasil disimpan

    # HAPUS INFO PENDAFTARAN
    def hapusDataPendaftaran(self): # fungsi hapus info pendaftaran
        selectedRow = self.mainUI.tableWidgetInfoPendaftaran.currentRow() # memilih baris pada tabel widget info pendaftaran

        periode = self.mainUI.tableWidgetInfoPendaftaran.item(selectedRow, 0).text() # pemilihan baris 0 pada tabel widget info pendaftaran adalah baris periode
        gelombang = self.mainUI.tableWidgetInfoPendaftaran.item(selectedRow, 1).text() # pemilihan baris 1 pada tabel widget info pendaftaran adalah baris gelombang

        model.deleteDataInfoPendaftaran(gelombang) # memanggil dari modul ( file ) model, fungsi delete data info pendaftaran

        self.mainUI.tableWidgetInfoPendaftaran.removeRow(selectedRow) # baris pada tabel widget info pendaftaran yang dipilih akan dihapus
        self.messagebox("INFO","Info Periode {} Berhasil Dihapus".format(periode)) # menampilkan notif info berhasil dihapus

    # MENAMPILKAN INFO PENDAFTARAN PADA ADMIN
    def viewDataInfoPendaftaranAdmin(self): # fungsi view info pendaftaran 
        data = model.viewDataInfoPendaftaran() # memanggil dari modul ( file ) model, fungsi view data info pendaftaran

        for info in data:
            rowPosition = self.mainUI.tableWidgetInfoPendaftaran.rowCount()
            self.mainUI.tableWidgetInfoPendaftaran.insertRow(rowPosition)
            self.mainUI.tableWidgetInfoPendaftaran.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(info[1]))
                # pada tabel widget info pendaftaran pada baris ke 0 akan di isi oleh data index ke 1 yaitu periode gelombang, diambil dari tabel TB_InfoPendaftaran pada database
            self.mainUI.tableWidgetInfoPendaftaran.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(info[0])))
                # pada tabel widget info pendaftaran pada baris ke 1 akan di isi oleh data index ke 0 yaitu gelombang, diambil dari tabel TB_InfoPendaftaran pada database
            self.mainUI.tableWidgetInfoPendaftaran.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(info[2]))
                # pada tabel widget info pendaftaran pada baris ke 2 akan di isi oleh data index ke 2 yaitu fakultas, diambil dari tabel TB_InfoPendaftaran pada database
            self.mainUI.tableWidgetInfoPendaftaran.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(info[3]))
                # pada tabel widget info pendaftaran pada baris ke 3 akan di isi oleh data index ke 3 yaitu prodi, diambil dari tabel TB_InfoPendaftaran pada database
            self.mainUI.tableWidgetInfoPendaftaran.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(info[4]))
                # pada tabel widget info pendaftaran pada baris ke 4 akan di isi oleh data index ke 4 yaitu keterangan info, diambil dari tabel TB_InfoPendaftaran pada database
            # baris 323 - 333 adalah proses plotting ( penempatan ) data pada tabel widget info pendaftaran 

    # MENAMPILKAN  DATA ( Ditampilkan data lengkap peserta )
    def viewData3(self): # fungsi view data 
        data = model.viewDataFromDB() # memanggil dari modul model, fungsi view data from db

        for biodata in data:
            rowPosition = self.mainUI.tableWidget_adminEdit.rowCount()
            self.mainUI.tableWidget_adminEdit.insertRow(rowPosition)
            self.mainUI.tableWidget_adminEdit.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(biodata[1]))
                # pada tabel widget admin edit pada baris ke 0 akan di isi oleh data index ke 1 yaitu nama, diambil dari tabel TB_Pendaftaran pada database
            self.mainUI.tableWidget_adminEdit.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(biodata[0])))
                # pada tabel widget admin edit pada baris ke 1 akan di isi oleh data index ke 0 yaitu nisn, diambil dari tabel TB_Pendaftaran pada database
            self.mainUI.tableWidget_adminEdit.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(biodata[2]))
                # pada tabel widget admin edit pada baris ke 2 akan di isi oleh data index ke 2 yaitu asal sekolah, diambil dari tabel TB_Pendaftaran pada database
            self.mainUI.tableWidget_adminEdit.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(biodata[3]))
                # pada tabel widget admin edit pada baris ke 3 akan di isi oleh data index ke 3 yaitu tempat tgl lahir, diambil dari tabel TB_Pendaftaran pada database
            self.mainUI.tableWidget_adminEdit.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(biodata[4]))
                # pada tabel widget admin edit pada baris ke 4 akan di isi oleh data index ke 4 yaitu agama, diambil dari tabel TB_Pendaftaran pada database
            self.mainUI.tableWidget_adminEdit.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(biodata[5]))
                # pada tabel widget admin edit pada baris ke 5 akan di isi oleh data index ke 5 yaitu alamat, diambil dari tabel TB_Pendaftaran pada database
            self.mainUI.tableWidget_adminEdit.setItem(rowPosition, 6, QtWidgets.QTableWidgetItem(biodata[6]))
                # pada tabel widget admin edit pada baris ke 6 akan di isi oleh data index ke 6 yaitu nomor hp, diambil dari tabel TB_Pendaftaran pada database
            self.mainUI.tableWidget_adminEdit.setItem(rowPosition, 7, QtWidgets.QTableWidgetItem(biodata[7]))
                # pada tabel widget admin edit pada baris ke 7 akan di isi oleh data index ke 7 yaitu prodi, diambil dari tabel TB_Pendaftaran pada database
            # baris 342 - 358 adalah proses plotting ( penempatan ) data kedalam tabel widget admin edit

    # HAPUS DATA PESERTA
    def hapusData(self): # fungsi hapus data
        selectedRow = self.mainUI.tableWidget_adminEdit.currentRow() # memilih baris pada tabel widget admin edit

        nama = self.mainUI.tableWidget_adminEdit.item(selectedRow, 0).text() # pemilihan baris 0 pada tabel widget admin edit adalah baris nama
        nisn = self.mainUI.tableWidget_adminEdit.item(selectedRow, 1).text() # pemilihan baris 1 pada tabel widget admin edit adalah baris nisn

        model.deleteDataFromDB(nisn) # memanggil modul model, fungsi delete data from db
        
        self.mainUI.tableWidget_adminEdit.removeRow(selectedRow) # baris pada tabel widget admin edit yang dipilih akan dihapus
        self.messagebox("INFO","Data Peserta {} Berhasil Dihapus".format(nama)) # notif data peserta berhasil dihapus

    # MENAMPILKAN DATA USER
    def viewDataUser(self): # fungsi view data user
        data = login_db.viewDataFromDB() # memanggil dari modul login_db fungsi view data from db

        for biodata in data:
            rowPosition = self.mainUI.tableWidget_user.rowCount()
            self.mainUI.tableWidget_user.insertRow(rowPosition)
            self.mainUI.tableWidget_user.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(biodata[1]))
                # pada tabel widget user baris 0 akan di isi oleh data index ke 1 yaitu password, diambil dari tabel TB_login pada database
            self.mainUI.tableWidget_user.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(biodata[0])))
                # pada tabel widget user baris 1 akan di isi oleh data index ke 0 yaitu username, diambil dari tabel TB_login pada database
            self.mainUI.tableWidget_user.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(biodata[2]))
                # pada tabel widget user baris 2 akan di isi oleh data index ke 2 yaitu email, diambil dari tabel TB_login pada database
            # baris 379 - 385 adalah proses plotting ( penempatan ) data pada tabel widget user

    # HAPUS DATA USER
    def hapusDataUser(self): # fungsi hapus data user
        selectedRow = self.mainUI.tableWidget_user.currentRow() # memilih baris pada tabel widget user

        user = self.mainUI.tableWidget_user.item(selectedRow, 0).text() # pemilihan baris 0 pada tabel widget user adalah baris username
        passwd = self.mainUI.tableWidget_user.item(selectedRow, 1).text() # pemilihan baris 1 pada tabel widget user adalah baris password

        login_db.deleteDataFromDB(passwd) # memanggil modul login_db, fungsi delete data from db
        
        self.mainUI.tableWidget_user.removeRow(selectedRow) # baris pada tabel widget user yang dipilih akan dihapus
        self.messagebox("INFO","User {} Berhasil Dihapus".format(user)) # notif user berhasil dihapus

    # CLEAR PADA MENU DAFTAR
    def clearData1(self): # fungsi clear data1 ( pada menu daftar )
        self.mainUI.lineEdit_nama.clear()
        self.mainUI.lineEdit_nisn.clear()
        self.mainUI.lineEdit_sekolah.clear()
        self.mainUI.lineEdit_ttl.clear()
        self.mainUI.lineEdit_agama.clear()
        self.mainUI.lineEdit_alamat.clear()
        self.mainUI.lineEdit_nomor.clear()

    # CLEAR PADA MENU CEK DATA PESERTA
    def clearData2(self): # fungsi clear data2 ( pada menu data peserta )
        self.mainUI.LineEdit_nama.clear()
        self.mainUI.LineEdit_nisn.clear()
        self.mainUI.LineEdit_sekolah.clear()
        self.mainUI.LineEdit_ttl.clear()
        self.mainUI.LineEdit_agama.clear()
        self.mainUI.LineEdit_alamat.clear()
        self.mainUI.LineEdit_nomor.clear()
        self.mainUI.LineEdit_prodi.clear()
        self.mainUI.lineEdit_cariNama.clear()

    # CLEAR PADA MENU PENGUMUMAN
    def clearDataPengumuman(self): # fungsi clear data pengumuman ( pada menu pengumuman )
        selectedRow = self.mainUI.tableWidget_pengumuman.currentRow()
        self.mainUI.tableWidget_pengumuman.removeRow(selectedRow)
        self.mainUI.lineEdit_pengumuman.clear()
        self.mainUI.label_lulus.hide()
        self.mainUI.label_gagal.hide()
        self.mainUI.label_13.hide()
        self.mainUI.tableWidget_pengumuman.hide()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loginWindow = QtWidgets.QDialog()

    loginUI = ProgramPendaftaran(loginWindow)

    loginWindow.show()
    sys.exit(app.exec_())