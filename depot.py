from tkinter import *
import fontawesome
import tkinter.ttk as ttk
from tkinter.messagebox import *
from fonction_commune import *
from datetime import datetime
from inscription import Inscription
class Depot:
      def __init__(self,page_2,context):
          #---------------------db------------------------
          self.connection = db_connect()
          self.cusor = self.connection.cursor()
          self.context = context
          #--------------------------------------------------
          self.id_selected = None
          self.montant_depose = None
          self.code_client = None
          body=Frame(page_2,bg='#fff')
          body.pack(anchor=W)
          header=Frame(body,bg='#fff')
          header.grid(row=0,sticky=E)
          middle=Frame(body,bg='#fff')
          middle.grid(row=1,sticky=W,pady=10)
          footer=Frame(body,bg='#fff')
          footer.grid(row=2,sticky=W)
          self.rechercher=StringVar()
          self.rechercher.set('Recherche')
          search = ttk.Entry(header,textvariable=self.rechercher,width=35)
          search.grid(row=0,pady=5,padx=5)
          search.bind('<Motion>', self.click_on_search)
          search.bind('<Leave>', self.leave_search)
          ttk.Button(header,text=fontawesome.icons['search']+" Recherche",command=self.recherche_).grid(row=0,column=1)
          self.numero_du_compte=StringVar()
          numeroCompte = ttk.Entry(middle,textvariable=self.numero_du_compte,width=25)
          numeroCompte.grid(row=0,padx=5,sticky=W)
          numeroCompte.bind('<Motion>', self.click_on_accountNum)
          numeroCompte.bind('<Leave>', self.leave_accountNum)
          self.montant=StringVar()
          montant = ttk.Entry(middle,width=25,textvariable=self.montant)
          montant.grid(row=0, column=1,pady=10)
          montant.bind('<Motion>', self.click_on_montant)
          montant.bind('<Leave>', self.leave_montant)
          bbox = Frame(middle)
          bbox.grid(row=1)
          ttk.Button(bbox,text='Deposer',command=self.depot).grid(row=1,sticky=W,padx=3)
          ttk.Button(bbox, text='Annulee le depot', command=self.cancelDepot).grid(row=1,column=1, sticky=W)
          #----------------------------Table---------------------
          self.table_x = ttk.Treeview(footer)
          self.table_x['column']=('CODE', 'nom_complet', 'montant_actuel', 'montant_depose', 'encien_montant', 'heure', 'date')
          self.table_x.heading('#0', text="ID")
          self.table_x.column('#0', width=70)
          self.table_x.heading('CODE', text='CODE')
          self.table_x.column('CODE', width=70, anchor=CENTER)
          self.table_x.heading('nom_complet', text='Nom Complet')
          self.table_x.heading("montant_actuel", text='Montant actuel')
          self.table_x.column('montant_actuel', width=90, anchor=CENTER)
          self.table_x.heading('montant_depose', text='Montant depose')
          self.table_x.column('montant_depose', width=100, anchor=CENTER)
          self.table_x.heading('encien_montant', text='Encien montant')
          self.table_x.column('encien_montant', width=100, anchor=CENTER)
          self.table_x.heading('heure', text='Heure')
          self.table_x.column('heure', width=80, anchor=CENTER)
          self.table_x.heading('date', text='Date')
          self.table_x.column('date', width=80, anchor=CENTER)
          self.table_x.pack(side=LEFT, padx=5, anchor=CENTER)
          self.table_x.bind('<<TreeviewSelect>>', self.selection_on_table)
          self.table_x.tag_configure('pair', background='#fff', foreground='black')
          self.table_x.tag_configure('impair', background='#888', foreground='#fff')
          scroll_bar_y=Scrollbar(footer, orient=VERTICAL, command=self.table_x.yview)
          scroll_bar_y.pack(side=RIGHT,fill=Y)
          self.table_x.configure(yscrollcommand=scroll_bar_y.set)
          self.init_value()

          self.afficher()
      def getReceptorInfo(self,code):
          self.connection, self.cusor = setConnAndCursor(self.connection, self.cusor)
          self.cusor.execute('select nom,prenom from compte where code=%s', [code])
          info_depositaire = self.cusor.fetchall()[0]
          info_depositaire = ' '.join(info_depositaire)
          return info_depositaire

      def selection_on_table(self, *args):
          row = self.table_x.selection()
          for item in row:
              self.id_selected = self.table_x.item(item, 'text')
              self.code_client = self.table_x.item(item, 'values')[0]
              self.montant_depose = self.table_x.item(item, 'values')[3]


          print(self.montant_depose)
      def cancelDepot(self):
          self.connection,self.cusor = setConnAndCursor(self.connection,self.cusor)
          #recuperer le montant du compte
          self.cusor.execute("select montant from compte where code=%s",[self.code_client])
          montant_actuel = self.cusor.fetchall()[0][0]
          if float(montant_actuel) < float(self.montant_depose):
              showwarning("message",f"Vous ne pouverz pas annulee ce depot!\n le compte n'a que {montant_actuel} gourdes")
          else:
              if askyesno('Confirmation',"etes vous sur"):
                  #soustraire le montant actuel du montant deposer
                  new_montant = float(montant_actuel) - float(self.montant_depose)
                  #insertion du montant actuel dans le compte
                  self.connection,self.cusor = setConnAndCursor(self.connection,self.cusor)
                  sql = 'update compte set montant=%s where code=%s'
                  self.cusor.execute(sql,[new_montant,self.code_client])
                  self.connection.commit()
                  #delete depot from table
                  self.connection, self.cusor = setConnAndCursor(self.connection, self.cusor)
                  sql = 'delete from depot where id=%s'
                  self.cusor.execute(sql, [self.id_selected])
                  self.connection.commit()
                  self.afficher()
                  print(new_montant)



      def depot(self):
          self.connection,self.cusor = setConnAndCursor(self.connection,self.cusor)

          if askyesno('info','voulez vous continuer'):
              numero_du_compte=self.numero_du_compte.get()
              nom_complet = self.getReceptorInfo(numero_du_compte)
              try:
                 montant_a_depose=float(self.montant.get())
                 # if number account exist
                 self.cusor.execute('select * from compte where code=%s', [numero_du_compte])
                 row = self.cusor.fetchall()
                 if len(row) > 0:
                     sql = 'select montant from compte where code=%s'
                     self.cusor.execute(sql, [numero_du_compte])
                     ancien_montant = float(self.cusor.fetchall()[0][0])
                     new_montant= ancien_montant + montant_a_depose
                     self.cusor.execute("update compte set montant=%s where code=%s",[new_montant,numero_du_compte])
                     self.connection.commit()
                     heure=datetime.now().time()
                     date=datetime.now().date()
                     print(date)
                     liste=[numero_du_compte,new_montant,montant_a_depose,ancien_montant,heure,date,nom_complet]
                     self.cusor.execute("insert into depot(code,montant_actuel,montant_depose,encient_montant,heure,date_,nom_complet) values(%s,%s,%s,%s,%s,%s,%s)",liste)
                     self.connection.commit()
                     self.afficher()
                     self.init_value()
                     showinfo('info','Depot effectue avec succes')
                 else:
                     showwarning('Erreur', "Ce numero de compte n'existe pas")
              except Exception as e:
                  if "could not convert string to float" in str(e):
                      showwarning("Avertissement","Vous devez mettre de chiffres dans la montans")
      def leave_search(self, *args):
          text = self.rechercher.get()
          if text == '':
              self.rechercher.set('Recherche')

      def click_on_search(self, *args):
          text = self.rechercher.get()
          if text == 'Recherche':
              self.rechercher.set('')
      def leave_accountNum(self, *args):
          text = self.numero_du_compte.get()
          if text == '':
              self.numero_du_compte.set('Numero du compte')

      def click_on_accountNum(self, *args):
          text = self.numero_du_compte.get()
          if text == 'Numero du compte':
              self.numero_du_compte.set('')
      def leave_montant(self, *args):
          text = self.montant.get()
          if text == '':
              self.montant.set('montant à deposé')

      def click_on_montant(self, *args):
          text = self.montant.get()
          if text == 'montant à deposé':
              self.montant.set('')

      def init_value(self):
          self.numero_du_compte.set('Numero du compte')
          self.montant.set("montant à deposé")
      def recherche_(self):
          self.connection, self.cusor = setConnAndCursor(self.connection, self.cusor)
          self.table_x.delete(*self.table_x.get_children())
          word=self.rechercher.get()
          self.cusor.execute('select * from depot where code=%s or id=%s',[word,word])
          rows=self.cusor.fetchall()
          i = 0
          for row in rows:
              self.table_x.insert('', i, i, text=row[0], values=('', row[2], row[3], row[4], row[5], row[6]))
              i += 1
      def afficher(self):
          self.connection, self.cusor = setConnAndCursor(self.connection, self.cusor)
          self.table_x.delete(*self.table_x.get_children())
          self.cusor.execute('select * from depot')
          rows=self.cusor.fetchall()
          print(rows)
          i=0
          for row in rows:
              if i %2==0:
                   self.table_x.insert('', i, i, text=row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7]), tags="pair")
              else:
                  self.table_x.insert('', i, i, text=row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7]),
                                      tags="impair")
              i+=1
          Inscription.afficher(self.context)
          self.init_value()
if __name__=='__main__':
   f=Tk()
   x=800
   y=500
   centrer(f,x,y)
   Depot(f)
   f.mainloop()
