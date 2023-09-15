import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

px.set_mapbox_access_token(open("map.txt").read())

# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/',  # '/' is home page and it represents the url
                   name='Interactive Map',  # name of page, commonly used as name of link
                   title='FP Store Clustering - Interactive Map',  # title that appears on browser's tab
                   
)

# page 1 data
# Create a sample DataFrame with your data
# Sample DataFrame
# data = {
#     'store name': ['Store A', 'Store B', 'Store C'],
#     'latitude': [40.62718, 40.63718, 40.74718],
#     'longitude': [-73.29494, -73.30494, -73.31494],
#     'cluster': ['Cluster 1', 'Cluster 2', 'Cluster 3']
# }

# df = pd.DataFrame(data)
df = pd.read_csv('test_df_d6.csv')

# Your layout code remains the same
# Create an information div that will display the cluster information
info_div = html.Div(id='cluster-info', style={'padding': '20px', 'color': '#808080'})

# Modify the layout to include the info_div
layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [html.Label("Select a Cluster"),
                     dcc.Dropdown(
                         options=[
                             {'label': 'All', 'value': 'All'}
                         ] + [{'label': cluster, 'value': cluster} for cluster in sorted(df['cluster'].unique())],
                         id='cluster-choice',
                         value='All',
                         style={'width': '200px'},
                     ),
                     ],
                    xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='map-fig', style={'height': '100vh', 'border': '0'})
                    ],
                    style={'position': 'relative', 'height': '100vh', 'width': '100vh'}
                ),
                dbc.Col(
                    [
                        info_div  # Display the cluster information div
                    ],
                    xs=10, sm=10, md=4, lg=4, xl=4, xxl=4,
                    style={'border': '1px solid #ccc', 'height': '60%', 'width': '15%', 'overflow-y': 'auto'}
                )
            ]
        )
    ]
)

@callback(
    [Output('map-fig', 'figure'),
     Output('cluster-info', 'children')],  # Also update the cluster information div
    Input('cluster-choice', 'value')
)
def update_map_and_info(selected_cluster):
    if selected_cluster == 'All':
        dff = df
    else:
        dff = df[df['cluster'] == selected_cluster]

    # Calculate the store count per cluster
    cluster_store_counts = dff['cluster'].value_counts()

    # Calculate marker sizes based on store counts
    marker_sizes = [cluster_store_counts.get(cluster, 0) for cluster in dff['cluster']]

    # Create a mapbox figure using Plotly Graph Objects scattermapbox
    color_mapping = {'Cluster 1': '#3FE0D0', 'Cluster 2': '#95C8D8', 'Cluster 3': '#588BAE', 
                     'Cluster 4': '#4682B4', 'Cluster 5': '#7285A5', 'Cluster 6': '#06214F'}

    fig = go.Figure()

    for i, (cluster_name, color) in enumerate(color_mapping.items()):
        cluster_data = dff[dff['cluster'] == cluster_name]
        fig.add_trace(go.Scattermapbox(
            lat=cluster_data['latitude'],
            lon=cluster_data['longitude'],
            mode='markers',
            marker=dict(
                size=17,
                color=color
            ),
            customdata=cluster_data[['store_num', 'store_name', 'grade', 'store_format', 'total_demand_amt_ly']],
            hovertemplate=(
                "<b>Store Num</b>: %{customdata[0]}<br><br>" +
                "Store Name: %{customdata[1]}<br>" +
                "Grade: %{customdata[2]}<br>" +
                "Store Format: %{customdata[3]}<br>" +
                "Total Demand Amt LY: %{customdata[4]:$,.0f}<br>"
                "<extra></extra>"
            ),
            name=cluster_name,  # Set the legend title
            legendgroup=f"cluster-{i}"  # Set the legend group
        ))

    fig.update_layout(
        mapbox_style='carto-positron',
        mapbox_center={'lat': 37.0902, 'lon': -95.7129},
        mapbox_zoom=4,
        hoverlabel=dict(
            bgcolor="white",
            font_size=14,
        ),
        showlegend=True  # Show the legend
    )

    # Example: Cluster information for different clusters
    cluster_info_dict = {
        'Cluster 1': html.Div([
        html.Strong("Cluster Size:"),
        html.Br(),
        "46",
        html.Br(),
        html.Strong("Grade:"),
        html.Br(),
        "F + UNKNOWN",
        html.Br(),
        html.Strong("Climate:"),
        html.Br(),
        "Mild, Cold",
        html.Br(),
        html.Strong("Region:"),
        html.Br(),
        "WEST COAST-LOS ANGELES and WEST COAST-SOUTHERN CALIFORNIA",
        html.Br(),
        html.Br(),
        html.Strong("This cluster over-indexed the most in:"),
        html.Br(),
        "Divisions: Apparel, Intimate Apparel, Womens Accessories",
        html.Br(),
        "Classes: Suits, Surf One Piece, Blazers Jackets, Slips, Belts",
        html.Br(),
        html.Br(),
        html.Strong("This Cluster under-indexed the most in:"),
        html.Br(),
        "Classes: Swim Tops, Sunglasses, Knit Tops, One Piece, Performance Bottoms",
    ], style={'font-family': 'Arial, sans-serif', 'font-size': '16px'}),
    'Cluster 2': html.Div([
        html.Strong("Cluster Size:"),
        html.Br(),
        "44",
        html.Br(),
        html.Strong("Grade:"),
        html.Br(),
        "F + UNKNOWN",
        html.Br(),
        html.Strong("Climate:"),
        html.Br(),
        "Cold, Hot",
        html.Br(),
        html.Strong("Region:"),
        html.Br(),
        "CENTRAL-GREATER CHICAGO and EAST COAST-MID-ATLANTIC DISTRICT",
        html.Br(),
        html.Br(),
        html.Strong("This cluster over-indexed the most in:"),
        html.Br(),
        "Divisions: Beauty, Womens Accessories, Apparel Division",
        html.Br(),
        "Classes: Heavy Knits, Movement Heavyweights, Casual Layering, Movement Bags, Sweaters",
        html.Br(),
        html.Br(),
        html.Strong("This Cluster under-indexed the most in:"),
        html.Br(),
        "Classes: Boots, Hair Accessories, Performance Camis, Sunglasses, Performance Leggings",
    ], style={'font-family': 'Arial, sans-serif', 'font-size': '16px'}),
    'Cluster 3': html.Div([
        html.Strong("Cluster Size:"),
        html.Br(),
        "28",
        html.Br(),
        html.Strong("Grade:"),
        html.Br(),
        "F + UNKNOWN",
        html.Br(),
        html.Strong("Climate:"),
        html.Br(),
        "Cold, Mild",
        html.Br(),
        html.Strong("Region:"),
        html.Br(),
        "EAST COAST-MID-ATLANTIC DISTRICT and CENTRAL-TEXAS",
        html.Br(),
        html.Br(),
        html.Strong("This cluster over-indexed the most in:"),
        html.Br(),
        "Divisions: Vintage, Movement, Womens Accesories",
        html.Br(),
        "Classes: Performance Shorts, Performance Layering, Casual Shorts, Casual Sets, Performance Camis",
        html.Br(),
        html.Br(),
        html.Strong("This Cluster under-indexed the most in:"),
        html.Br(),
        "Classes: Performance Bottoms, Casual Bottoms, Lounge, Woven Blouses, Movement Hats",
    ], style={'font-family': 'Arial, sans-serif', 'font-size': '16px'}),
    'Cluster 4': html.Div([
        html.Strong("Cluster Size:"),
        html.Br(),
        "25",
        html.Br(),
        html.Strong("Grade:"),
        html.Br(),
        "F + UNKNOWN",
        html.Br(),
        html.Strong("Climate:"),
        html.Br(),
        "Hot, Mild",
        html.Br(),
        html.Strong("Region:"),
        html.Br(),
        "EAST COAST-SOUTHEAST DISTRICT and CENTRAL-TEXAS",
        html.Br(),
        html.Br(),
        html.Strong("This cluster over-indexed the most in:"),
        html.Br(),
        "Divisions: Vintage, Movement",
        html.Br(),
        "Classes: Performance Shorts, In Case Jewelry, Casual Shorts, Performance Layering, Performance Camis",
        html.Br(),
        html.Br(),
        html.Strong("This Cluster under-indexed the most in:"),
        html.Br(),
        "Classes: Undies, Swim Tops, Movement Socks, Surf One Piece, Woven Blouses",
    ], style={'font-family': 'Arial, sans-serif', 'font-size': '16px'}),
    'Cluster 5': html.Div([
        html.Strong("Cluster Size:"),
        html.Br(),
        "25",
        html.Br(),
        html.Strong("Grade:"),
        html.Br(),
        "F + UNKNOWN",
        html.Br(),
        html.Strong("Climate:"),
        html.Br(),
        "Mild, Cold",
        html.Br(),
        html.Strong("Region:"),
        html.Br(),
        "EAST COAST-NEW ENGLAND and WEST COAST-NORTHWEST DISTRICT",
        html.Br(),
        html.Br(),
        html.Strong("This cluster over-indexed the most in:"),
        html.Br(),
        "Divisions: Beauty, Movement, Intimate Apparel",
        html.Br(),
        "Classes: Movement Hats, Heavy Knits, Casual One Pieces, Casual Outerwear, Movement Heavyweights",
        html.Br(),
        html.Br(),
        html.Strong("This Cluster under-indexed the most in:"),
        html.Br(),
        "Classes: Movement Bags, Movement Accessories, Slips, Movement Socks, Bras Movement",
    ], style={'font-family': 'Arial, sans-serif', 'font-size': '16px'}),
    'Cluster 6': html.Div([
        html.Strong("Cluster Size:"),
        html.Br(),
        "14",
        html.Br(),
        html.Strong("Grade:"),
        html.Br(),
        "A1 + UNKNOWN",
        html.Br(),
        html.Strong("Climate:"),
        html.Br(),
        "Hot, Cold",
        html.Br(),
        html.Strong("Region:"),
        html.Br(),
        "EAST COAST-FLORIDA DISTRICT and EAST COAST-MVMT - EAST COAST",
        html.Br(),
        html.Br(),
        html.Strong("This cluster over-indexed the most in:"),
        html.Br(),
        "Divisions: Movement, Intimate Apparel, Apparel Division, Beauty",
        html.Br(),
        "Classes: Performance One Pieces, Surf One Piece, Performance Bottoms, Bras Movement, Casual Shorts",
        html.Br(),
        html.Br(),
        html.Strong("This Cluster under-indexed the most in:"),
        html.Br(),
        "Classes: Knit Tops, One Piece, Jeans, In Case Jewelry, Movement Bags",
    ], style={'font-family': 'Arial, sans-serif', 'font-size': '16px'}),
    # Similarly format other clusters...
}

   # Create cluster information HTML
    if selected_cluster == 'All':
        cluster_info_html = None  # No cluster information for 'All'
    else:
        cluster_info_html = cluster_info_dict[selected_cluster]

    return fig, cluster_info_html