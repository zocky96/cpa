from tkinter import *
from tkinter.messagebox import *
import tkinter.ttk as ttk
import sqlite3
from fonction_commune import *
from hashlib import sha1
from cryptography.fernet import Fernet
class Db_and_user:
      def __init__(self):
          self.conn = sqlite3.connect('conf/configure.db')
          self.cursor = self.conn.cursor()
          key = 'yA1bBtGYWRK85fri8m5BjvbC277YjDdgYLoW8hAVRec='
          self.crypter = Fernet(key)
          fenetre=Tk()
          fenetre.title("Configuration de la base de donnee et gestion utilisateu")
          width=600
          height=400
          centrer(fenetre,width,height)
          body=Frame(fenetre)
          body.pack(anchor=W,padx=5)
          header=Frame(body)
          header.grid()

          footer=Frame(body)
          footer.grid(row=2)
          onglet = ttk.Notebook(header)
          onglet.grid(sticky=W)
          page_1 = Frame(onglet)
          page_2 = Frame(onglet)
          onglet.add(page_1, text="Configuration de la base de donnees")
          onglet.add(page_2, text="Gestion utilisateur")
          in_side_page_1 = Frame(page_1)
          in_side_page_1.grid(row=1)
          Label(in_side_page_1, text='Host : ', fg='blue').grid(sticky=W, pady=5)
          # ---------------------------------
          self.host = StringVar()
          host = ttk.Entry(in_side_page_1, textvariable=self.host)
          host.grid(row=0, column=1, sticky=W)
          # ----------------------------------------------
          Label(in_side_page_1, text='User name : ', fg='blue').grid(row=1, sticky=W, pady=5)
          self.user__ = StringVar()
          user = ttk.Entry(in_side_page_1, textvariable=self.user__)
          user.grid(row=1, column=1)
          # ----------------------------------------------------
          self.passwd = StringVar()
          Label(in_side_page_1, text="Password", fg='blue').grid(row=2, sticky=W, pady=5)
          password = ttk.Entry(in_side_page_1, textvariable=self.passwd)
          password.grid(row=2, column=1, sticky=W)
          Label(in_side_page_1, text="Data base : ", fg="blue").grid(row=3, sticky=W)
          self.data_base = StringVar()
          data_base = ttk.Entry(in_side_page_1, textvariable=self.data_base)
          data_base.grid(row=3, column=1, sticky=W, pady=3)
          self.enregistre = ttk.Button(in_side_page_1, text='Enregistrer', command=self.enregistrer)
          self.enregistre.grid(row=4, column=1, sticky=E)
          # page 2
          # id,nom,prenom,user_name,password
          form_section=Frame(page_2)
          form_section.grid(row=0,sticky=W,pady=5)
          self.nom = StringVar()
          ttk.Entry(form_section, textvariable=self.nom, width=30).grid(row=0,pady=6,padx=5)
          self.prenom = StringVar()
          ttk.Entry(form_section, textvariable=self.prenom, width=30).grid(row=0, column=1)
          self.user = StringVar()
          ttk.Entry(form_section, textvariable=self.user, width=30).grid(row=1,)
          self.user_password = StringVar()
          ttk.Entry(form_section, textvariable=self.user_password, width=30).grid(row=1, column=1)
          button_section=Frame(page_2)
          button_section.grid(row=1,sticky=W)
          ttk.Button(button_section,text='Enregistrer',command=self.save_user).grid(row=0)
          ttk.Button(button_section, text='Modifier',command=self.modifier_user).grid(row=0,column=1)
          ttk.Button(button_section, text='Suprimmer',command=self.supprimer_user).grid(row=0,column=2)
          table_section=Frame(page_2)
          table_section.grid(row=2)
          #---------------------------------------
          self.table = ttk.Treeview(table_section)
          self.table['column'] = ('nom', 'prenom', 'user', 'mot de passe', 'log date')
          self.table.heading('#0', text='ID')
          self.table.column('#0', width=80, minwidth=120, anchor=CENTER)
          self.table.column('nom', width=80, minwidth=120, anchor=CENTER)
          self.table.heading('nom', text='nom')
          self.table.heading('prenom', text='prenom')
          self.table.column('prenom', width=80, minwidth=120, anchor=CENTER)
          self.table.heading('user', text='user')
          self.table.column('user', width=80, minwidth=120, anchor=CENTER)
          self.table.heading('mot de passe', text='mot de passe')
          self.table.column('mot de passe', width=80, minwidth=120, anchor=CENTER)
          self.table.heading('log date', text='log date')
          self.table.column('log date', width=80, minwidth=120, anchor=CENTER)
          self.table.pack(side=BOTTOM, pady=4)
          self.table.pack_propagate(0)
          self.table.bind('<<TreeviewSelect>>',self.selection)
          av_y = ttk.Scrollbar(self.table, orient='vertical', command=self.table.yview)
          av_y.pack(side=RIGHT, fill=Y)
          av_x = ttk.Scrollbar(self.table, orient='horizontal', command=self.table.xview)
          av_x.pack(side=BOTTOM, fill=X)
          self.table.config(xscrollcommand=av_x.set, yscrollcommand=av_y.set)
          self.init_values()
          self.init_values_2()
          self.afficher()
          fenetre.mainloop()
      def init_values_2(self):
          self.nom.set('Nom')
          self.prenom.set('Prenom')
          self.user.set('User name')
          self.user_password.set("Password")
      def modifier_user(self):
          row=self.table.selection()
          for item in row:
              id=self.table.item(item,'text')

          nom = self.nom.get()
          prenom = self.prenom.get()
          user = self.user.get()
          #password = self.user_password.get()

          password = sha1(str(self.user_password.get()).encode()).hexdigest()
          liste = [nom, prenom, user, password,id]
          self.cursor.execute('''update users set nom=?,prenom=?,user_name=?,password=? where id=?''',liste)
          self.conn.commit()
          self.init_values_2()
          self.afficher()
          showinfo('info', 'Utilisateur modifier avec succes')
      def afficher(self):
          self.table.delete(*self.table.get_children())
          self.cursor.execute('''select * from users''')
          rows=self.cursor.fetchall()
          n=0
          for row in rows:
              self.table.insert('',n,n,text=row[0],values=(row[1],row[2],row[3],row[4]))
              n+=1
      def selection(self,*args):
          row=self.table.selection()
          for item in row:
              id=self.table.item(item,'text')
              items=self.table.item(item,'values')
              nom=items[0]
              prenom=items[1]
              user=items[2]
              password=items[3]
          self.nom.set(nom)
          self.prenom.set(prenom)
          self.user.set(user)
          self.user_password.set(password)

      def supprimer_user(self):
          row=self.table.selection()
          for item in row:
              id=self.table.item(item,'text')
              self.cursor.execute('''delete from users where id=?''',[id])
              self.conn.commit()
          self.init_values_2()
          self.afficher()
          showinfo('info','Utilisateur supprimer avec succes')
      def save_user(self):
          nom=self.nom.get()
          prenom=self.prenom.get()
          user=self.user.get()
          password = sha1(str(self.user_passwordd.get()).encode()).hexdigest()
          #password=self.user_password.get()
          liste=[nom,prenom,user,password]
          self.cursor.execute('''insert into users(nom,prenom,user_name,password) values(?,?,?,?)''',liste)
          self.conn.commit()
          self.init_values_2()
          self.afficher()
          showinfo('info', 'Utilisateur enregistrer avec succes')
      def init_values(self):
          self.cursor.execute("select host from db_config")
          host_ = bytes(self.cursor.fetchall()[0][0], 'ascii')
          host_ = self.crypter.decrypt(host_).decode()
          self.host.set(host_)
          self.cursor.execute("select passwd from db_config")
          passwd_ = bytes(self.cursor.fetchall()[0][0], 'ascii')
          passwd_ = self.crypter.decrypt(passwd_).decode()
          self.passwd.set(passwd_)
          self.cursor.execute("select data_base_name from db_config")
          data_base = bytes(self.cursor.fetchall()[0][0], 'ascii')
          data_base = self.crypter.decrypt(data_base).decode()
          self.data_base.set(data_base)
          self.cursor.execute("select user from db_config")
          user_ = bytes(self.cursor.fetchall()[0][0], 'ascii')
          user_ = self.crypter.decrypt(user_).decode()
          self.user__.set(user_)
      def enregistrer(self):
          host=self.host.get().encode()
          user=self.user__.get().encode()
          password=self.passwd.get().encode()
          data_base=self.data_base.get().encode()
          #cryptage
          host = self.crypter.encrypt(host).decode()
          user = self.crypter.encrypt(user).decode()
          password = self.crypter.encrypt(password).decode()
          data_base = self.crypter.encrypt(data_base).decode()
          liste=[user,host,password,data_base,1]

          self.cursor.execute('''update db_config set user=?,host=?,passwd=?,data_base_name=? where id=?''',liste)
          self.conn.commit()
          self.init_values()
          showinfo("Enregistrement",'enregistrer avec succes')
if __name__=='__main__':
   Db_and_user()