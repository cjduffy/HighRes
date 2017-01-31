#!/usr/bin/env python

from tkinter import *

from tkinter import messagebox

top=Tk()
top.geometry = ('100x100')
def helloCallBack():
		msg=messagebox.showinfo("Hello Everyone", "Hello")

B=Button(top, text = "Hello", command= "return" )
B.place(x=50, y=50)
top.mainloop()
