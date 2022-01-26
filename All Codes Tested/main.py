from tkinter import *
# import cv2

root = Tk()
root.title("Best Calculator Ever!!!")

#defining and putting buttons onscreen

myEntry = Entry(root, width = 50, bg="white", fg="black", borderwidth=10)
myEntry.grid(row=0,column=0,columnspan=3, padx=10, pady=10)

button_1 = Button(root, text="1", padx=40, pady=20, bg="white", fg="black", borderwidth=10, command=lambda: buttonClick(1))
button_1.grid(row=3, column=0)

button_2 = Button(root, text="2", padx=40, pady=20, bg="white", fg="black", borderwidth=10, command=lambda: buttonClick(2))
button_2.grid(row=3, column=1)

button_3 = Button(root, text="3", padx=40, pady=20, bg="white", fg="black", borderwidth=10, command=lambda: buttonClick(3))
button_3.grid(row=3, column=2)

button_4 = Button(root, text="4", padx=40, pady=20, bg="white", fg="black", borderwidth=10, command=lambda: buttonClick(4))
button_4.grid(row=2, column=0)

button_5 = Button(root, text="5", padx=40, pady=20, bg="white", fg="black", borderwidth=10, command=lambda: buttonClick(5))
button_5.grid(row=2, column=1)

button_6 = Button(root, text="6", padx=40, pady=20, bg="white", fg="black", borderwidth=10, command=lambda: buttonClick(6))
button_6.grid(row=2, column=2)

button_7 = Button(root, text="7", padx=40, pady=20, bg="white", fg="black", borderwidth=10, command=lambda: buttonClick(7))
button_7.grid(row=1, column=0)

button_8 = Button(root, text="8", padx=40, pady=20, bg="white", fg="black", borderwidth=10, command=lambda: buttonClick(8))
button_8.grid(row=1, column=1)

button_9 = Button(root, text="9", padx=40, pady=20, bg="white", fg="black", borderwidth=10, command=lambda: buttonClick(9))
button_9.grid(row=1, column=2)

button_0 = Button(root, text="0", padx=40, pady=20, bg="white", fg="black", borderwidth=10, command=lambda: buttonClick(0))
button_0.grid(row=4, column=0)

button_plus = Button(root, text = "+", padx=35, pady=15, bg = "white", fg = "black", borderwidth=10, command=lambda: buttonClick("+"))
button_plus.grid(row=4, column=1)

button_minus = Button(root, text = "-", padx=35, pady=15, bg = "white", fg = "black", borderwidth=10, command=lambda: buttonClick("-"))
button_minus.grid(row=4, column=2)

button_times = Button(root, text = "*", padx=35, pady=15, bg = "white", fg = "black", borderwidth=10, command=lambda: buttonClick("*"))
button_times.grid(row=5, column=1)

button_divide = Button(root, text = "/", padx=35, pady=15, bg = "white", fg = "black", borderwidth=10, command=lambda: buttonClick("/"))
button_divide.grid(row=5, column=2)

button_clear = Button(root, text = "clear", padx=35, pady=15, bg = "white", fg = "black", borderwidth=10, command=lambda: buttonClick("clear"))
button_clear.grid(row=5, column=0)

button_equal = Button(root, text="=", padx=150, pady=15, bg="white", fg="black", borderwidth=10, command=lambda: buttonClick("="))
button_equal.grid(row=6, column=0, columnspan=3)

def buttonClick(button):

    global funcao, store

    if button == "=":
        if funcao == "+":
            current = myEntry.get()
            current = store + float(current)
            myEntry.delete(0,END)
            myEntry.insert(0, str(current))

        elif funcao == "*":
            current = myEntry.get()
            current = store * float(current)
            myEntry.delete(0,END)
            myEntry.insert(0, str(current))

        elif funcao == "-":
            current = myEntry.get()
            current = store - float(current)
            myEntry.delete(0,END)
            myEntry.insert(0, str(current))

        elif funcao == "/":
            current = myEntry.get()
            current = store / float(current)
            myEntry.delete(0,END)
            myEntry.insert(0, str(current))

    elif button == "clear":
        current = 0
        myEntry.delete(0, END)

    elif button == "+":
        funcao = "+"
        current = float(myEntry.get())
        store = current
        myEntry.delete(0, END)

    elif button == "*":
        funcao = "*"
        current = float(myEntry.get())
        store = current
        myEntry.delete(0, END)

    elif button == "-":
        funcao = "-"
        current = float(myEntry.get())
        store = current
        myEntry.delete(0, END)

    elif button == "/":
        funcao = "/"
        current = float(myEntry.get())
        store = current
        myEntry.delete(0, END)

    else:
        current = myEntry.get()  # getting number on display
        myEntry.delete(0, END)  # deleting all numbers on display
        myEntry.insert(0, str(current) + str(button))  # displaying the numbers deleted and the last one inserted



root.mainloop()

