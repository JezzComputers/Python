import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import random

# Set up the application
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(
    children=[
        html.H1("Updating Gauge and Graph", id="title"),
        dcc.Graph(id="gauge-chart"),
        dcc.Graph(id="line-chart"),
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0),  # Update every second
        dcc.Store(id='data-store')
    ],
    id="dashboard"
)

# Add custom CSS styles
app.css.append_css({
    "external_url": "https://raw.githubusercontent.com/plotly/dash-sample-apps/master/apps/dash-dark-theme/custom.css"
})

# Callback function to update the gauge and graph
@app.callback([Output('gauge-chart', 'figure'), Output('line-chart', 'figure'), Output('data-store', 'data')],
              [Input('interval-component', 'n_intervals')],
              [dash.dependencies.State('data-store', 'data')])
def update_charts(n, data):
    value = random.randint(0, 100)  # Generate a random value between 0 and 100

    # Update the data list
    data = data or []
    data.append(value)
    data = data[-10:]  # Keep the last 10 data points

    # Store the updated data
    app.config['suppress_callback_exceptions'] = True

    # Create the gauge chart
    gauge_chart = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        gauge={
            "axis": {"range": [None, 100]},
            "steps": [
                {"range": [0, 50], "color": "lightgray"},
                {"range": [50, 100], "color": "gray"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": 90
            }
        }
    ))

    # Set the layout for the gauge chart
    gauge_chart.update_layout(title="Updating Gauge Chart")

    # Create the line graph
    x_data = list(range(len(data)))
    y_data = data

    line_graph = go.Figure(go.Scatter(x=x_data, y=y_data, mode='lines+markers'))

    # Set the layout for the line graph
    line_graph.update_layout(title="Updating Line Graph")

    return gauge_chart, line_graph, data

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)