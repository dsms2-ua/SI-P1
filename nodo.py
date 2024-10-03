#Coordenadas de la casilla del estado y alguna información del padre
#para una casilla inicial será none pero para las siguientes si que tednremos información
#coste de venir desde el padre a él

import casilla

class Nodo():
    def __init__(self, casilla, padre, coste, cal):
        self.casilla = casilla
        self.f = 0
        self.h = 0
        if padre == None: #En caso de que sea la casillla de partida
            self.padre = None
            self.g = 0
            self.cal = 0
        else: #Cualquier otro caso
            self.padre = padre
            self.g = padre.g + coste
            self.cal = padre.cal + cal
            
    def calculaF(self):
        self.f = self.g + self.h
        
    def setH(self, h):
        self.h = h
    
    def getCasilla(self):
        return self.casilla
    
    def getG(self):
        return self.g

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f
    
    def __gt__(self, other):
        return self.f > other.f
    
    def __ge__(self, other):
        return self.f >= other.f