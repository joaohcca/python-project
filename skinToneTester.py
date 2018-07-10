import numpy as np
import cv2

def displayContagem(frame,celular,tablet,notebook):
    cv2.rectangle(frame, (485, 100), (635, 30), (0, 255, 0), 2)
    cv2.putText(frame, "Celulares: {}".format(str(celular)), (490, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
    cv2.putText(frame, "Tablets: {}".format(str(tablet)), (490, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
    cv2.putText(frame, "Notebooks: {}".format(str(notebook)), (490, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 1), 2)
    return

cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    if not ret: break
#Convertendo frame para cor HSV(Necessario para nao desenhar contornos sobre cor Humana)
    framePele = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#Valor hsv referente a cor da pele humana: [[[103 109 234]]]
    peleInferior = np.array([0,10,60])
    peleSuperior = np.array([35,180,255])

#Limitando os valores da cor da pele
    mascara = cv2.inRange(framePele, peleInferior, peleSuperior)
    #mascara = cv2.dilate(mascara, None, iterations=2)
    #mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, (5,5))
    res = cv2.bitwise_and(frame,frame, mask= mascara)
    celular = 10
    tablet = 24
    notebook = 156

    displayContagem(frame,celular,tablet,notebook)

#Exibindo Resultado
    cv2.imshow('frame',frame)
    #cv2.imshow('mask',mascara)
    #cv2.imshow('res',res)
#fechando janela
    if cv2.waitKey(20) & 0xFF == ord('q'): break
#Encerrando camera
cap.release()
cv2.destroyAllWindows()
