from Map import Map
from Fourmi import Fourmi
from data import get_data

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import pygame

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

