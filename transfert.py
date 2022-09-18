from tkinter import *
import fontawesome
import tkinter.ttk as ttk
from fonction_commune import *
from tkinter.messagebox import *
from  datetime import datetime

from inscription import Inscription


class Transfert:
      def __init__(self,page_2,context):
          # ---------------------db------------------------
          self.connection = db_connect()
          self.cusor = self.connection.cursor()
          # --------------------------------------------------
          self.context = context
          self.id_selected = None
          self.montant_depose = None
          self.code_client_depositaire = None
          self.code_client_recepteur = None
          body=Frame(page_2,bg='#fff')
          body.pack(fill=BOTH)
          header=Frame(body,bg='#fff')
          header.pack(anchor=E)
          middle=Frame(body,bg='#fff')
          middle.pack(fill=BOTH)
          footer=Frame(body,bg='#fff')
          footer.pack(fill=BOTH)
          self.rechercher=StringVar()
          self.rechercher.set('Recherche')
          search = ttk.Entry(header,textvariable=self.rechercher,width=35)
          search.grid(row=0,pady=5,padx=5)
          search.bind('<Motion>', self.click_on_search)
          search.bind('<Leave>', self.leave_search)
          ttk.Button(header,text=fontawesome.icons['search']+" Recherche",command=self.search_bar).grid(row=0,column=1)
          self.numero_de_compte_du_depositaire=StringVar()
          ncd = ttk.Entry(middle,textvariable=self.numero_de_compte_du_depositaire,width=35)
          ncd.grid(row=0,padx=5,sticky=W)
          ncd.bind('<Motion>', self.click_on_ncd)
          ncd.bind('<Leave>', self.leave_ncd)
          #ttk.Button(middle, text='Transferer', command=self.transfert).grid(row=2, sticky=W, padx=3)
          # ----------------------------Table-------------
          self.numero_de_compte_du_recepteur=StringVar()
          ncr = ttk.Entry(middle,textvariable=self.numero_de_compte_du_recepteur,width=35)
          ncr.grid(row=0,column=1,sticky=W)
          ncr.bind('<Motion>', self.click_on_ncr)
          ncr.bind('<Leave>', self.leave_ncr)
          #ttk.Button(middle, text='Transferer', command=self.transfert).grid(row=2, sticky=W, padx=3)
          # ----------------------------Table-------------
          self.montant=StringVar()
          montant = ttk.Entry(middle,width=25,textvariable=self.montant)
          montant.grid(row=1,pady=10,sticky=W,padx=5)
          montant.bind('<Motion>', self.click_on_montant)
          montant.bind('<Leave>', self.leave_montant)
          bbox = Frame(middle)
          bbox.grid(row=2,sticky=W)
          ttk.Button(bbox,text='Transferer',command=self.transfert).grid(row=2,sticky=W,padx=3)
          ttk.Button(bbox, text='Annulee le transfer', command=self.canceltransfert).grid(row=2,column=1, sticky=W, padx=3)
          #----------------------------Table---------------------
          self.table=ttk.Treeview(footer)
          self.table['column']=('depositaire','recepteur','montant','heure','date',"numero_du_depositaire",'numero_du_recepteur')
          self.table.heading('#0',text="ID")
          self.table.column('#0',width=70)
          self.table.heading('depositaire',text='Depositaire')
          self.table.column('depositaire',width=80,anchor=CENTER)
          self.table.heading('recepteur',text='Recepteur')
          self.table.column('recepteur',width=80,anchor=CENTER)
          self.table.heading("montant",text='Montant')
          self.table.column('montant',width=80,anchor=CENTER)
          self.table.heading('heure',text='Heure')
          self.table.column('heure',width=80,anchor=CENTER)
          self.table.heading('date',text='Date')
          self.table.column('date',width=80,anchor=CENTER)
          self.table.heading('numero_du_depositaire',text='Numero du depositaire')
          self.table.column('numero_du_depositaire',width=130,anchor=CENTER)
          self.table.heading('numero_du_recepteur',text='Numero du recepteur')
          self.table.column('numero_du_recepteur',width=160,anchor=CENTER)
          self.table.pack(side=LEFT,padx=5,)
          self.table.pack_propagate(0)
          self.table.tag_configure('pair', background='#fff', foreground='black')
          self.table.tag_configure('impair', background='#888', foreground='#fff')
          self.table.bind('<<TreeviewSelect>>', self.selection_on_table)
          scroll_bar_y=Scrollbar(footer,orient=VERTICAL,command=self.table.yview())
          scroll_bar_y.pack(side=LEFT,fill=Y)
          self.table.configure(yscrollcommand=scroll_bar_y.set)
          self.afficher()
          self.init_value()

      def selection_on_table(self, *args):
          row = self.table.selection()
          for item in row:
              self.id_selected = self.table.item(item, 'text')
              self.code_client_depositaire = self.table.item(item, 'values')[5]
              self.code_client_recepteur = self.table.item(item, 'values')[6]
              self.montant_depose = float(self.table.item(item, 'values')[2])
          print(self.montant_depose)
      def canceltransfert(self):
          montant_recepteur = self.getMontant(self.code_client_recepteur)
          montant_depositaire = self.getMontant(self.code_client_depositaire)
          # insertion du montant actuel dans le compte
          new_montant = float(montant_depositaire) + float(self.montant_depose)
          self.connection, self.cusor = setConnAndCursor(self.connection, self.cusor)
          sql = 'update compte set montant=%s where code=%s'
          self.cusor.execute(sql, [new_montant, self.code_client_depositaire])
          self.connection.commit()
          # insertion du montant actuel dans le compte
          new_montant = float(montant_recepteur) - float(self.montant_depose)
          self.connection, self.cusor = setConnAndCursor(self.connection, self.cusor)
          sql = 'update compte set montant=%s where code=%s'
          self.cusor.execute(sql, [new_montant, self.code_client_recepteur])
          self.connection.commit()
          # delete depot from table
          self.connection, self.cusor = setConnAndCursor(self.connection, self.cusor)
          sql = 'delete from transfert where id=%s'
          self.cusor.execute(sql, [self.id_selected])
          self.connection.commit()
          self.afficher()
          print(montant_depositaire)


      def getMontant(self,code):
          self.connection, self.cusor = setConnAndCursor(self.connection, self.cusor)
          # recuperer le montant du compte
          self.cusor.execute("select montant from compte where code=%s", [code])
          montant_actuel = self.cusor.fetchall()[0][0]
          return montant_actuel

      def leave_montant(self, *args):
          text = self.montant.get()
          if text == '':
              self.montant.set('montant a tranferé')

      def click_on_montant(self, *args):
          text = self.montant.get()
          if text == 'montant a tranferé':
              self.montant.set('')
      def leave_search(self, *args):
          text = self.rechercher.get()
          if text == '':
              self.rechercher.set('Recherche')

      def click_on_search(self, *args):
          text = self.rechercher.get()
          if text == 'Recherche':
              self.rechercher.set('')
      def leave_ncd(self, *args):
          text = self.numero_de_compte_du_depositaire.get()
          if text == '':
              self.numero_de_compte_du_depositaire.set('Numero du compte depositaire')

      def click_on_ncd(self, *args):
          text = self.numero_de_compte_du_depositaire.get()
          if text == 'Numero du compte depositaire':
              self.numero_de_compte_du_depositaire.set('')
      def leave_ncr(self, *args):
          text = self.numero_de_compte_du_recepteur.get()
          if text == '':
              self.numero_de_compte_du_recepteur.set('Numero de compte du recepteur')

      def click_on_ncr(self, *args):
          text = self.numero_de_compte_du_recepteur.get()
          if text == 'Numero de compte du recepteur':
              self.numero_de_compte_du_recepteur.set('')
      def getInfo(self,code):
          self.connection, self.cusor = setConnAndCursor(self.connection, self.cusor)
          self.cusor.execute('select nom,prenom from compte where code=%s', [code])
          info = self.cusor.fetchall()[0]
          info = ' '.join(info)
          return info
      def transfert(self):
          self.connection, self.cusor = setConnAndCursor(self.connection, self.cusor)
          code_depositaire= self.numero_de_compte_du_depositaire.get()
          montant=float(self.montant.get())
          code_recepteur=self.numero_de_compte_du_recepteur.get()
          # depo_name = self.getInfo(code_depositaire)
          # rep_name = self.getInfo(self.code_client_recepteur)
          #---depositaire
          # if number account exist
          self.cusor.execute('select montant from compte where code=%s', [code_depositaire])
          row = self.cusor.fetchall()
          if len(row) > 0:
             montant_depositaire=float(row[0][0])
             # ---recepteur
             self.cusor.execute('select montant from compte where code=%s', [code_recepteur])
             row = self.cusor.fetchall()
             if len(row) > 0:
                    montant_recepteur = float(row[0][0])
                    # ---update depositaire and recepteur
                    #depositaire
                    montant_compte_depositaire=montant_depositaire - montant
                    self.cusor.execute("update compte set montant=%s where code=%s",[montant_compte_depositaire,code_depositaire])
                    self.connection.commit()
                    #recepteur
                    montant_compte_recepteur = montant_recepteur + montant
                    self.cusor.execute("update compte set montant=%s where code=%s",[montant_compte_recepteur, code_recepteur])
                    self.connection.commit()
                    #save transfert
                    self.cusor.execute('select nom,prenom from compte where code=%s',[code_depositaire])
                    info_depositaire=self.cusor.fetchall()[0]
                    info_depositaire='_'.join(info_depositaire)
                    #info recepteur
                    self.cusor.execute('select nom,prenom from compte where code=%s', [code_recepteur])
                    info_recepteur = self.cusor.fetchall()[0]
                    info_recepteur = '_'.join(info_recepteur)
                    heure=datetime.now().time()
                    date=datetime.now().date()
                    liste=[info_depositaire,info_recepteur,montant,heure,date,code_depositaire,code_recepteur]
                    self.cusor.execute("insert into transfert(nom_depositaire,nom_recepteur,montant,heure,date_,numero_compte_depositaire,numero_compte_recepteur) values(%s,%s,%s,%s,%s,%s,%s)",liste)
                    self.connection.commit()
                    self.afficher()
                    self.init_value()
                    showinfo('info',"Argent transferer avec succes")

             else:
                 showwarning('Erreur', "le numero de compte du recepteur n'existe pas")


          else:
              showwarning('Erreur', "Ce numero de compte n'existe pas")
      def search_bar(self):
          self.connection, self.cusor = setConnAndCursor(self.connection, self.cusor)
          self.table.delete(*self.table.get_children())
          word = self.rechercher.get()
          self.cusor.execute('select * from transfert where id=%s', [word])
          rows = self.cusor.fetchall()
          i = 0
          for row in rows:
              self.table.insert('', i, i, text=row[0], values=('', row[2], row[3], row[4], row[5], row[6]))
              i += 1
      def afficher(self):
          self.connection, self.cusor = setConnAndCursor(self.connection, self.cusor)
          self.table.delete(*self.table.get_children())
          self.cusor.execute('select * from transfert')
          rows=self.cusor.fetchall()
          i=0
          for row in rows:
              if i%2==0:
                 self.table.insert('',i,i,text=row[0],values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7]),tags='pair')
              else:
                  self.table.insert('', i, i, text=row[0],
                                    values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7]), tags='impair')
              i+=1
          Inscription.afficher(self.context)
          self.init_value()

      def init_value(self):
          self.numero_de_compte_du_depositaire.set('Numero du compte depositaire')
          self.montant.set("montant a tranferé")
          self.numero_de_compte_du_recepteur.set('Numero de compte du recepteur')
if __name__=='__main__':
   f=Tk()
   x=800
   y=500
   centrer(f,x,y)
   Transfert(f)
   f.mainloop()
