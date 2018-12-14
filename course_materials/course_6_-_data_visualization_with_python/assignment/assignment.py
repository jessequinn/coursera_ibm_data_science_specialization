import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium

survey = pd.read_csv('./Data_Science_Topics_Survey.csv')

survey.columns = ['Date', 'Data Visualization', 'Machine Learning',
                  'Data Analysis / Statistics', 'Big Data (Spark / Hadoop)', 'Data Journalism', 'Deep Learning']

# print(survey['Data Visualization'].value_counts())

list = []
for i in range(len(survey.columns) - 1):
    list.append(survey.ix[:, i + 1].value_counts().tolist())

transformed_survey = pd.DataFrame(
    list, columns=['Very interested', 'Somewhat interested', 'Not interested'])
transformed_survey.set_index(survey.columns[1:], inplace=True)
transformed_survey.sort_index(inplace=True)

transformed_survey = transformed_survey[['Not interested', 'Somewhat interested', 'Very interested']]

print(transformed_survey)

transformed_survey = transformed_survey[['Very interested', 'Somewhat interested', 'Not interested']]

transformed_survey.sort_values(
    by='Very interested', ascending=False, inplace=True)

transformed_survey['Very interested'] = transformed_survey['Very interested'].div(
    len(survey.index)).mul(100).round(2)
transformed_survey['Somewhat interested'] = transformed_survey['Somewhat interested'].div(
    len(survey.index)).mul(100).round(2)
transformed_survey['Not interested'] = transformed_survey['Not interested'].div(
    len(survey.index)).mul(100).round(2)

print(transformed_survey)

ax = transformed_survey.plot.bar(width=0.8, figsize=(
    20, 8), color=('#5cb85c', '#5bc0de', '#d9534f'), fontsize=14)

ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_yticklabels([])
plt.yticks([])

# easier to read labels
plt.xticks(rotation=0)

plt.title("Percentage of Respondents' Interest in Data Science Areas", fontsize=16)

for p in ax.patches:
    b = p.get_bbox()
    val = "{:.2f}".format(b.y1 + b.y0)
    ax.annotate(val, ((b.x0 + b.x1)/2 - 0.09, b.y1 + 0.5), fontsize=14)

plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig('assignment.png')

crime = pd.read_csv('./Police_Department_Incidents_-_Previous_Year__2016_.csv')

df = crime['PdDistrict'].value_counts().rename_axis(
    'Neighbourhood').reset_index(name='Count')

df.sort_values(by=['Count'], inplace=True, ascending=False)

print(df)

# San Francisco latitude and longitude values
latitude = 37.77
longitude = -122.45

# create a numpy array of length 6 and has linear spacing from the minium total immigration to the maximum total immigration
threshold_scale = np.linspace(df['Count'].min(),
                              df['Count'].max(),
                              6, dtype=int)
threshold_scale = threshold_scale.tolist()  # change the numpy array to a list
# make sure that the last value of the list is greater than the maximum immigration
threshold_scale[-1] = threshold_scale[-1] + 1

sanfran_map = folium.Map(
    location=[latitude, longitude], zoom_start=12)

sanfran_geo = r'./san-francisco.json'

sanfran_map.choropleth(
    geo_data=sanfran_geo,
    data=df,
    columns=['Neighbourhood', 'Count'],
    key_on='feature.properties.DISTRICT',
    threshold_scale=threshold_scale,
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Crime Rate in San Francisco',
    reset=True
)

import os
import time
from selenium import webdriver

delay=5
fn='sanfran.html'
tmpurl='file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=fn)
sanfran_map.save(fn)

browser = webdriver.Chrome()
browser.get(tmpurl)
#Give the map tiles some time to load
time.sleep(delay)

browser.save_screenshot('sanfran.png')
browser.quit()
