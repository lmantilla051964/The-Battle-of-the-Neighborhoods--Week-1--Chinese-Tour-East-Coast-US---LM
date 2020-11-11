#!/usr/bin/env python
# coding: utf-8

# In[14]:


import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe
import folium # map rendering library

print('Libraries imported.')


# In[31]:


###Import Libraries for the Notebook - To understand where in the East Coast i am going to start my cuisien tourism


# In[15]:


get_ipython().system('conda install -c conda-forge geopy --yes ')
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values


# In[32]:


##Prepare Foursquare for the localization of Chinese Venues in 4 main Cities in the East Coast


# In[16]:


CLIENT_ID = 'HTEQQEAY2ZKJEFL1UTEQMSBQKNTDMEJ4TF4DBLCLGFS2D0YK' # your Foursquare ID
CLIENT_SECRET = 'FYIR54J22WICJ0RA0XBYE4C0SX20JJADKI3XFDODWE4ICGHZ' # your Foursquare Secret
VERSION = '20201111' # Foursquare API version

print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)


# In[17]:


# type your answer here
LIMIT = 500 # Maximum is 100
cities = ["New York, NY", 'Chicago, IL', 'Jersey City, NJ', 'Boston, MA']
results = {}
for city in cities:
    url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&near={}&limit={}&categoryId={}'.format(
        CLIENT_ID, 
        CLIENT_SECRET, 
        VERSION, 
        city,
        LIMIT,
        "4bf58dd8d48988d145941735") # CHINESE PLACE CATEGORY ID
    results[city] = requests.get(url).json()


# In[18]:


df_venues={}
for city in cities:
    venues = json_normalize(results[city]['response']['groups'][0]['items'])
    df_venues[city] = venues[['venue.name', 'venue.location.address', 'venue.location.lat', 'venue.location.lng']]
    df_venues[city].columns = ['Name', 'Address', 'Lat', 'Lng']


# In[33]:


##To understand the Number of Venues per City


# In[20]:


## Number of Venues per City NY, Chicago, NJ, Boston


# In[19]:


maps = {}
for city in cities:
    city_lat = np.mean([results[city]['response']['geocode']['geometry']['bounds']['ne']['lat'],
                        results[city]['response']['geocode']['geometry']['bounds']['sw']['lat']])
    city_lng = np.mean([results[city]['response']['geocode']['geometry']['bounds']['ne']['lng'],
                        results[city]['response']['geocode']['geometry']['bounds']['sw']['lng']])
    maps[city] = folium.Map(location=[city_lat, city_lng], zoom_start=11)

    # add markers to map
    for lat, lng, label in zip(df_venues[city]['Lat'], df_venues[city]['Lng'], df_venues[city]['Name']):
        label = folium.Popup(label, parse_html=True)
        folium.CircleMarker(
            [lat, lng],
            radius=5,
            popup=label,
            color='blue',
            fill=True,
            fill_color='#3186cc',
            fill_opacity=0.7,
            parse_html=False).add_to(maps[city])  
    print(f"Total number of Chinese places in {city} = ", results[city]['response']['totalResults'])
    print("Showing Top 100")


# In[34]:


## Once we identified the number of chinese venues in the 4 cities i need to understand the density and distance to spend less money in transportation to visist them


# In[21]:


maps[cities[0]]


# In[22]:


maps[cities[1]]


# In[23]:


maps[cities[2]]


# In[24]:


maps[cities[3]]


# In[36]:


## Creates a Central point in each of the cities to see the average distance - Mean Distance


# In[25]:


maps = {}
for city in cities:
    city_lat = np.mean([results[city]['response']['geocode']['geometry']['bounds']['ne']['lat'],
                        results[city]['response']['geocode']['geometry']['bounds']['sw']['lat']])
    city_lng = np.mean([results[city]['response']['geocode']['geometry']['bounds']['ne']['lng'],
                        results[city]['response']['geocode']['geometry']['bounds']['sw']['lng']])
    maps[city] = folium.Map(location=[city_lat, city_lng], zoom_start=11)
    venues_mean_coor = [df_venues[city]['Lat'].mean(), df_venues[city]['Lng'].mean()] 
    # add markers to map
    for lat, lng, label in zip(df_venues[city]['Lat'], df_venues[city]['Lng'], df_venues[city]['Name']):
        label = folium.Popup(label, parse_html=True)
        folium.CircleMarker(
            [lat, lng],
            radius=5,
            popup=label,
            color='blue',
            fill=True,
            fill_color='#3186cc',
            fill_opacity=0.7,
            parse_html=False).add_to(maps[city])
        folium.PolyLine([venues_mean_coor, [lat, lng]], color="green", weight=1.5, opacity=0.5).add_to(maps[city])
    
    label = folium.Popup("Mean Co-ordinate", parse_html=True)
    folium.CircleMarker(
        venues_mean_coor,
        radius=10,
        popup=label,
        color='green',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(maps[city])

    print(city)
    print("Mean Distance from Mean coordinates")
    print(np.mean(np.apply_along_axis(lambda x: np.linalg.norm(x - venues_mean_coor),1,df_venues[city][['Lat','Lng']].values)))


# In[37]:


##The best city based on the Mean Coordinates is New York, followed by New Jersey, those two coties are going to be my Tourism goal


# In[26]:


maps[cities[0]]


# In[27]:


maps[cities[1]]


# In[28]:


maps[cities[2]]


# In[29]:


maps[cities[3]]


# In[30]:


## New York is the best place and the second one is New Jersey, my tour starts in NY and then in NJ


# In[ ]:




