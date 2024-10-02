from nodo import Nodo
from casilla import *
        
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

def AEstrella(inicial, final, mapi, camino):
    listaInterior = []
    listaFrontera = []
    
    nodoInicial = Nodo(inicial, None, 0, 0)
    nodoInicial.setH(0)
    nodoInicial.calculaF()
    listaFrontera.append(nodoInicial)
    
    while len(listaFrontera) != 0:
        #Ordenamos la lista frontera
        listaFrontera.sort(key=lambda x: x.f)
        n = listaFrontera[0]
        
        if n.casilla == final:
            #Reconstruir camino iterando por padres
            actual = n
            while actual.getCasilla() != inicial:
                camino[actual.getFila()][actual.getColumna()] == 'c'
                actual = actual.padre
            for i in camino:
                for j in camino[0]:
                    print(camino[i][j])
                print()
            return n.coste, n.cal
        
        listaFrontera.remove(n)
        listaInterior.append(n)
        
        #Generamos los hijos y comprobamos que no estén en la lista interior
        for i in range(8):
            nuevaPos, coste = generarHijo(n.getCasilla(), i)
            
            #Comprobamos que el hijo sea una casilla accesible
            if bueno(mapi, nuevaPos) and esValida(mapi, nuevaPos):                
                g = n.getG() + coste
                #Comprobamos que el nodo no esté en la lista interior
                isIn = False
                for elem in listaInterior:
                    if elem.casilla == nuevaPos:
                        isIn = True
                        m = elem
                        break
                
                if not isIn:
                    print("Genero")
                    m = Nodo(nuevaPos, n, coste, 0)
                    m.setH(0)
                    m.calculaF()
                    listaFrontera.append(m)
                else:
                    if g < m.getG():
                        m.padre = n
                        m.g = g
                        m.calculaF()
    return -1, -1