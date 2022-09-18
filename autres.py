from tkinter import *
import tkinter.ttk as ttk
import awesometkinter as atk
from fonction_commune import *
class Autres:
      def __init__(self,fenetre):
          prog=atk.RadialProgressbar(fenetre)
          prog.grid(row=1)
if __name__=='__main__':
   f=Tk()
   x=800
   y=500
   centrer(f,x,y)
   Autres(f)
   f.mainloop()