# Import required libraries
import pandas as pd
from dash import dcc, html, Dash, Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Extract max and min payload
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Extract unique launch sites
launch_sites = spacex_df['Launch Site'].unique()

# Create a Dash application
app = Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    # Dashboard title
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Task 1: Dropdown for Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [{'label': site, 'value': site} for site in launch_sites],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    
    html.Br(),

    # Task 2: Pie chart placeholder
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # Task 3: Payload range slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,  # Slider starting point
        max=10000,  # Slider ending point
        step=1000,  # Slider interval
        marks={i: f'{i}' for i in range(0, 11000, 1000)},  # Slider tick marks
        value=[min_payload, max_payload]  # Default range selection
    ),

    html.Br(),

    # Task 4: Scatter chart placeholder
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Task 2: Add a callback function for `site-dropdown` as input and `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        filtered_df = spacex_df
        fig = px.pie(filtered_df, names='Launch Site', values='class',
                     title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', 
                     title=f"Total Success vs Failure for {selected_site}")
    return fig

# Task 4: Add a callback function for `site-dropdown` and `payload-slider` as inputs and `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Extract the payload range
    low, high = payload_range
    
    # Filter the dataframe by payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                            (spacex_df['Payload Mass (kg)'] <= high)]
    
    # If 'ALL' sites are selected, display scatter plot for all sites
    if selected_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for all Sites',
            labels={'class': 'Launch Outcome'}
        )
    else:
        # Filter the dataframe for the selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs Success for {selected_site}',
            labels={'class': 'Launch Outcome'}
        )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
