import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

data_file = "formatted_output.csv"

try:
    df = pd.read_csv(data_file)
except FileNotFoundError:
    raise Exception(f"{data_file} not found. Ensure the data file exists in the project directory.")

df['date'] = pd.to_datetime(df['date'])

df = df.sort_values(by='date')

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1("Pink Morsel Sales Visualiser", style={'text-align': 'center'}),

    dcc.Graph(
        id='sales-line-chart',
        figure=px.line(
            df,
            x='date',
            y='sales',
            title='Sales Over Time',
            labels={'date': 'Date', 'sales': 'Sales ($)'},
        ).update_layout(
            shapes=[
                dict(
                    type='line',
                    x0='2021-01-15',
                    x1='2021-01-15',
                    y0=0,
                    y1=df['sales'].max(),
                    line=dict(color='Red', dash='dash'),
                )
            ],
            annotations=[
                dict(
                    x='2021-01-15',
                    y=df['sales'].max(),
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
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
