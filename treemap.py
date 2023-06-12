"""
Author: Mariska Spigt <13355406>
File:   treemap.py
Date:   06/2023

Graduation Project BSc Informatica
Description:

Sources:
* https://dash.plotly.com/dash-html-components/button
* https://plotly.com/python/sunburst-charts/
"""
import plotly.graph_objects as go
import pandas as pd
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
df = pd.read_csv('new_data.csv')
# set global count for button clicks
count = 0

# the different levels of the visualization
levels = ['property', 'course', 'trajectory']

def build_treemap_dataframe(df, levels):
    """
    Build a hierarchy of levels for Treemap chart.

    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root. Based on
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
            'Computer Systemen': Path('descriptions/trajectories/computer_systemen.txt').read_text(),
            'Academische Vaardigheden': Path('descriptions/trajectories/academische_vaardigheden.txt').read_text(),
            'Data en Informatie Systemen': Path('descriptions/trajectories/data_informatie_systemen.txt').read_text(),
            'Mathematics and Computer Science Theory': Path('descriptions/trajectories/math_cs_theory.txt').read_text(),
            'Modelgebaseerde Systemen': Path('descriptions/trajectories/model_gebaseerd.txt').read_text(),
            'Software Systemen': Path('descriptions/trajectories/software_systemen.txt').read_text(),
            'Academische Vaardigheden Informatica 1': Path('descriptions/courses/y1/avi1.txt').read_text(),
            'Architectuur en Computer Organisatie (CS)': Path('descriptions/courses/y1/arco.txt').read_text(),
            'Architectuur en Computer Organisatie (AV)': Path('descriptions/courses/y1/arco.txt').read_text(),
            'Inleiding Programmeren (SWS)': Path('descriptions/courses/y1/ip.txt').read_text(),
            'Discrete Wiskunde en Logica (MCST)': Path('descriptions/courses/y1/diswis.txt').read_text(),
            'Datastructuren voor IN (DIS)': Path('descriptions/courses/y1/datastructuren.txt').read_text(),
            'Datastructuren voor IN (SWS)': Path('descriptions/courses/y1/datastructuren.txt').read_text(),
            'Datastructuren voor IN (MCST)': Path('descriptions/courses/y1/datastructuren.txt').read_text(),
            'Programmeertalen (SWS)': Path('descriptions/courses/y1/progtalen.txt').read_text(),
            'Lineaire algebra KI/INF (MCST)': Path('descriptions/courses/y1/linalg.txt').read_text(),
            'Automaten en Formele Talen (MCST)': Path('descriptions/courses/y1/aft.txt').read_text(),
            'Besturingssystemen (CS)': Path('descriptions/courses/y1/besturingssys.txt').read_text(),
            'Internet of Things (MCST)': Path('descriptions/courses/y1/iot.txt').read_text(),
            'Internet of Things (AV)': Path('descriptions/courses/y1/iot.txt').read_text(),
            'Internet of Things (DIS)': Path('descriptions/courses/y1/iot.txt').read_text(),
            'Academische Vaardigheden Informatica 2': Path('descriptions/courses/y2/avi2.txt').read_text(),
            'Networks and Network Security (DIS)': Path('descriptions/courses/y2/nns.txt').read_text(),
            'Networks and Network Security (SWS)': Path('descriptions/courses/y2/nns.txt').read_text(),
            'Moderne Databases voor IN/IK (DIS)': Path('descriptions/courses/y2/moderne_db.txt').read_text(),
            'Distributed and Parallel Programming (CS)': Path('descriptions/courses/y2/dpp.txt').read_text(),
            'Distributed and Parallel Programming (AV)': Path('descriptions/courses/y2/dpp.txt').read_text(),
            'Numerical Recipes Project (MCST)': Path('descriptions/courses/y2/nrp.txt').read_text(),
            'Algoritmen en Complexiteit (MCST)': Path('descriptions/courses/y2/alco.txt').read_text(),
            'Introduction Computational Science (MCST)': Path('descriptions/courses/y2/ics.txt').read_text(),
            'Introduction Computational Science (MS)': Path('descriptions/courses/y2/ics.txt').read_text(),
            'Introduction Computational Science (AV)': Path('descriptions/courses/y2/ics.txt').read_text(),
            'Statistisch Redeneren (MCST)': Path('descriptions/courses/y2/sr.txt').read_text(),
            'Introduction to Computer Vision (MCST)': Path('descriptions/courses/y2/icv.txt').read_text(),
            'Introduction to Computer Vision (MS)': Path('descriptions/courses/y2/icv.txt').read_text(),
            'Reflectie op de Digitale Samenleving (AV)': Path('descriptions/courses/y2/reflectie.txt').read_text(),
            'Project Software Engineering (SWS)': Path('descriptions/courses/y2/pse.txt').read_text(),
        })

        dataframe = pd.concat([dataframe,entry], ignore_index=True)

    # the root of the chart
    bit = pd.DataFrame([dict(id='BSc Informatica Trajecten', parent='', hovertext='De BSc Informatica bestaat uit zes trajecten', ec='180')])
    dataframe = pd.concat([dataframe, bit], ignore_index=True)

    # set hovertext for properties
    dataframe = dataframe.fillna('Voor meer informatie, raadpleeg studiegids.uva.nl/')
    return dataframe

# dict to set the colors for the squares in the treemap, based on the
# colors in datanose
trajectory_colors = {
    'Computer Systemen': '#FF8986',
    'Academische Vaardigheden': '#96DD99',
    'Data en Informatie Systemen': '#FDFD96',
    'Mathematics and Computer Science Theory':'#AFD5F0',
    'Modelgebaseerde Systemen':'#FFBE65',
    'Software Systemen': '#C3B1E1',
}

# create dataframe to create the treemap
dataframe = build_treemap_dataframe(df, levels)

# set the color for the different trajectories using the color dict
dataframe.loc[dataframe['parent'] == 'BSc Informatica Trajecten', 'color'] = dataframe['id'].map(trajectory_colors)
fig = go.Figure()

# set properties of the figure
fig.add_trace(go.Treemap(
    labels=dataframe['id'],
    parents=dataframe['parent'],
    marker=dict(
        colors=dataframe['color'],
    ),
    customdata=dataframe['hovertext'],
    hovertemplate='<b>%{label} </b><br>%{customdata}<extra></extra>',
    maxdepth=2,
    ))

fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

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
                        figure=fig,
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
    app.run_server(debug=True, port=8051)
