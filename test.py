from tkinter import *
import tkinter.ttk as ttk
import awesometkinter as atk
from fonction_commune import *
from ttkthemes import ThemedTk
f=ThemedTk()
f.get_themes()
#f.set_theme('alt')
x=300
y=300
st=ttk.Style()
st.configure('BW.TButton',background='#7cb62f',foreground='#fff')
t=atk.RadialProgressbar(f,bg='#2642EB',fg='yellow', text_fg='red')
t.pack(pady=5)
t.start()
z=ttk.Progressbar(f)
z.pack(pady=5)
z.start()
b=Button(f,text='button simple',).pack(pady=5)
ttk.Button(f,text='ttk button').pack(pady=5)
atk.Button3d(f,text='atk button 3d').pack(pady=5)
centrer(f,x,y)
f.mainloop()