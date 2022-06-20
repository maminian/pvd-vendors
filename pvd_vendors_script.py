#!/usr/bin/env python
# coding: utf-8

# In[1]:


# RUN THIS CELL FIRST or the notebook won't work
#!pip install geopandas
import numpy as np
import pandas as pd
import geopandas as gpd
from IPython.display import display
import matplotlib.pyplot as plt

# These help the maps display nicely in the notebook
get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams['figure.figsize'] = [30, 20]

# This line tells iPython to not display warnings.
import warnings
warnings.filterwarnings('ignore')


# In[478]:


ri = gpd.read_file('tl_2020_44_tract')
ri.info()


# In[479]:


pvdCounty = ri[ri.COUNTYFP=='007']
pvdCounty.info()


# In[480]:


pvdCounty['NAME']= pvdCounty['NAME'].astype(str).astype(float)


# In[481]:


pvd = pvdCounty[pvdCounty.NAME < 40]


# In[ ]:





# In[482]:


get_ipython().system('pip install altair')
get_ipython().system('pip install gpdvega')
get_ipython().system('pip install altair vega_datasets')


# In[483]:



# Create the pandas DataFrame
current = pd.read_csv('vendors.csv')

current[['lat', 'long']] = current['Lat/Lon'].str.split(',', expand=True)
 
# print dataframe.
current


# In[484]:



# Create the pandas DataFrame
proposed = pd.read_csv('proposed.csv')

proposed = proposed[:44]


proposed[['lat', 'long']] = proposed['Lat/Lon'].str.split(',', expand=True)
 
# print dataframe.
proposed


# In[485]:



# Create the pandas DataFrame
current_ICERM = pd.read_csv('vendors_ICERM.csv')

current_ICERM[['lat', 'long']] = current_ICERM['Lat/Lon'].str.split(',', expand=True)
 
# print dataframe.
current_ICERM


# In[486]:


import altair as alt
import gpdvega 




bg = alt.Chart(pvd).mark_geoshape(
).encode( 
).properties( 
    width=800,
    height=500
)


points = alt.Chart(current).mark_circle(color='#ffffff').encode(
    latitude='lat:Q',
    longitude='long:Q',
    size=alt.value(50),


)

bg + points


# In[487]:


income = pd.read_csv('income.csv', index_col = [0])


# In[488]:


income


# In[489]:


income['GEOID']= income['GEOID'].astype(str).astype(str)


# In[490]:


income.count()


# In[491]:


income = income[income['GEOID'].str.len()>10]


# In[492]:


income


# In[493]:


income.rename(index = {"geometry": 'income_geometry'}, inplace = True)
pvd_income = pvd.merge(income, how = 'left', on = 'GEOID')


# In[494]:



gpd_pvd_income = gpd.GeoDataFrame(
    pvd_income[['variable','geometry_x','estimate', 'GEOID']], geometry='geometry_x')


# In[495]:


gpd_pvd_income


# In[551]:


import altair as alt
import gpdvega 

current_ICERM = current_ICERM[:-1]

gpd_pvd_income['estimate']= gpd_pvd_income['estimate'].astype(int)
bg = alt.Chart(gpd_pvd_income).mark_geoshape(
).encode( color = 'estimate'
).properties( 
    width=800,
    height=800
)


AMS = alt.Chart(current).mark_circle(color='#ffffff',opacity=1).encode(
    latitude='lat:Q',
    longitude='long:Q',
    size=alt.value(50),
    tooltip=["Name:N"]
)


ICERM = alt.Chart(current_ICERM).mark_circle(color='red').encode(
    latitude='lat:Q',
    longitude='long:Q',
    size=alt.value(50),
    tooltip=["Name:N"]
)

proposed_vendors = alt.Chart(proposed).mark_circle(color='black').transform_fold( ['Horsepower', 'Miles_per_Gallon'], as_=['Measure', 'Value'] ).encode(
    latitude='lat:Q',
    longitude='long:Q',
    size=alt.value(50),
    tooltip=["Name:N"]
)

# import random

# proposed_vendors_text = proposed_vendors.mark_text(color='black',align='left',baseline='middle').encode(
#     text='Name:N',

# )



line_B = proposed_vendors.transform_filter(
    alt.datum.Measure == 'Horsepower').mark_line(color='#F18727').encode(
    alt.Y('Proposed Vendors:Q', axis=alt.Axis(title='Horsepower'))
)
line_A = proposed_vendors.transform_filter(
    alt.datum.Measure == 'Miles_per_Gallon'
).encode(
    alt.Y('average(Value):Q', axis=alt.Axis(title='Miles_per_Gallon')),
)

bg + AMS + ICERM + proposed_vendors

(bg + AMS + ICERM + proposed_vendors).save('chart.html')


# In[553]:



(bg + AMS +  proposed_vendors + ICERM +alt.layer(line_B,line_A).resolve_scale(y='independent'))


# In[ ]:




current_ICERM
# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




