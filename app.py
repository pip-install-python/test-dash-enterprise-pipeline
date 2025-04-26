from dash import *
import dash_leaflet as dl

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=["https://use.fontawesome.com/releases/v6.2.1/css/all.css"])
server = app.server

# Define the layout of the app
app.layout = html.Div(
    [
        dcc.Store(id='osrs_map_store', storage_type='session', data=0),
        dl.Map(center=[-79, -137], zoom=7, children=[
            dl.TileLayer(id='osrs_tile_layer', url='https://raw.githubusercontent.com/Explv/osrs_map_tiles/master/0/{z}/{x}/{y}.png', minZoom=4, maxZoom=11, tms=True),
            dl.TileLayer(id='osrs_tile_layer_second',
                         url='https://raw.githubusercontent.com/Explv/osrs_map_tiles/master/0/{z}/{x}/{y}.png',
                         minZoom=4, maxZoom=11, tms=True, opacity=0.2),

            dl.EasyButton(
                            icon="fa-search",
                            title="Search OSRS Map",
                            id="search_osrs_map_display_btn",
                            n_clicks=1,
                        ),
            dl.EasyButton(
                            icon="fa-arrow-circle-up",
                            title="Up a Layer",
                            id="osrs_up_btn",
                            n_clicks=1,
            ),
            dl.EasyButton(
                            icon="fa fa-arrow-circle-down",
                            title="Down a Layer",
                            id="osrs_down_btn",
                            n_clicks=1,
            ),

        ], id='osrs_map', style={'width': '100%', 'height': '95vh'})
    ]
)

@callback(
    Output('osrs_tile_layer', 'url'),
    Output('osrs_map_store', 'data'),
    Input('osrs_up_btn', 'n_clicks'),
    Input('osrs_down_btn', 'n_clicks'),
    State('osrs_map_store', 'data')
)
def update_osrs_map(n_clicks_up, n_clicks_down, map_store):
    ctx = callback_context
    if not ctx.triggered:
        return 'https://raw.githubusercontent.com/Explv/osrs_map_tiles/master/0/{z}/{x}/{y}.png', no_update
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'osrs_up_btn' and map_store < 3:
            map_store += 1
        elif button_id == 'osrs_down_btn' and map_store > 0:
            map_store -= 1
        z = '{z}'
        x = '{x}'
        y = '{y}'
        return f'https://raw.githubusercontent.com/Explv/osrs_map_tiles/master/{map_store}/{z}/{x}/{y}.png', map_store


if __name__ == "__main__":
    app.run(debug=True, port=7654)