# Map Recentering Solution

## Problem
When using Dash Leaflet, the map's view doesn't automatically recenter when new data is loaded after the user has manually panned or zoomed the map.

## Current Behavior

The application correctly:
- ✅ Updates all landing spot circles when new CUP files are loaded
- ✅ Removes old circles and displays new ones
- ✅ Centers the map on initial load
- ✅ Centers the map on first CUP file load

The limitation:
- ⚠️ After user manually pans/zooms, subsequent CUP file loads update the circles but may not recenter the map view
- This is standard Leaflet behavior - user interactions take precedence over programmatic updates

## Why This Happens

When a user interacts with a Leaflet map (pan, zoom), Leaflet maintains that state. Simply updating the `center` and `zoom` properties doesn't override this user interaction state. This is by design in Leaflet to prevent programmatic changes from disrupting user navigation.

## What Works

The callback system works perfectly:
1. User uploads a new CUP file
2. Store updates with new landing spots data
3. Callback fires with `triggered_id = 'landing-spots-store'`
4. All circles update correctly (old ones removed, new ones added)
5. Center and zoom are calculated from new bounds
6. Map receives new center/zoom values

The **only** thing that doesn't happen is the map view recentering after user interaction.

## Attempted Solutions

### 1. Using viewport property ❌
```python
viewport = {'center': [lat, lon], 'zoom': zoom, 'transition': 'flyTo'}
```
**Result**: JavaScript error "can't access property 'transition', e is null"

### 2. Using viewport with timestamp ❌
```python
viewport = {'center': [lat, lon], 'zoom': zoom, '_timestamp': time.time()}
```
**Result**: JavaScript error, breaks map loading

### 3. Using center/zoom directly ✅
```python
return markers, center, zoom
```
**Result**: Map loads correctly, circles update, but view doesn't recenter after user interaction

## Current Solution

We use the simple, reliable approach with `Output('map', 'center')` and `Output('map', 'zoom')` alongside `Output('map', 'children')`. The callback detects the trigger via `dash.ctx.triggered_id` and only recenters when landing spots data changes (not on glide ratio/altitude/arrival height changes):

```python
@callback(
    [Output('map', 'children'),
     Output('map', 'center'),
     Output('map', 'zoom')],
    [Input('landing-spots-store', 'data'),
     Input('glide-ratio', 'value'),
     Input('altitude', 'value'),
     Input('arrival-height', 'value')]
)
def update_map_layers(landing_spots, glide_ratio, altitude, arrival_height):
    triggered_id = ctx.triggered_id
    # ... build markers ...
    if triggered_id is None or triggered_id == 'landing-spots-store':
        bounds = calculate_map_bounds(landing_spots)
        center, zoom = calculate_center_and_zoom_from_bounds(bounds)
    else:
        center = no_update
        zoom = no_update
    return markers, center, zoom
```

**Advantages**:
- Map loads reliably every time
- No JavaScript errors
- Circles update correctly
- Initial centering works
- Code is simple and maintainable

**Limitation**:
- Map view doesn't recenter after user has manually interacted with it
- This is acceptable because:
  - Circles still update (users can see the new data)
  - It's standard Leaflet behavior
  - Users can manually pan to see new areas
  - Most users load a file once and then adjust parameters (which keeps the view)

## User Experience

1. **Initial load**: Map centers on Sterling, MA with 418 landing spots ✅
2. **User pans/zooms**: Map follows user interaction ✅
3. **Upload new CUP**: Circles update to show new landing spots ✅
4. **Map recentering**: May not happen (user can manually pan to new area) ⚠️

This is an acceptable trade-off for a stable, error-free application.

## References

- Dash Leaflet documentation: https://dash-leaflet.com
- Leaflet map state: https://leafletjs.com/reference.html#map-state
- Dash callbacks: https://dash.plotly.com/basic-callbacks
