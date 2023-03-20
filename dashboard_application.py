# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import wget


spacex_dataset = wget.download("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
spacex_dash_app = wget.download("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application and folder.
app = dash.Dash(__name__)
server = app.server
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                html.P("Created by Molo Munyansanga", style={'textAlign': 'center'}),

                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                ],
                                                value='ALL',
                                                placeholder="Select a Launch Site here",
                                                searchable=True
                                                ),

                                html.Br(),
                                # If a specific launch site was selected,
                                # show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                # Add payload mass slider text
                                html.P(id="slider-text"),
                                
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500',
                                                       10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])


#a callback function for `site-dropdown` as input
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Total Successful Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        site_chosen = entered_site
        mask = filtered_df['Launch Site'] == site_chosen
        fig = px.pie(filtered_df[mask], names='class',
                     title=f'Total Successful Launches For Site {site_chosen}')
        return fig



# a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart`.
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              [Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, mass):

    # filter masses from payload slider
    mass_1 = spacex_df['Payload Mass (kg)'] >= float(mass[0])
    mass_2 = spacex_df['Payload Mass (kg)'] <= float(mass[1])
    
    filtered_df = spacex_df[mass_1][mass_2]
    
    if entered_site == 'ALL':

        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color="Booster Version Category",
                         title=f'Correlation between Payload Mass and Launch Success for All Sites for Payload Mass(kg) Between {mass[0]} and {mass[1]}')
        return fig
    else:
        
        # return the outcomes scatter chart for a selected site
        site_chosen = entered_site
        mask = filtered_df['Launch Site'] == site_chosen
        fig = px.scatter(filtered_df[mask], x='Payload Mass (kg)', y='class', color="Booster Version Category",
                         title=f'Correlation between Payload Mass and Launch Success for Site {site_chosen}')
        return fig
@app.callback(Output('slider-text', 'children'),
              [Input(component_id='payload-slider', component_property='value')])

def get_success_rate(mass):
"""
    A function that gets the success rate from the inputted mass.
"""
    # filter masses from payload slider
    mass_1 = spacex_df['Payload Mass (kg)'] >= float(mass[0])
    mass_2 = spacex_df['Payload Mass (kg)'] <= float(mass[1])
    
    filtered_df = spacex_df[mass_1][mass_2]
    
    rate = (filtered_df['class'].value_counts().loc[1])/filtered_df['class'].value_counts().sum() * 100
    rate = 'Payload range (Kg): ' + str(round(rate, 2)) + '% Success Rate'
    
    return rate
    
    
if __name__ == '__main__':
    app.run_server()
Dash is running on http://127.0.0.1:8050/

Dash is running on http://127.0.0.1:8050/

Dash is running on http://127.0.0.1:8050/



