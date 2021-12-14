from tkinter import *
from tkinter import messagebox, filedialog, ttk
from PIL import ImageTk, Image, ImageDraw
import threading
import datetime
import imutils
import os
import cv2
import numpy as np
import dlib
from math import hypot
import time


###############################################################################
###############################################################################
###############################################################################
###############################################################################


def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)



def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
    # hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    # ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)
    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
    ratio = hor_line_lenght / ver_line_lenght
    return ratio


###############################################################################
###############################################################################
###############################################################################
###############################################################################


root = Tk()
root.bind("<Escape>", lambda e: root.quit())
root.title("Facial Matching System")
root.geometry("200x60")

button_root1 = Button(root, text="Register", bg="black", fg="white", borderwidth=10, padx=10, anchor=E, command=lambda: register())
button_root1.grid(row=0, column=0, padx=5, pady=10)
button_root2 = Button(root, text="Scan", bg="black", fg="white", padx=18, borderwidth=10, anchor=W) # command=lambda: scan()    ->     FUNÇAO DE MATCHING FACIAL, FEITA PELO SAMUEL
button_root2.grid(row=0, column=1, padx=5, pady=10)

global img_counter, nome
img_counter = 0

def register():
    global top, cap, label, nome
    top = Toplevel()
    top.title("Facial Matching System Register Window")

    width, height = 800, 600
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    fr = LabelFrame(top, padx=10, pady=10)
    fr.pack(padx=5, pady=5)
    label = Label(fr)
    label.pack()

    nome = Entry(top, width=50)
    nome.pack()
    nome.insert(0, "Enter Your Name Here (DELETE THIS FIRST!!!) ")

    button = Button(top, text="Take Picture!", bg="black", fg="white", borderwidth=10, anchor=S,
                    command=lambda: picture())
    button.pack(anchor=S)
    button = Button(top, text="Quit", bg="black", fg="white", borderwidth=10, anchor=S,
                    command=top.destroy)
    button.pack(anchor=S)

    show_frame()

def show_frame():
    # Get the latest frame and convert into Image
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image=img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    # Repeat after an interval to capture continuously
    label.after(10, show_frame)
    

def picture():
    global img_counter, top, nome, img_name

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    
    photo = False
    
    while not(photo):
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            
            landmarks = predictor(gray, face)
            left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
            right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
            blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
            if blinking_ratio > 5.7:
                time.sleep(1)
                ret, frame = cap.read()
                cv2.imshow("test", frame)
                photo=True
                print('1')
        
        # cv2.imshow("Frame", frame)
        # key = cv2.waitKey(1)
        # if key == 27:
        #     break
    # print('2')
    # cap.release()

    # ret, frame = cap.read()
    # cv2.imshow("test", frame)

    confirmation = messagebox.askquestion("Picture Confirmation", "Do You Accept This Picture?")
    if confirmation == "yes":
        # filename = filedialog.asksaveasfilename(mode="w", defaultextension=".jpg")
        # if not filename:
        #     return
        # edge.save(filename)

        img_name = nome.get() + "_{}.png".format(img_counter) # O PROBLEMA PODE SER NO NOME.GET()? SÓ ADQUIRI DADOS UMA VEZ A CADA DIGITAÇÃO?

        parent_directory = r"C:\Users\user\Desktop\UA\5_Ano\Biometria\Projeto\FaceDetect-master\Faces"

        os.chdir(parent_directory)

        directory = nome.get()
        pics_dir = "Photos"

        if os.path.exists(directory):
            print("User Already Exists But A New Picture Will Be Added!")
            Label(top, text="User Already Exists But A New Picture Will Be Added!").pack()

            path = os.path.join(parent_directory, directory)
            path = os.path.join(path, pics_dir)
            os.chdir(path)

            while os.path.exists(os.path.join(path, img_name)):
                img_counter += 1
                img_name = nome.get() + "_{}.png".format(img_counter)

            cv2.imwrite(img_name, frame)
            nome = print("{} written!".format(img_name))
            Label(top, text=nome).pack()
            Label(top, text="Picture Taken and Saved").pack()
            img_counter += 1


        else:
            print("Creating New User And A New Picture Will Be Added!")
            Label(top, text="Creating New User And A New Picture Will Be Added!").pack()
            path = parent_directory

            while os.path.exists(os.path.join(path, img_name)):
                img_counter += 1
                img_name = nome.get() + "_{}.png".format(img_counter)

            cv2.imwrite(img_name, frame)
            nome = print("{} written!".format(img_name))
            Label(top, text=nome).pack()
            Label(top, text="Picture Taken and Saved").pack()
            img_counter += 1
    else:
        Label(top, text="Picture Not Taken, Try Again!").pack()

# width, height = 800, 600
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
#
# fr = LabelFrame(root, padx=10, pady=10)
# fr.pack(padx=5, pady=5)
# label = Label(fr)
# label.pack()
#
# button = Button(root, text="Take Picture!", bg="black", fg="white", borderwidth=10, anchor=S, command=lambda: picture())
# button.pack(anchor=S)
#
# show_frame()
root.mainloop()