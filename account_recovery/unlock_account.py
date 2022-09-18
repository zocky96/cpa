from tkinter import *
from fonction_commune import *
import tkinter.ttk as ttk
from tkinter.messagebox import *
from ttkthemes import ThemedTk
import sqlite3
import random
import string
class Unlock:
    def __init__(self,fenetre_principal):
        #----------db connect ------------------
        self.connection=db_connect()
        self.cursor=self.connection.cursor()
        #-----------------------------------------------------------
        fenetre=Toplevel()
        #fenetre.transient(fenetre_principal)
        fenetre.config(bg='#fff')
        x=400
        y=400
        self.liste_champs=[]
        self.liste_valeur=[]
        self.header=Frame(fenetre,bg='#fff')
        self.header.pack(pady=20)
        self.middle=Frame(fenetre,bg='#fff')
        self.middle.pack()
        self.footer=Frame(fenetre,bg='#fff')
        self.footer.pack()
        Label(self.header,text='Recuperation du compte',bg='#fff',font=('arial',10)).pack()
        self.email=StringVar()
        self.email.set('Entrer votre adresse mail')
        self.style = ttk.Style()
        self.style.configure("TButton", font=('arial', 15), relief=FLAT, background='#7cb62f', foreground='#fff')
        ttk.Entry(self.header,textvariable=self.email,width=35).pack(pady=10,ipady=2)
        ttk.Button(self.header,text='Envoyer',style='TButton',command=self.get_email).pack()
        centrer(fenetre,x,y)
        fenetre.mainloop()
    def get_email(self):
        self.mail=self.email.get()
        self.cursor.execute('select * from users where email=%s',[self.mail])
        row=self.cursor.fetchall()
        if len(row) > 0:

            self.cursor.execute('select * from users where email=%s and blocker=%s',[self.mail,'True'])
            row=self.cursor.fetchall()
            if len(row) > 0:

                Label(self.middle, text='Entrer le code de verification', bg='#fff', fg='#7cb62f', font=('arial,5')).pack()
                for i in range(6):
                    champ = ttk.Entry(self.middle, width=5)
                    champ.pack(side=LEFT, padx=5, pady=50)
                    self.liste_champs.append(champ)

                ttk.Button(self.footer, text='Valider', style='TButton',command=self.valider).pack()
            else:
                showwarning('info',"ce compte n'est pas bloquer")
        else:
            showwarning('erreur',"cet email n'est pas dans la dase de donnee")

    
    def valider(self):
        for i in self.liste_champs:
            self.liste_valeur.append(i.get())
        valeur=''.join(self.liste_valeur)
        sql="select confirm_code from users where email=%s"

        self.cursor.execute(sql,[self.mail])
        row=self.cursor.fetchall()
        code=row[0][0]
        if str(code)==str(valeur):
            sql="update users set blocker=%s,confirm_code=%s,tentative=%s where email=%s"
            self.cursor.execute(sql,['False','',0,self.mail])
            self.connection.commit()
            showinfo('info','Votre compte a ete debloquer')
        else:
            showerror('Erreur',"le code saisi est incorrect")
if __name__=='__main__':

    Unlock(0)