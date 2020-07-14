import googlemaps
import pandas as pd
import numpy as np
import json

inicio = join2.loc[:,'geo_tag'].tolist()
fin = join2.loc[:,'coord_popular_place'].tolist()

distancia_km = []
tiempo_caminando = []

gmaps = googlemaps.Client(key='')

for x,y in zip(inicio,fin):
    origins = x
    destination = y
    result = gmaps.distance_matrix(origins, destination, mode='walking')
    distancia_km.append(result["rows"][0]["elements"][0]["distance"]["text"])
    tiempo_caminando.append(result["rows"][0]["elements"][0]["duration"]["text"])

distance_matrix = pd.DataFrame({'distancia_km':distancia_km, 'tiempo_caminando':tiempo_caminando})
distance_matrix['i1'] = distance_matrix.index
join2['i1'] = join2.index


join3 = pd.merge(left = join2, right = distance_matrix, how='left', on = 'i1')
del join3['merge']
del join3['i1']

# sample_utf_8.to_csv('final_sample.csv', encoding = 'utf-8')
# sample_utf_16.to_csv('final_sample.csv', encoding = 'utf-16')
