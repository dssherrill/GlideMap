"""
Glide Range Map - Python Dash Bootstrap Version
Copyright (c) David S. Sherrill

This file is part of Glide Range Map.

Glide Range Map is free software: you can redistribute it and/or modify it under the terms 
of the GNU General Public License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version.

Glide Range Map is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Glide Range Map. 
If not, see https://www.gnu.org/licenses/.
"""

import base64
import io
import re
import os
from dash import Dash, html, dcc, Input, Output, State, callback, no_update, ctx
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import pandas as pd

# Constants matching the JavaScript version
GLIDE_RATIO_MIN = 1
GLIDE_RATIO_MAX = 100
GLIDE_RATIO_DEFAULT = 20
ALTITUDE_MIN = 0
ALTITUDE_MAX = 50000
ALTITUDE_DEFAULT = 3500
ARRIVAL_HEIGHT_MIN = 0
ARRIVAL_HEIGHT_MAX = 10000
ARRIVAL_HEIGHT_DEFAULT = 1000

# Safety factors for arrival height validation
# If arrival height >= altitude, adjust it to be safe:
# - Use 90% of altitude as a safety factor
# - Or ensure at least 100 ft buffer, whichever is smaller
ARRIVAL_HEIGHT_SAFETY_FACTOR = 0.9
ARRIVAL_HEIGHT_MIN_BUFFER = 100

# Landing site styles
GRASS_SURFACE = 2
OUTLANDING = 3
GLIDING_AIRFIELD = 4
AIRPORT = 5

# Default CUP file path
DEFAULT_CUP_FILE_PATH = 'Sterling, Massachusetts 2021 SeeYou.cup'


def feet_to_meters(feet):
    """Convert feet to meters"""
    return feet * 0.3048


def meters_to_feet(meters):
    """Convert meters to feet"""
    return meters / 0.3048


def calculate_radius(glide_ratio, altitude, arrival_height, elevation):
    """Calculate glide range radius in meters"""
    r = feet_to_meters(glide_ratio * (altitude - arrival_height - elevation))
    if pd.isna(r):
        r = 1.0
    else:
        r = max(r, 1.0)
    return r


def parse_cup_coordinate(coord_str, is_longitude=False):
    """
    Parse CUP coordinate format
    Latitude Format: ddmm.mmm{N|S} (e.g., "5107.830N" = 51° 07.830' North)
    Longitude Format: dddmm.mmm{E|W} (e.g., "01410.467E" = 014° 10.467' East)
    """
    if is_longitude:
        degrees = float(coord_str[:3])
        minutes = float(coord_str[3:9])
        sign = 1 if coord_str[-1] == 'E' else -1
    else:
        degrees = float(coord_str[:2])
        minutes = float(coord_str[2:8])
        sign = 1 if coord_str[-1] == 'N' else -1
    
    return sign * (degrees + minutes / 60.0)


def parse_cup_elevation(elev_str):
    """Parse CUP elevation format (can be in feet or meters)"""
    if elev_str.endswith("ft"):
        return float(elev_str[:-2])
    elif elev_str.endswith("m"):
        return meters_to_feet(float(elev_str[:-1]))
    return 0


def parse_cup_file(contents):
    """
    Parse a CUP file and return a list of landing spots
    
    CUP format (CSV):
    name,code,country,lat,lon,elev,style,rwdir,rwlen,freq,desc
    0    1    2       3   4   5    6     7     8     9    10
    """
    try:
        # Decode base64 content if it's a data URL (starts with data:)
        if contents.startswith('data:'):
            content_type, content_string = contents.split(',', 1)
            decoded = base64.b64decode(content_string).decode('utf-8')
        else:
            # Plain text content (for local file loading)
            decoded = contents
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Invalid CUP file format. Expected 'data:' URL or plain text content: {e}")
    
    # Remove tasks section if present
    task_location = decoded.find("-----Related Tasks-----")
    if task_location != -1:
        decoded = decoded[:task_location]
    
    # Parse CSV
    lines = decoded.strip().split('\n')
    if len(lines) < 2:
        return []
    
    landing_spots = []
    
    # Skip header line
    for line in lines[1:]:
        if not line.strip():
            continue
        
        try:
            parts = line.split(',')
            if len(parts) < 7:
                continue
            
            name = parts[0].strip('"')
            lat_str = parts[3].strip('"')
            lon_str = parts[4].strip('"')
            elev_str = parts[5].strip('"')
            style = int(parts[6].strip('"'))
            
            # Only process landing spots
            if style not in [GRASS_SURFACE, OUTLANDING, GLIDING_AIRFIELD, AIRPORT]:
                continue
            
            lat = parse_cup_coordinate(lat_str, is_longitude=False)
            lon = parse_cup_coordinate(lon_str, is_longitude=True)
            elevation = parse_cup_elevation(elev_str)
            
            landing_spots.append({
                'name': name,
                'lat': lat,
                'lon': lon,
                'elevation': elevation,
                'style': style
            })
        except Exception as e:
            print(f"Error parsing line: {line[:50]}... Error: {e}")
            continue
    
    return landing_spots


def load_default_cup_file():
    """Load the default CUP file on startup"""
    try:
        if os.path.exists(DEFAULT_CUP_FILE_PATH):
            with open(DEFAULT_CUP_FILE_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
                return parse_cup_file(content)
    except Exception as e:
        print(f"Error loading default CUP file: {e}")
    return []


def calculate_center_and_zoom_from_bounds(bounds):
    """
    Calculate center and zoom level from bounds
    Returns (center, zoom) tuple
    """
    if not bounds:
        return default_center, 9
    
    # Extract coordinates
    min_lat, min_lon = bounds[0]
    max_lat, max_lon = bounds[1]
    
    # Calculate center
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2
    center = [center_lat, center_lon]
    
    # Calculate zoom level based on coordinate span
    lat_diff = max_lat - min_lat
    lon_diff = max_lon - min_lon
    max_diff = max(lat_diff, lon_diff)
    
    # Zoom level calculation (rough approximation)
    # Each zoom level roughly doubles the scale
    if max_diff > 10:
        zoom = 6
    elif max_diff > 5:
        zoom = 7
    elif max_diff > 2:
        zoom = 8
    elif max_diff > 1:
        zoom = 9
    elif max_diff > 0.5:
        zoom = 10
    elif max_diff > 0.2:
        zoom = 11
    elif max_diff > 0.1:
        zoom = 12
    else:
        zoom = 13
    
    return center, zoom


def calculate_map_bounds(landing_spots):
    """
    Calculate map bounds from landing spots
    Returns [[min_lat, min_lon], [max_lat, max_lon]] for use with Dash Leaflet bounds property
    """
    if not landing_spots:
        # Return None to indicate no bounds (will use default center/zoom)
        return None
    
    # Find min/max coordinates
    lats = [spot['lat'] for spot in landing_spots]
    lons = [spot['lon'] for spot in landing_spots]
    
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    
    # Return bounds in Leaflet format: [[south, west], [north, east]]
    # Add small padding (1% of range) to avoid markers on edge
    lat_padding = (max_lat - min_lat) * 0.01 or 0.01
    lon_padding = (max_lon - min_lon) * 0.01 or 0.01
    
    bounds = [
        [min_lat - lat_padding, min_lon - lon_padding],  # Southwest corner
        [max_lat + lat_padding, max_lon + lon_padding]   # Northeast corner
    ]
    
    return bounds


# Initialize the Dash app with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Expose the Flask server for production deployment (gunicorn, etc.)
server = app.server

# Add custom CSS for full-height layout via index_string
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                margin: 0;
                padding: 0;
                overflow: hidden;
            }
            .app-container {
                display: flex;
                flex-direction: column;
                height: 100vh;
            }
            .header-section {
                padding: 1rem;
                background-color: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
            }
            .content-section {
                display: flex;
                flex: 1;
                overflow: hidden;
            }
            .sidebar {
                width: 350px;
                overflow-y: auto;
                padding: 1rem;
                background-color: #ffffff;
                border-right: 1px solid #dee2e6;
            }
            .map-section {
                flex: 1;
                position: relative;
                overflow: hidden;
                display: flex;
                flex-direction: column;
            }
            #map-container {
                flex: 1;
                height: 100%;
                min-height: 0;
            }
            .instructions-overlay {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 1000;
                max-width: 400px;
                width: 90%;
                pointer-events: none;
            }
            .instructions-overlay > * {
                pointer-events: auto;
            }
            .footer-section {
                padding: 0.5rem;
                background-color: #f8f9fa;
                border-top: 1px solid #dee2e6;
                text-align: center;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Default landing spots (Sterling, Massachusetts area)
default_center = [42.426, -71.793]

# App layout with full-height map and sidebar controls
app.layout = html.Div([
    html.Div([
        # Header
        html.Div([
            html.H2("Glide Range Map", className="mb-1"),
            html.P(
                "Interactive visualization of glider range",
                className="text-muted mb-0",
                style={'fontSize': '0.9rem'}
            )
        ], className="header-section"),
        
        # Main content area with sidebar and map
        html.Div([
            # Left sidebar with controls
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Glide Parameters", className="card-title mb-3"),
                        
                        dbc.Label("Glide Ratio", html_for="glide-ratio", className="mt-2"),
                        dbc.Input(
                            id="glide-ratio",
                            type="number",
                            min=GLIDE_RATIO_MIN,
                            max=GLIDE_RATIO_MAX,
                            step=0.1,
                            value=GLIDE_RATIO_DEFAULT,
                            className="mb-1"
                        ),
                        dbc.FormText("Glider's glide ratio (e.g., 20:1)", className="mb-3"),
                        
                        dbc.Label("Altitude MSL (ft)", html_for="altitude", className="mt-2"),
                        dbc.Input(
                            id="altitude",
                            type="number",
                            min=ALTITUDE_MIN,
                            max=ALTITUDE_MAX,
                            step=100,
                            value=ALTITUDE_DEFAULT,
                            className="mb-1"
                        ),
                        dbc.FormText("Current altitude above sea level", className="mb-3"),
                        
                        dbc.Label("Arrival Height (ft)", html_for="arrival-height", className="mt-2"),
                        dbc.Input(
                            id="arrival-height",
                            type="number",
                            min=ARRIVAL_HEIGHT_MIN,
                            max=ARRIVAL_HEIGHT_MAX,
                            step=100,
                            value=ARRIVAL_HEIGHT_DEFAULT,
                            className="mb-1"
                        ),
                        dbc.FormText("Minimum safe arrival height", className="mb-3"),
                        
                        html.Hr(),
                        
                        html.H5("Load CUP File", className="card-title mt-3 mb-3"),
                        dcc.Upload(
                            id='upload-cup',
                            children=dbc.Button(
                                "Upload CUP File",
                                color="primary",
                                className="mb-2",
                                style={'width': '100%'}
                            ),
                            multiple=False,
                            style={'display': 'block'}
                        ),
                        html.Div(id='upload-status', className="text-muted small"),
                    ])
                ])
            ], className="sidebar"),
            
            # Right side - Map
            html.Div([
                # Instructions overlay (centered on map)
                html.Div([
                    dbc.Alert(
                        [
                            html.Strong("Quick Guide", className="d-block mb-2"),
                            html.Ul([
                                html.Li("Green: Airports/airfields", className="small"),
                                html.Li("Blue: Grass strips", className="small"),
                                html.Li("Yellow: Landable fields", className="small"),
                            ], className="mb-2", style={'paddingLeft': '1.2rem'}),
                            html.P("Adjust parameters on the left. Range circles ignore terrain.", className="small mb-0")
                        ],
                        color="info",
                        dismissable=True,
                        className="shadow"
                    )
                ], className="instructions-overlay"),
                
                # Map container
                html.Div(
                    id="map-container",
                    children=[
                        dl.Map(
                            id="map",
                            center=default_center,
                            zoom=9,
                            style={'width': '100%', 'height': '100%'},
                            children=[
                                dl.TileLayer(
                                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                                ),
                                # Layers control - initially empty, populated by callback
                                dl.LayersControl(
                                    position="topleft",
                                    id="layers-control"
                                )
                            ]
                        )
                    ],
                    style={'width': '100%', 'height': '100%'}
                )
            ], className="map-section"),
        ], className="content-section"),
        
        # Footer
        html.Div([
            html.Small([
                "Glide Range Map | ",
                html.A("GitHub", href="https://github.com/dssherrill/GlideMap", target="_blank")
            ], className="text-muted")
        ], className="footer-section"),
    ], className="app-container"),
    
    # Store for landing spots data - load default CUP file on initialization
    dcc.Store(id='landing-spots-store', data=load_default_cup_file()),
    
    # Store for map key to force recentering when data changes
    dcc.Store(id='map-key-store', data=0)
])


@callback(
    [Output('landing-spots-store', 'data'),
     Output('upload-status', 'children')],
    Input('upload-cup', 'contents'),
    State('upload-cup', 'filename')
)
def load_cup_file(contents, filename):
    """Load and parse a CUP file"""
    if contents is None:
        # Don't update when no file is uploaded (default data is already loaded in Store)
        return no_update, no_update
    
    try:
        landing_spots = parse_cup_file(contents)
        if not landing_spots:
            return [], html.Span("No landing spots found in file", className="text-warning")
        
        return landing_spots, html.Span(
            f"Loaded {len(landing_spots)} landing spots from {filename}",
            className="text-success"
        )
    except Exception as e:
        return [], html.Span(f"Error loading file: {str(e)}", className="text-danger")


@callback(
    Output('map-key-store', 'data'),
    Input('landing-spots-store', 'data'),
    State('map-key-store', 'data')
)
def update_map_key(landing_spots, current_key):
    """Increment map key when landing spots change to force map remount"""
    # Increment counter whenever landing spots change
    return current_key + 1


@callback(
    Output('map-container', 'children'),
    [Input('landing-spots-store', 'data'),
     Input('glide-ratio', 'value'),
     Input('altitude', 'value'),
     Input('arrival-height', 'value')],
    [State('map-key-store', 'data')]
)
def update_map(landing_spots, glide_ratio, altitude, arrival_height, map_key):
    """Update map with landing spots and glide range circles"""
    if not landing_spots:
        return no_update
    
    # Validate inputs
    glide_ratio = max(GLIDE_RATIO_MIN, min(GLIDE_RATIO_MAX, glide_ratio or GLIDE_RATIO_DEFAULT))
    altitude = max(ALTITUDE_MIN, min(ALTITUDE_MAX, altitude or ALTITUDE_DEFAULT))
    arrival_height = max(ARRIVAL_HEIGHT_MIN, min(ARRIVAL_HEIGHT_MAX, arrival_height or ARRIVAL_HEIGHT_DEFAULT))
    
    # Ensure arrival height is less than altitude
    if arrival_height >= altitude:
        # Apply safety factor: use either 90% of altitude or ensure minimum buffer
        arrival_height = max(0, min(
            altitude * ARRIVAL_HEIGHT_SAFETY_FACTOR, 
            altitude - ARRIVAL_HEIGHT_MIN_BUFFER
        ))
    
    # Create separate layer groups for different landing site types
    airports_markers = []
    grass_strips_markers = []
    landables_markers = []
    
    # Color mapping for different landing site types (matching JavaScript version)
    style_colors = {
        AIRPORT: '#AAC896',           # Green for airports
        GLIDING_AIRFIELD: '#AAC896',  # Green for gliding airfields
        GRASS_SURFACE: '#AAAADC',     # Blue for grass strips
        OUTLANDING: '#E6E696'         # Yellow for landable fields
    }
    
    for spot in landing_spots:
        try:
            radius = calculate_radius(glide_ratio, altitude, arrival_height, spot['elevation'])
            color = style_colors.get(spot['style'], 'gray')
            
            # Create circle for glide range
            circle = dl.Circle(
                center=[spot['lat'], spot['lon']],
                radius=radius,
                color='black',
                fillColor=color,
                fillOpacity=0.5,
                weight=1,
                children=[
                    dl.Popup(
                        html.Div([
                            html.Strong(spot['name']),
                            html.Br(),
                            f"Elevation: {spot['elevation']:.0f} ft",
                            html.Br(),
                            f"Range: {radius/1000:.1f} km"
                        ])
                    )
                ]
            )
            
            # Add to appropriate layer based on style
            if spot['style'] in [AIRPORT, GLIDING_AIRFIELD]:
                airports_markers.append(circle)
            elif spot['style'] == GRASS_SURFACE:
                grass_strips_markers.append(circle)
            elif spot['style'] == OUTLANDING:
                landables_markers.append(circle)
                
        except Exception as e:
            print(f"Error creating marker for {spot.get('name', 'unknown')}: {e}")
            continue
    
    # Recenter map when landing spots change (not when parameters change)
    # Also recenter on initial page load when default data is present
    triggered_id = ctx.triggered_id if ctx.triggered_id else None
    
    # Check if this is initial load (no triggered_id) or if landing spots changed
    if triggered_id is None or triggered_id == 'landing-spots-store':
        # Calculate new bounds based on landing spots
        bounds = calculate_map_bounds(landing_spots)
        
        # Calculate center and zoom from bounds
        center, zoom = calculate_center_and_zoom_from_bounds(bounds)
        
        # Create a new map container with unique key to force remount
        # The key is on the div, not the Map itself (Map doesn't support key prop)
        # This ensures the map recenters even after user has manually panned/zoomed
        new_map_container = html.Div(
            key=f"map-container-{map_key}",  # Unique key forces React remount
            children=[
                dl.Map(
                    id="map",
                    center=center,
                    zoom=zoom,
                    style={'width': '100%', 'height': '100%'},  # Fill parent container
                    children=[
                        dl.TileLayer(
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        ),
                        # Layers control with overlay layers as children
                        dl.LayersControl([
                            dl.Overlay(
                                dl.LayerGroup(children=airports_markers),
                                name='<span style="background: #AAC896; width: 10px; height: 10px; display: inline-block; margin-right: 5px;"></span>Airports',
                                checked=True,
                                id="airports-layer"
                            ),
                            dl.Overlay(
                                dl.LayerGroup(children=grass_strips_markers),
                                name='<span style="background: #AAAADC; width: 10px; height: 10px; display: inline-block; margin-right: 5px;"></span>Grass Strips',
                                checked=True,
                                id="grass-layer"
                            ),
                            dl.Overlay(
                                dl.LayerGroup(children=landables_markers),
                                name='<span style="background: #E6E696; width: 10px; height: 10px; display: inline-block; margin-right: 5px;"></span>Landable Fields',
                                checked=True,
                                id="landables-layer"
                            ),
                        ], position="topleft", id="layers-control")
                    ]
                )
            ]
        )
        
        return new_map_container
    else:
        # When only parameters change, we still recreate the map but with existing key
        # This updates the circles without recentering the map
        # Calculate current center from existing data
        bounds = calculate_map_bounds(landing_spots)
        center, zoom = calculate_center_and_zoom_from_bounds(bounds)
        
        # Use existing map_key so map doesn't remount (preserves user pan/zoom)
        updated_map_container = html.Div(
            key=f"map-container-{map_key}",  # Same key, no remount
            children=[
                dl.Map(
                    id="map",
                    center=center,
                    zoom=zoom,
                    style={'width': '100%', 'height': '100%'},
                    children=[
                        dl.TileLayer(
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        ),
                        # Layers control with overlay layers as children
                        dl.LayersControl([
                            dl.Overlay(
                                dl.LayerGroup(children=airports_markers),
                                name='<span style="background: #AAC896; width: 10px; height: 10px; display: inline-block; margin-right: 5px;"></span>Airports',
                                checked=True,
                                id="airports-layer"
                            ),
                            dl.Overlay(
                                dl.LayerGroup(children=grass_strips_markers),
                                name='<span style="background: #AAAADC; width: 10px; height: 10px; display: inline-block; margin-right: 5px;"></span>Grass Strips',
                                checked=True,
                                id="grass-layer"
                            ),
                            dl.Overlay(
                                dl.LayerGroup(children=landables_markers),
                                name='<span style="background: #E6E696; width: 10px; height: 10px; display: inline-block; margin-right: 5px;"></span>Landable Fields',
                                checked=True,
                                id="landables-layer"
                            ),
                        ], position="topleft", id="layers-control")
                    ]
                )
            ]
        )
        
        return updated_map_container


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
