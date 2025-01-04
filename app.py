import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Load the formatted data
data_file = "formatted_output.csv"

# Read the CSV file into a DataFrame
try:
    df = pd.read_csv(data_file)
except FileNotFoundError:
    raise Exception(f"{data_file} not found. Ensure the data file exists in the project directory.")

# Convert the 'date' column to datetime for sorting and filtering
df['date'] = pd.to_datetime(df['date'])

# Sort the data by date
df = df.sort_values(by='date')

# Create the Dash app
app = dash.Dash(__name__)

# Application Layout
app.layout = html.Div(style={'font-family': 'Arial, sans-serif'}, children=[
    # Header with CSS styling
    html.H1("Pink Morsel Sales Visualiser", style={'text-align': 'center', 'color': '#4CAF50'}),

    # Region filter radio buttons
    html.Div([
        html.Label("Select Region", style={'font-size': '16px', 'font-weight': 'bold'}),
        dcc.RadioItems(
            id='region-filter',
            options=[
                {'label': 'North', 'value': 'north'},
                {'label': 'East', 'value': 'east'},
                {'label': 'South', 'value': 'south'},
                {'label': 'West', 'value': 'west'},
                {'label': 'All', 'value': 'all'},
            ],
            value='all',  # Default value
            style={'display': 'inline-block', 'margin-right': '10px', 'font-size': '14px'}
        ),
    ], style={'text-align': 'center', 'margin-bottom': '20px'}),

    # Line Chart for Sales
    dcc.Graph(id='sales-line-chart'),

])

# Callback to update the line chart based on selected region
@app.callback(
    Output('sales-line-chart', 'figure'),
    [Input('region-filter', 'value')]
)
def update_chart(region):
    # Filter the data based on the selected region
    if region != 'all':
        filtered_df = df[df['region'] == region]
    else:
        filtered_df = df

    # Create the line chart
    fig = px.line(
        filtered_df,
        x='date',
        y='sales',
        title=f'Sales Over Time (Region: {region.capitalize()})',
        labels={'date': 'Date', 'sales': 'Sales ($)'},
    )

    # Add the vertical line for the price increase
    fig.update_layout(
        shapes=[
            dict(
                type='line',
                x0='2021-01-15',
                x1='2021-01-15',
                y0=0,
                y1=filtered_df['sales'].max(),
                line=dict(color='Red', dash='dash'),
            )
        ],
        annotations=[
            dict(
                x='2021-01-15',
                y=filtered_df['sales'].max(),
                xref="x",
                yref="y",
                text="Price Increase (15th Jan 2021)",
                showarrow=True,
                arrowhead=2,
                ax=-40,
                ay=-40,
            )
        ]
    )

    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
