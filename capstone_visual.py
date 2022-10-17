#!/usr/bin/env python
# coding: utf-8

# <center>
#     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/logo.png" width="300" alt="cognitiveclass.ai logo" />
# </center>
# 

# ## Application
# 

# In[1]:


pip install dash


# In[4]:


pip install wget


# In[5]:


import wget
site_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
file_name = wget.download(site_url)
print(file_name)


# In[42]:


# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


spacex_df


# In[43]:


# Create a dash application
app = dash.Dash(__name__)

## Create an app layout

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                   id='site-dropdown',
                                   options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                    placeholder="Select a Launch Site here", value='ALL',
                                    searchable=True),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                min=0,
                                max=10000,
                                step=1000,
                                value=[min_payload,max_payload],
                                marks={
                                0: '0 kg',
                                2500: '2500',
                                5000: '5000',
                                7500: '7500',
                                10000: '10000'
                                }),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# In[44]:



# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
Output(component_id='success-pie-chart', component_property='figure'),
Input(component_id='site-dropdown', component_property='value')
)
def get_pie(value):
    filtered_df = spacex_df
    if value == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches By Site')
        return fig

    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == value].groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        title = f"Total Success Launches for site {value}"
        fig = px.pie(filtered_df,values='class count', names='class', title=title)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
Output(component_id='success-payload-scatter-chart', component_property='figure'),
[Input(component_id='site-dropdown', component_property='value'),
Input(component_id='payload-slider', component_property='value')]
)

def get_scatter(value1,value2):
    filtered_df2_1=spacex_df[(spacex_df['Payload Mass (kg)'] > value2[0]) & (spacex_df['Payload Mass (kg)'] < value2[1])]

    if value1=='ALL':
        fig= px.scatter(filtered_df2_1,x="Payload Mass (kg)",y="class",color="Booster Version Category",        title="Correlation between Payload and Success for All sites")
        return fig
    else :
        filtered_df2_2=filtered_df2_1[filtered_df2_1['Launch Site']==value1]
        fig= px.scatter(filtered_df2_2,x="Payload Mass (kg)",y="class",color="Booster Version Category",        title=f"Correlation between Payload and Success for site {value1}")
        return fig


# In[45]:


# Run the app
if __name__ == '__main__':
    app.run_server()


# Finding Insights Visually
# Now with the dashboard completed, you should be able to use it to analyze SpaceX launch data, and answer the following questions:
# 
# Which site has the largest successful launches?
# - KSC LC-39A
# 
# Which site has the highest launch success rate?
# - KSC LC-39A
# 
# Which payload range(s) has the highest launch success rate?
# - 2-4k
# 
# Which payload range(s) has the lowest launch success rate?
# - 6-8k
# 
# Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest
# launch success rate?
# - B5

# In[ ]:




