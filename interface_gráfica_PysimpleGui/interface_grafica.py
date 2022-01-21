import cv2, PySimpleGUI as sg
from math import hypot
import dlib
import time
from tkinter import messagebox
import os
from skimage import io
import face_recognition as fr
import numpy as np
import pickle
from fer import FER


###############################################################################
#######################  VARIÁVEIS GLOBAIS  ###################################
###############################################################################

predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()

img_counter = 0

w, h = sg.Window.get_screen_size()

with open("subject_files.pkl",'rb') as f:
    encodeList = pickle.load(f)


if (bool(encodeList)):
    pass
else:
    encodeList = {}

###############################################################################
################################  FUNÇÕES  ####################################
###############################################################################


def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
    ratio = hor_line_lenght / ver_line_lenght
    return ratio


def findEncondings(img,name):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    encode = fr.face_encodings(img)[0]
    encodeList.update({name:encode})
    updateEncodings(encodeList)

def updateEncodings(encode):
    with open("subject_files.pkl",'wb') as f:
        pickle.dump(encode, f)

###############################################################################
################  TELAS  DA INTERFACE GRÁFICA  ################################
###############################################################################


class Inicio:
    def __init__(self):
        #layout
        self.layout = [[sg.Text("Sistema de Segurança - Reconhecimento Facial",font=("Consolas",40))],
                       [sg.Button('Registar',font=("Consolas",30)), sg.Button('Entrar',font=("Consolas",30)), sg.Button('Cancel',font=("Consolas",30)) ]]
        #janela
        self.janela = sg.Window("Sistema de Segurança").layout(self.layout)
        #extrair os dados da tela
        self.button, self.values = self.janela.read()

    def close(self):
        self.janela.close();


class Registar:
    def __init__(self):
        #layout
        self.layout = [[sg.Text('Nome',font=("Consolas",30)),sg.Input(key='nome',font=("Consolas",30))],
                       [sg.Button('Continuar',font=("Consolas",30)), sg.Button('Cancel',font=("Consolas",30))]]
        #janela
        self.janela = sg.Window("Registar").layout(self.layout)
        #extrair os dados da tela
        self.button, self.values = self.janela.read()

    def close(self):
        self.janela.close();

        
class Entrar:
    def __init__(self):
        #layout
        self.layout = [[sg.Text('Nome',font=("Consolas",30)),sg.Input(key='nome',font=("Consolas",30))],
                       [sg.Button('Continuar',font=("Consolas",30)), sg.Button('Cancel',font=("Consolas",30))]]
        #janela
        self.janela = sg.Window("Entrar").layout(self.layout)
        #extrair os dados da tela
        self.button, self.values = self.janela.read()

    def close(self):
        self.janela.close()


###############################################################################
################################  MAIN  #######################################
###############################################################################

TelaInicial = Inicio(); # Iniciar interface 


while True:
    
    if TelaInicial.button == sg.WIN_CLOSED or TelaInicial.button == 'Cancel':  # Fechar interface
        break
    
    ########### Interface para registar ############## 
    elif TelaInicial.button == 'Registar': 
        
        TelaInicial.close()
        TelaRegistar = Registar();
        
        while True:
            
            if TelaRegistar.button == sg.WIN_CLOSED or TelaRegistar.button == 'Cancel': # Fechar interface para registar
                break
           
            elif TelaRegistar.button == 'Continuar': # Depois de escrever o nome tira-se a foto 
                
                window, cap = sg.Window('Foto', [[sg.Image(filename='', key='image')], ], location=(0, 0), grab_anywhere=True), cv2.VideoCapture(0)
                s_out = False
               
                while (window(timeout=20)[0] != sg.WIN_CLOSED) and (s_out == False):
                   ##### secção responsável por detetar o piscar de olhos e tirar a foto ######### 
                    window['image'](data=cv2.imencode('.png', cv2.flip(cap.read()[1],1))[1].tobytes()) # atualizar a imagem na janela da interface
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
                            window['image'](data=cv2.imencode('.png', cv2.flip(cap.read()[1],1))[1].tobytes())
                            _, frame = cap.read()
                  
                    ############################################################# 
                    ##################  Guardar a imagem ########################
                            confirmation = messagebox.askquestion("", "Do You Accept This Picture?")
                            if confirmation == "yes":
                        
                                img_name = TelaRegistar.values['nome'] + "_{}.png".format(img_counter)
                        
                                parent_directory = r"C:\Users\user\Desktop\UA\5_Ano\Biometria\Projeto\FaceDetect-master\Faces"
                                path = os.path.join(parent_directory, img_name)
                                
                                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                                frame = cv2.flip(frame,1)
                                
                                io.imsave(path,frame)
                                s_out = True
                                img_counter += 1;
                                findEncondings(frame,TelaRegistar.values['nome'])
                                

                
                cap.release()
                window.close()
                break
                
        TelaRegistar.close();
        TelaInicial = Inicio();
    
        
    ########### Interface para entrar ############## 
    elif TelaInicial.button == 'Entrar':
        
        TelaInicial.close()
        TelaEntrar = Entrar();
        
        while True:
            
            if TelaEntrar.button == sg.WIN_CLOSED or TelaEntrar.button == 'Cancel': 
                break
           
            elif TelaEntrar.button == 'Continuar':
                
                nome = TelaEntrar.values['nome'].upper()
                window, cap = sg.Window('Foto', [[sg.Image(filename='', key='image')], ], location=(0, 0), grab_anywhere=True), cv2.VideoCapture(0)
                s_out = False
                t0 = time.time() ##### LINHA Nº1
                while (window(timeout=20)[0] != sg.WIN_CLOSED) and (s_out == False):
                   
                    window['image'](data=cv2.imencode('.png', cv2.flip(cap.read()[1],1))[1].tobytes())
                    _, frame = cap.read()
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = detector(gray)
            
                    
  #####################################  EMOTION DETECTOR ALGORITHM  ############################################## 
                    if ((time.time()-t0) > 5): ##### LINHA Nº2
                      
    # CODIGO LENTO, PROCURAR SOLUÇÃO PARA QUE ESTA PARTE DO CÓDIGO NAO FIQUE CORRENDO CONSTANTEMENTE #
                    
                          detect = FER(mtcnn=True)
                          emotions = detect.detect_emotions(frame)
                          # print(detect.detect_emotions(frame))
                          if(emotions[0]["emotions"]["fear"] >= 0.35):
                              print("Subject maybe under threat - Warning For Emergency situation!")
                          elif(emotions[0]["emotions"]["angry"] >= 0.35):
                              print("Subject possibly highly stressed - You should relax!")
                          else:
                              print("Subject not under threat!")
                            
                          t0 = time.time() ##### LINHA Nº3
                    
                  
                                
            ##################################################################################  
            
            
                    for face in faces:
                        

                            
                        landmarks = predictor(gray, face)
                        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
                        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
                        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
                       
                        if blinking_ratio > 5.7:
                            time.sleep(1)
                            window['image'](data=cv2.imencode('.png', cv2.flip(cap.read()[1],1))[1].tobytes())
                            _, frame = cap.read()
                            
                            
                            frame = cv2.resize(frame,(0,0),None,0.25,0.25)
                            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                            
                            facesCurFrame = fr.face_locations(frame)
                            encodesCurFrame = fr.face_encodings(frame,facesCurFrame)
                            
                            listOfValues = encodeList.values()
                            listOfValues = list(listOfValues)
                            listOfKeys = encodeList.keys()
                            listOfKeys = list(listOfKeys)
                            
                            
                            for encondeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
                                
                                matches = fr.compare_faces(listOfValues, encondeFace)
                                faceDist = fr.face_distance(listOfValues, encondeFace)
                                matchIndex = np.argmin(faceDist)

                         
                                
                                if np.amin(faceDist) < 0.5:
                                    if (matches[matchIndex]) and (nome == listOfKeys[matchIndex].upper()):
                                        confirmation = messagebox.showinfo("", f'{nome}')
                                    else:
                                        confirmation = messagebox.showinfo("", "Not Matching. Access denied!")
                                       # print("Not Matching. Access denied!") 
                                else:
                                    confirmation = messagebox.showinfo("", "Desconhecido. Acesso negado!")
                        
                                s_out = True
    
                
                cap.release()
                window.close()
                break    
                
        TelaEntrar.close();
        TelaInicial = Inicio();

    
TelaInicial.close()







