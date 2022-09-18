from tkinter import *
import ttk
from functools import partial
from cryptography.fernet import Fernet
from fonction_commune import *
import sqlite3
from hashlib import sha1
from tkinter.messagebox import *
import os
from conf_db_and_user_manager import Db_and_user
class Configuration:
      def __init__(self):
          key = 'yA1bBtGYWRK85fri8m5BjvbC277YjDdgYLoW8hAVRec='
          self.crypter=Fernet(key)
          try:
              os.mkdir('conf')
          except:
              pass
          #db
          if os.path.exists('conf/configure.db'):
              pass
          else:
             self.conn = sqlite3.connect('conf/configure.db')
             self.cursor = self.conn.cursor()
             self.cursor.execute('''CREATE TABLE IF NOT EXISTS db_config(id INTENGER,user BLOB,passwd BLOB,host BLOB,data_base_name BLOB)''')
             self.conn.commit()
             self.cursor.execute('''INSERT INTO db_config(id,user,passwd,host,data_base_name) VALUES(?,?,?,?,?)''',[1,"gAAAAABiFQG5VX4OjkqqVSR5RVciNJHdX48m5SPBF_EJJAi3chxYhwgt-WnClz9EuWlFgcfbbuNLfKZdyHhOWiaf7MtBhnPghA==",'gAAAAABgMfyr4pr_OCCNWuUae4kELhp5Ol4HdsnaW0tAgEmOreNCi2g4o1deXOh4i4zytBopMPgP0EUoVLu7JeaxBX8BxZM2VA==',"gAAAAABgMfhGaT53Gs-PhoFC2YDeTDLXNAN8Ts578JpAaFqCWjxLhS1t9EG_NQReM-waSSyCvG_gVCvJxj0k-cYFb4LJkYQYLA==","gAAAAABgMfiPLfdtVOaz8z9T8EohHRRggLYEZ0P2lub4QxY3RX-FOCaMhBltT1M0yCataPamBm1aWcKSph0emZtOUVBvd9UzLA=="])
             self.conn.commit()
             self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,nom TEXT,prenom TEXT,user_name TEXT,password TEXT)''')
             self.conn.commit()
             self.cursor.execute('''INSERT INTO users(nom,prenom,user_name,password) values(?,?,?,?)''',['Doe','John','admin','0ab10b21d5da20009cec7debe5175d8cfcdadbd2'])
             self.conn.commit()

          self.conn = sqlite3.connect('conf/configure.db')
          self.cursor = self.conn.cursor()
          self.fenetre=Tk()
          self.fenetre.title("Login")
          x=400
          y=400
          #----------------------
          self.cursor.execute("select user from db_config")
          host_=bytes(self.cursor.fetchall()[0][0],'ascii')
          centrer(self.fenetre,x,y)
          #les frames
          self.the_frames(self.fenetre)
          logo_login=PhotoImage(file='images/Login.png').subsample(10,10)
          Label(self.header,image=logo_login).grid(padx=150)
          self.user=StringVar()
          self.user.set('user name')
          self.user_=ttk.Entry(self.header,textvariable=self.user,width=30)
          self.user_.grid(row=1,pady=10)
          self.user_.focus()
          self.user_.bind('<Key Down>', self.focus_passwd)
          self.user_.bind('Return',self.login)
          self.passwd=StringVar()
          self.passwd.set('password')
          self.password=ttk.Entry(self.header,textvariable=self.passwd,width=30,show='*')
          self.password.grid(row=2,pady=5)
          self.password.bind('<Key Up>',self.focus_user)
          self.password.bind('<Return>',self.login)
          self.connecte=ttk.Button(self.header,text='login',command=partial(self.login,self.fenetre))
          self.connecte.grid(row=3)
          self.fenetre.mainloop()
      def the_frames(self,fenetre):
          self.body = Frame(fenetre)
          self.body.grid()
          self.header = Frame(self.body)
          self.header.grid()
          self.middle = Frame(self.body)
          self.middle.grid(row=1)
          self.footer = Frame(self.body)
          self.footer.grid(row=2)
      def the_frames_(self,fenetre):
          body = Frame(fenetre)
          body.grid()
          header = Frame(self.body)
          header.grid(sticky=W)
          middle = Frame(self.body)
          middle.grid(row=1,sticky=W)
          footer = Frame(self.body)
          footer.grid(row=2,sticky=W)
          return header,middle,footer
      def focus_user(self,event):
          self.user_.focus()
      def focus_passwd(self,event):
          self.password.focus()

      def lauch_configure_frame(self):
          self.fenetre.destroy()
          d=Db_and_user()

      def login(self,fenetre,*args):
          user=self.user.get()
          passwd=sha1(str(self.passwd.get()).encode()).hexdigest()
          adm_user="zocky"
          adm_passwd='reredorere'
          self.cursor.execute('''SELECT * FROM users WHERE user_name=? and password=?''',[user,passwd])
          liste=self.cursor.fetchall()
          if len(liste)>0:
             self.lauch_configure_frame()
          else:
              showwarning('Avertissement',"le nom d'utilisateur ou le mot de passe est incorrect")
if __name__=='__main__':
   c=Configuration()