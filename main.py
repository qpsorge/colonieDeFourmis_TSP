from Map import Map
from Fourmi import Fourmi
from data import get_data

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
# graphical version
import pygame
import cv2
import time

# Retrieve data 
(_CITIES, (_CITIES_N,mean_x,mean_y,std_x,std_y), _NODES, epsilon, gamma) = get_data()

# Config for execution of main.py
graphic = False 
N_CIRCUIT = 20
N_FOURMIS = 20
df_res = pd.DataFrame()
verbose = False

# Ant search
if not(graphic):
    for pheromone_impact in [0.8] : #[0.1*i for i in range(11)]:#
        for distance_impact in [0.6] : #[0.1*i for i in range(11)]:#
            for nb_trial in range(1):
                pheromones_map = Map()

                if(verbose):
                    print(pheromones_map)

                fourmis_pop=[]

                for circuit in range(N_CIRCUIT): #circuit number
                    if verbose:
                        print(f"Circuit {circuit} ")
                    fourmis = [Fourmi(_CITIES[random.randint(0,_NODES-1)],pheromone_impact=pheromone_impact, distance_impact=distance_impact) for i in range(N_FOURMIS)]
                    for turn in range(_NODES+1):
                        if verbose:
                            print(f"Turn {turn}")
                        for f in range(len(fourmis)):
                            fourmis[f].move(
                                fourmis[f].choose_movement(pheromones_map), 
                                pheromones_map
                            )
                        if verbose:
                            print(pheromones_map)
                    if verbose:
                        [print(f) for f in fourmis]
                        [print(f.path_length()) for f in fourmis]
                    df_res[f"Circuit {circuit}"]=[f.path_length() for f in fourmis]
                    if verbose:
                        print(pheromones_map.adj_mat)
                    # Normalize the pheromone spread in map
                    pheromones_map.normalize_pheromones()
                    fourmis_pop = np.append(fourmis_pop, fourmis)
                    if verbose:
                        print(pheromones_map.adj_mat)

                print(f"Adj mat path : ")
                pheromones_map.print_results()

                if verbose:
                    print(np.array([np.round(x,2) for x in pheromones_map.adj_mat]))
                    print(f" Shape {pheromones_map.adj_mat.shape}, type {pheromones_map.adj_mat.dtype}")
                
                    print(df_res.head())
                    print(f" First circuit (0 pheromones on map) : L({df_res['Circuit 0'].mean()}, {df_res['Circuit 0'].std()})")
                    print(f" Last circuit  (Stable pheromones on map) : L({df_res[f'Circuit {N_CIRCUIT-1}'].mean()},{df_res[f'Circuit {N_CIRCUIT-1}'].std()})")

                best_f = fourmis_pop[np.argmin([f.path_length() for f in fourmis_pop])]
                print("\n====================== SOLUTION OPTIMALE")
                print(best_f)
                print(f"Distance du chemin : {np.round(best_f.path_length(),2)} u.l (distance euclidienne longitude, latitude)")
                print("======================")
                                
                #plt.figure(figsize=(12,6))
                #df_res[["Circuit "+str(i*20) for i in range(9)]].boxplot()
                #plt.title(f"Boites à moustaches représentant la disparité des chemins explorés par 20 fourmis à chaque circuit\npheromone_impact={np.round(pheromone_impact,2)} , distance_impact={np.round(distance_impact,2)}")
                #plt.ylabel("Longueur du chemin parcouru")
                #plt.show()
                #plt.savefig(f"AnalyseStatistique/{nb_trial}_boxplot_p{pheromone_impact*100}_d{distance_impact*100}.png")

else : #Graphic version yet to be fixed (just drop from colab notebook)
    pygame.init()

    WIDTH=700
    HEIGHT=700
    OFFSET=WIDTH/2
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    done = False
    is_blue = True
    x = 0
    y = 0
    epsilon=1

    font=pygame.font.Font(None, 24)
    city_color = (255, 100, 0)
    ant_color  = (0,255,100)
    __circuit__ = []

    def text_objects(text, font):
        textSurface = font.render(text, True, (255,255,255))
        return textSurface, textSurface.get_rect()

    def message_display(text, coord):
        largeText = pygame.font.Font(None, 24)
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = coord
        screen.blit(TextSurf, TextRect)
        pygame.display.update()

    def draw_map():
        # Center point
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(OFFSET,OFFSET,1,1))
                
        # Draw every city position and text it
        coord_text=[]
        for i in range(len(_CITIES_N)):
            city=_CITIES_N[i]
            x_coord = OFFSET+(int)((OFFSET-200)*city[0])
            y_coord = OFFSET+(int)((OFFSET-200)*city[1])
            coord_text.append((x_coord, y_coord))
            pygame.draw.rect( screen, city_color, pygame.Rect(x_coord,y_coord, 16,16) )
            __circuit__.append((x_coord,y_coord))
        return coord_text

    def display_and_clear(n, end_turn=False):
        # DISPLAY
        pygame.display.flip()

        #convert image so it can be displayed in OpenCV
        view = pygame.surfarray.array3d(screen)
        #  convert from (width, height, channel) to (height, width, channel)
        view = view.transpose([1, 0, 2])
        #  convert from rgb to bgr
        img_bgr = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)
        #Display image, clear cell every 0.5 seconds
        #cv2.imshow("img",img_bgr)

        coord_text = draw_map()
        for i in range(len(coord_text)):
            message_display(_CITIES[i][0], coord_text[i])

        time.sleep(n)
        #output.clear()
        # Clean screen
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,WIDTH,HEIGHT) )
        # Draw Map
        coord_text = draw_map()
        for i in range(len(coord_text)):
            message_display(_CITIES[i][0], coord_text[i])


    # END FONCTIONS DECLARATION

    while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True
            
            # Clean screen
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,WIDTH,HEIGHT) )
            # Draw Map
            draw_map()
            
            #SMA ALGO FOR ANTS
            pheromones_map = Map()
            print(pheromones_map.adj_mat)
            f = Fourmi(_CITIES[0])
            
            #ALGO
            n_fourmis = 3
            fourmis= [Fourmi(_CITIES[random.randint(0,_NODES-1)]) for i in range(n_fourmis)]
            colors = [(200+i*55.0/n_fourmis,200+i*55.0/n_fourmis,200+i*55/n_fourmis) for i in range(len(fourmis))]
            for turn in range(_NODES+1):
                message_display(f"Turn {turn}", (350,350))
                for i in range(len(fourmis)):
                    f=fourmis[i]
                    f.move(
                        f.choose_movement(pheromones_map), 
                        pheromones_map
                    )
                    #GUI ANT
                    x_ant,y_ant = f.coord_to_display(350, mean_x,mean_y,std_x,std_y)
                    pygame.draw.circle(screen,colors[i],   (x_ant+8,y_ant+8),8,0)
                    #pygame.draw.rect(screen, colors[i], pygame.Rect(x_ant, y_ant, 18, 18))
                display_and_clear(3)

            display_and_clear(1, True)
            done=True
            
            pheromones_map.print_results()
            print(__circuit__)
