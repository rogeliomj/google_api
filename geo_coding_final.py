import googlemaps
import pandas as pd
import numpy as np
import json

dir = '/Users/rogeliomj/Documents/python/tesis/plataforma_cdmx/inmuebles_danados.csv'
df = pd.read_csv(dir)
direcciones = df.iloc[:,5].tolist()

# Nos conectamos al API de Google Maps

gmaps_key = googlemaps.Client(key = 'AIzaSyAdZKjevohQs7fHJn3NpZJ70DDtcAsj4rI')
lat = []
lng = []
for i in direcciones:
    try:
        geocode_result = gmaps_key.geocode(i)
        lat_ = geocode_result[0]['geometry']['location']['lat']
        lng_ = geocode_result[0]['geometry']['location']['lng']
        lat.append(lat_)
        lng.append(lng_)

    except IndexError:
        lat.append(np.nan)
        lng.append(np.nan)

df_coordenadas = pd.DataFrame({'latitud':lat,'longitud':lng})

df['i1'] = df.index
df_coordenadas['i1'] = df_coordenadas.index

join = pd.merge(df, df_coordenadas, how = 'right', on = 'i1')

del join['i1']

join.to_csv('/Users/rogeliomj/Documents/python/tesis/plataforma_cdmx/escuelas_danadas_geocoded.csv', index = False)
