#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Ing Mackby
#
# Created:     25/02/2021
# Copyright:   (c) Ing Mackby 2021
# Licence:     <your licence>
#----------------------------------------------------------------------------
from tkinter import*
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from datetime import date
#instantition de la fenetre
root=Tk()
root.title("ECKOGAM_BANK")
root.geometry("900x500")

#les notebook,les fenetres

def update(rows):
    table_etudiant.delete(*table_etudiant.get_children())
    for i in rows:
        table_etudiant.insert('','end',values=i)
def insert():
    id=entry_id.get()
    nom=entry_nom.get()
    prenom=entry_prenom.get()
    classe=entry_classe.get()
    query="INSERT INTO Etudiant(Id,Nom,Prenom,Classe) VAlUES(%s,%s,%s,%s)"
    val=(id,nom,prenom,classe)
    cursor.execute(query,val)
    mysqldb.commit()
    show()

    show()
def show():
    query="SELECT Id,Nom,Prenom,Classe FROM Etudiant"
    cursor.execute(query)
    rows=cursor.fetchall()
    update(rows)

def modifier():
    nom=entry_nom.get()
    prenom=entry_prenom.get()
    classe=entry_classe.get()
    id=entry_id.get()
    query="UPDATE Etudiant SET Nom=%s,Prenom=%s,Classe=%s WHERE Id=%s"
    val=(nom,prenom,classe,id)
    cursor.execute(query,val)
    mysqldb.commit()
    show()
def effacer():

    id=entry_id.get()
    if id=="":
        messagebox.showerror("Important","Vous n'avez pas donné Id du client a supprimer")

    else:
        query="DELETE FROM Etudiant WHERE Id= "+id
        cursor.execute(query)
        mysqldb.commit()
        messagebox.showinfo("Important","suppression reussir")

        show()


mysqldb=mysql.connector.connect(host="192.168.43.82",user="root",password="",database="college_prive",port=3306)
cursor=mysqldb.cursor()

notebook=ttk.Notebook(root)

fenetre1= Frame(notebook,bg="lavender")
fenetre2=Frame(notebook,bg="black")

notebook.add(fenetre1,text="Utilisateur")
notebook.add(fenetre2,text="Administrateur")
notebook.pack(fill="both",expand="yes",padx=10,pady=10)

#les frames Etudiants
etudiant_Frame=LabelFrame(fenetre1,text="Liste des Etudiant",bg="turquoise",font="arial")
etudiant_Frame.pack(fill="both",expand="yes",padx=10,pady=10)
etudiant_command=LabelFrame(fenetre1,text="Ajouter Un etudiant",bg="lavender")
etudiant_command.pack(fill="both",expand="yes")

#table

scale=Scrollbar(etudiant_Frame)
scale.pack(side=RIGHT,fill=Y)
table_etudiant=ttk.Treeview(etudiant_Frame,yscrollcommand=scale.set,columns=(1,2,3,4),show="headings",height=4)

table_etudiant.pack(fill="both",expand="yes")
scale.config(command=table_etudiant.yview)

table_etudiant.heading(1,text="Id")
table_etudiant.heading(2,text="Nom")
table_etudiant.heading(3,text="Prenom")
table_etudiant.heading(4,text="Classe")
query="SELECT Id,Nom,Prenom,Classe FROM Etudiant"
cursor.execute(query)
rows=cursor.fetchall()
update(rows)

#les text saisie pour fenetre1 et etudiantFrame 2
label_id=Label(etudiant_command,text="Id")
label_id.grid(row=1,column=0,padx=10,pady=20)
entry_id=Entry(etudiant_command)
entry_id.grid(row=1,column=1,padx=10,pady=10)

label_nom=Label(etudiant_command,text="Nom")
label_nom.grid(row=2,column=0,padx=10,pady=10)
entry_nom=Entry(etudiant_command)
entry_nom.grid(row=2,column=1,padx=10,pady=10)

label_prenom=Label(etudiant_command,text="Prenom")
label_prenom.grid(row=3,column=0,padx=10,pady=10)
entry_prenom=Entry(etudiant_command)
entry_prenom.grid(row=3,column=1,padx=10,pady=10)

label_classe=Label(etudiant_command,text="Classe")
label_classe.grid(row=4,column=0,padx=10,pady=10)
entry_classe=Entry(etudiant_command)
entry_classe.grid(row=4,column=1,padx=10,pady=10)

btchek=Checkbutton(etudiant_command, text="Masculin")

btchek.grid(row=1,column=2,padx=10,pady=10)

btchekGason=Checkbutton(etudiant_command,text="Feminin")
today=date.today()
labeldate=Label(etudiant_command,text=today,font=("Helvetica",12))
labeldate.grid(row=1,column=3,pady=10,padx=10)


btchekGason.grid(row=1,column=3)
sp=Spinbox(etudiant_command,from_=10,to=100)
#sp.grid(row=2,column=10)

bout_Enregister=Button(etudiant_command,command=insert,text="Enregistrer",bg="TURQUOISE")
bout_Enregister.grid(row=5,column=0,padx=10,pady=10)

bout_Modifier=Button(etudiant_command,command=modifier, text="Modifier",bg="TURQUOISE")
bout_Modifier.grid(row=5,column=1,padx=10,pady=10)

bout_Supprimer=Button(etudiant_command,command=effacer,text="Supprimer",bg="TURQUOISE")
bout_Supprimer.grid(row=5,column=2,padx=10,pady=10)

root.mainloop()

