import sqlite3
from cryptography.fernet import Fernet
import mysql.connector
def centrer(fenetre, x, y):
    ecran_x = fenetre.winfo_screenwidth()
    ecran_y = fenetre.winfo_screenheight()
    fen_x = x
    fen_y = y
    posX = (ecran_x // 2) - (fen_x // 2)
    posY = (ecran_y // 2) - (fen_y // 2)
    fenetre.geometry("{}x{}+{}+{}".format(fen_x, fen_y, posX, posY))
def setConnAndCursor(conn,cursor):
    cursor.close()
    conn.close()
    conn = db_connect()
    cursor = conn.cursor()
    return conn,cursor
def db_connect():
    user, host, passwd, data_base =decryp_data()
    conn = mysql.connector.connect(host=host, use_pure=True, user=user, passwd=passwd,database=data_base,port=3306)
    create_table(conn)
    return conn
def decryp_data():
    key = 'yA1bBtGYWRK85fri8m5BjvbC277YjDdgYLoW8hAVRec='
    crypter = Fernet(key)
    # ----------------------------------------------
    conn = sqlite3.connect('conf/configure.db')
    cursor = conn.cursor()
    cursor.execute('''select * from db_config''')
    rows = cursor.fetchall()
    # user=[0][1]
    # password=[0][2]
    user = crypter.decrypt(bytes(rows[0][1], 'ascii')).decode()
    host = crypter.decrypt(bytes(rows[0][3], 'ascii')).decode()
    passwd = crypter.decrypt(bytes(rows[0][2], 'ascii'))
    data_base = crypter.decrypt(bytes(rows[0][4], 'ascii')).decode()
    return user,host,passwd,data_base
def create_database():
    user, host, passwd, data_base = decryp_data()
    conn = mysql.connector.connect(host=host,user=user,passwd=passwd)

    cursor = conn.cursor()
    cursor.execute(f"create database {data_base}")
    conn.commit()
def create_table(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("create table users(id int primary key auto_increment,nom varchar(255),prenom varchar(255),user varchar(255),poste varchar(255),passwd blob,log_date date,tentative int,blocker varchar(255),email varchar(255),confirm_code varchar(255),deja_bloquer varchar(255))")
        cursor.execute("insert into users(nom,prenom,user,poste,passwd,email,blocker,deja_bloquer,tentative) values('desir','renaldo','zock','adm','7110eda4d09e062aa5e4a390b0a572ac0d2c0220','zocky58@gmail.com','False','False',0)")
        conn.commit()
    except:
        pass
    try:
        cursor.execute(
            "create table compte(nom varchar(255),prenom varchar(255),nif varchar(255),code varchar(50) unique,telephone varchar(255),nom_personne_a_contacter varchar(255),telephone_personne_a_contacte varchar(255),signature_autorise varchar(255),type_de_compte varchar(255),montant decimal(12.4))")
        conn.commit()
    except:
        pass
    try:
        # cursor.execute(
        #     "create table compte_suprimmer(nom varchar(255),prenom varchar(255),nif varchar(255) unique,code int(15) unique,telephone varchar(255),nom_personne_a_contacter varchar(255),telephone_personne_a_contacte varchar(255),signature_autorise varchar(255),type_de_compte varchar(255))")
        # conn.commit()
        pass
    except:
        pass
    try:
        cursor.execute(
            'create table depot(id int primary key auto_increment,code varchar(50),nom_complet varchar(255),montant_actuel decimal(12.5),montant_depose decimal(12.9),encient_montant decimal(12.9),heure varchar(255),date_ date)')
    except:
        pass
    try:
        cursor.execute(
            'create table retrait(id int primary key auto_increment,code varchar(50),nom_complet varchar(255),montant_actuel decimal(12.5),montant_retirer decimal(12.9),encient_montant decimal(12.9),heure varchar(255),date_ date)')
    except:
        pass
    try:
        cursor.execute(
            'create table transfert(id int primary key auto_increment,nom_depositaire varchar(255),nom_recepteur varchar(255),montant decimal(12.9),heure varchar(255),date_ date,numero_compte_depositaire varchar(255),numero_compte_recepteur varchar(255))')
    except:
        pass


