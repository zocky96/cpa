import requests
from tkinter import *
from threading import Thread
import os
import awesometkinter as atk
import tkinter.ttk as ttk
from functools import partial
from win10toast import ToastNotifier
from fonction_commune import *
from tkinter.messagebox import *
import sqlite3
from  cryptography.fernet import Fernet
class Update:
      def __init__(self,fenetre_principal,version):
          try:
              os.mkdir('temp')
          except:
              pass
          #---------------- init values ----------------------
          self.total_size=None
          self.file_name=None
          self.progress_value=0
          #----------------------------------------------------
          version=str(version)
          self.update_notifier=False
          version_onfile = self.check_update(version)
          print(version_onfile)
          if float(version) < float(version_onfile):
              fenetre=Toplevel()
              fenetre.config(bg='#fff')
              fenetre.focus()
              fenetre.title('Mise a jour')
              #fenetre.overrideredirect(True)
              #------------------ frames ----------------------
              body=Frame(fenetre,bg='#fff')
              body.pack()
              header=Frame(body,bg='#fff')
              header.pack()
              middle=Frame(body,bg='#fff')
              middle.pack(pady=30)
              footer=Frame(body,bg='#fff')
              footer.pack()
              try:
                 fenetre.transient(fenetre_principal)
              except:
                   pass
              self.update_notifier=True
              x=600
              y=400
              centrer(fenetre,x,y)
              if askyesno("info", "Nouvelle version detecter,acceptez vous de telecharge la mise a jour"):
                  #
                  partie_poucentage=Frame(middle)
                  partie_poucentage.grid(row=0,pady=20)
                  Label(partie_poucentage,text='Telechargement de la mise a jour',bg='#fff',font=('arial',15)).grid(row=0,column=0,sticky=W)
                  self.text_value=StringVar()
                  self.text_value.set('0 %')
                  #text_value=Label(partie_poucentage,textvariable=self.text_value,bg='#fff')
                  #text_value.grid(row=0,column=1,sticky=W)
                  self.progress_bar=atk.RadialProgressbar(middle,bg='yellow',fg='#7cb62f', text_fg='red',size=200)
                  self.progress_bar.grid(row=1)
                  exit_button=ttk.Button(footer,text='exit',command=lambda x:fenetre.destroy())
                  exit_button.grid()
                  self.thread_download_update()
              else:
                  fenetre.destroy()
              fenetre.mainloop()
          elif float(version) == float(version_onfile):
               showinfo("info","vous avez la derniere version")
      def thread_download_update(self):
          t=Thread(target=self.download_update)
          t.start()
      def download_update(self):
          conn = sqlite3.connect('conf/configure.db')
          cursor = conn.cursor()
          cursor.execute('''select host from db_config''')
          host = cursor.fetchall()[0][0]
          key = 'yA1bBtGYWRK85fri8m5BjvbC277YjDdgYLoW8hAVRec='
          crypter = Fernet(key)
          host = crypter.decrypt(bytes(host, 'ascii')).decode()

          url="http://"+host+"/pnh/last version/pnh.exe"
          request_for_download_programme=requests.get(url,stream=True)
          if 'Content-Length' in request_for_download_programme.headers:
              self.total_size=request_for_download_programme.headers['Content-Length']
          try:
              self.file_name=url.split("/")[-1]
          except:
              showerror("erreur","le nom du fichier est introuvavle")
          with open('temp/'+self.file_name,'wb') as file_:
               for part in request_for_download_programme.iter_content(chunk_size=51200):
                   if part:
                      file_.write(part)
                      current_size=os.path.getsize('temp/'+self.file_name)
                      percent= ( int(current_size) * 100 // int(self.total_size))
                      self.text_value.set(str(percent)+" %")
                      self.progress_bar.set(int(percent))
                      self.progress_bar.update()
          self.text_value.set(str(100) + " %")
          self.progress_bar.set(value=int(100))
          self.progress_bar.update()
      def check_update(self,version,):
          conn=sqlite3.connect('conf/configure.db')
          cursor=conn.cursor()
          cursor.execute('''select host from db_config''')
          host=cursor.fetchall()[0][0]
          key = 'yA1bBtGYWRK85fri8m5BjvbC277YjDdgYLoW8hAVRec='
          crypter=Fernet(key)
          host=crypter.decrypt(bytes(host,'ascii')).decode()
          version=float(version)
          url = 'http://'+host+'/pnh/version/version.txt'
          version_onfile = requests.get(url)
          version_onfile = version_onfile.text
          return version_onfile
       


if __name__=='__main__':
   Update(0,0.0)