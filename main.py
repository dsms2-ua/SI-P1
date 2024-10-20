import sys, pygame
from casilla import *
from mapa import *
from sesion1 import *
from pygame.locals import *
from nodo import *
from algoritmos import *
import time
import io
import sys
import os




MARGEN=5
MARGEN_INFERIOR=60
TAM=30
NEGRO=(0,0,0)
HIERBA=(200, 250, 160)
MURO=(30, 70, 140)
AGUA=(173, 216, 230) 
ROCA=(110, 75, 48)
AMARILLO=(255, 255, 0) 

# ---------------------------------------------------------------------
# Funciones
# ---------------------------------------------------------------------

# Devuelve si una casilla del mapa se puede seleccionar como destino o como origen
def bueno(mapi, pos):
    res= False
    
    if mapi.getCelda(pos.getFila(),pos.getCol())==0 or mapi.getCelda(pos.getFila(),pos.getCol())==4 or mapi.getCelda(pos.getFila(),pos.getCol())==5:
       res=True
    
    return res
    
# Devuelve si una posición de la ventana corresponde al mapa
def esMapa(mapi, posicion):
    res=False     
    
    if posicion[0] > MARGEN and posicion[0] < mapi.getAncho()*(TAM+MARGEN)+MARGEN and \
    posicion[1] > MARGEN and posicion[1] < mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res= True       
    
    return res
    
#Devuelve si se ha pulsado algún botón
def pulsaBoton(mapi, posicion):
    res=-1
    
    if posicion[0] > (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2-65 and posicion[0] < (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2-15 and \
       posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res=1
    elif posicion[0] > (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2+15 and posicion[0] < (mapi.getAncho()*(TAM+MARGEN)+MARGEN)//2+65 and \
       posicion[1] > mapi.getAlto()*(TAM+MARGEN)+MARGEN+10 and posicion[1] < MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN:
        res=2

    
    return res
   
# Construye la matriz para guardar el camino
def inic(mapi):    
    cam=[]
    for i in range(mapi.alto):        
        cam.append([])
        for j in range(mapi.ancho):            
            cam[i].append('.')
    
    return cam

def inicUnos(mapi):
    cam = []
    for i in range(mapi.alto):
        cam.append([])
        for j in range(mapi.ancho):
            cam[i].append(-1)
    
    return cam

def devuelveHeuristica(opt):
    if opt == 0:
        return "Manhattan"
    if opt == 1:
        return "Euclidea"
    if opt == 2:
        return "Chebychev"
    if opt == 3:
        return "Octil"
    if opt == 4:
        return "Ninguna"

#Definimos una función para redirigir la salida a un archivo de texto plano
def imprimirResumenTXT(mapa, inicio, final, heuristica, camino, estados, coste, calorias, tiempo, estadosInterior):
    buffer = io.StringIO()
    sys.stdout = buffer

    #1. Imprimir el mapa
    print(mapa)
    
    #2. Casilla de inicio y final
    print("Casilla de inicio: {}".format(inicio))
    print("Casilla de final: {}\n".format(final))

    #3. Heurística utilizada
    heu = devuelveHeuristica(heuristica)
    print("La heuristica utilizada es: {}\n".format(heu))

    #4. Imprimir la matriz de camino final
    for i in range(mapa.alto):
        for j in range(mapa.ancho):
            print(camino[i][j], end=" ")
        print("")
    print("")

    #5. Imprimir la matriz de orden de generación de estados
    for i in range(mapa.alto):
        for j in range(mapa.ancho):
            print(f"{estados[i][j]:>3}", end=" ")
        print("")
    print("")

    #6. Coste y calorías finales
    print("El coste del camino final es: {}".format(coste))
    print("Las calorias totales del camino son: {}\n".format(calorias))

    #7. Tiempo utilizado
    print("El tiempo de computo del camino es: {:.5f} segundos\n".format(tiempo))

    #8. Número de estados de lista interior
    print("El numero de estados en la lista interior es: {}\n".format(estadosInterior))

    sys.stdout = sys.__stdout__
    contenido = buffer.getvalue()

    if len(sys.argv)==1: #si no se indica un mapa coge mapa.txt por defecto
        file='mapa'
    else:
        file=sys.argv[-1]

    nombre_sin_extension = os.path.splitext(file)[0]

    nombre = "ejecuciones/" + nombre_sin_extension + "/ejecucion" + heu + ".txt"

    #Antes de generar el archivo borramos el anterior
    if os.path.exists(nombre):
        os.remove(nombre)

    with open(nombre, "w") as f:
        f.write(contenido)
        
# función principal
def main():
    pygame.init()    
    
    reloj=pygame.time.Clock()
    
    if len(sys.argv)==1: #si no se indica un mapa coge mapa.txt por defecto
        file='mapa.txt'
    else:
        file=sys.argv[-1]
         
    mapi=Mapa(file)     
    camino=inic(mapi)
    orden = inicUnos(mapi)   
    
    anchoVentana=mapi.getAncho()*(TAM+MARGEN)+MARGEN
    altoVentana= MARGEN_INFERIOR+mapi.getAlto()*(TAM+MARGEN)+MARGEN    
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension)
    pygame.display.set_caption("Practica 1")
    
    boton1=pygame.image.load("boton1.png").convert()
    boton1=pygame.transform.scale(boton1,[50, 30])
    
    boton2=pygame.image.load("boton2.png").convert()
    boton2=pygame.transform.scale(boton2,[50, 30])
    
    personaje=pygame.image.load("rabbit.png").convert()
    personaje=pygame.transform.scale(personaje,[TAM, TAM])
    
    objetivo=pygame.image.load("carrot.png").convert()
    objetivo=pygame.transform.scale(objetivo,[TAM, TAM])
    
    coste=-1
    cal=0
    running= True    
    origen=Casilla(-1,-1)
    destino=Casilla(-1,-1)
    
    while running:        
        #procesamiento de eventos
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                running=False 
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                
                if pulsaBoton(mapi, pos)==1 or pulsaBoton(mapi, pos)==2:
                    if origen.getFila()==-1 or destino.getFila()==-1:
                        print('Error: No hay origen o destino')
                    else:
                        camino=inic(mapi)
                        if pulsaBoton(mapi, pos)==1:
                            ###########################                                                 
                            #coste, cal=llamar a A estrella  
                            inicio = time.perf_counter()
                            coste, cal, heuristica, estadosInterior = AEstrella(origen, destino, mapi, camino, orden)
                            final = time.perf_counter()

                            tiempo = final - inicio
                            
                            
                            if coste==-1:
                                print('Error: No existe un camino válido entre origen y destino')
                            else:
                                imprimirResumenTXT(mapi, origen, destino, heuristica, camino, orden, coste, cal, tiempo, estadosInterior)

                        else:
                            ###########################                                                   
                            #coste, cal=llamar a A estrella subepsilon                       
                            if coste==-1:
                                print('Error: No existe un camino válido entre origen y destino')
                            
                elif esMapa(mapi,pos):                    
                    if event.button==1: #botón izquierdo                        
                        colOrigen=pos[0]//(TAM+MARGEN)
                        filOrigen=pos[1]//(TAM+MARGEN)
                        casO=Casilla(filOrigen, colOrigen)                        
                        if bueno(mapi, casO):
                            origen=casO
                            #-----------------SESIÓN 1-----------------
                            #Aquí llamamos a la función que nos comprueba los posibles caminos
                            #imprimePosiciones(mapi, origen)
                        else: # se ha hecho click en una celda no accesible
                            print('Error: Esa casilla no es válida')
                    elif event.button==3: #botón derecho
                        colDestino=pos[0]//(TAM+MARGEN)
                        filDestino=pos[1]//(TAM+MARGEN)
                        casD=Casilla(filDestino, colDestino)                        
                        if bueno(mapi, casD):
                            destino=casD
                        else: # se ha hecho click en una celda no accesible
                            print('Error: Esa casilla no es válida')         
        
        #código de dibujo        
        #limpiar pantalla
        screen.fill(NEGRO)
        #pinta mapa
        for fil in range(mapi.getAlto()):
            for col in range(mapi.getAncho()):                
                if camino[fil][col]!='.':
                    pygame.draw.rect(screen, AMARILLO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapi.getCelda(fil,col)==0:
                    pygame.draw.rect(screen, HIERBA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapi.getCelda(fil,col)==4:
                    pygame.draw.rect(screen, AGUA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                elif mapi.getCelda(fil,col)==5:
                    pygame.draw.rect(screen, ROCA, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)                                    
                elif mapi.getCelda(fil,col)==1:
                    pygame.draw.rect(screen, MURO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                    
        #pinta origen
        screen.blit(personaje, [(TAM+MARGEN)*origen.getCol()+MARGEN, (TAM+MARGEN)*origen.getFila()+MARGEN])        
        #pinta destino
        screen.blit(objetivo, [(TAM+MARGEN)*destino.getCol()+MARGEN, (TAM+MARGEN)*destino.getFila()+MARGEN])       
        #pinta botón
        screen.blit(boton1, [anchoVentana//2-65, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        screen.blit(boton2, [anchoVentana//2+15, mapi.getAlto()*(TAM+MARGEN)+MARGEN+10])
        #pinta coste y energía
        if coste!=-1:            
            fuente= pygame.font.Font(None, 25)
            textoCoste=fuente.render("Coste: "+str(coste), True, AMARILLO)            
            screen.blit(textoCoste, [anchoVentana-90, mapi.getAlto()*(TAM+MARGEN)+MARGEN+15])
            textoEnergía=fuente.render("Cal: "+str(cal), True, AMARILLO)
            screen.blit(textoEnergía, [5, mapi.getAlto()*(TAM+MARGEN)+MARGEN+15])
            
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        
    pygame.quit()
    
#---------------------------------------------------------------------
if __name__=="__main__":
    main()
