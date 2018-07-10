import cv2
import numpy as np
import sqlite3 as sq3
import math
import datetime
import time

#inicialização de Variaveis Globais
objetoLabel = 0
celular = 0
tablet = 0
notebook = 0
objetoDesconhecido =0
linhaReferencia = 200
ThresholdBinarizacao = 70
areaMinima = 200
areaMaxObjeto1 = 1200
areaMinObjeto2 = 1500
areaMaxObjeto2 = 3000
areaMinObjeto3 = 4000
areaMaxObjeto3 = 6000
frameReferencia = None
objNotAssigned = 0

def shapeDraw(cnt):
    cv2.drawContours(frame, contorno, -1, (0, 255, 0), 3)
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

def contador(cX,coordenadaLinhaX):
    if (coordenadaLinhaX - cX) > 10:
# impedindo que o objeto seja contado inumeras vezes
        return 1
    else:
        return 0

def displayContagem(frame,celular,tablet,notebook,objetoDesconhecido):
    cv2.rectangle(frame, (485, 120), (635, 30), (0, 255, 0), 2)
    cv2.putText(frame, "Celulares: {}".format(str(celular)), (490, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
    cv2.putText(frame, "Tablets: {}".format(str(tablet)), (490, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
    cv2.putText(frame, "Notebooks: {}".format(str(notebook)), (490, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
    cv2.putText(frame, "Desconhcecido: {}".format(str(objetoDesconhecido)), (490, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
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
    coordenadaLinhaX = int(largura / 2) - linhaReferencia
    cv2.line(frame, (coordenadaLinhaX, 0), (coordenadaLinhaX, largura), (255, 0, 0), 2)

#Encontrando os contornos
    _,contorno,_ = cv2.findContours(mask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#*********************************************************CONTAGEM DE OBJETOS E EXIBIÇÂO NA TELA************************************************************************
#Definindo as propriedades dos contornos
    for cnt in contorno:
#Area e Perimetro
        area = cv2.contourArea(cnt)
        perimetro = cv2.arcLength(cnt, True)
        print('Area: ',area)
        #print('Perimetro: ', perimetro)

# Desenhando contornos apartir de uma dado tamanho(Pra ignorar pequenos contornos)
        if contorno != None:
            if area > areaMinima:
                shapeDraw(cnt)
#Definindo Objeto de acordo com suas propriedades
                objetoLabel = shapeIdentifier()
#Calculando Centroide do Objeto
                M = cv2.moments(cnt)
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
                centroide = (cX, cY)
                #print('Centroide: ',centroide)
                cv2.circle(frame,centroide,1,(0,0,0),5)
# Verificar passagem do centroide pela linha de referencia e Contabilização do Objeto
                if (contador(cX,coordenadaLinhaX)):
                    if objetoLabel == 1:
                        celular += 1
                    if objetoLabel == 2:
                        tablet += 1
                    if objetoLabel == 3:
                        notebook += 1
                    else:
                        objetoDesconhecido +=1
                else:
                    print('Aguardando Contagem')
        else:
            print('Nenhum Contorno foi Detectado \n')

#Display de informação de contagem
    displayContagem(frame,celular,tablet,notebook,objetoDesconhecido)

#Verificar se o objeto nao identificado passo multiplas vezes e oferecer cadastro: EXTRA
        #objNotAssigned += 1

#******************************************ARMAZENAMENTO DE INFORMAÇÔES NO BANCO DE DADOS**************************************************************
#inicializando tabela com dados pra database
    conn = sq3.connect('produtos.db')
    prod = conn.cursor()

    prod.execute("""
    CREATE TABLE clientes (
    	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    	tipo TEXT NOT NULL,
    	area FLOAT,
    	perimetro FLOAT,
    	evento_em DATE NOT NULL,
    	evento_type STRING(3) NOT NULL
    );
    """)
    conn.close();

    # inserindo dados na tabela

    #obj é uma tupla com os dados

    prod.executemany("""
    INSERT INTO produtos (id, tipo, area, perimetro, evento_em, evento_type)
    VALUES (?,?,?,?,?,?)
    """, obj)
    conn.commit()

   #removendo dados da database usando o id como indicador
    id_produto = 8

    # excluindo um registro da tabela
    prod.execute("""
    DELETE FROM produtos
    WHERE id = ?
    """, (id_produto,))

    conn.commit()
#**********************************************************ENCERRANDO APLICAÇÃO************************************************************************

    cv2.imshow('mascara', mask)
    cv2.imshow('original', frame)

#fechando janela
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

#Encerrando camera
cap.release()
cv2.destroyAllWindows()
