import threading
import time
from tkinter import *
import tkinter.ttk as ttk
from tkinter.messagebox import *
from fonction_commune import *
import fontawesome as fa
class Inscription:
      def __init__(self, page_1,signature):
          self.context = self
          #--------------------------db-----------------------
          self.connection = db_connect()
          self.cursor = self.connection.cursor()
          #--------------------------------------------------------
          self.show_client=True
          frame_search = Frame(page_1,bg='#fff')
          frame_search.pack(anchor=E,pady=5)
          self.recherche=StringVar()
          self.recherche.set('Recherche')
          search = ttk.Entry(frame_search,width=35,textvariable=self.recherche)
          search.grid(row=0,padx=5)
          search.bind('<Motion>', self.click_on_search)
          search.bind('<Leave>', self.leave_search)
          ttk.Button(frame_search,text=fa.icons['search']+' Recherche',command=self.search).grid(row=0,column=1,padx=1)
          big_body=Frame(page_1,bg='#fff')
          big_body.pack(side=LEFT,fill=BOTH)
          body=Frame(big_body,bg='#fff')
          body.pack(side=LEFT,fill=BOTH)
          en_tete=Frame(body,bg='#fff')
          #en_tete.grid(row=0,sticky=W)
          en_tete.pack(fill=BOTH)

          pied=Frame(body,bg='#fff')
          #pied.grid(row=2,sticky=W)
          pied.pack(fill=BOTH)
          millieu = Frame(body,bg='#fff' )
          # millieu.grid(row=1,sticky=W)
          millieu.pack(anchor=CENTER)

          donnee_personelle=LabelFrame(en_tete,text='Donnees personnel',fg='#888',bg='#fff')
          donnee_personelle.grid()
          self.nom = StringVar()
          nom = ttk.Entry(donnee_personelle, textvariable=self.nom, width=50)
          nom.grid(row=0, padx=5, pady=5)
          nom.bind('<Motion>', self.click_on_name)
          nom.bind('<Leave>', self.leave_name)
          self.prenom = StringVar()
          prenom = ttk.Entry(donnee_personelle, textvariable=self.prenom, width=50)
          prenom.grid(row=0, column=1, )
          prenom.bind('<Motion>', self.click_on_prenom)
          prenom.bind('<Leave>', self.leave_prenom)
          self.nif = StringVar()
          nif = ttk.Entry(donnee_personelle,textvariable=self.nif,width=50)
          nif.grid(row=1,column=0,pady=5)
          nif.bind('<Motion>', self.click_on_nif)
          nif.bind('<Leave>', self.leave_nif)
          self.code=StringVar()
          code = ttk.Entry(donnee_personelle,textvariable=self.code,width=50)
          code.grid(row=1,column=1)
          code.bind('<Motion>', self.click_on_code)
          code.bind('<Leave>', self.leave_code)
          self.telephone = StringVar()
          phone = ttk.Entry(donnee_personelle, textvariable=self.telephone, width=50)
          phone.grid(row=2, column=0)
          phone.bind('<Motion>', self.click_on_phone)
          phone.bind('<Leave>', self.leave_phone)

          self.adresse = StringVar()
          adresse = ttk.Entry(donnee_personelle, textvariable=self.adresse, width=50)
          adresse.grid(row=2,column=1)
          adresse.bind('<Motion>', self.click_on_adresse)
          adresse.bind('<Leave>', self.leave_adresse)
          other_case=LabelFrame(en_tete,text='Personne a contacter',fg='#888',bg='#fff')
          other_case.grid(row=1,pady=10)
          self.nom_secour=StringVar()
          nom_secour = ttk.Entry(other_case,textvariable=self.nom_secour,width=50)
          nom_secour.grid(row=0,padx=5)
          nom_secour.bind('<Motion>', self.click_on_nom_secour)
          nom_secour.bind('<Leave>', self.leave_nom_secour)
          self.telephone_secour=StringVar()
          phone_secour = ttk.Entry(other_case,textvariable=self.telephone_secour,width=50)
          phone_secour.grid(row=0,column=1)
          phone_secour.bind('<Motion>', self.click_on_phone_secour)
          phone_secour.bind('<Leave>', self.leave_phone_secour)
          foot=Frame(en_tete,bg='#fff')
          foot.grid(row=2,pady=5)
          #-------------------------------------
          style=ttk.Style()
          style.configure("WM.TButton",relief=FLAT,background='#7cb62f',foreground='#fff')
          style.configure("TButton", relief=FLAT, background='#7cb62f',foreground='#fff')
          #------------------- button-----------

          ttk.Button(millieu, text='Supprimer',command=self.delete_client,style='WM.TButton').grid(row=0,column=1,padx=5)
          ttk.Button(millieu, text='Modifier',command=self.modifier,style='WM.TButton').grid(row=0,column=2,padx=5)
          #ttk.Button(millieu, text='Refresh', command=self.afficher, style='WM.TButton').grid(row=0, column=3)
          self.signature=StringVar()
          self.signature.set(signature)
          #----------------------------------------------------
          boxCash = Frame(body,bg='#7cb62f')
          boxCash.pack(anchor=W)

          Label(boxCash,text='TOTAL : ',bg="#fff",font=("arial",14)).grid()
          self.total = StringVar()
          Label(boxCash,textvariable=self.total,bg="#fff",fg="#7cb62f",font=("arial",14)).grid(row=0,column=1)
          self.getSumCash()
          #--------------------------------------------------------------------------
          values=['Journalier','Mensuel','Annuel']
          self.type_de_compte=ttk.Combobox(foot,width=27,value=values)
          self.type_de_compte.grid(row=0,column=1,padx=5)
          ttk.Button(foot, text='Enregistrer', command=self.save_client, style="WM.TButton").grid(row=0, column=2)
          table_case=Frame(pied)
          table_case.grid(row=3)
          self.table=ttk.Treeview(table_case)
          self.table['column']=('nom','prenom','montant','nif','telephone','type','signature')
          self.table.heading('#0',text='CODE')
          self.table.column('#0',width=80,minwidth=80,anchor=CENTER)
          self.table.heading('nom',text='Nom')
          self.table.column('nom',width=80,minwidth=100,anchor=CENTER)
          self.table.heading('prenom',text='Prenom')
          self.table.column('prenom', width=80, minwidth=110, anchor=CENTER)
          self.table.heading('montant',text='Montant')
          self.table.column('montant',width=80,minwidth=80,anchor=CENTER)
          self.table.heading('nif',text='Nif')
          self.table.column('nif', width=80, minwidth=80, anchor=CENTER)
          self.table.heading('telephone',text='Telephone')
          self.table.column('telephone', width=80, minwidth=120, anchor=CENTER)
          self.table.heading('type',text='Type de compte')
          self.table.column('type', width=80, minwidth=130, anchor=CENTER)
          self.table.heading('signature',text='Signature autorise')
          self.table.column('signature', width=80, minwidth=90, anchor=CENTER)
          self.table.pack(side=LEFT,fill=BOTH)
          self.table.pack_propagate(0)
          self.table.bind('<<TreeviewSelect>>',self.selection_on_table)
          scroll_bar_y=Scrollbar(table_case,orient=VERTICAL)
          scroll_bar_y.pack(side=RIGHT,fill=Y)
          scroll_bar_x=Scrollbar(self.table,orient=HORIZONTAL,command=self.table.xview)
          self.table.config(xscrollcommand=scroll_bar_x.set,yscrollcommand=scroll_bar_y.set)
          scroll_bar_x.pack(fill=X,side=BOTTOM)
          self.init_values()

          self.afficher()
      def getSumCash(self):
          self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
          self.cursor.execute("select sum(montant) from compte")
          montant = self.cursor.fetchall()[0][0]
          if montant == None:
              montant = 0
          self.total.set(f'{montant} Gourdes')

      def leave_search(self, *args):
          text = self.recherche.get()
          if text == '':
              self.recherche.set('Recherche')

      def click_on_search(self, *args):
          text = self.recherche.get()
          if text == 'Recherche':
              self.recherche.set('')
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
      def leave_nif(self, *args):
          text = self.nif.get()
          if text == '':
              self.nif.set('Nif')

      def click_on_nif(self, *args):
          text = self.nif.get()
          if text == 'Nif':
              self.nif.set('')
      def leave_code(self, *args):
          text = self.code.get()
          if text == '':
              self.code.set('Code')

      def click_on_code(self, *args):
          text = self.code.get()
          if text == 'Code':
              self.code.set('')
      def leave_phone(self, *args):
          text = self.telephone.get()
          if text == '':
              self.telephone.set('Telephone')

      def click_on_phone(self, *args):
          text = self.telephone.get()
          if text == 'Telephone':
              self.telephone.set('')
      def leave_adresse(self, *args):
          text = self.adresse.get()
          if text == '':
              self.adresse.set('Adresse')

      def click_on_adresse(self, *args):
          text = self.adresse.get()
          if text == 'Adresse':
              self.adresse.set('')
      def leave_phone_secour(self, *args):
          text = self.telephone_secour.get()
          if text == '':
              self.telephone_secour.set('Telephone')

      def click_on_phone_secour(self, *args):
          text = self.telephone_secour.get()
          if text == 'Telephone':
              self.telephone_secour.set('')
      def leave_nom_secour(self, *args):
          text = self.nom_secour.get()
          if text == '':
              self.nom_secour.set('Nom complet')

      def click_on_nom_secour(self, *args):
          text = self.nom_secour.get()
          if text == 'Nom complet':
              self.nom_secour.set('')
      def init_values(self):
          self.nom.set('Nom')
          self.prenom.set('Prenom')
          self.nif.set('Nif')
          self.code.set('Code')
          self.telephone.set('Telephone')
          self.nom_secour.set('Nom complet')
          self.telephone_secour.set('Telephone')
          self.type_de_compte.set('Type de compte')
          self.adresse.set('Adresse')
      def selection_on_table(self,*args):
          row=self.table.selection()

          for item in row:
              code=self.table.item(item,'text')
              items=self.table.item(item,'values')
              #print(items)
          self.type_de_compte.set(items[5])
          self.nom.set(items[0])
          self.prenom.set(items[1])
          self.nif.set(items[3])
          self.code.set(code)
          self.telephone.set(items[4])
          self.nom_secour.set('')
          self.signature.set(items[6])
          self.telephone_secour.set('Telephone')
          self.nom_secour.set('Nom complet')

      def afficher(self):
          self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
          self.table.delete(*self.table.get_children())
          sql="select * from compte"
          # self.connection.close()
          # self.connection=db_connect()
          # self.cursor=self.connection.cursor()
          self.cursor.execute(sql)
          rows=self.cursor.fetchall()
          i=0
          self.table.tag_configure('pair',background='#fff',foreground='black')
          self.table.tag_configure('impair',background='#888',foreground='#fff')
          for row in rows:
              if i%2==0:
                 self.table.insert('',i,i,text=row[3],values=(row[0],row[1],row[9],row[2],row[4],row[8],row[7]),tags='pair')
              else:
                  self.table.insert('', i, i, text=row[3],values=(row[0],row[1],row[9],row[2],row[4],row[8],row[7]),
                                    tags='impair')
              i+=1
          self.getSumCash()
          self.init_values()


      def search(self):
          self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
          self.table.delete(*self.table.get_children())
          search=self.recherche.get()
          self.cursor.execute("select * from compte where code=%s or nom=%s or prenom=%s or nif=%s or telephone=%s or type_de_compte=%s or signature_autorise=%s",[search,search,search,search,search,search,search])
          rows=self.cursor.fetchall()

          i=0
          if len(rows) > 0:
              for row in rows:
                  self.table.insert('', i, i, text=row[3], values=(row[0], row[1], row[9], row[2], row[4], row[8], row[7]),tags='pair')
                  i+=1
          else:
              showwarning('erreur', "ce code n'existe pas")



      def modifier(self):
          self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
          nom=self.nom.get()
          prenom=self.prenom.get()
          nif=self.nif.get()
          code=self.code.get()
          telephone=self.telephone.get()
          nom_secours=self.nom_secour.get()
          signature=self.signature.get()
          telephone_secours=self.telephone_secour.get()
          type_de_compte=self.type_de_compte.get()
          liste=[nom,prenom,nif,telephone,nom_secours,telephone_secours,signature,type_de_compte,code]
          sql='update compte set nom=%s,prenom=%s,nif=%s,telephone=%s,nom_personne_a_contacter=%s,telephone_personne_a_contacte=%s,signature_autorise=%s,type_de_compte=%s where code=%s'
          self.cursor.execute(sql,liste)
          self.connection.commit()
          self.afficher()
          showinfo('info','Modifier avec succes')
      def delete_client(self):
          self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
          row = self.table.selection()
          for item in row:
              code = self.table.item(item, 'text')
              items = self.table.item(item, 'values')
          nom=items[0]
          prenom=items[1]
          nif=items[2]
          telephone=items[3]
          #nom_secours=self.nom_secour.get()
          signature=items[5]
          #telephone_secours=self.telephone_secour.get()
          type_de_compte=items[4]
          liste = [nom, prenom, nif, code, telephone, signature, type_de_compte]
          # sql = "insert into compte_suprimmer(nom,prenom,nif,code,telephone,signature_autorise,type_de_compte) values(%s,%s,%s,%s,%s,%s,%s)"
          # self.cursor.execute(sql, liste)
          # self.connection.commit()
          sql_='delete from compte where code=%s'
          self.cursor.execute(sql_,[code])
          self.connection.commit()
          self.afficher()
          showinfo('info','Suprimmer avec succes')
      def save_client(self):
          self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
          nom=self.nom.get()
          prenom=self.prenom.get()
          nif=self.nif.get()
          code=self.code.get()
          telephone=self.telephone.get()
          nom_secours=self.nom_secour.get()
          signature=self.signature.get()
          telephone_secours=self.telephone_secour.get()
          type_de_compte=self.type_de_compte.get()
          montant_initialise=0.0
          liste=[nom,prenom,nif,code,telephone,nom_secours,telephone_secours,signature,type_de_compte,montant_initialise]
          try:
              sql="insert into compte(nom,prenom,nif,code,telephone,nom_personne_a_contacter,telephone_personne_a_contacte,signature_autorise,type_de_compte,montant) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
              self.cursor.execute(sql,liste)
              self.connection.commit()
              showinfo('info','Client enregistrer avec succes')
              self.afficher()
          except Exception as e:
              print(e)
              if str("code") in str(e):
                  showwarning('Avertissement',"Ce code est deja dans la base de donne")
              elif str("nif"):
                  showwarning('Avertissement', "Ce nif est deja dans la base de donne")



if __name__=="__main__":
   f=Tk()
   x=800
   y=500
   centrer(f,x,y)
   f.config(bg='#fff')
   h=Inscription(f,'')
   f.mainloop()