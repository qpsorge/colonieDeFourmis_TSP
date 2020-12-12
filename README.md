# Approche de résolution du problème du voyageur de commerce, ou TSP (Traveling-Salesman Problem) :

### How to setup :
##### 1 : install dependencies
> pip install -r requirement.txt
##### 2 : Launch main.py (choose to put verbose=True or verbose=False to have printed execution)
> python main.py
##### Else : execute cells of global_notebook_colab.ipynb (for the graphical version upload it to colab to test it)
###### A améliorer : add graphical version using pygame without colab requirement

### Présentation de cette solution au problème TSP
Basée sur les systèmes multi agents, et notamment sur les colonies de fourmis.
Des statistiques calculées sur la convergence de l'algorithme d'exploration des colonies de fourmis sont fournis.
Dans le dossier AnalyseStatistique, vous trouverez de nombreux boxplots représentant des statistiques descriptives sur l'évolution de la longueur du chemin parcouru par 20 fourmis au cours d'un certain nombre de circuit en fonction de la prise en compte de la 
* visibilité (inverse de la distance)
* phéromones (basés sur la mémoire collective)

### Résumé global
Une carte commune est modélisée comme étant un graphe où l'on peut déposer entre chaque noeud (sur les arcs) des quantités de phéromones qui vont influencer le choix des fourmis.
A chaque tour, les fourmis se déplacent sur une carte commune où est disponible le taux de phéromone par arc. 
Chaque fourmi change donc de ville en fonction de deux critères : taux de phéromone et visibilité.
Lorsque les fourmis ont fini leur circuit (passage par toutes les villes en revenant à la ville initiale), elles déposent une quantité de phéromone sur chaque arc inversement proportionnelle à la longueur totale du circuit parcouru.
Ainsi, les fourmis ayant trouvé les meilleurs circuit (distance la plus faible), vont déposer des quantités de phéromone plus importantes et mener vers une certaine convergence vers une solution de distance faible.

### Génie Logiciel
Pour modéliser cette colonie de fourmis, j'ai fait le choix personnel d'utiliser 2 classes pour factoriser au mieux le code:
* Fourmi (pour coder chaque agent et ses intéractions élémentaires)
* Map    (pour fournir une carte globale avec des methodes pour effectuer facilement certaines opérations)
###### A améliorer : responsabilité séparée