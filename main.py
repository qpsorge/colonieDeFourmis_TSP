from Map import Map
from Fourmi import Fourmi
from data import get_data
import pygame
import numpy as np
import random
import pandas as pd
import matplotlib.pyplot as plt

(_CITIES, (_CITIES_N,mean_x,mean_y,std_x,std_y), _NODES, epsilon, gamma) = get_data()

graphic = False
df_res = pd.DataFrame()

if not(graphic):

    for pheromone_impact in [0.1*i for i in range(11)]:#[0.8] : #
        for distance_impact in [0.1*i for i in range(11)]:#[0.6] : #
            for nb_trial in range(3):
                pheromones_map = Map()
                print(pheromones_map)

                fourmis_pop=[]

                for circuit in range(161): #circuit number
                    print(f"Circuit {circuit} ")
                    fourmis = [Fourmi(_CITIES[random.randint(0,_NODES-1)],pheromone_impact=pheromone_impact, distance_impact=distance_impact) for i in range(20)]
                    for turn in range(_NODES+1):
                        #print(f"Turn {turn}")
                        for f in range(len(fourmis)):
                            fourmis[f].move(
                                fourmis[f].choose_movement(pheromones_map), 
                                pheromones_map
                            )
                        #print(pheromones_map)
                        # Add new pheromones & evaporate old ones
                        #pheromones_map.pheromones_to_map()
                        #Normalize them 
                    #[print(f) for f in fourmis]
                    #[print(f.path_length()) for f in fourmis]
                    df_res[f"Circuit {circuit}"]=[f.path_length() for f in fourmis]
                    #print(pheromones_map.adj_mat)
                    pheromones_map.normalize_pheromones()
                    fourmis_pop = np.append(fourmis_pop, fourmis)
                    #print(pheromones_map.adj_mat)


                #print(np.array([np.round(x,2) for x in pheromones_map.adj_mat]))
                print(f" Shape {pheromones_map.adj_mat.shape}, type {pheromones_map.adj_mat.dtype}")

                print(f"Adj mat path : ")
                #pheromones_map.print_results()

                best_f = fourmis_pop[np.argmin([f.path_length() for f in fourmis_pop])]
                print("======================")
                print(best_f)
                print(best_f.path_length())
                print("======================")

                print(df_res)
                print(f" First circuit (0 pheromones on map) : L({df_res['Circuit 0'].mean()}, {df_res['Circuit 0'].std()})")
                print(f" Last circuit  (Stable pheromones on map) : L({df_res['Circuit 160'].mean()},{df_res['Circuit 160'].std()})")
                
                plt.figure(figsize=(12,6))
                df_res[["Circuit "+str(i*20) for i in range(9)]].boxplot()
                plt.title(f"Boites à moustaches représentant la disparité des chemins explorés par 20 fourmis à chaque circuit\npheromone_impact={np.round(pheromone_impact,2)} , distance_impact={np.round(distance_impact,2)}")
                plt.ylabel("Longueur du chemin parcouru")
                #plt.show()
                plt.savefig(f"AnalyseStatistique/{nb_trial}_boxplot_p{pheromone_impact*100}_d{distance_impact*100}.png")

