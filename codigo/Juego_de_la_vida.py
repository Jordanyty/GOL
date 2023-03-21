import pygame
import numpy as np
import time

pygame.init()

width, height = 500, 500
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

# Numero de celdas
nxC, nyC = 50,50
# Dimensiones de la celda
dimCW = width / nxC
dimCH = height / nyC

# Estado de las celdas. Vivas = 1; Muertas = 0
gameState = np.zeros((nxC, nyC))



#Runner 2
gameState[5,10] = 1
gameState[5,12] = 1
gameState[6,11] = 1
gameState[6,12] = 1
gameState[7,11] = 1
#Box 1
gameState[18,15] = 1
gameState[17,16] = 1
gameState[17,15] = 1
gameState[18,16] = 1

# Control de la ejecucion del juego
pauseExect = False

# Bucle de ejecucion
while True:
    
    newGameState = np.copy(gameState)
    
    screen.fill(bg)
    time.sleep(0.1)
    
    # Registramos eventos de teclado y ratón.
    ev = pygame.event.get()
    
    for event in ev:
        # Detectamos si se preciona una tecla
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
            
            
        mouseClick = pygame.mouse.get_pressed()
      
        if (sum(mouseClick)) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]


    for y in range(0, nxC):
        for x in range(0, nyC):
            
            if not pauseExect:
            
                #Calculamos el numero de vecinos cercanos:
                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                        gameState[(x    ) % nxC, (y - 1) % nyC] + \
                        gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                        gameState[(x - 1) % nxC, (y    ) % nyC] + \
                        gameState[(x + 1) % nxC, (y    ) % nyC] + \
                        gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                        gameState[(x    ) % nxC, (y + 1) % nyC] + \
                        gameState[(x + 1) % nxC, (y + 1) % nyC]
                        
                # Rule 1: Una célula muerta con exactamente 3 vecincas vivas, "revive" o "nace".
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                
                #Rule 2: Una celcula viva con menos de 2 o mas de 3 vecinas vivas, "muere".
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                        newGameState[x, y] = 0 
                       
            # Creamos el poligono de cada celda a dibujar
            poly = [((x)   * dimCW, y     * dimCH),
                    ((x+1) * dimCW, y     * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x)   * dimCW, (y+1) * dimCH)]
            
            # Y dibujamos la celda para cada par de x e y
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, width=1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, width=0)
                
    # Actualizamos el estado del juego
    gameState = np.copy(newGameState)

    pygame.display.flip()