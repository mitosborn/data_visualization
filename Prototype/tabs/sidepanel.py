import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html 
import dash_bootstrap_components as dbc 
import dash_table
import pandas
from dash.dependencies import Input, Output
import datetime
from app import app
import json
from tabs import tab1, tab2
from database import transforms

df = transforms.master_df
selection = {'Air Quality':'AQ','Greenhouse Gases':'GHG','Water Quality':'WQ','Economics':'ECON'}
years = [{'label': '2015', 'value': 2015}, {'label': '2016', 'value': 2016}, {'label': '2017', 'value': 2017}, {'label': '2018', 'value': 2018}, {'label': '2019', 'value': 2019},{'label': '2015-2019 Average', 'value': 'avg'}]
interval = [{'label':'Daily','value':'daily'},{'label':'Weekly','value':'weekly'},{'label':'Monthly','value':'monthly'},{'label':'Rolling 14 day average','value':'rolling'}]
AQ_source = 'https://www.tceq.texas.gov/agency/data/lookup-data/download-data.html'
GHG_source = "https://science.jpl.nasa.gov/EarthScience/index.cfm"

PLOTLY_LOGO = "https://cdn.freelogovectors.net/wp-content/uploads/2019/10/rice-university_logo.png"

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="50px")),
                    dbc.Col(dbc.NavbarBrand("Texas Environmental COVID Tracker", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://plot.ly",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
    ],
    color="dark",
    dark=True,
)


layout = html.Div([navbar,dbc.Row([dbc.Col(
        html.Div([
         #html.H2('Filters'),
            html.H3('Select group'), dcc.Dropdown(
                       id='sub-group',
                         options = [{'label':i,'value':selection[i]} for i in selection.keys()],
                         searchable = False, clearable = False, placeholder = 'Select a group',value ='AQ'),
        html.Div([html.H3('Select Parameter'), dcc.Dropdown(id = 'parameter',searchable = False,options = [{"label": "Air Quality - NO2", "value": "NO2"}],clearable = False,value = 'NO2')
                   ]), html.Div([html.H3('Layers',id = 'water_title'),dbc.RadioItems(id = 'wtr_layer',options=[
                {'label':'None','value':'None'},
                {'label': 'Major Aquifers', 'value': 'Major Aquifers'},
                {'label': 'River Basins', 'value': 'River Basins'},
                {'label': 'Watersheds', 'value': 'Watersheds'}

            ],
        value='None')]),html.Div([html.H3("Mode"),dbc.Checklist(id = 'mode',options = [
                                                                                       {'label':'Take difference between 2020 and other years','value':True}],value = [True],inline = True,switch=True)]),html.Div([html.H3("Comparison Year"),dcc.Dropdown(id = 'comp_year',options = years,searchable = False,clearable = False, value='avg')]),html.Div([html.H3('Interval'),dbc.RadioItems(id = 'date_interval',options = [
                                                                                       {'label':'Monthly','value':'monthly'},{'label':'Annual','value':'annual'}],value = 'monthly')]),html.Div([html.H3('Select Month', id = 'date_title'),dcc.Slider(id = 'date_range',min = 1, max = 12)

                                                                                                                                                                                                 ])], style={'marginBottom': 50, 'marginTop': 25, 'marginLeft':15, 'marginRight':15}), width=2)

    ,dbc.Col(html.Div([
            tab1.layout]), width=5), dbc.Col(html.Div([dcc.Graph(id = 'model'),
                                        dbc.Row([dbc.Col(html.Div([html.H5('Show Timeline'),dbc.RadioItems(id = 'time_lines',options = [
                                                                                       {'label':'Show','value':True},{'label':'Hide','value':False}],value = True)]
    )),dbc.Col(html.Div([html.H5("Compare Other Years"),dcc.Dropdown(id = 'years',options = years,searchable = False,multi = True,value=['avg'])])),dbc.Col(html.Div([html.H5("Averaging Interval"),dbc.RadioItems(id = 'avg_type',options = interval,value = 'daily')]))])
                                        ]),width = 5)]),dbc.Row(dbc.Col([html.Label([html.H6('Data Sources'),' Air Quality: ', html.A('TCEQ', href=AQ_source,target = "_blank"),', Greenhouse Gases: ',html.A('NASA',href = GHG_source,target="_blank")]),dcc.Markdown('''---
                                        Reminder to replace this with Markdown!''')
]))
    
    ])


