import pandas as pd
import requests
from bs4 import BeautifulSoup
import geopandas as gpd
from datetime import datetime
from datetime import date
import dateutil.parser as dparser
import streamlit as st
import json
from bokeh.models import ColumnDataSource, GeoJSONDataSource, LinearColorMapper, ColorBar, DateSlider
from bokeh.plotting import figure
from bokeh.palettes import brewer
from bokeh.models import HoverTool
# scrape information from RKI
url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find('table')
rows = table.find_all('tr')
data = []
for row in rows[1:-1]:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols[:-1]]
    data.append([ele for ele in cols if ele])
data = [x for x in data if x != []]
data = [[x[0],x[1]] for x in data]
for row in data:
    row[1] = row[1].replace('.','')

s = soup.find('div',{'id':'content'})
retrieval_time = s.find_all('p',class_ = 'null')
retrieval_time = retrieval_time[0].text
retrieval_time = dparser.parse(retrieval_time,fuzzy=True)
retrieval_time = retrieval_time.strftime('%d.%m.%Y %H:%M')
state_data = pd.DataFrame(data,columns=['Bundesland','Fälle'])
bundeslaender = 'bundes.geojson'
state_data['Fälle'] = pd.to_numeric(state_data['Fälle'])
state_to_abb = {'Baden-Württemberg':'BW','Bayern':'BY','Berlin':'BE', 'Brandenburg':'BB','Bremen':'HB','Hamburg':'HH','Hessen':'HE','Mecklenburg-Vorpommern':'MV',
                'Niedersachsen':'NI','Nordrhein-Westfalen':'NW','Rheinland-Pfalz':'RP','Saarland':'SL','Sachsen':'SN','Sachsen-Anhalt':'ST', 'Schleswig-Holstein':'SH',
               'Thüringen':'TH','Repatriierte':'R','Gesamt':'G'}
temp = [state_to_abb[i] for i in state_data['Bundesland']]
state_data['id'] = temp
@st.cache
def get_shape_data():
    return gpd.read_file('bundes.geojson')
b = get_shape_data()
state_data = state_data.merge(b[['id','geometry']],on=['id'])
state_data['cases'] = state_data['Fälle']
state_data = gpd.GeoDataFrame(state_data, geometry='geometry')
state_data.crs = 'epsg:4326'
json_data = json.dumps(json.loads(state_data.to_json()))
geosource = GeoJSONDataSource(geojson = json_data)
text = f"# Data from {retrieval_time}"
st.markdown(text)
@st.cache
def make_map(geosource):
    palette = brewer['OrRd'][8]
    palette = palette[::-1]
    column = 'Fälle'
    vals = state_data[column]
    #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    color_mapper = LinearColorMapper(palette = palette, low = vals.min(), high = vals.max())
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=500, height=20,
                             location=(0,0), orientation='horizontal')

    tools = 'wheel_zoom,pan,reset,hover'
    p = figure(title = 'Corona virus in Germany', plot_height=800 , plot_width=850, toolbar_location='right', tools=tools,sizing_mode='scale_width')
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False
    #Add patch renderer to figure
    p.patches('xs','ys', source=geosource, fill_alpha=1, line_width=0.5, line_color='black',
                  fill_color={'field' :column , 'transform': color_mapper})
    #Specify figure layout.
    p.add_layout(color_bar, 'below')
    hover = p.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = [
        ("Bundesland", "@Bundesland"),
        ("Fälle", '@cases'),
    ]
    return p
p = make_map(geosource)
p
'''
Data Source: [Robert Koch Insititut](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html)
'''
'''
# Archive data
'''
@st.cache
def get_archive_data():
    archd = pd.read_csv('archive.csv')
    arch_data = pd.DataFrame()
    arch_data['id'] = archd.columns[1:-1]
    total_rows = archd.shape[0]
    for i in range(total_rows):
        arch_data[archd.iloc[i,0]] = archd.iloc[i,1:-1].values
    return arch_data
def make_df(b,selected):
    a = get_archive_data()
    a = a[['id',selected]]
    a[selected] = pd.to_numeric(a[selected])
    a = a.merge(b[['id','geometry']],on=['id'])
    a = gpd.GeoDataFrame(a, geometry='geometry')
    a.crf = 'epsg:4326'
    return a
def make_archive_map(b,selected):
    t = f'### Data from {selected}'
    st.markdown(t)
    geo_source = make_df(b,selected)
    palette = brewer['OrRd'][8]
    palette = palette[::-1]
    vals = geo_source[selected]
    json_data = json.dumps(json.loads(geo_source.to_json()))
    geosource = GeoJSONDataSource(geojson = json_data)
    #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    color_mapper = LinearColorMapper(palette = palette, low = vals.min(), high = vals.max())
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8, width=500, height=20,
                             location=(0,0), orientation='horizontal')

    tools = 'wheel_zoom,pan,reset,hover'
    p = figure(plot_height=800 , plot_width=850, toolbar_location='right', tools=tools,sizing_mode='scale_width')
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.axis.visible = False
    #Add patch renderer to figure
    p.patches('xs','ys', source=geosource, fill_alpha=1, line_width=0.5, line_color='black',
                  fill_color={'field' :selected , 'transform': color_mapper})
    #Specify figure layout.
    p.add_layout(color_bar, 'below')
    hover = p.select_one(HoverTool)
    hover.point_policy = "follow_mouse"
    hover.tooltips = [
        ("Bundesland", "@id"),
        ("Fälle", "@{"+selected+"}"),
    ]
    return p
selected = st.selectbox(
    'Select a date and time',
     get_archive_data().columns[1:],
     index=0)
archive_data = make_archive_map(b,selected)
archive_data
