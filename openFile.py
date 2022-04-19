
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from RushHour import *

def openFile():
    filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                          title="Open file okay?",
                                          filetypes= (("text files","*.txt"),
                                          ("all files","*.*")))
    #print(filepath)
    file = open(filepath,'r')
    print(file.read())
    file.close()
    root.destroy()
    RushH(filepath)

def mainFile():
    print("Entra")
    global root
    
    root = tk.Tk()
    root.config(width=300, height=200)
    root.title("Rush Hour")

    Welcome = tk.Label(text = "    Welcome to Rush Hour Game!    ",
                 font=('arial bold', 18))
    Welcome.pack()

    File = tk.Label(text = "    Select the file of the game you want to resolve.    ",
                 font=('Helvetica roman', 13))
    File.pack()

    boton = tk.Button(
        text="Select file",
        command=openFile,
        bg='#008C33',
        fg='White',
        activebackground='#007A2C',
        activeforeground='White',
        font=('arial bold', 15)).pack(pady=20)
    root.mainloop()

#root.destroy()

