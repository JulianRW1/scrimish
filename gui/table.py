from tkinter import *

root = Tk()

def myClick():
    myLabel = Label(root, text='You Clicked!')
    myLabel.pack()

mybutton = Button(root, text='click me!', command=myClick)
mybutton.pack()

root.mainloop()