from fonction_commune import *
from tkinter import *
import tkinter.ttk as ttk
from ttkthemes import ThemedTk
from account_recovery.unlock_account import Unlock
class Recovery:
    def __init__(self,fenetre_principal):
        self.fenetre=Toplevel()
        self.fenetre.transient(fenetre_principal)
        self.fenetre.resizable(False,False)
        x=500
        y=200
        body=Frame(self.fenetre)
        body.pack()
        centrer(self.fenetre,x,y)
        style=ttk.Style()
        style.configure("TButton",font=('arial',15),relief=FLAT,background='#7cb62f', foreground='#fff')
        ttk.Button(body,text='Mot de passe oublie',style="TButton").pack(side=LEFT,ipadx=20,ipady=40,padx=10,pady=30)
        ttk.Button(body, text='Compte bloquer',style="TButton",command=self.unlock).pack(side=LEFT,ipadx=20,ipady=40)

        self.fenetre.mainloop()
    def unlock(self):
        u=Unlock(self.fenetre)
if __name__=='__main__':
    fenetre = ThemedTk()
    fenetre.get_themes()
    fenetre.set_theme('clam')
    Recovery(fenetre)
    fenetre.mainloop()