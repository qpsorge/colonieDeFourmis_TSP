# global dependancies
import numpy as np
import matplotlib.pyplot as plt
# local dependancies
from data import get_data
from utilities import distance

(_CITIES, _, _NODES, _, _) = get_data()

class Map:
    def __init__(self):
        self.adj_mat = np.ones((_NODES,_NODES))/_NODES
        self.pheromones_to_add = np.zeros((_NODES,_NODES))
    
    def add_pheromones(self, quantity, path):
        # for each path arc
        for i in range(len(path)-1):
          node_ini, node_end = path[i], path[i+1]
          #extract index of node :
          index_ini, index_end = _CITIES.index(node_ini), _CITIES.index(node_end)
          #Add pheromones in the good arc
          self.pheromones_to_add[index_ini,index_end]+=quantity
          self.pheromones_to_map()
    
    def pheromones_to_map(self,ro=0.8):
        self.adj_mat= ro*self.adj_mat + self.pheromones_to_add
    
    def normalize_pheromones(self):
        self.adj_mat/=np.sum(self.adj_mat)
    
    def get_pheromones_intensity(self, node_ini, node_end):
        index_ini = _CITIES.index(node_ini)
        index_end = _CITIES.index(node_end)
        return self.adj_mat[index_ini,index_end]

    def path_from_adj_mat(self):
        adj_mat_copy = self.adj_mat.copy()
        tab=[0]
        for _ in range(_NODES):
          if (np.argmax(adj_mat_copy[tab[-1],:]) in tab):
            adj_mat_copy[tab[-1],np.argmax(adj_mat_copy[tab[-1],:])]=0
          tab.append(np.argmax(adj_mat_copy[tab[-1],:]))
        return [(i,_CITIES[i][0]) for i in tab]

    def path_length_from_adj_mat(self):
      path = self.path_from_adj_mat()
      coords_path = [_CITIES[x[0]][1] for x in path]
      path_distance_tab = [distance(coords_path[i], coords_path[i+1]) for i in range(len(coords_path)-1)]
      return np.sum(path_distance_tab)

    def print_results(self):
      #Print Adj mat
      data = self.adj_mat
      fig, ax = plt.subplots()
      im = ax.imshow(data, cmap=plt.get_cmap('hot'), interpolation='nearest',
                        vmin=np.min(data), vmax=np.max(data))
      fig.colorbar(im)
      plt.title("Normalized adjacence matrix with pheromone's intensity")
      plt.xlabel("City nodes")
      plt.ylabel("City nodes")
      plt.show()
      # Path & length
      print(self.path_from_adj_mat())
      print(self.path_length_from_adj_mat())
      return 0

    def __str__(self):
        print(f"Adj mat of pheromones :\n{self.adj_mat}")
        return ""
