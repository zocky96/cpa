#import ttk
import tkinter.ttk as ttk
from tkinter import *
from tkinter.messagebox import *
from hashlib import sha1
from fonction_commune import *
class Utilisateur:
    def __init__(self,p_fen,poste,user):
        self.my_user_name = user
        self.poste_parametre=poste
        self.fenetre_utilisateur = p_fen
        self.conn=db_connect()
        self.cur=self.conn.cursor()
        try:
           self.cur.execute("create table users(id int primary key auto_increment,nom varchar(255),prenom varchar(255),user varchar(255),poste varchar(255),passwd blob,log_date date,tentative int,blocker varchar(255),email varchar(255),confirm_code varchar(255))")
        except:
            pass
        #self.fenetre_utilisateur.rowconfigure(0, weight=1)
        #self.fenetre_utilisateur.columnconfigure(0, weight=1)
        self.body=Frame(self.fenetre_utilisateur,bg='#fff')
        #self.body.grid(row=0,sticky=NW,padx=5)
        self.body.pack(anchor=W)
        self.header=Frame(self.body,bg='#fff')
        #self.header.grid(row=0,)
        self.header.pack()
        self.middle=Frame(self.body,bg='#fff')
        #self.middle.grid(row=1,sticky='w',padx=5,pady=10)
        self.middle.pack(anchor=W)
        self.footer=Frame(self.body,bg='#fff')
        #self.footer.grid(row=2)
        self.footer.pack()
        self.button_bottom=Frame(self.body)
        self.button_bottom.pack()
        self.action = Frame(self.body,bg='#fff')
        self.action.pack(anchor=E)
        self.log=ttk.Button(self.header,text='')

        self.nom=StringVar()

        nom = ttk.Entry(self.middle,textvariable=self.nom,width=40)
        nom.grid(row=0,sticky='w')
        nom.bind('<Motion>', self.click_on_name)
        nom.bind('<Leave>', self.leave_name)
        self.prenom=StringVar()
        prenom = ttk.Entry(self.middle,textvariable=self.prenom,width=40)
        prenom.grid(row=0,column=1,sticky='w',pady=5,padx=5)
        prenom.bind('<Motion>', self.click_on_prenom)
        prenom.bind('<Leave>', self.leave_prenom)
        self.user=StringVar()
        user = ttk.Entry(self.middle,textvariable=self.user,width=40)
        user.grid(row=2,sticky='w',pady=5)
        user.bind('<Motion>', self.click_on_user)
        user.bind('<Leave>', self.leave_user)
        liste_poste=['PDG','Directeur','Secretaire','Caissier']
        self.poste=ttk.Combobox(self.middle,value=liste_poste,width=38)
        self.poste.grid(row=2,column=1,padx=5,sticky='w')
        if poste == "Caissier":
           self.poste.configure(stat=DISABLED)

        self.password=StringVar()
        passwd = ttk.Entry(self.middle,textvariable=self.password,width=40)
        passwd.grid(row=4,sticky='w')
        passwd.bind('<Motion>', self.click_on_passwd)
        passwd.bind('<Leave>', self.leave_passwd)
        self.confirm_password=StringVar()
        passwdC = ttk.Entry(self.middle,textvariable=self.confirm_password,width=40)
        passwdC.grid(row=4,column=1, sticky='w',padx=5,pady=5)
        passwdC.bind('<Motion>', self.click_on_passwdC)
        passwdC.bind('<Leave>', self.leave_passwdC)
        self.email=StringVar()
        email = ttk.Entry(self.middle,textvariable=self.email,width=40)
        email.grid(row=5,sticky=W)
        email.bind('<Motion>', self.click_on_email)
        email.bind('<Leave>', self.leave_email)
        frame_tree=Frame(self.footer)
        frame_tree.grid(row=2,sticky="w")
        self.tree=ttk.Treeview(frame_tree)
        self.tree['column']=('nom','prenom','user','poste','mot de passe','log date')
        self.tree.heading('#0',text='ID' )
        self.tree.column('#0', width=80,minwidth=120,anchor=CENTER)
        self.tree.column('nom',width=80,minwidth=120,anchor=CENTER)
        self.tree.heading('nom',text='nom')
        self.tree.heading('prenom',text='prenom')
        self.tree.column('prenom', width=80,minwidth=120,anchor=CENTER)
        self.tree.heading('user',text='user')
        self.tree.column('user', width=80,minwidth=120,anchor=CENTER)
        self.tree.heading('poste',text='poste')
        self.tree.column('poste', width=80,minwidth=120,anchor=CENTER)
        self.tree.heading('mot de passe',text='mot de passe')
        self.tree.column('mot de passe', width=80,minwidth=120,anchor=CENTER)
        self.tree.heading('log date',text='log date')
        self.tree.column('log date', width=80,minwidth=120,anchor=CENTER)
        self.tree.pack(side=BOTTOM,pady=4)
        self.tree.pack_propagate(0)
        self.tree.tag_configure('pair', background='#fff', foreground='black')
        self.tree.tag_configure('impair', background='#888', foreground='#fff')
        av_y=Scrollbar(self.tree,orient='vertical',command=self.tree.yview)
        av_y.pack(side=RIGHT,fill=Y)
        av_x=Scrollbar(self.tree,orient='horizontal',command=self.tree.xview)
        av_x.pack(side=BOTTOM,fill=X)
        self.tree.config(xscrollcommand=av_x.set,yscrollcommand=av_y.set)
        self.action=Frame(frame_tree,bg='#fff')
        self.action.pack(side=LEFT)

        enregistrer=ttk.Button(self.action,text='enregistrer',command=self.save)
        enregistrer.pack(pady=5)
        supprimer=ttk.Button(self.button_bottom,text='Supprimer',command=self.supprimer)
        supprimer.grid(row=0,column=0,padx=1)
        modifier=ttk.Button(self.button_bottom,text='Modifier',command=self.update)
        modifier.grid(row=0,column=1)
        if poste =='Caissier' or poste=='Secretaire':
            enregistrer.configure(stat=DISABLED)
            #modifier.configure(stat=DISABLED)
            supprimer.configure(stat=DISABLED)
            self.show_my_info()
        else:
            self.afficherx()
        self.tree.bind('<<TreeviewSelect>>',self.selectionner)

        self.init_values()
        self.fenetre_utilisateur.mainloop()

    def leave_name(self, *args):
        text = self.nom.get()
        if text == '':
            self.nom.set('Nom')

    def click_on_name(self, *args):
        text = self.nom.get()
        if text == 'Nom':
            self.nom.set('')

    def leave_prenom(self, *args):
        text = self.prenom.get()
        if text == '':
            self.prenom.set('Prenom')

    def click_on_prenom(self, *args):
        text = self.prenom.get()
        if text == 'Prenom':
            self.prenom.set('')
    def leave_user(self, *args):
        text = self.user.get()
        if text == '':
            self.user.set('User name')

    def click_on_user(self, *args):
        text = self.user.get()
        if text == 'User name':
            self.user.set('')
    def leave_passwd(self, *args):
        text = self.password.get()
        if text == '':
            self.password.set('Mot de passe')

    def click_on_passwd(self, *args):
        text = self.password.get()
        if text == 'Mot de passe':
            self.password.set('')
    def leave_passwdC(self, *args):
        text = self.confirm_password.get()
        if text == '':
            self.confirm_password.set('confirmer le mot de passe')

    def click_on_passwdC(self, *args):
        text = self.confirm_password.get()
        if text == 'confirmer le mot de passe':
            self.confirm_password.set('')
    def leave_email(self, *args):
        text = self.email.get()
        if text == '':
            self.email.set('Email')

    def click_on_email(self, *args):
        text = self.email.get()
        if text == 'Email':
            self.email.set('')
    def init_values(self):
        self.prenom.set("Prenom")
        self.confirm_password.set("confirmer le mot de passe")
        self.password.set("Mot de passe")
        self.poste.set("Poste")
        self.nom.set("Nom")
        self.user.set("User name")
        self.email.set('Email')
    def update(self):
        nom = self.nom.get()
        prenom = self.prenom.get()
        poste = self.poste.get()
        user = str(self.user.get())
        password = sha1(str(self.password.get()).encode("utf-8")).hexdigest()
        confirm_password = sha1(str(self.confirm_password.get()).encode("utf-8")).hexdigest()

        if password == confirm_password:
            info=[nom,prenom,user,poste,password,self.id_a]
            req = "update users set nom=%s ,prenom=%s ,user=%s ,poste=%s ,passwd=%s where id=%s"
            # print(info)
            self.cur.execute(req,info)
            self.conn.commit()
            self.afficherx()
            self.afficherx()
            showinfo('info','Modifier avec succes')
            self.init_values()
        else:
            showwarning("Avertissement", "Entrez le meme mot de passe dans les deux champs")
    def selectionner(self,*args):
        row=self.tree.selection()
        for nom in row:
            self.id_a=self.tree.item(nom,'text')
            li=self.tree.item(nom,'value')
            self.nom.set(li[0])
            self.prenom.set(li[1])
            self.user.set(li[2])
            self.poste.set(li[3])
            self.password.set(li[4])
            self.confirm_password.set(li[4])

    def supprimer(self):
        info=self.tree.selection()
        for nom in info:
            id=self.tree.item(nom,'text')
            req='delete from users where id=%s'
            self.cur.execute(req,[id])
            self.afficherx()
            self.conn.commit()
            self.afficherx()
            showinfo('info','supprimer avec succes')
    def show_my_info(self):
        self.tree.delete(*self.tree.get_children())
        req = 'select * from users where user=%s'
        self.cur.execute(req,[self.my_user_name])
        rows = self.cur.fetchall()
        n = 0
        for row in rows:
            if n % 2:
                self.tree.insert('', n, n, text=row[0], values=(row[1], row[2], row[3], row[4], row[5]), tags='pair')
            else:
                self.tree.insert('', n, n, text=row[0], values=(row[1], row[2], row[3], row[4], row[5]),
                                 tags='impair')
            n += 1
    def afficherx(self,*args):
        if self.poste_parametre == 'Caissier' or self.poste_parametre == 'Secretaire':
            pass
        else:
            self.tree.delete(*self.tree.get_children())
            req='select * from users'
            self.cur.execute(req)
            rows=self.cur.fetchall()
            n=0
            for row in rows:
                if n%2:
                   self.tree.insert('',n,n,text=row[0],values=(row[1],row[2],row[3],row[4],row[5]),tags='pair')
                else:
                    self.tree.insert('', n, n, text=row[0], values=(row[1], row[2], row[3], row[4], row[5]),
                                     tags='impair')
                n+=1
    def ifUserExist(self,user):
        req = "select * from users where user=%s"
        self.cur.execute(req,[user])
        rows = self.cur.fetchall()
        if len(rows) > 0:
            return True
        else:
            return False

    def save(self):
        nom = self.nom.get()
        prenom = self.prenom.get()
        poste = self.poste.get()
        user = str(self.user.get())
        password = sha1(str(self.password.get()).encode("utf-8")).hexdigest()
        confirm_password = sha1(str(self.confirm_password.get()).encode("utf-8")).hexdigest()
        email=self.email.get()
        user_exist = self.ifUserExist(user)
        if user_exist:
            showwarning("erreur","ce nom d'utilisateur est deja pris")
        else:
            if poste == "Directeur" or poste == "Secretaire" or poste == "Caissier":
                if password == confirm_password:
                   info=[nom,prenom,user,poste,password,0,'False',email]
                   req="insert into users (nom,prenom,user,poste,passwd,tentative,blocker,email) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                   #print(info)
                   self.cur.execute(req,info)
                   self.conn.commit()
                   self.afficherx()
                   showinfo('info','Enregistrer avec succes')
                   self.init_values()
                   self.fenetre_utilisateur.focus()
                else:
                    showwarning("Avertissement","Entrez le meme mot de passe dans les deux champs")
            else:
                showwarning("Avertissement", "Selectionner la poste")









if __name__=='__main__':
    f=Tk()
    x=800
    y=500
    centrer(f,x,y)
    Utilisateur(f,'PDG','')
    f.mainloop()