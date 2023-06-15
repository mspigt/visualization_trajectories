"""
Author: Mariska Spigt <13355406>
File:   sunburst.py
Date:   06/2023

Graduation Project BSc Informatica
Description:

Sources:
* https://dash.plotly.com/dash-html-components/button
* https://plotly.com/python/sunburst-charts/
"""
import dash
from dash import dcc, ctx, html
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from dash.dependencies import Input, Output

# set application name
app = dash.Dash(__name__)
app.title = "Visualisatie leerlijnen"
# read data file
sheet = "https://docs.google.com/spreadsheets/d/10UCdVVGtJNmEkLoJGqDAduRmQMAa_Z0sYsEFsKCN5AI/export?format=csv&gid=137840079"
df = pd.read_csv(sheet)
sheet_2 = "https://docs.google.com/spreadsheets/d/1CexXZkL6qVgCB0chLWqKDMA714ocBT3W6G_hmKgu52w/export?format=csv&gid=0"
descriptions = pd.read_csv(sheet_2)
# set global count for button clicks
count = 0

# the different levels of the visualization
levels = ['property', 'course', 'trajectory']


def build_sunburst_dataframe(df, levels):
    """
    Build a hierarchy of levels for Sunburst chart.

    Levels are given starting from the bottom to the top of the hierarchy,
    i.e., the last level corresponds to the root. Based on
    https://plotly.com/python/sunburst-charts/
    """

    dataframe = pd.DataFrame(columns=['id', 'parent', 'hovertext', 'ec'])
    for i, level in enumerate(levels):
        entry = pd.DataFrame(columns=['id', 'parent', 'hovertext', 'ec'])
        dfg = df.groupby(levels[i:]).sum()
        dfg = dfg.reset_index()
        entry['id'] = dfg[level].copy()

        # set parent
        if i < len(levels) - 1:
            entry['parent'] = dfg[levels[i+1]].copy()
        else:
            entry['parent'] = 'BSc Informatica Trajecten'

        entry['hovertext'] = entry['id'].map({
            'Computer Systemen': descriptions['Descriptions'][0],
            'Academische Vaardigheden': descriptions['Descriptions'][1],
            'Data en Informatie Systemen': descriptions['Descriptions'][2],
            'Math and Computer Science Theory': descriptions['Descriptions'][3],
            'Modelgebaseerde Systemen': descriptions['Descriptions'][4],
            'Software Systemen': descriptions['Descriptions'][5],
            'Academische Vaardigheden Informatica 1': descriptions['Descriptions'][6],
            'Architectuur en Computer Organisatie (CS)': descriptions['Descriptions'][7],
            'Architectuur en Computer Organisatie (AV)': descriptions['Descriptions'][7],
            'Inleiding Programmeren (SWS)': descriptions['Descriptions'][8],
            'Discrete Wiskunde en Logica (MCST)': descriptions['Descriptions'][9],
            'Datastructuren voor IN (DIS)': descriptions['Descriptions'][10],
            'Datastructuren voor IN (SWS)': descriptions['Descriptions'][10],
            'Datastructuren voor IN (MCST)': descriptions['Descriptions'][10],
            'Programmeertalen (SWS)': descriptions['Descriptions'][12],
            'Lineaire algebra KI/INF (MCST)': descriptions['Descriptions'][13],
            'Automaten en Formele Talen (MCST)': descriptions['Descriptions'][14],
            'Besturingssystemen (CS)': descriptions['Descriptions'][15],
            'Internet of Things (MCST)': descriptions['Descriptions'][16],
            'Internet of Things (AV)': descriptions['Descriptions'][16],
            'Internet of Things (DIS)': descriptions['Descriptions'][16],
            'Academische Vaardigheden Informatica 2': descriptions['Descriptions'][17],
            'Networks and Network Security (DIS)': descriptions['Descriptions'][18],
            'Networks and Network Security (SWS)': descriptions['Descriptions'][18],
            'Moderne Databases voor IN/IK (DIS)': descriptions['Descriptions'][19],
            'Distributed and Parallel Programming (CS)': descriptions['Descriptions'][20],
            'Distributed and Parallel Programming (AV)': descriptions['Descriptions'][20],
            'Algoritmen en Complexiteit (MCST)': descriptions['Descriptions'][21],
            'Numerical Recipes Project (MCST)': descriptions['Descriptions'][22],
            'Introduction Computational Science (MCST)': descriptions['Descriptions'][23],
            'Introduction Computational Science (MS)': descriptions['Descriptions'][23],
            'Introduction Computational Science (AV)': descriptions['Descriptions'][23],
            'Statistisch Redeneren (MCST)': descriptions['Descriptions'][24],
            'Introduction to Computer Vision (MCST)': descriptions['Descriptions'][25],
            'Introduction to Computer Vision (MS)': descriptions['Descriptions'][25],
            'Reflectie op de Digitale Samenleving (AV)': descriptions['Descriptions'][26],
            'Project Software Engineering (SWS)': descriptions['Descriptions'][27],
        })

        dataframe = pd.concat([dataframe, entry], ignore_index=True)

    root_traject = pd.DataFrame([dict(id='BSc Informatica Trajecten', parent='', hovertext='De BSc Informatica bestaat uit zes trajecten', ec='180')])
    dataframe = pd.concat([dataframe, root_traject], ignore_index=True)

    # set hovertext for propertue
    dataframe = dataframe.fillna('Voor meer informatie, raadpleeg studiegids.uva.nl/')
    return dataframe

# dict to set the colors for the squares in the treemap, based on the
# colors in datanose
trajectory_colors = {
    'Computer Systemen': '#FF8986',
    'Academische Vaardigheden': '#96DD99',
    'Data en Informatie Systemen': '#FDFD96',
    'Math and Computer Science Theory':'#AFD5F0',
    'Modelgebaseerde Systemen':'#FFBE65',
    'Software Systemen': '#C3B1E1',
}

# create dataframe to create the treemap
dataframe = build_sunburst_dataframe(df, levels)

# set the color for the different trajectories using the color dict
dataframe.loc[dataframe['parent'] == 'BSc Informatica Trajecten', 'color'] = dataframe['id'].map(trajectory_colors)
fig = go.Figure()

# set properties of the figure
fig.add_trace(go.Sunburst(
    labels=dataframe['id'],
    parents=dataframe['parent'],
    marker=dict(
        colors=dataframe['color'],
    ),
    customdata=dataframe['hovertext'],
    hovertemplate='<b>%{label} </b><br>%{customdata}<extra></extra>',
    maxdepth=2,
))

fig.update_layout(margin=dict(t=0, b=0, r=0, l=0))

# set the lay out of the page
app.layout = html.Div(
    style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '90vh'},
    children=[
        html.Div(
            style={'width': '80%', 'display': 'grid', 'grid-template-columns': '1fr'},
            children=[
                # div component for the title and the button
                html.Div(
                    style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center', 'margin-bottom': '10px'},
                    children=[
                        html.H1('Visualisatie van de inhoud van BSc Informatica', style={'font-family': 'Roboto'}),
                        html.Button('Uitleg', id='button_id', n_clicks=0),
                    ]
                ),
                # div component for the text from the explanation button
                html.Div(
                    style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '10px', 'margin-top': '-10px'},
                    children=[
                        html.Div('', id='container-button-timestamp', style={'margin-top': '0px', 'font-family': 'Roboto'}),
                    ]
                ),
                # div component for the chart
                html.Div(
                    dcc.Graph(
                        figure=fig.update_layout(font={'size': 17}),
                        style={'height': 'calc(80vh - 70px)', 'font-family': 'Roboto', 'padding-top': '5px'},
                    )
                ),
            ],
        ),
    ],
)


@app.callback(
    Output('container-button-timestamp', 'children'),
    Input('button_id', 'n_clicks'),
)
def displayClick(btn1):
    """
    Clicking the button activates this function by adapting the message in
    the div.
    """
    # use the global count
    global count
    # unclicked the message is empty
    msg = html.P([])
    # if the button is clicked
    if "button_id" == ctx.triggered_id:
        # count==0 means the information needs to be shown
        if count == 0:
            msg = html.P(['Deze interactieve tool kan gebruikt worden om een \
                          beter inzicht te krijgen in de inhoud van de BSc \
                          Informatica. De bachelor is opgedeeld in zes \
                          verschillende trajecten: door op een traject te \
                          klikken krijg je de vakken te zien. Door op \
                          een vak te klikken krijg je enkele kernwoorden \
                          te zien die zouden kunnen worden gebruikt om \
                          het vak te omschrijven. Voor meer informatie over \
                          de inhoud van de bachelor of specifieke vakken, \
                          raadpleeg de studiegids.'])
            count = count + 1
        # count != 0 means the information should be empty
        else:
            msg = html.P([html.Br()])
            count = count - 1

    return html.Div(msg)


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
