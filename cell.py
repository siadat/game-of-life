import pygame
import sys
import os
import random
import math
from pygame.locals import *

width  = 800
height = 800

initial_state = [\
        "---------------------------", 
        "---------------------------", 
        "---##----------------------", 
        "----#----------------------", 
        "------#--##----#-----------", 
        "----------#---#-#----------", 
        "---------------#-----------", 
        "----------##---#-----------", 
        "----------##---#-----------", 
        "---------------#-----------", 
        "-----#---------#----##-----", 
        "---#-#---------#----#------", 
        "----##---------#----#------",
        "---------------------------", 
        "---------------------------", 
        "---------------------------", 
        "-------------#-------------", 
        "-----------#-#-------------", 
        "------------##-------------",
        ]

def get_new_vel(vel, acc):
    vel += acc
    if vel != 0:
        vel /= 1.5
        if abs(vel) < 0.01:
            vel = 0
    return vel

def ascii_to_ca(str_list):
    ca_dict = {}
    pos_y = 0
    for str in str_list:
        pos_y += 1
        pos_x = 0
        for char in str:
            pos_x += 1
            if char is not '-':
                ca_dict[(pos_x, pos_y)] = [1, 0]
    return ca_dict

def update_neighbours(dict):
    death_rate = 0.05
    newdict = {}
    for key in dict:
        
        if dict[key][0] <= 0: # out of range
            continue
        elif dict[key][0] > 0 and dict[key][0] < 1: # tah moonde
            if key not in newdict:
                newdict[key] = dict[key]
            else:
                newdict[key][0] = dict[key][0]
            continue

        if key not in newdict:
            newdict[key] = [dict[key][0],0]
        else:
            newdict[key][0] = dict[key][0]

        x = key[0]
        y = key[1]
        
        if (x+1, y) in newdict:
            newdict[(x+1, y)][1] += 1
        else:
            newdict[(x+1, y)] = [0, 1]

        if (x, y+1) in newdict:
            newdict[(x, y+1)][1] +=1
        else:
            newdict[(x, y+1)] = [0, 1]

        if (x+1, y+1) in newdict:
            newdict[(x+1, y+1)][1] += 1
        else:
            newdict[(x+1, y+1)] = [0, 1]

        if (x-1, y) in newdict:
            newdict[(x-1, y)][1] += 1
        else:
            newdict[(x-1, y)] = [0, 1]

        if (x, y-1) in newdict:
            newdict[(x, y-1)][1] += 1
        else:
            newdict[(x, y-1)] = [0, 1]

        if (x-1, y-1) in newdict:
            newdict[(x-1, y-1)][1] += 1
        else:
            newdict[(x-1, y-1)] = [0, 1]

        if (x+1, y-1) in newdict:
            newdict[(x+1, y-1)][1] += 1
        else:
            newdict[(x+1, y-1)] = [0, 1]

        if (x-1, y+1) in newdict:
            newdict[(x-1, y+1)][1] += 1
        else:
            newdict[(x-1, y+1)] = [0, 1]

    for key in newdict:
        neighbours = newdict[key][1]
        newdict[key][1] = 0
        
        if neighbours == 3:
            newdict[key][0] = 1
        elif newdict[key][0]==1:
            if neighbours == 2:
                newdict[key][0] = 1
            elif neighbours > 3 or neighbours < 2:
                #newdict[key][0] = 0
                newdict[key][0] = newdict[key][0] - death_rate
                
        elif newdict[key][0]<1 and newdict[key][0]>0:
            newdict[key][0] = newdict[key][0] - death_rate
            if newdict[key][0] < 0:
                newdict[key][0] = 0
    return newdict




def main():
    print("""
    Usage:
        Play/Pause         Enter
        Add alive cells    Left Mouse Button
        Pan                Up/Down/Left/Right Arrows
        Zoom               -/=
        Quit               Esc or Q
    """)

    if not pygame.font:  print 'Warning, fonts disabled'
    if not pygame.mixer: print 'Warning, sound disabled'

    pygame.init()

    top = left = 0
    cell_width = 10
    cell_margin = 0
    r = g = b = 0
    counter = 0

    window = pygame.display.set_mode((width, height)) 
    pygame.display.set_caption('CA') 
    screen = pygame.display.get_surface()
    ground = pygame.Surface(screen.get_size() )
    ground.fill((20, 20, 50))
    ground = ground.convert()
    grid = pygame.Surface((cell_width,cell_width))
    grid.fill((250, 250, 250))
    grid = grid.convert()
    clock = pygame.time.Clock()
    paused = True
    mouse_down = False

    width_growing_vel = 0
    width_growing_acc = 0
    panx_move_vel = 0
    panx_move_acc = 0
    pany_move_vel = 0
    pany_move_acc = 0

    ca_dict = ascii_to_ca(initial_state)

    while True:
        grid = pygame.Surface((cell_width,cell_width))
        grid = grid.convert()
        counter += 1
        input = pygame.event.get()

        for event in input:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    sys.exit(0)
                elif event.key == pygame.K_RETURN:
                    paused = not paused
                elif event.key == pygame.K_MINUS:
                    width_growing_acc = -2
                elif event.key == pygame.K_EQUALS:
                    width_growing_acc = 2
                elif event.key == pygame.K_LEFT:
                    panx_move_acc = +40
                elif event.key == pygame.K_RIGHT:
                    panx_move_acc = -40
                elif event.key == pygame.K_UP:
                    pany_move_acc = +40
                elif event.key == pygame.K_DOWN:
                    pany_move_acc = -40
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False

        width_growing_vel = get_new_vel(width_growing_vel, width_growing_acc)

        cell_width += width_growing_vel
        if cell_width < 1:
            cell_width = 1

        panx_move_vel = get_new_vel(panx_move_vel, panx_move_acc)
        pany_move_vel = get_new_vel(pany_move_vel, pany_move_acc)
        
        left += panx_move_vel
        top += pany_move_vel

        panx_move_acc = 0
        pany_move_acc = 0
        width_growing_acc = 0

        if mouse_down:
            mouse_pos = pygame.mouse.get_pos()
            i = (mouse_pos[0] - left) / (cell_width+cell_margin)
            j = (mouse_pos[1] - top) / (cell_width+cell_margin)

            ca_dict[(i,j)] = [1,0]

        screen.blit(ground, (0, 0))
        for (cell, value) in ca_dict.iteritems():
            
            if value[0] == 0:
                continue

            color = math.floor ( value[0]*250 );

            r = color
            g = color - (256 - color) ** 2 / 80
            b = 0
            if g < 0:
                g = 0
            
            grid.fill((r,g,b))
            screen.blit(grid, (
                cell[0] * (cell_width + cell_margin) + left, 
                cell[1] * (cell_width + cell_margin) + top))
                
        pygame.display.flip()
        clock.tick(30)
        if not paused:
            ca_dict = update_neighbours(ca_dict)

if __name__ == "__main__":
  sys.exit(main())
