from nodo import Nodo
from casilla import *
import heapq
        
def generarHijo(pos, caso):
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
    if valor == 4: #Agua
        cal = 4
    if valor == 6: #Roca
        cal = 6

    return cal

def AEstrella(inicial, final, mapi, camino, orden):
    listaInterior = []
    listaFrontera = []
    
    nodoInicial = Nodo(inicial, None, 0, 0)
    nodoInicial.setH(0)
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
            for i in range(len(camino)):
                for j in range(len(camino[0])):
                    print(camino[i][j], end='')
                print()

            for i in range(len(orden)):
                for j in range(len(orden[0])):
                    print(orden[i][j], end=' ')
                print()
            return n.g, n.cal
        
        listaInterior.append(n) #Añadimos a la lista de nodos explorados
        
        #Generamos los hijos y comprobamos que no estén en la lista interior
        for i in range(8):
            nuevaPos, coste = generarHijo(n.getCasilla(), i)
            calorias = calcularCalorias(mapi, nuevaPos)
            
            #Comprobamos que el hijo sea una casilla accesible
            if bueno(mapi, nuevaPos) and esValida(mapi, nuevaPos):
                orden[nuevaPos.getFila()][nuevaPos.getCol()] = cont
                cont += 1                
                g = n.getG() + coste
                
                #Comprobamos que el nodo no esté en la lista interior
                isIn = False
                for elem in listaInterior:
                    if elem.casilla == nuevaPos:
                        isIn = True
                        m = elem
                        break
                
                if not isIn:
                    m = Nodo(nuevaPos, n, coste, calorias)
                    m.setH(0)
                    m.calculaF()
                    heapq.heappush(listaFrontera, m)
                else:
                    if g < m.getG():
                        m.padre = n
                        m.g = g
                        m.calculaF()
    return -1, -1