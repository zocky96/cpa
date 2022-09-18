from tkinter import *
from ttkthemes import ThemedTk,ThemedStyle
import tkinter.ttk as ttk
from inscription import Inscription
from depot import Depot
from retrait import Retrait
from transfert import Transfert
from rapport import Rapport
from autres import Autres
from fonction_commune import *
from functools import partial
from update import Update
from tkinter.messagebox import *
import fontawesome as fa
class Menu_:
    def __init__(self,poste,signature,user):
        self.connection = db_connect()
        self.cursor = self.connection.cursor()
        self.fenetre = ThemedTk()
        self.signature = signature
        self.fenetre.config(bg='#fff')
        self.fenetre.get_themes()
        self.fenetre.set_theme('clam')
        self.fenetre.title('Menu')
        self.fenetre.iconbitmap("images/icons/menu icon.ico")
        width = 820
        height = 695
        body=Frame(self.fenetre,bg='#fff')
        body.pack(fill=BOTH)
        header = Frame(body,bg='#fff')
        header.pack(fill=X)
        footer = Frame(body,bg='#fff')
        footer.pack(side=BOTTOM, fill=X)
        # ---------------------menu bar------------------------#
        menu_bar = Menu(self.fenetre)
        menu_1 = Menu(menu_bar, tearoff=0)
        # menu_1.add_command(label="Connecte")
        menu_1.add_command(label="deconnecté", command=partial(self.deconnecte, self.fenetre))
        menu_bar.add_cascade(label="Connexion", menu=menu_1)
        # ----------------- propos-------------------------
        menu_2 = Menu(menu_bar, tearoff=0)
        # menu_2.add_command(label="aide")
        menu_bar.add_cascade(label="A propos", menu=menu_2)

        # ------------------------ mise a jour -------------------#
        menu_3 = Menu(menu_bar, tearoff=0)
        menu_3.add_command(label="mise a jour",command=self.update_app)
        menu_bar.add_cascade(label='Aide', menu=menu_3)
        centrer(self.fenetre, width, height)
        Label(header,text="Caisse Populaire de l'amitie",font=('arial',16),bg='#fff').pack()
        Label(header, text="(CPA)", font=('arial', 14),bg='#fff').pack()
        style=ttk.Style()
        style.configure("BW.TNotebook",background='red')
        onglet = ttk.Notebook(header,)
        onglet.pack(fill=BOTH)
        page_1 = Frame(onglet,bg='#fff')
        page_2 = Frame(onglet,bg='#fff')
        page_3 = Frame(onglet,bg='#fff')
        page_4 = Frame(onglet,bg='#fff')
        page_5 = Frame(onglet,bg="#fff")
        page_6=Frame(onglet,bg='#fff')
        onglet.add(page_1, text='Inscription       ')
        onglet.add(page_2, text='Depot         ')
        onglet.add(page_3, text='Retrait       ')
        onglet.add(page_4, text='Transfert       ')
        onglet.add(page_5, text='Rapport et Gestion utilisateur       ')
        #onglet.add(page_6,text='Autres       ')
        status_bar = Frame(self.fenetre, relief=SUNKEN, bd=1,height=10,bg='#fff')
        status_bar.pack(side=BOTTOM, anchor=W, fill=X,ipady=5)
        Label(status_bar, text='Status : ',bg='#fff').pack(side=LEFT)
        Label(status_bar, text='Connecté '+fa.icons['check'], fg='green',bg='#fff').pack(side=LEFT)
        centrer(self.fenetre, width, height)
        self.fenetre.config(menu=menu_bar)
        self.fenetre.protocol("WM_DELETE_WINDOW", self.fermeture)
        inscription=Inscription(page_1,self.signature)
        context = inscription.context
        depot=Depot(page_2,context)
        retrait=Retrait(page_3,context)
        transfert=Transfert(page_4,context)
        rapport=Rapport(page_5,poste,user)
        #autres=Autres(page_6,self.connection)

        self.fenetre.mainloop()



    def fermeture(self):
        if askyesno('info',"voulez vous fermez la fenetre"):
            self.fenetre.destroy()

    def update_app(self):
        u=Update(self.fenetre,0.0)

    def deconnecte(self,fenetre):
        fenetre.destroy()
        from main import Login
        login=Login()






if __name__=='__main__':
   Menu_('PDG','re','re')
