import googlemaps
import pandas as pd
import numpy as np

df1 = pd.read_csv('condesa.csv', encoding = 'utf-16', index_col = 'Unnamed: 0')
df1.reset_index(inplace=True)
del df1['index']
direcciones = df1.iloc[:, 1].tolist()

# Nos conectamos al API de Google Maps

gmaps_key = googlemaps.Client(key = 'AIzaSyAdZKjevohQs7fHJn3NpZJ70DDtcAsj4rI')
geo_tags = []
for i in direcciones[0:5]:
    try:
        geocode_result = gmaps_key.geocode(i)
        lat = geocode_result[0]['geometry']['location']
        geo_tags.append(lat)
    except IndexError:
        geo_tags.append(np.nan)

df_coordenadas = pd.DataFrame({'geo_tag':geo_tags})

df1['i1'] = df1.index
df_coordenadas['i1'] = df_coordenadas.index

join = pd.merge(df1, df_coordenadas, how = 'right', on = 'i1')

del join['i1']

join['merge'] = join['geo_tag'].astype(str)

# API de Google Places

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


# Preparación para distance matrix

join2 = pd.merge(right = join, left= popular_places, how = 'left', on = 'merge')
join2['i1'] = join2.index
# Creamos listas con las coordenadas de inicio y final para usarlas como inputs en el api de distance matrix

inicio = join2.loc[:,'geo_tag'].tolist()
fin = join2.loc[:,'coord_popular_place'].tolist()

distancia_km = []
tiempo_caminando = []
gmaps = googlemaps.Client(key='AIzaSyAdZKjevohQs7fHJn3NpZJ70DDtcAsj4rI')

for x,y in zip(inicio,fin):
    origins = x
    destination = y
    result = gmaps.distance_matrix(origins, destination, mode='walking')
    distancia_km.append(result["rows"][0]["elements"][0]["distance"]["text"])
    tiempo_caminando.append(result["rows"][0]["elements"][0]["duration"]["text"])

distance_matrix = pd.DataFrame({'distancia_km':distancia_km, 'tiempo_caminando':tiempo_caminando})
distance_matrix['i1'] = distance_matrix.index

join3 = pd.merge(left = join2, right = distance_matrix, how='left', on = 'i1')

# join3.to_csv('final_sample.csv', encoding = 'utf-8')
join3.to_csv('final_sample.csv', encoding = 'utf-16')
