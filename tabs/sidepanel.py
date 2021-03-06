import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app
from tabs import plots
from database import data_importer

df = data_importer.master_df
selection = {'Air Quality': 'AQ',
             'Greenhouse Gases': 'GHG', 'COVID Cases/Deaths': 'ECON'}
dashboard_spacing = {'margin-bottom': '1.2em'}

# Define averaging intervals available on the time series plot
interval = [{'label': 'Daily', 'value': 'daily'}, {'label': 'Weekly',
                                                   'value': 'weekly'}, {'label': 'Monthly', 'value': 'monthly'}]

# Define years available to display on the time series plot
years = [{'label': '2015', 'value': 2015}, {'label': '2016', 'value': 2016}, {'label': '2017', 'value': 2017},
         {'label': '2018', 'value': 2018}, {'label': '2019', 'value': 2019},
         {'label': '2015-2019 Average', 'value': 2000}]

# External links for Rice logo
RICE_LOGO = "https://cdn.freelogovectors.net/wp-content/uploads/2019/10/rice-university-logo.png"


# ------------------------------- ABOUT BUTTON -------------------------------

modal = html.Div(
    [
        dbc.Button(dcc.Markdown('''##### About'''),
                   id="open", className="mr-1"),
        dbc.Modal(
            [
                dbc.ModalHeader(dcc.Markdown('''### About''')),
                dbc.ModalBody(dcc.Markdown('''
                                            #### Background
                                            This dashboard was created as part of a research project investigating the envrionmental and socioeconomic impacts of the COVID-19 pandemic
                                            at Rice University.   
                                            
                                            The data shown was collected during a period of March 2020 - August 1, 2020.\n
                                        
                                            #### How to use
                                            1. Select a group from the top selector.
                                                * If Air Quality or Greenhouse Gases is selected, select an environmental indicator using the 'Select Parameter' dropdown.
                                                    * The *Mode Selector* allows you to view the selected year or the difference between 2020 and the selected year on the heatmap.
                                                    * Under *Interval*, you can select whether you'd like to see data on a monthly or yearly interval. If the interval is monthly, you can choose to 
                                                    view data for a single month from January - July.
                                                    * View the results of your selection on the heatmap. 
                                                    * Click on a county to see a timeseries breakdown of emissions for the selected county.
                                                
                                                * If  COVID Cases/Deaths is selected, select either Race/Ethnicity to see a county breakdown of COVID incidence vs Race/Ethnicity, or 
                                                select PM2.5 to see how PM2.5 concentration relates to COVID incidences.
                                            

                                            #### Data sources
                                            - Air Quality: [Texas Commission on Environmental Quality](https://www.tceq.texas.gov/agency/data/lookup-data/download-data.html)
                                            - Greenhouse Gases: [National Aeronautics and Space Administration (NASA)](https://science.jpl.nasa.gov/EarthScience/index.cfm)
                                            - COVID Cases/Deaths: [Texas Health and Human Services](https://dshs.texas.gov/coronavirus/AdditionalData.aspx)


                                            #### Contact Us
                                            * Sylvia Dee: 
                                                * Email: sylvia.dee@rice.edu
                                                * Website: [https://sylviadeeclimate.org/](https://sylviadeeclimate.org/)
                                            * If you have any questions or feedback you would like to provide regarding the website, please fill out 
                                            this [form https://forms.gle/giV2igcs44U7GWFo9](https://forms.gle/giV2igcs44U7GWFo9).

                                            #### Collaborators
                                            Annie Xu, Mitchell Osborn, Sarah Preston, Sylvia G. Dee, Ted Loch-Temzelides, Mark Torres, Caroline Masiello, Daniel Cohan, 
                                            Chima Adiole, Nathan Botton, Samantha Breaux, Melinda Ding, Benjamin Gelman, Lingkun Guo, Lucia Lu, Joanna Zhou
                                    
                                            ''')),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            id="modal",
            centered=True,
            scrollable=True,
            size="xl",
            style={"margin-top": "10rem"}
        ),
    ]
)


# ------------------------------- NAV BAR -------------------------------
navbar = dbc.Navbar(
    [
        html.A(
            # Create two columns: one containing the Rice logo, the other containing the dashboard title
            dbc.Row(
                [
                    dbc.Col(html.Img(src=app.get_asset_url('rice.png'),
                                     style={"padding-right": "0.5rem", "padding-left": "0.5rem", "width": "80%"}),
                            width={"size": 2}),
                    dbc.Col(dbc.NavbarBrand("Texas Covid-19 Environmental Impacts",
                                            className="d-inline-block text-wrap", style={
                                                'font-size': '2.75rem', 'font-family': 'Trajan', 'color': '#00205B',
                                                'font-weight': 'bold', 'text-align': 'left'}),
                            width={"size": 10}
                            ),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://earthscience.rice.edu/",  # External link to Rice ESCI website
        ),
        # dbc.NavbarToggler(id="navbar-toggler"),
        modal
    ],
    color="light",
    dark=False, style={"position": "sticky", "top": "0", "width": "100%", "background": "#fff", "z-index": "2000"}
)


# ------------------------------- TIME SERIES PLOT -------------------------------
# Define the time series plot that resides on the right side of the dashboard
timeline_toggle = dbc.Col([html.Div([html.H5('Show Timeline'), dbc.RadioItems(id='time_lines', options=[
                          {'label': 'Show', 'value': True}, {'label': 'Hide', 'value': False}], value=True)])])
timeline_year_selector = dbc.Col(html.Div([html.H5("Compare Other Years"), dbc.Checklist(
    id='years', options=years, value=[2000], inline=True)]))
select_averaging_interval = dbc.Col(html.Div([html.H5(
    "Averaging Interval"), dbc.RadioItems(id='avg_type', options=interval, value='daily')]))

# Put all the components together
time_series = dbc.Col(
    dbc.Container([dbc.Row(dbc.Col([dcc.Graph(id='model', style={'height': '100%'})]), style={'height': '92%'}),
                   dbc.Row([timeline_toggle, timeline_year_selector, select_averaging_interval], style={'height': '8%'}, id='ts_controls')],
                  style={"height": "70%"},
                  fluid=True), width=8, lg=5)

# ------------------------------- LEFT CONTROL PANEL -------------------------------
# Define controls on left side of dashboard
select_env_group = html.Div([html.H3('Select group'), dcc.Dropdown(
    id='sub-group',
    options=[{'label': i, 'value': selection[i]} for i in selection.keys()],
    searchable=False, clearable=False, value='AQ')], style=dashboard_spacing)
select_parameter = html.Div([html.H3('Select Parameter'),
                             dcc.Dropdown(id='parameter', searchable=False, options=[
                                          {"label": "Air Quality - NOx", "value": "NOx"}], clearable=False, value='NOx')
                             ], style=dashboard_spacing)
select_water_layers = html.Div([html.H3('Layers', id='water_title'), dbc.RadioItems(id='wtr_layer', options=[
    {'label': 'None', 'value': 'None'},
    {'label': 'Major Aquifers', 'value': 'Major Aquifers'},
    {'label': 'River Basins', 'value': 'River Basins'},
    {'label': 'Watersheds', 'value': 'Watersheds'}], value='None')])

select_difference_mode = html.Div([html.H3("Mode"), dbc.Checklist(id='mode', options=[
                                  {'label': 'Take difference between 2020 and other years', 'value': True}], value=[True], inline=True, switch=True)], style=dashboard_spacing)

# The comp year 2000 is used internally to represent the average of 2015-2019
select_comp_year = html.Div(dcc.Dropdown(
    id='comp_year', options=years, searchable=False, clearable=False, value=2000))

select_interval = html.Div([html.H3('Interval'), dbc.RadioItems(id='date_interval', options=[
    {'label': 'Monthly', 'value': 'monthly'}, {'label': 'Annual', 'value': 'annual'}], value='monthly')], style=dashboard_spacing)
select_month = html.Div([html.H3('Select Month', id='date_title'), dcc.Slider(
    id='date_range', min=1, max=12)], style=dashboard_spacing)

# Combine all controls into a control panel on the left side of the dashboard
controls = dbc.Col(html.Div([select_env_group, select_parameter, select_water_layers,
                             html.Div([select_difference_mode,
                                       html.Div(
                                           [html.Div(id='mode_title'), select_comp_year], style=dashboard_spacing),
                                       select_interval, select_month], id="econ_mode")],
                            style={'marginBottom': 50, 'marginTop': 25, 'marginLeft': 15, 'marginRight': 25}),
                   width=4, lg=2)


# ------------------------------- HEAT MAP -------------------------------
# Import heat map from tab1
heat_map = dbc.Col(plots.layout, width=8, lg=5)


# Combine all components into master layout
layout = html.Div([navbar, dbc.Container([dbc.Row([controls, heat_map, time_series], style={'height': '100%', 'margin': '1'})],
                                         style={"height": "100%", "width": "100%"}, fluid=True)],
                  style={"height": "100vh", "width": "100vw"}
                  )
