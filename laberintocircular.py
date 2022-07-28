#!/usr/bin/python3
##############################################################
# Create, print and resolve a console based circular laberinth
# python3 laberintocircular.py 
# 2022 - Antonio Royo
##############################################################
import time
import curses
from curses import wrapper
import random

#Constants
WALL_DELIMITER = "#"
LABERINTH_OPEN_PATH = " "
SOLUTION_PATH = "*"

#Coordinates are always passed in the order y,x, and the top-left corner of a window is coordinate (0,0).

def main(stdscr):
    #Wall colour
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    #Laberinth path colour
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    #Colour of the text messages
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    #Resolution path colour
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    #The laberinth is initially filled with the border character (space) and the wall character (#)
    #The laberinth has a fixed size in each execution
    minH = 0
    minV = 0
    maxH = 23 
    maxV = 23
    centroH = 12  
    centroV = 12
    #Open path list from the current cursor position
    openDirection = []
    #The direction variable means the way the cursor is moving. 0 -> right, 1 -> down, 2 -> left, 3 -> up
    #Always starts with direction -1
    direction = -1
    #List A holds the laberinth map
    A = []
    A.append("                       ")
    for i in range (1,maxV-1,1):
        A.append(" ##################### ")
    A.append("                       ")
    #Starting from the center, iterate to create the laberith
    cursorH = centroH
    cursorV = centroV
    #Initial spot
    A[cursorV-1] = A [cursorV-1][:cursorH-1] + LABERINTH_OPEN_PATH + A [cursorV-1][cursorH:]
    #Define the laberinth corridors
    for j in range (2,11,2):
        #Horizontal
        for i in range (cursorH-(1+j),cursorH+j):
            A[cursorV-(1+j)] = A [cursorV-(1+j)][:i] + LABERINTH_OPEN_PATH + A [cursorV-(1+j)][i+1:]
        for i in range (cursorH-(1+j),cursorH+j):
            A[cursorV+(j-1)] = A [cursorV+(j-1)][:i] + LABERINTH_OPEN_PATH + A [cursorV+(j-1)][i+1:]
        #Vertical
        for i in range (cursorV-j,cursorV+j):
            A[i] = A [i][:cursorH-(1+j)] + LABERINTH_OPEN_PATH + A [i][cursorH-j:]
        for i in range (cursorV-j,cursorV+j):
            A[i] = A [i][:cursorH+(j-1)] + LABERINTH_OPEN_PATH + A [i][cursorH+j:]

    #Define the exit doors in each laberinth ring
    #1 is the upper side, 2 is right side, 3 lower side, 4 left side
    for j in range (1,11,2):
        #A random number defines on what side the door will be opened
        lado = random.randint(1,4)
        if lado == 1 :
            A[cursorV-(j+1)] = A[cursorV-(j+1)][:cursorH-1] + LABERINTH_OPEN_PATH + A [cursorV-(j+1)][cursorH:]
        elif lado == 2 :
            A[cursorV-1] = A[cursorV-1][:cursorH+(j-1)] + LABERINTH_OPEN_PATH + A [cursorV-1][cursorH+(j):]
        elif lado == 3 :
            A[cursorV+(j-1)] = A[cursorV+(j-1)][:cursorH-1] + LABERINTH_OPEN_PATH + A [cursorV+(j-1)][cursorH:]
        else :
            A[cursorV-1] = A[cursorV-1][:cursorH-(j+1)] + LABERINTH_OPEN_PATH + A [cursorV-1][cursorH-(j):]
  
    #Resolution algorithm #####################################################################
    #The direction variable means the way to follow. 0 -> right, 1 -> down, 2 -> left, 3 -> up
    	
    #Supporting functions ##############
    #Print the laberinth on the screen
    def imprimeLaberinto():
        nonlocal maxV
        nonlocal A
        for i in range (1,maxV,1):
            time.sleep (0.1) #Small delay to make the laberinth build more visually attractive
            stdscr.addstr(i,0,A[i], curses.color_pair(1))
            stdscr.refresh()
    #Function to count the number of open paths from a given position
    def numCaminos():
        nonlocal V
        nonlocal H
        nonlocal A
        nonlocal maxH
        nonlocal maxV
        nonlocal openDirection
        caminos = 0
        if (V+2) < maxV :
            if A[V+1][H] == LABERINTH_OPEN_PATH: 
                caminos += 1
                #stdscr.addstr(0,0,"1 salida abajo     ", curses.color_pair(3))
                openDirection.append (1)
        if (V-2) >= 0:
            if A[V-1][H] == LABERINTH_OPEN_PATH: 
                caminos += 1
                #stdscr.addstr(0,0,"1 salida arriba     ", curses.color_pair(3))
                openDirection.append (3)
        if (H+2) <= maxH :
            if A[V][H+1] == LABERINTH_OPEN_PATH: 
                caminos += 1
                #stdscr.addstr(0,0,"1 salida derecha     ", curses.color_pair(3))
                openDirection.append (0)
        if (H-2) >= 0:
            if A[V][H-1] == LABERINTH_OPEN_PATH: 
                caminos += 1
                #stdscr.addstr(0,0,"1 salida izquierda     ", curses.color_pair(3))
                openDirection.append (2)
        return caminos

    def moveUp():
        nonlocal nV
        nonlocal V
        nonlocal H
        nonlocal A
        nonlocal direction
        #Include the solution path in the current position
        A[V] = A [V][:H] + SOLUTION_PATH + A [V][H+1:]
        stdscr.addstr(V,H,SOLUTION_PATH, curses.color_pair(4))            
        #Include the solution path in the next position
        nV = V - 1
        A[V-1] = A [V-1][:H] + SOLUTION_PATH + A [V-1][H+1:]
        stdscr.addstr(nV,H,SOLUTION_PATH, curses.color_pair(4))
        stdscr.refresh()
        V = nV
        direction = 3
    def moveDown():
        nonlocal nV
        nonlocal V
        nonlocal H
        nonlocal A
        nonlocal direction
        #Include the solution path in the current position
        A[V] = A [V][:H] + SOLUTION_PATH + A [V][H+1:]
        stdscr.addstr(V,H,SOLUTION_PATH, curses.color_pair(4))            
        #Include the solution path in the next position
        nV = V + 1
        A[V+1] = A [V+1][:H] + SOLUTION_PATH + A [V+1][H+1:]
        stdscr.addstr(nV,H,SOLUTION_PATH, curses.color_pair(4))
        stdscr.refresh()
        V = nV
        direction = 1
    def moveRight():    
        nonlocal nH
        nonlocal H
        nonlocal V
        nonlocal A
        nonlocal direction
        #Include the solution path in the next position
        nH = H + 1
        A[V] = A [V][:H] + SOLUTION_PATH + A [V][H+1:]
        stdscr.addstr(V,nH,SOLUTION_PATH, curses.color_pair(4))
        stdscr.refresh()
        H = nH
        direction = 0
    def moveLeft():
        nonlocal nH
        nonlocal H
        nonlocal V
        nonlocal A
        nonlocal direction
        #Include the solution path in the next position
        nH = H -1
        A[V] = A [V][:H-1] + SOLUTION_PATH + A [V][H:]
        stdscr.addstr(V,nH,SOLUTION_PATH, curses.color_pair(4))
        stdscr.refresh()
        H = nH
        direction = 2
    
    #End of supporting functions ##################
    
    #We print the laberinth on the screen for the first time
    imprimeLaberinto()    
    #Final messages and closure of the build algorithm
    stdscr.addstr(maxV-1,0,"Wall symbol: " + WALL_DELIMITER + " Laberinth path: \"" + LABERINTH_OPEN_PATH + "\" ", curses.color_pair(3))
    stdscr.addstr(0,0,"Build finished! Press a key to solve     ", curses.color_pair(3))
    stdscr.refresh()
    stdscr.getkey()
    
    #################################################
    #Search algorithm to solve the laberinth
    #################################################
    #We always start at the center position
    #Flag to end the main loop
    finalizado = False
    #Start position is initially assigned
    V = centroH-1
    H = centroV-1
    #Coordinates of the next laberinth cell to try. Initially equal to the start position
    nV = V
    nH = H
    finalizado = False
    numCam = 0

    #Start resolution from the first position
    A[V] = A [V][:H] + SOLUTION_PATH + A [V][H+1:]
    stdscr.addstr(V,H,A[V][H], curses.color_pair(4))
    stdscr.refresh()
            
    #Loop to search for a solution
    while not(finalizado):
        time.sleep (0.2) #Small delay to make the laberinth build more visually attractive
        openDirection.clear()
        numCam = numCaminos()
        stdscr.addstr(0,0,"                                                                                               ", curses.color_pair(4))
        stdscr.addstr(0,0,"Laberinth resolution in progress        V=" + str(V) +" H=" + str(H), curses.color_pair(4))
        #Uncomment to debug stdscr.addstr(maxV-1,0,"V,H " + A[V][H] + " V,H+1 " + A[V][H+1] + " V,H-1 " + A[V][H-1] + " V+1,H " + A[V+1][H] + " V-1,H " + A[V-1][H] + "     ", curses.color_pair(3))
        stdscr.refresh()
        
        #Check for termination
        if (V == minV+1 or V == maxV-2 or H == minH+1 or H == maxH-2 ):
            #Final messages and algorithm closure
            stdscr.addstr(maxV-1,0,"Exit path: *                                                          ", curses.color_pair(3))
            stdscr.addstr(0,0,"Exit found! Press a key to close the program    ", curses.color_pair(3))
            stdscr.refresh()
            stdscr.getkey()
            finalizado = True
        #If there is only one open path, we take it
        elif numCam == 1: 
            #Open path on the right
            if (openDirection[0] == 0):
                moveRight()
            #Open path on top
            elif (openDirection[0] == 3):
                moveUp()
            #Open path on the left
            elif (openDirection[0] == 2):
                moveLeft()
            #Open path at the bottom
            elif (openDirection[0] == 1):
                moveDown()
        elif numCam == 2:
            #We take an exit if it exists
            if ((3 in openDirection) and (0 in openDirection) and (direction == 0)):
                moveUp()
            elif ((3 in openDirection) and (0 in openDirection)):
                moveRight()
            elif ((3 in openDirection) and (2 in openDirection) and (direction == 2)):
                moveUp()
            elif ((3 in openDirection) and (2 in openDirection) and (direction == 3)):
                moveLeft()
            elif ((3 in openDirection) and (1 in openDirection)):
                moveDown()
            elif ((0 in openDirection) and (2 in openDirection)):
                moveRight()                
            elif ((0 in openDirection) and (1 in openDirection) and (direction == 0)):
                moveDown() 
            elif ((0 in openDirection) and (1 in openDirection) and (direction == 1)):
                moveRight() 
            elif ((2 in openDirection) and (1 in openDirection) and (direction == 2)):
                moveDown()
            elif ((2 in openDirection) and (1 in openDirection) and (direction == 1)):
                moveLeft()  
        #If there are three open paths, one of them is an exit             
        elif numCam == 3:
            #We take an exit if it exists
            if ((3 in openDirection) and direction == 3):
                #Move up
                moveUp()
            elif ((1 in openDirection) and direction == 1):
                #Move down
                moveDown()
            elif ((0 in openDirection) and direction == 0):
                #Move to the right
                moveRight()
            elif ((2 in openDirection) and direction == 2):
                #Move left
                moveLeft()
        else:
            stdscr.addstr(0,0,"No exit found                                         ", curses.color_pair(3))
            stdscr.refresh()
            stdscr.getkey()
            finalizado = True            
        
wrapper(main)


