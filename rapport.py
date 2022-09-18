from tkinter import *
from tkcalendar import DateEntry
import babel.numbers
import tkinter.ttk as ttk
from tkinter.messagebox import *
from prettytable import from_db_cursor
from fonction_commune import *
from utilisateur import Utilisateur
import os
class Rapport:
      def __init__(self,page_5,poste,user):
          try:
              os.mkdir('rapport')
          except:
              pass
          #----------------db--------------
          self.connection=db_connect()
          self.cursor = self.connection.cursor()
          self.cursor_2 = self.connection.cursor()
          #--------------------------------------
          header=LabelFrame(page_5,text='Rapport',bg='#fff')
          header.grid(row=0,padx=3,ipady=1,sticky=W,pady=30)
          self.date=DateEntry(header,date_pattern='y/mm/dd')
          self.date.grid(row=0,padx=5)
          liste=['Tout','Depot','Retrait','Transfert']
          self.db_table=ttk.Combobox(header,value=liste)
          self.db_table.grid(row=0,column=1,padx=5)
          self.imprimer=ttk.Button(header,text='',command=self.impression)
          self.imprimer.grid(row=0,column=2)
          middle=LabelFrame(page_5,text="Gestion utilisateur",bg='#fff')
          middle.grid(row=1)
          self.init_values()
          Utilisateur(middle,poste,user)
      def createFolder(self):
          try:
              os.mkdir(os.path.expanduser("~\desktop\\Rapport"))
          except:
              pass
      def ifRapportExist(self,filename):
          if os.path.exists(filename):
              os.remove(filename)
          else:
              pass

      def impression(self):
          self.createFolder()
          db_table=self.db_table.get()
          print(db_table)
          date=self.date.get()
          if db_table=='Tout':
             #depot
             self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
             self.cursor.execute('select * from depot where date_=%s',[date])
             mytable = from_db_cursor(self.cursor)
             self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
             self.cursor.execute("select sum(montant_depose) as total from depot where date_=%s", [date])
             sum_table = from_db_cursor(self.cursor)
             path_file="Tout "+str(date)+'.txt'
             path_file=path_file.replace('/','_')
             path_file=os.path.expanduser("~\desktop\\Rapport\\") + path_file
             self.ifRapportExist(path_file)
             with open(path_file,'a') as rapport_file:
                  rapport_file.write("                                   Caisse Populaire de l'amitier\n")
                  rapport_file.write("                                               CPA\n")
                  rapport_file.write("\n")
                  rapport_file.write("                                               DEPOT\n")
                  rapport_file.write("\n")
                  rapport_file.write(str(mytable)+"\n")
                  rapport_file.write(str(sum_table)+"\n")
                  #retrait
                  self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
                  self.cursor.execute('select * from retrait where date_=%s', [date])
                  mytable = from_db_cursor(self.cursor)
                  rapport_file.write("                                               RETRAIT\n")
                  rapport_file.write("\n")
                  rapport_file.write(str(mytable) + "\n")
                  self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
                  self.cursor.execute("select sum(montant_retirer) as Total from retrait where date_=%s", [date])
                  sum_table = from_db_cursor(self.cursor)
                  rapport_file.write(str(sum_table))
                  #transfert
                  self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
                  self.cursor.execute('select * from transfert where date_=%s', [date])
                  mytable = from_db_cursor(self.cursor)
                  self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
                  self.cursor.execute("select sum(montant) as Total from transfert where date_=%s", [date])
                  sum_table = from_db_cursor(self.cursor)
                  rapport_file.write("                                               TRANSFERT\n")
                  rapport_file.write("\n")
                  rapport_file.write(str(mytable) + "\n")
                  rapport_file.write(str(sum_table)+"\n")
             os.startfile(os.path.abspath(path_file),'print')
             showinfo('info','Impression terminer')

          elif db_table=='Depot':
            self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
            self.cursor.execute('select * from depot where date_=%s', [date])
            mytable = from_db_cursor(self.cursor)
            path_file = "Depot " + str(date) + '.txt'
            path_file = path_file.replace('/', '_')
            path_file = os.path.expanduser("~\desktop\\rapport\\" + path_file)
            self.ifRapportExist(path_file)
            self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
            self.cursor.execute("select sum(montant_depose) as total from depot where date_=%s",[date])
            sum_table = from_db_cursor(self.cursor)
            with open(path_file, 'a') as rapport_file:
                  rapport_file.write("                                   Caisse Populaire de l'amitier\n")
                  rapport_file.write("                                               CPA\n")
                  rapport_file.write("\n")
                  rapport_file.write("                                               DEPOT\n")
                  rapport_file.write("\n")
                  rapport_file.write(str(mytable) + "\n")
                  rapport_file.write(str(sum_table))

            os.startfile(os.path.abspath(path_file), 'print')
            showinfo('info', 'Impression terminer')
          elif db_table=='Retrait':
              self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
              self.cursor.execute('select * from retrait where date_=%s', [date])
              mytable = from_db_cursor(self.cursor)
              self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
              self.cursor.execute("select sum(montant_retirer) as Total from retrait where date_=%s",[date])
              sum_table = from_db_cursor(self.cursor)
              path_file = "Retrait " + str(date) + '.txt'
              path_file = path_file.replace('/', '_')
              path_file = os.path.expanduser("~\\desktop\\rapport\\" + path_file)
              self.ifRapportExist(path_file)
              with open(path_file, 'a') as rapport_file:
                  rapport_file.write("                                   Caisse Populaire de l'amitier\n")
                  rapport_file.write("                                               CPA\n")
                  rapport_file.write("\n")
                  rapport_file.write("                                               RETRAIT\n")
                  rapport_file.write("\n")
                  rapport_file.write(str(mytable) + "\n")
                  rapport_file.write(str(sum_table)+"\n")
              os.startfile(os.path.abspath(path_file), 'print')
              showinfo('info', 'Impression terminer')
          elif db_table=='Transfert':
              self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
              self.cursor.execute('select * from transfert where date_=%s', [date])
              mytable = from_db_cursor(self.cursor)
              self.connection, self.cursor = setConnAndCursor(self.connection, self.cursor)
              self.cursor.execute("select sum(montant) as Total from transfert where date_=%s",[date])
              sum_table = from_db_cursor(self.cursor)
              path_file = "Transfer " + str(date) + '.txt'
              path_file = path_file.replace('/', '_')
              path_file = os.path.expanduser("~\\desktop\\rapport\\" + path_file)
              self.ifRapportExist(path_file)
              with open(path_file, 'a') as rapport_file:
                  rapport_file.write("                                   Caisse Populaire de l'amitier\n")
                  rapport_file.write("                                               CPA\n")
                  rapport_file.write("\n")
                  rapport_file.write("                                               Transfer\n")
                  rapport_file.write("\n")
                  rapport_file.write(str(mytable) + "\n")
                  rapport_file.write(str(sum_table)+"\n")
              os.startfile(os.path.abspath(path_file), 'print')
              showinfo('info', 'Impression terminer')
          else:
              showerror('Avertissement','Erreur')
      def init_values(self):
          self.db_table.set('Tout')
          self.imprimer['text']='Imprimer'
if __name__=='__main__':
   f=Tk()
   x=800
   y=500
   centrer(f,x,y)
   Rapport(f,'','')
   f.mainloop()