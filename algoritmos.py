from nodo import Nodo
from casilla import *
import heapq
import math
        
def generarHijo(pos, caso):
    coste = 1
    if caso == 0:
        nueva = Casilla(pos.getFila() - 1, pos.getCol() - 1)
        coste = 1.5
    elif caso == 1:
        nueva = Casilla(pos.getFila() - 1, pos.getCol())
    elif caso == 2:
        nueva = Casilla(pos.getFila() - 1, pos.getCol() + 1)
        coste = 1.5
    elif caso == 3:
        nueva = Casilla(pos.getFila(), pos.getCol() + 1)
    elif caso == 4:
        nueva = Casilla(pos.getFila() + 1, pos.getCol() + 1)
        coste = 1.5
    elif caso == 5:
        nueva = Casilla(pos.getFila() + 1, pos.getCol())
    elif caso == 6:
        nueva = Casilla(pos.getFila() + 1, pos.getCol() - 1)
        coste = 1.5
    elif caso == 7:
        nueva = Casilla(pos.getFila(), pos.getCol() - 1)
    
    return nueva, coste

def bueno(mapi, pos):
    res= False
    
    if mapi.getCelda(pos.getFila(),pos.getCol())==0 or mapi.getCelda(pos.getFila(),pos.getCol())==4 or mapi.getCelda(pos.getFila(),pos.getCol())==5:
       res=True
    
    return res

def esValida(mapi, pos):
    valida = True
    i = pos.getFila()
    j = pos.getCol()

    if i >= 0 and i < mapi.getAlto() and j >= 0 and j < mapi.getAncho():
        valida = True

    return valida

def calcularCalorias(mapi, pos):
    cal = 0
    valor = mapi.getCelda(pos.getFila(), pos.getCol())

    if valor == 0: #Hierba
        cal = 2
    elif valor == 4: #Agua
        cal = 4
    elif valor == 5: #Roca
        cal = 6

    return cal

def heuristicaManhattan(pos, final,):
    return abs(pos.getFila() - final.getFila()) + abs(pos.getCol() - final.getCol())

def heuristicaEuclidea(pos, final):
    return math.sqrt((pos.getFila() - final.getFila())**2 + (pos.getCol() - final.getCol())**2)

def heuristicaChebychev(pos, final):
    return max(abs(pos.getFila() - final.getFila()), abs(pos.getCol() - final.getCol()))

def heuristicaOctil(pos, final):
    dx = abs(pos.getFila() - final.getFila())
    dy = abs(pos.getCol() - final.getCol())
    return abs(dx - dy) + 1.5 * min(dx, dy)

def heuristica(pos, final, opt): 
    if opt == 0:
        return 0
    if opt == 1:
        return heuristicaManhattan(pos, final)
    elif opt == 2:
        return heuristicaEuclidea(pos, final)
    elif opt == 3:
        return heuristicaChebychev(pos, final)
    elif opt == 4:
        return heuristicaOctil(pos, final)

def AEstrella(inicial, final, mapi, camino, orden, opt):
    listaInterior = []
    listaFrontera = []
    
    nodoInicial = Nodo(inicial, None, 0, 0)
    
    h = heuristica(inicial, final, opt)
        
    nodoInicial.setH(h)
    nodoInicial.calculaF()
    
    heapq.heappush(listaFrontera, nodoInicial)

    orden[inicial.getFila()][inicial.getCol()] = 0
    cont = 1
    
    while len(listaFrontera) != 0:
        #Extraemos el nodo en la cima del heap
        n = heapq.heappop(listaFrontera)
        
        if n.casilla == final:
            #Reconstruir camino iterando por padres
            actual = n
            while actual.getCasilla() != inicial:
                camino[actual.getCasilla().getFila()][actual.getCasilla().getCol()] = 'c'
                actual = actual.padre

            return n.g, n.cal, len(listaInterior)
        
        listaInterior.append(n) #Añadimos a la lista de nodos explorados
        
        #Generamos los hijos y comprobamos que no estén en la lista interior
        for i in range(8):
            nuevaPos, coste = generarHijo(n.getCasilla(), i)
            calorias = calcularCalorias(mapi, nuevaPos)
            
            #Comprobamos que el hijo sea una casilla accesible
            if bueno(mapi, nuevaPos) and esValida(mapi, nuevaPos):                
                g = n.getG() + coste
                #Comprobamos que el nodo no esté en la lista interior
                inInterior = False
                
                for elem in listaInterior:
                    if elem.casilla == nuevaPos:
                        inInterior = True
                        m = elem
                        break
                
                if not inInterior:
                    orden[nuevaPos.getFila()][nuevaPos.getCol()] = cont
                    cont += 1
                    
                    #Comprobamos si esta en la listaFrontera
                    inFrontera = False
                    for j in range(len(listaFrontera)):
                        if listaFrontera[j].casilla == nuevaPos:
                            posicion = j
                            inFrontera = True  
                            break

                    if not inFrontera:
                        m = Nodo(nuevaPos, n, coste, calorias)
                        h = heuristica(nuevaPos, final, opt)
                        m.setH(h)
                        m.calculaF()
                        heapq.heappush(listaFrontera, m)
                    
                    else:
                        if g < listaFrontera[posicion].getG():
                            listaFrontera[posicion].padre = n
                            listaFrontera[posicion].g = g
                            listaFrontera[posicion].calculaF()

    return -1, -1, len(listaInterior)

def buscaMinimoCal(listaFocal):
    nodoFocal = listaFocal[0]
    for nodo in listaFocal:
        if nodo.cal < nodoFocal.cal:
            nodoFocal = nodo
            
    return nodoFocal

def AEstrellaEpsilon(inicial, final, mapi, camino, orden, opt, epsilon):
    listaInterior = []
    listaFrontera = []
    listaFocal = [] #Lista de nodos prometedores con respecto a epsilon
    
    nodoInicial = Nodo(inicial, None, 0, 0)
    h = heuristica(inicial, final, opt)
    nodoInicial.setH(h)
    nodoInicial.calculaF()
    
    heapq.heappush(listaFrontera, nodoInicial)

    orden[inicial.getFila()][inicial.getCol()] = 0
    cont = 1
    
    while len(listaFrontera) != 0:
        #Extraemos el nodo en la cima del heap
        n = heapq.heappop(listaFrontera)
        
        #Si hemos llegado al final, reconstruimos el camino y devolvemos coste y calorías
        if n.casilla == final:
            #Reconstruir camino iterando por padres
            actual = n
            while actual.getCasilla() != inicial:
                camino[actual.getCasilla().getFila()][actual.getCasilla().getCol()] = 'c'
                actual = actual.padre

            return n.g, n.cal, len(listaInterior)
        
        listaInterior.append(n) #Añadimos a la lista de nodos explorados
        
        #Llenamos la lista focal
        minF = n.getF()
        listaFocal = [nodo for nodo in listaFrontera if nodo.getF() <= (1 + epsilon) * minF]
        
        #Seleccionamos el nodo con menor calorias
        if len(listaFocal) != 0:
            nodoFocal = buscaMinimoCal(listaFocal)
        else:
            nodoFocal = n
            
        #Generamos los hijos y comprobamos que no estén en la lista interior
        for i in range(8):
            nuevaPos, coste = generarHijo(nodoFocal.getCasilla(), i)
            calorias = calcularCalorias(mapi, nuevaPos)
            
            #Comprobamos que el hijo sea una casilla accesible
            if bueno(mapi, nuevaPos) and esValida(mapi, nuevaPos):                
                g = nodoFocal.getG() + coste
                #Comprobamos que el nodo no esté en la lista interior
                inInterior = False
                for elem in listaInterior:
                    if elem.casilla == nuevaPos:
                        inInterior = True
                        m = elem
                        break
                
                if not inInterior:
                    orden[nuevaPos.getFila()][nuevaPos.getCol()] = cont
                    cont += 1
                    #Comprobamos si esta en la listaFrontera
                    inFrontera = False
                    for j in range(len(listaFrontera)):
                        if listaFrontera[j].casilla == nuevaPos:
                            posicion = j
                            inFrontera = True  
                            break

                    if not inFrontera:
                        m = Nodo(nuevaPos, nodoFocal, coste, calorias)
                        h = heuristica(nuevaPos, final, opt)
                        m.setH(h)
                        m.calculaF()
                        heapq.heappush(listaFrontera, m)
                    
                    else:
                        if g < listaFrontera[posicion].getG():
                            listaFrontera[posicion].padre = nodoFocal
                            listaFrontera[posicion].g = g
                            listaFrontera[posicion].calculaF()

    return -1, -1, len(listaInterior)