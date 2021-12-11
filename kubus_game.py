import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

Titik = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

Garis = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

Sisi = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

Warna = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )

def Set_Titik(Jarak_max, Jarak_min = -20, camera_X = 0, camera_Y = 0):
    camera_X = -1*int(camera_X)
    camera_Y = -1*int(camera_Y)

    X_acak = random.randrange(camera_X-75,camera_X+75)
    Y_acak = random.randrange(camera_Y-75,camera_Y+75)
    Z_acak = random.randrange(-1*Jarak_max,Jarak_min)

    Titik_baru = []

    for ttk in Titik:
        ttk_baru = []

        new_X = ttk[0] + X_acak
        new_Y = ttk[1] + Y_acak
        new_Z = ttk[2] + Z_acak

        ttk_baru.append(new_X)
        ttk_baru.append(new_Y)
        ttk_baru.append(new_Z)

        Titik_baru.append(ttk_baru)

    return Titik_baru

def Kubus(Titik): 
    glBegin(GL_QUADS)
    for surface in Sisi:
        x = 0
        for vertex in surface:
            x+=1
            glColor3fv(Warna[x])
            glVertex3fv(Titik[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in Garis:
        for vertex in edge:
            glVertex3fv(Titik[vertex]) 
    glEnd()

def Main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    Jarak_max = 100
    gluPerspective(45, (display[0]/display[1]), 0.1, Jarak_max)
    glTranslatef(0,0, -40)
    
    X_move = 0
    Y_move = 0

    cur_X = 0
    cur_Y = 0

    game_speed = 2
    direction_speed = 2

    Kubus_ku = {}

    for x in range(50):
        Kubus_ku[x] = Set_Titik (Jarak_max) 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    X_move = direction_speed
                if event.key == pygame.K_RIGHT:
                    X_move = -1*direction_speed

                if event.key == pygame.K_UP:
                    Y_move = -1*direction_speed
                if event.key == pygame.K_DOWN:
                    Y_move = direction_speed
        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    X_move = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    Y_move = 0
            
        x = glGetDoublev(GL_MODELVIEW_MATRIX)
        pov_Z = x[3][2]

        cur_X += X_move
        cur_Y += Y_move

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glTranslatef(X_move,Y_move,game_speed)

        for each_cube in Kubus_ku:
            if pov_Z <= Kubus_ku[each_cube][0][2]:
                new_max = int(-1*(pov_Z-(Jarak_max*2)))
                Kubus_ku[each_cube] = Set_Titik(new_max,int(pov_Z-Jarak_max), cur_X, cur_Y)
           
        pygame.display.flip()
Main()
