# global dependancies
import random
import numpy as np
# local dependancies
from Map import Map
from utilities import distance
from data import get_data

(_CITIES, _, _NODES, epsilon, gamma) = get_data()

class Fourmi:
    __prenoms__=["Gabrielle", "Alphonse", "Kevin", "Loana", "Fleche","Mimi","Marguerite","Pomme","Hercule","Gigantor","Atlas","Tom","Rachelle","Violette","MiniPouce","Rinie","Pitchoune","Josie","Lucie","Garfield","Rose","Greg","Laurent","Florian","Solene","Cathy","Marie","Isabelle","Arnaud","Paul","Lea","Quentin","Marine","Brigitte","Judith","Sucrine","Mirabelle","Citrouille","Ange","Cléopatre","Cléo"]
    def __init__(self, position:tuple, pheromone_impact=None, distance_impact=None):
        '''
        Creates an ant with \n
        - an initial position \n
        - a list of string (a memory of visited cities)
        '''
        self.pos = position if position is not None else None
        self.cities = [position]
        self.quality = 5
        self.prenom = Fourmi.__prenoms__[random.randint(0,len(Fourmi.__prenoms__)-1)]
        self.size = random.randint(5,10)
        self.color = tuple([100+30*random.randint(0,4) for i in range(3)])

        self.pheromone_impact = 0.8 if pheromone_impact is None else pheromone_impact
        self.distance_impact = 0.7 if distance_impact is None else distance_impact
    
    def choose_movement(self, map:Map):
        '''
        Returns a tuple (initial_node, future_node) for the ant
        '''
        #Une fourmi ne peut visiter qu'une fois chaque ville
        possible_move=[]

        # Cas 1 : on n a pas encore visité toutes les villes
        if(len(self.cities) < len(_CITIES)):
          
          for city in _CITIES:
              if(city not in self.cities):
                  possible_move.append(city)
          if(len(possible_move)>0):
              #Les villes proches ont plus de chance d'être choisies => softmax
              distances = []
              for city in possible_move:
                  distances.append(distance(self.pos[1],city[1])) # distance ini-arrivée
              
              visibility = [1/(x+epsilon) for x in distances]
              powered_visibility = np.array(visibility)**(self.distance_impact)

              pheromones_intensity = [map.get_pheromones_intensity(self.pos,city) for city in possible_move]
              powered_pheromones_intensity = np.array(pheromones_intensity)**(self.pheromone_impact)
              
              chances =  (gamma + powered_visibility * powered_pheromones_intensity) / np.sum((gamma + powered_visibility * powered_pheromones_intensity)) #softmax(visibility)

              #for i in range(len(possible_move)):
                  #print(f"Score de {self.pos[0]} à {possible_move[i][0]} : visibility {np.round(visibility[i],1)}, pheromones {np.round(pheromones_intensity[i],1)},chance {np.round(chances[i],3)}")
              
              choice = np.argmax(chances)
              #print(f"Choix : {possible_move[choice]}")
              return (self.pos,possible_move[choice])

        # Cas 2 : On a visité toutes les villes, il faut rentrer à la dernière
        elif (len(self.cities) == len(_CITIES)):
          return (self.pos,self.cities[0]) 
        # Cas 3 : la fourmi a fini son tour
        elif (len(self.cities) == len(_CITIES)+1):
          return 0
        else :
          return -1

    def move(self,possible_move_choice,map):
        if type(possible_move_choice) == tuple :
          self.pos=possible_move_choice[1]
          self.cities.append(possible_move_choice[1])
        elif (possible_move_choice == 0):
          #print("Depot des phéromones sur le circuit")
          #ajout de phéromone
          map.add_pheromones(quantity=self.quality/self.path_length(), path=self.cities) #node_ini=possible_move_choice[0],node_end=possible_move_choice[1])
          map.pheromones_to_map()
        else : 
          print("Useless c'est la fin ^^'")
          return 0

    def path_length(self):
      coords_path = [x[1] for x in self.cities]
      path_distance_tab = [distance(coords_path[i], coords_path[i+1]) for i in range(len(coords_path)-1)]
      return np.sum(path_distance_tab)

    def coord_to_display(self, OFFSET, mean_x, mean_y, std_x, std_y ):
        x_coord = OFFSET+(int)((OFFSET-200)*(self.pos[1][0]-mean_x)/std_x)
        y_coord = OFFSET+(int)((OFFSET-200)*(self.pos[1][1]-mean_y)/std_y)
        return (x_coord,y_coord)
                   
    def __str__(self):
        print(f"Agent secret {self.prenom} au rapport")
        print(f"\tPosition actuelle : {self.pos[0]}")
        print(f"\tVilles visitées : {[x[0] for x in self.cities]}")
        return ""
