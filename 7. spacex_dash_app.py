import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Leer los datos de lanzamiento de SpaceX en un dataframe de pandas
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Crear una aplicación dash
app = dash.Dash(__name__)

# Crear un diseño para la aplicación
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    # TASK 1: Agregar una lista desplegable para habilitar la selección del sitio de lanzamiento
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL SITES'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                 ],
                 value='ALL SITES',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),

    # TASK 2: Agregar un gráfico de pastel para mostrar el recuento total de lanzamientos exitosos para todos los sitios
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # TASK 3: Agregar un control deslizante para seleccionar el rango de carga útil
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=min_payload,
                    max=max_payload,
                    step=1000,
                    marks={int(min_payload): f'{min_payload}', int(max_payload): f'{max_payload}'},
                    value=[min_payload, max_payload]),

    # TASK 4: Agregar un gráfico de dispersión para mostrar la correlación entre carga útil y éxito de lanzamiento
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


# TASK 2: Agregar una función de callback para `site-dropdown` como entrada, `success-pie-chart` como salida
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL SITES':
        fig = px.pie(spacex_df, 
                     values='class', 
                     names='Launch Site', 
                     title='Total Success Launches by Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, 
                     names='class', 
                     title=f'Total Success Launches for site {entered_site}')
        return fig


# TASK 4: Agregar una función de callback para `site-dropdown` y `payload-slider` como entradas, `success-payload-scatter-chart` como salida
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]

    if entered_site == 'ALL SITES':
        fig = px.scatter(filtered_df, 
                         x='Payload Mass (kg)', 
                         y='class', 
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, 
                         x='Payload Mass (kg)', 
                         y='class', 
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for site {entered_site}')
        return fig


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server()
