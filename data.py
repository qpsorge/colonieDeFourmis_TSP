import numpy as np

# Latitude longitude
_CITIES = (
    ("Bordeaux", (44.833333,-0.566667)), 
    ("Paris",(48.8566969,2.3514616)),
    ("Nice",(43.7009358,7.2683912)),
    ("Lyon",(45.7578137,4.8320114)),
    ("Nantes",(47.2186371,-1.5541362)),
    ("Brest",(48.4,-4.483333)),
    ("Lille",(50.633333,3.066667)),
    ("Clermont-Ferrand",(45.783333,3.083333)),
    ("Strasbourg",(48.583333,7.75)),
    ("Poitiers",(46.583333,0.333333)),
    ("Angers",(47.466667,-0.55)),
    ("Montpellier",(43.6,3.883333)),
    ("Caen",(49.183333,-0.35)),
    ("Rennes",(48.083333,-1.683333)),
    ("Pau",(43.3,-0.366667))
)

_NODES = len(_CITIES)
epsilon = 0.0001
gamma = 0.2

def get_data():
    #Returns (_CITIES, preprocessing_cities(_CITIES), _NODES, epsilon, gamma)
    return (_CITIES, preprocessing_cities(_CITIES), _NODES, epsilon, gamma)

# Preprocessing
def preprocessing_cities(_CITIES):
    _CITIES_POS = [ [x[1][0],x[1][1]] for x in _CITIES ]

    _CITIES_X=[x[0] for x in _CITIES_POS]
    _CITIES_Y=[y[1] for y in _CITIES_POS]

    mean_x, mean_y = np.mean(_CITIES_X), np.mean(_CITIES_Y)
    std_x, std_y   = np.std(_CITIES_X), np.std(_CITIES_Y)

    print(f"X\nMean : {mean_x}, Standard deviation : {mean_y}\n")
    print(f"Y\nMean : {std_x}, Standard deviation : {std_y}")

    _CITIES_N_X= (_CITIES_X-mean_x)/std_x
    _CITIES_N_Y= (_CITIES_Y-mean_y)/std_y

    _CITIES_N = []
    for i in range(len(_CITIES_N_X)):
        _CITIES_N.append([_CITIES_N_X[i],_CITIES_N_Y[i]])

    _CITIES_N = (((_CITIES_N)))
    return (_CITIES_N,mean_x,mean_y,std_x,std_y)
