import dash
import numpy as np
import pandas as pd
import plotly as py
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot, plot
from plotly.subplots import make_subplots

df = pd.read_csv("GlobalLandTemperaturesByCountry.csv")
df = df.drop("AverageTemperatureUncertainty", axis=1)
df = df.rename(columns={'dt': 'Date'})
df = df.rename(columns={'AverageTemperature': 'AvTemp'})
df = df.dropna()
df_countries = df.groupby(['Country', 'Date']).sum().reset_index().sort_values('Date', ascending=False
                                                                               )

# Masking by data range
start_date = '2000-01-01'
end_date = '2002-01-01'
mask = (df_countries['Date'] > start_date) & (df_countries['Date'] <= end_date)
df_countries = df_countries.loc[mask]

fig = go.Figure(data=go.Choropleth(locations=df_countries['Country'], locationmode='country names',
                z=df_countries['AvTemp'], colorscale='Reds', marker_line_color='black', marker_line_width=0.5))
fig.update_layout(title_text='Climate Change', title_x=0.5, geo=dict(
    showframe=False, showcoastlines=False, projection_type='equirectangular'))


# Climate change by timeline
# Manipulating the original dataframe
df_countrydate = df_countries.groupby(['Date', 'Country']). sum().reset_index()
# Creating the visualization
fig2 = px.choropleth(df_countrydate, locations="Country", locationmode="country names",
                     color="AvTemp", hover_name="Country", animation_frame="Date")
fig2.update_layout(title_text='Average Temperature Change',
                   title_x=0.5, geo=dict(showframe=False, showcoastlines=False, ))


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

agg = ['Arab World', 'Caribbean small states',
       'Central Europe and the Baltics', 'Early-demographic dividend',
       'East Asia & Pacific',
       'East Asia & Pacific (excluding high income)',
       'East Asia & Pacific (IDA & IBRD countries)', 'Euro area',
       'Europe & Central Asia',
       'Europe & Central Asia (excluding high income)',
       'Europe & Central Asia (IDA & IBRD countries)', 'European Union',
       'Fragile and conflict affected situations',
       'Heavily indebted poor countries (HIPC)', 'High income',
       'IBRD only', 'IDA & IBRD total', 'IDA blend', 'IDA only',
       'IDA total', 'Late-demographic dividend',
       'Latin America & Caribbean',
       'Latin America & Caribbean (excluding high income)',
       'Latin America & the Caribbean (IDA & IBRD countries)',
       'Least developed countries: UN classification',
       'Low & middle income', 'Low income', 'Lower middle income',
       'Middle East & North Africa',
       'Middle East & North Africa (excluding high income)',
       'Middle East & North Africa (IDA & IBRD countries)',
       'Middle income', 'North America', 'Not classified', 'OECD members',
       'Other small states', 'Pacific island small states',
       'Post-demographic dividend', 'Pre-demographic dividend',
       'Small states', 'South Asia', 'South Asia (IDA & IBRD)',
       'Sub-Saharan Africa', 'Sub-Saharan Africa (excluding high income)',
       'Sub-Saharan Africa (IDA & IBRD countries)', 'Upper middle income',
       'World']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


dashboardurl = 'https://github.com/Chugh-Kanika/ISE-198-Dashboard-tutorial-using-Dash-Python-/blob/main/Wdi%20data%20for%20dashboard.xlsx?raw=true'
df_dash = pd.read_excel(dashboardurl, na_values='..')
df_dash.shape
df_newdash = df_dash.drop(['Country Code',  'Series Code'], axis=1)
df_nonagg = df_newdash[-df_newdash['Country Name'].isin(agg)]
df_flat = df_nonagg.melt(
    id_vars=["Country Name", "Series Name"], var_name="Year", value_name="value")
df_flat[['Year', 'NA']] = df_flat.Year.str.split(" ", expand=True)
df_flat = df_flat.dropna(axis=0, subset=['Country Name'])

available_country = df_flat['Country Name'].unique()

# Below code defines the layout of the dashboard. It defines how the dashboard will appear as a web page.
# For this dashboard, there are two dropdowns to select two countries for comparison and two time series chart for the
# pre-defined parameter which get updated based on the country selected.

# Dash Core Component - Dropdown and Graph is being used where Time-series graph will update based on country selected
app.layout = html.Div(children=[
    html.H1(children='Climate Change Dashboard', style={
        'textAlign': 'center'
    }),

    html.Div(children='''
      Select Countries for comparative analysis''', style={
        'textAlign': 'center'
    }),

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='country1',
                options=[{'label': i, 'value': i} for i in available_country],
                value='China', clearable=False
            )], style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='country2',
                options=[{'label': i, 'value': i} for i in available_country],
                value='United States', clearable=False
            )], style={'width': '49%', 'display': 'inline-block'})],
        style={'borderBottom': 'thin lightgrey solid',
               'backgroundColor': 'rgb(250, 250, 250)',
               'padding': '10px 5px'}),
    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='x-time-series')], style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='y-time-series')], style={'width': '49%', 'display': 'inline-block'})],
            style={'borderBottom': 'thin lightgrey solid',
                   'backgroundColor': 'rgb(250, 250, 250)',
                   'padding': '10px 5px'}
        ),
        html.Div([
            html.Div([
                dcc.Graph(id='x-time-series1')], style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='y-time-series1')], style={'width': '49%', 'display': 'inline-block'})],
            style={'borderBottom': 'thin lightgrey solid',
                   'backgroundColor': 'rgb(250, 250, 250)',
                   'padding': '10px 5px'}
        )



    ]),

    html.Br(),
    html.Br(),


    html.H1(children='World Map Plots ', style={
        'textAlign': 'center'
    }),

    html.Br(),
    html.Br(),

    html.Div([
        dcc.Graph(id='world-map-1', figure=fig)], style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='world-map-2', figure=fig2)], style={'width': '49%', 'display': 'inline-block'}),





])


# Below code defines the callback in the dashboard, callbacks add the interactivity in dashboard,
# Input value is from the dropdown and output is the time series chart
@ app.callback(
    dash.dependencies.Output(
        'x-time-series', 'figure'), dash.dependencies.Output('y-time-series', 'figure'),
    dash.dependencies.Input('country1', 'value'),
    dash.dependencies.Input('country2', 'value')
)
# Below code defines the function that will create a dataframe and a time series graph based on country selected in the dropdown.
def update_charts(country1, country2):
    filtered_df = df_flat.loc[df_flat['Country Name'] == country1]

    CO2_df = filtered_df.loc[filtered_df['Series Name']
                             == 'CO2 emissions (kt)']
    maxv = CO2_df.nlargest(1, 'value')['value'].values.tolist()
    minv = CO2_df.nsmallest(1, 'value')['value'].values.tolist()

    filtered_df2 = df_flat.loc[df_flat['Country Name'] == country2]
    CO2_df2 = filtered_df2.loc[filtered_df2['Series Name']
                               == 'CO2 emissions (kt)']

    maxv2 = CO2_df2.nlargest(1, 'value')['value'].values.tolist()
    minv2 = CO2_df2.nsmallest(1, 'value')['value'].values.tolist()

    maxva2 = max(maxv + maxv2)
    minva2 = min(minv + minv2)

    figure1 = px.line(CO2_df, x='Year', y='value', title='CO2 emissions (kt)',
                      range_y=[minva2, maxva2])
    figure2 = px.line(CO2_df2, x='Year', y='value', title='CO2 emissions (kt)',
                      range_y=[minva2, maxva2])
    return figure1, figure2


@ app.callback(
    dash.dependencies.Output(
        'x-time-series1', 'figure'), dash.dependencies.Output('y-time-series1', 'figure'),
    dash.dependencies.Input('country1', 'value'),
    dash.dependencies.Input('country2', 'value')
)
# Different code to find min,max values
def update_charts(country1, country2):
    filtered_df = df_flat.loc[df_flat['Country Name'] == country1]

    CO2_df = filtered_df.loc[filtered_df['Series Name']
                             == 'Methane emissions (kt of CO2 equivalent)']
    maxv = CO2_df.nlargest(1, 'value')['value'].values.tolist()
    minv = CO2_df.nsmallest(1, 'value')['value'].values.tolist()

    filtered_df2 = df_flat.loc[df_flat['Country Name'] == country2]
    CO2_df2 = filtered_df2.loc[filtered_df2['Series Name']
                               == 'Methane emissions (kt of CO2 equivalent)']

    maxv2 = CO2_df2.nlargest(1, 'value')['value'].values.tolist()
    minv2 = CO2_df2.nsmallest(1, 'value')['value'].values.tolist()

    maxva2 = max(maxv + maxv2)
    minva2 = min(minv + minv2)

    figure1 = px.line(CO2_df, x='Year', y='value', title='Methane emissions (kt of CO2 equivalent)',
                      range_y=[minva2, maxva2])
    figure2 = px.line(CO2_df2, x='Year', y='value', title='Methane emissions (kt of CO2 equivalent)',
                      range_y=[minva2, maxva2])
    return figure1, figure2


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
