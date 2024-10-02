from casilla import Casilla
from mapa import Mapa
from main import *

def bueno(mapi, pos):
    res= False
    
    if mapi.getCelda(pos.getFila(),pos.getCol())==0 or mapi.getCelda(pos.getFila(),pos.getCol())==4 or mapi.getCelda(pos.getFila(),pos.getCol())==5:
       res=True
    
    return res

def nuevaCasilla(pos, caso):
    coste = 1
    if caso == 0:
        nueva = Casilla(pos.getFila() - 1, pos.getCol() - 1)
        coste = 1.5
    if caso == 1:
        nueva = Casilla(pos.getFila() - 1, pos.getCol())
    if caso == 2:
        nueva = Casilla(pos.getFila() - 1, pos.getCol() + 1)
        coste = 1.5
    if caso == 3:
        nueva = Casilla(pos.getFila(), pos.getCol() + 1)
    if caso == 4:
        nueva = Casilla(pos.getFila() + 1, pos.getCol() + 1)
        coste = 1.5
    if caso == 5:
        nueva = Casilla(pos.getFila() + 1, pos.getCol())
    if caso == 6:
        nueva = Casilla(pos.getFila() + 1, pos.getCol() - 1)
        coste = 1.5
    if caso == 7:
        nueva = Casilla(pos.getFila(), pos.getCol() - 1)
    
    return nueva, coste

def calcularCalorias(mapi, pos):
    cal = 0
    valor = mapi.getCelda(pos.getFila(), pos.getCol())

    if valor == 0: #Hierba
        cal = 2
    if valor == 4: #Agua
        cal = 4
    if valor == 6: #Roca
        cal = 6

    return cal

def esValida(mapi, pos):
    valida = True
    i = pos.getFila()
    j = pos.getCol()

    if i >= 0 and i < mapi.getAlto() and j >= 0 and j < mapi.getAncho():
        valida = True

    return valida

def imprimePosiciones(mapi, initPos):
    print("La posición inicial es: ({},{})".format(initPos.getFila(), initPos.getCol()))

    #Analizamos las 8 posibles soluciones:
    for i in range(8):
        nueva, coste = nuevaCasilla(initPos, i)
        if bueno(mapi, nueva) and esValida(mapi, nueva):
            
            print("La posición ({},{}) es accesible.".format(nueva.getFila(), nueva.getCol()))
            print("El coste para acceder es {} y gasta {} calorías". format(coste, calcularCalorias(mapi, nueva)))