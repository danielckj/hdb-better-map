# -*- coding: utf-8 -*-
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import sys
from os import path
from pathlib import Path
from plotly.subplots import make_subplots
import random
import glob

#Part 1: Data import, cleaning and preparation

external_stylesheets = ['assets\bWLwgP.css']
pd.set_option('mode.chained_assignment', None) #Turn off settingwithcopy warning
COL_PLOTLY_RESALE_LABEL_FORMAT = "Plotly Label for {} room in last {} months"
COL_RESALE_PRICE_FORMAT = "Average Resale Price for {}-Room in Last {} months"
FILE_MAPBOX_TOKEN = "mapbox_token.txt"
COL_ADDRESS = "address"
COL_AGE_CURR = "Age at 2024"
COL_FLAT_TYPE = "flat_type"
COL_ROOM_COUNT = "Room Count"
COL_PRICE = "resale_price"
COL_TRANSACTION_DATE = "Transaction Date"
COL_STOREY = "storey_range"
COL_AREA = "floor_area_sqm"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)
    
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_folder=resource_path('assets'), prevent_initial_callbacks=True)

def plotdata_to_dict(list_of_plotdata):
    '''
    builds dict for linking plotting data in list_of_plotdata to labels
    needed for creating drop-down list for choosing data to plot
    
    returns list of dicts with labels for each KPI, and first entry for drop-down table
    '''
    drop_down_plotdata = []
    for plotdata in list_of_plotdata:
        drop_down_plotdata.append({'value': plotdata, 'label': plotdata})
    first = list_of_plotdata[0]
    return (drop_down_plotdata, first)
# End Part 1

# Part 2: building web display
def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H6("HDB Block Data"),
                ],
            )
        ],
    )
def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab1",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="kpi-tab",
                        label="KPIs",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )

# Time to call Part 1
"""
Define data_for_plotting and plotdata_list manually, for simple data
data_for_plotting: single dataframe containing all data to be plotted
plotdata_list: list of data labels referencing data to be plotted
"""

target_path = Path('C:/Users/leadd/Documents/HDB Better Map')
data_for_plotting = pd.read_csv("HDB Ages and Prices as of 2024-04-22.csv")
raw_data = pd.read_csv("HDB as of 2024-04-22 all info.csv")
# plotdata_params: dict mapping titles of data to be plotted, 
#   to corresponding legend ranges and mouseover text label
plotdata_params = {
    "Age at 2024": 
        {"cmax": 40,
         "cmin": 0,
         "text": "Plotly Label by Age"
            },
    "Resale Prices up to Apr 2024":
        {"cmax": 7e5,
         "cmin": 0,
         "text": COL_PLOTLY_RESALE_LABEL_FORMAT
            },
    }
plotdata_list = list(plotdata_params.keys())
plotdata_dict,plotdata_first = plotdata_to_dict(plotdata_list)

# Mapbox token. Needed for accessing Mapbox maps
try:
    with open("mapbox_token.txt") as f:
        mapbox_token = f.read()
        mapbox_token_valid = True
except:
    # if you don't have a Mapbox token it's ok, you'll still be able to use OpenStreetMaps
    mapbox_token = None
    mapbox_token_valid = False
    print("MapBox API token not found, MapBox map layer will be disabled")

# Continued Part 2, previously with data from Part 1
first_data_cmax = plotdata_params[plotdata_first]["cmax"]
first_data_cmin = plotdata_params[plotdata_first]["cmin"]
first_data_text_col = plotdata_params[plotdata_first]["text"]
fig3 = go.Figure(
    go.Scattermapbox(
        go.Scattermapbox(     
                    lat=data_for_plotting["latitude"],
                    lon=data_for_plotting["longitude"],
                    mode= 'markers',
                    marker = go.scattermapbox.Marker(
                        size= 10,
                        color = data_for_plotting[plotdata_first],
                        colorscale = 'Rainbow',
                        cmax = first_data_cmax,
                        cmin = first_data_cmin,
                        reversescale = False,
                        showscale = True
                        ),
                    showlegend = True,
                    name = plotdata_first,
                    text = data_for_plotting[first_data_text_col],
                    )
        )
    )
# initiating map as mapbox
'''
fig3.update_layout(
    mapbox = go.layout.Mapbox(
                accesstoken = mapbox_token,
                style='streets',
                center={'lat': 1.35, 'lon': 103.8,},
                zoom = 11,
                ),
    clickmode="event")
'''
# initiating map as OSM
fig3.update_layout(
    mapbox_style='open-street-map',
    mapbox_center_lat=1.35,
    mapbox_center_lon=103.8,
    mapbox_zoom=11,
    clickmode="event")
fig3.update_layout(
    margin={"r":10,"t":10,"l":0,"b":2},
    height = 700,
    autosize=True,
    uirevision=True)
fig3.update_yaxes(automargin=True)


app.layout = html.Div(
children=[
    html.Div([
        html.H4('HDB Block Data'), 
        
        html.Div([
                dcc.Dropdown(
                    id='data-to-plot-dropdown',
                    options=plotdata_dict,
                    value=plotdata_first,
                    clearable=False
                )],style={'width': '20%', 'display': 'inline-block', 'margin-right':'5px'}),
        html.Div([
                dcc.Dropdown(
                    id='map-type-dropdown',
                    options=[
                        {'label': 'Mapbox', 'value': 'MB', 'disabled': not mapbox_token_valid},
                        {'label': 'OpenStreetMaps', 'value' : 'OSM'}
                             ],
                    value='OSM',
                    clearable=False
                )],style={'width': '15%', 'display': 'inline-block', 'margin-right':'5px'}),
        html.Div([
                dcc.Dropdown(
                    id='room-count-dropdown',
                    options=[
                        {'label': '3-Room', 'value': '3'},
                        {'label': '4-Room', 'value': '4'},
                        {'label': '5-Room', 'value': '5'},
                             ],
                    value='4',
                    clearable=False
                )],style={'width': '15%', 'display': 'inline-block', 'margin-right':'5px'}),
        html.Div([
                dcc.Dropdown(
                    id='transaction-window-dropdown',
                    options=[
                        {'label': 'Last 6 Months', 'value': '6'},
                        {'label': 'Last 12 Months', 'value': '12'},
                             ],
                    value='6',
                    clearable=False
                )],style={'width': '15%', 'display': 'inline-block', 'margin-right':'5px'}),
        ]),   
    html.Div(
        [dcc.Graph(
            id='user-graph2',
            figure=fig3
            ),
    ]),
    html.Div([
        dcc.Markdown("""
            **Past Transactions**

            Click on points on the map.
        """),
        html.Pre(id='click-data'),
    ], className='three columns')
    ]
    )

# End Part 2
     
# Part 3: interactive actions 
     
@app.callback(
    Output('user-graph2', 'figure'),
    [Input('data-to-plot-dropdown','value'),
    Input('map-type-dropdown','value'),
    Input('room-count-dropdown','value'),
    Input('transaction-window-dropdown','value'),
    ],
    # prevent_initial_call=False
    )
def update_figure(selected_plotdata, selected_map_type, selected_room_count, selected_transaction_window):
    '''
    updates the figure object displayed based on any interaction with the page. 
    Arguments follow order in app callback line directly preceding this
    
    returns:
        traces: list containing figure objects to be plotted (Scattermapbox for 5G scanning)
        layout: layout of page
    '''
    traces = []
    count_points_plotted = 0
    plotting_df = data_for_plotting
    selected_data_cmax = plotdata_params[selected_plotdata]["cmax"]
    selected_data_cmin = plotdata_params[selected_plotdata]["cmin"]
    if selected_plotdata == "Age at 2024":
        # ages of blocks: simple text label choice
        selected_data_text_col = plotdata_params[selected_plotdata]["text"]
        data_to_plot = plotting_df[selected_plotdata]
    elif selected_plotdata == "Resale Prices up to Apr 2024":
        # resale prices: need to select correct column for text label
        selected_data_text_col = plotdata_params[selected_plotdata]["text"].format(
            selected_room_count, selected_transaction_window)
        data_to_plot = plotting_df[COL_RESALE_PRICE_FORMAT.format(selected_room_count, selected_transaction_window)]
    
    traces.append(go.Scattermapbox(     
                lat=plotting_df["latitude"],
                lon=plotting_df["longitude"],
                mode= 'markers',
                marker = go.scattermapbox.Marker(
                    size= 10,
                    color = data_to_plot,
                    colorscale = 'Rainbow',
                    cmax = selected_data_cmax, # higher values: yellow > orange > red
                    cmin = selected_data_cmin, # lower values: green > blue > purple
                    reversescale = False,
                    showscale = True
                    ),
                showlegend = True,
                name = selected_plotdata,
                text = plotting_df[selected_data_text_col],
                ))
    count_points_plotted += len(plotting_df)
    
    title_text = selected_plotdata + ", {} points plotted".format(count_points_plotted)
                
    # map and layout controls: different layout structure for OSM and Mapbox
    if selected_map_type == 'OSM':
        mapstyle ='open-street-map'
        maplayers=[]
        
        layout = go.Layout(
            mapbox_style=mapstyle,
            mapbox_layers=maplayers,
            mapbox_center_lat=1.35,
            mapbox_center_lon = 103.8,
            mapbox_zoom = 11,
            title = {"text": title_text, 
                    "x": 1, "xref": "paper", "xanchor": "right", 
                    "y": 0.05, "yref": "container", },
            margin={"r":10,"t":0,"l":10,"b":10},
            height = 700,
            autosize=True,
            legend=dict(x=0, y=-0.01, orientation='h'),
            uirevision=True)
    else:
        layout = go.Layout(
            mapbox = go.layout.Mapbox(
                    accesstoken = mapbox_token,
                    style='streets',
                    center={'lat': 1.35, 'lon': 103.8,},
                    zoom = 11,
                    ),
            title = {"text": title_text, 
                        "x": 1, "xref": "paper", "xanchor": "right", 
                        "y": 0.05, "yref": "container", },
            margin={"r":10,"t":0,"l":10,"b":10},
            height = 700,
            autosize=True,
            legend=dict(x=0, y=-0.01, orientation='h'),
            uirevision=True)
            
    return {
        'data': traces,
        'layout':layout
    }

@app.callback(
    Output('click-data', 'children'),
    [Input('user-graph2', 'clickData'),
     Input('room-count-dropdown','value'),
     Input('transaction-window-dropdown','value'),
    ],
    # prevent_initial_call=False
    )
def update_clickData_title(clickData, selected_room_count, selected_transaction_window):
    '''
    Upon clicking on a block on the map,
    creates table of past transactions for selected block to be printed below map.
    Transactions are for selected room count and transaction window

    '''
    # identify target address that was clicked on
    target_addr_raw = clickData["points"][0]["text"]
    target_addr_len = target_addr_raw.find("<br>")
    target_addr = target_addr_raw[:target_addr_len]
    
    # creating title string
    title_str = "{}: {}-Room Transactions in Last {} Months".format(target_addr, selected_room_count, selected_transaction_window)
    
    # extract transactions from data that was clicked on
    target_df_raw = raw_data[raw_data[COL_ADDRESS] == target_addr]
    target_df = target_df_raw[(target_df_raw[COL_FLAT_TYPE] == "{} ROOM".format(selected_room_count)) &
                          (target_df_raw["Transaction Within {}-month Window".format(selected_transaction_window)])]
    target_df = target_df[[COL_TRANSACTION_DATE, COL_ADDRESS, COL_FLAT_TYPE, COL_STOREY, COL_AREA, COL_PRICE]]

    return_table = dash_table.DataTable(target_df.to_dict('records'))
    
    return [title_str, return_table]
    
if __name__ == '__main__':
    app.run_server(debug=False)    


