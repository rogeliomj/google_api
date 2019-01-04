import googlemaps
import pandas as pd
import numpy as np
import json

punto_inicial = []
coord = []
name = []
address = []
type_ = []

gmaps = googlemaps.Client(key = 'AIzaSyAdZKjevohQs7fHJn3NpZJ70DDtcAsj4rI')

for geo in geo_tags:
    try:
        search_on_location = gmaps.places_nearby(type="restaurant", location=geo, radius=1000)
        for x in range(len(search_on_location['results'])):
            coordinates = search_on_location['results'][x]['geometry']['location']
            nombre = search_on_location['results'][x]['name']
            direccion = search_on_location['results'][x]['vicinity']
            tipo = search_on_location['results'][x]['types'][0]
            coord.append(coordinates)
            name.append(nombre)
            address.append(direccion)
            type_.append(tipo)
            punto_inicial.append(str(geo))
    except TypeError:
        coord.append(np.nan)
        name.append(np.nan)
        address.append(np.nan)
        type_.append(np.nan)
        punto_inicial.append(str(geo))

popular_places = pd.DataFrame({'merge':punto_inicial, 'coord_popular_place':coord, 'nombre':name, 'Dirección_pop_place':address, 'tipo':type_})
