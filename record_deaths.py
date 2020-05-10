import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import dateutil.parser as dparser
from csv import writer
from csv import DictWriter

url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find('table')
rows = table.find_all('tr')
data = []
for row in rows[1:]:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])
data = [x for x in data if x != []]
for row in data:
    row[0] = row[0].replace('\xad','')
    row[0] = row[0].replace('\n','')
    row[-1] = row[-1].replace('.', '')
data = [[x[0],x[-1]] for x in data]
s = soup.find('div',{'id':'content'})
retrieval_time = s.find('p').text
retrieval_time = dparser.parse(retrieval_time,fuzzy=True)
retrieval_time = retrieval_time.strftime('%d.%m.%Y %H:%M')
state_data = pd.DataFrame(data,columns=['Bundesland','Todesfälle'])
state_data['Todesfälle'] = pd.to_numeric(state_data['Todesfälle'])
state_to_abb = {'Baden-Württemberg':'BW','Bayern':'BY','Berlin':'BE', 'Brandenburg':'BB','Bremen':'HB','Hamburg':'HH','Hessen':'HE','Mecklenburg-Vorpommern':'MV',
                'Niedersachsen':'NI','Nordrhein-Westfalen':'NW','Rheinland-Pfalz':'RP','Saarland':'SL','Sachsen':'SN','Sachsen-Anhalt':'ST', 'Schleswig-Holstein':'SH',
               'Thüringen':'TH','Repatriierte':'R','Gesamt':'total'}
temp = [state_to_abb[i] for i in state_data['Bundesland']]
state_data['id'] = temp
total = state_data['Todesfälle'].sum()
case_dict = pd.Series(state_data.Todesfälle.values,index=state_data.id).to_dict()
case_dict['retrieval_time'] = retrieval_time
def append_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)
field_names = ['retrieval_time','BW','BY','BE','BB','HB','HH','HE','MV','NI','NW','RP','SL','SN','ST','SH','TH','total']
append_dict_as_row('death_archive.csv',case_dict,field_names)
print(case_dict)
