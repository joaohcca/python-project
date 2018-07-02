# import cv2
# import numpy as np
# import math
# import datetime
#
# #Inicializando a Camera
# cap = cv2.VideoCapture(0)
# #background = cv2.createBackgroundSubtractorMOG2()
# _,frame = cap.read()
# avg = np.float32(frame)
# #Rodando Loop para captura de frame
# while(1):
# #Leitura de Video
#     _,frame = cap.read()
# #Calculando mediana frame a frame
#     cv2.accumulateWeighted(frame,avg,0.001)
#     background = cv2.convertScaleAbs(avg)
#
# #Convertendo frame para escala de cinza
#     background = cv2.cvtColor(background,cv2.COLOR_BGR2GRAY)
#     grayFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#
# #Reduzindo Ruidos com Filtro gaussiano
#     grayFrame = cv2.GaussianBlur(grayFrame,(5,5),0)
#     #background_mask = background.apply(frame)
#
# #SEGMENTAÇÃO DE IMAGEM
#     foreground = cv2.absdiff(background,grayFrame)
#
# #Setando um valor de treshold
#     _,thresh = cv2.threshold(foreground,127,255,cv2.THRESH_BINARY)
#     thresh = cv2.dilate(thresh,None,iterations=2)
#     img,contorno,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
#     cv2.drawContours(img,contorno,-1,(0,255,0),3)
#     cv2.imshow('mascara',img)
#     cv2.imshow('contorno',frame)
#
# #fechando janela
#     if cv2.waitKey(20) & 0xFF == ord('q'):
#         break
#
# #Encerrando camera
# cap.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np
import math
import datetime

#Inicializando a Camera
cap = cv2.VideoCapture(0)
firstFrame = None
#Capturando frame para adaptação da luz ambiente
for i in range(0,20):
    _,frame = cap.read()

#Rodando Loop para captura de frame
while(1):
#Leitura de Video
    _,frame = cap.read()
#convertendo frame para tons de cinza(Necessario para encontrar os contornos)
    frameGray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#Aplicando filtro gaussiano para diminuir o ruido da imagem
    frameGray = cv2.GaussianBlur(frameGray,(15,15),0)
#Comparando frames
    if firstFrame is None:
        firstFrame = frameGray
    background = cv2.absdiff(firstFrame,frameGray)
#Criando uma Mascara binaria(Mais facil computação e necessario para os contornos)
    _,mask = cv2.threshold(background,127,255,cv2.THRESH_BINARY)
#Encontrando os contornos
    _,contorno,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
#Desenhando os contornos na imagem
    cv2.drawContours(frame,contorno,-1,(0,255,0),3)
#Exibindo Video
    cv2.imshow('mascara',mask)
    cv2.imshow('frame',frame)

#fechando janela
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

#Encerrando camera
cap.release()
cv2.destroyAllWindows()
