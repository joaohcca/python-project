import cv2
import numpy as np
import math
import datetime

#inicialização de Variaveis Globais
objetoLabel = 0
celular = 0
tablet = 0
notebook = 0
linhaReferencia = 100
ThresholdBinarizacao = 70
areaMinima = 1000
areaMaxObjeto1 = 10000
areaMinObjeto2 = 15000
areaMaxObjeto2 = 30000
areaMinObjeto3 = 40000
areaMaxObjeto3 = 60000
frameReferencia = None
objNotAssigned = 0

def shapeDraw(cnt):
    cv2.drawContours(frame, contorno, -1, (0, 255, 0), 3)
    #(x, y, w, h) = cv2.boundingRect(cnt)
    #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return


def shapeIdentifier():
    # Avalianando qual o objeto
    if area > areaMinima and area < areaMaxObjeto1:
        objeto = 1
        print('Celular Identificado')
    if area > areaMinObjeto2 and area < areaMaxObjeto2:
        objeto = 2
        print('Tablet Identificado')
    if area > areaMinObjeto3 and area < areaMaxObjeto3:
        objeto = 3
        print('Computador Identificado')
    else:
        print('Objeto Nao Identificado')
        objeto = 4
    return(objeto)

def contador(centroide,coordenadaLinha):
    #if cv2.absdiff()
    return

#*************************************SUBTRAÇÂO DE BACKGROUND E IDENTIFICAÇÂO DE OBJETO**************************************************************
#Inicializando a Camera
cap = cv2.VideoCapture(0)

#forca a camera a ter resolucao 640x480
cap.set(3,640)
cap.set(4,480)

#Capturando frame para adaptação da luz ambiente
for cont in range(0,20):
    ret,frame = cap.read()

#Rodando Loop para captura de frame
while True:
#Leitura de Video e determinação de parametros de altura e largura de acordo com a resolução
    ret,frame = cap.read()
    altura = np.size(frame, 0)
    largura = np.size(frame, 1)

#Caso não seja possivel obter o frame encerrar
    if not ret: break

#convertendo frame para tons de cinza(Necessario para encontrar os contornos)
    frameCinza = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

#Convertendo frame para cor HSV(Necessario para nao desenhar contornos sobre cor Humana)
    #framePele = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

#Valor hsv referente a cor da pele humana
    #peleInferior = np.array([0,10,60])
    #peleSuperior = np.array([35,180,255])

#Limitando os valores da cor da pele
    #mascara = cv2.inRange(framePele, peleInferior, peleSuperior)
    #res = cv2.bitwise_and(frame,frame, mask= mascara)

#Aplicando filtro gaussiano para diminuir o ruido da imagem
    frameBlur = cv2.GaussianBlur(frameCinza,(21,21),0)

#Comparando frames para a subtração de background
    if frameReferencia is None:
        frameReferencia = frameBlur
        continue
    background = cv2.absdiff(frameReferencia,frameBlur)

#Criando uma Mascara binaria(Mais facil computação e necessario para os contornos)
    mask = cv2.threshold(background,ThresholdBinarizacao,255,cv2.THRESH_BINARY)[1]
    mask = cv2.dilate(mask, None, iterations=2)

#Desenhando Linha de referencia na tela
    coordenadaLinhaY = int(altura / 2) - linhaReferencia
    print(coordenadaLinhaY)
    cv2.line(frame, (coordenadaLinhaY, 0), (coordenadaLinhaY, largura), (255, 0, 0), 2)

#Encontrando os contornos
    _,contorno,_ = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#*********************************************************CONTAGEM DE OBJETOS E EXIBIÇÂO NA TELA************************************************************************
#Definindo as propriedades dos contornos
    for cnt in contorno:
#Area e Perimetro
        area = cv2.contourArea(cnt)
        perimetro = cv2.arcLength(cnt, True)
        #print('Area: ',area)
        #print('Perimetro: ', perimetro)

# Desenhando contornos apartir de uma dado tamanho(Pra ignorar pequenos contornos)
        if contorno != None:
            if area > areaMinima:
                shapeDraw(cnt)
                shapeIdentifier()
                # Calculando Centroide do Objeto
                M = cv2.moments(cnt)
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
                centroide = (cX, cY)
                #print('Centroide: ',centroide)
                cv2.circle(frame,centroide,1,(0,0,0),5)
# Verificar passagem do centroide pela linha de referencia

# Contabilizar Objeto

# Display do qtd

        else:
            #print('Nenhum Contorno foi Detectado \n')

#Verificar se o objeto nao identificado passo multiplas vezes e oferecer cadastro: EXTRA
        #objNotAssigned += 1

#******************************************ARMAZENAMENTO DE INFORMAÇÔES NO BANCO DE DADOS**************************************************************


#**********************************************************ENCERRANDO APLICAÇÃO************************************************************************

    cv2.imshow('mascara', mask)
    cv2.imshow('original', frame)

#fechando janela
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

#Encerrando camera
cap.release()
cv2.destroyAllWindows()
