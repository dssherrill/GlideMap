# Map Recentering Solution

## Problem
When using Dash Leaflet, updating the map's `center` and `zoom` properties doesn't reliably recenter the map after the user has manually panned or zoomed. This is because:

1. Leaflet maintains internal state about the map's position
2. Dash/React doesn't trigger updates when property values appear unchanged
3. Simply setting `center=[new_lat, new_lon]` doesn't override user interaction state

## Solution: Viewport with Timestamp

We use the `viewport` property with a timestamp to force Dash to recognize each update as unique:

```python
viewport = {
    'center': [lat, lon],
    'zoom': zoom_level,
    'transition': 'flyTo',      # Smooth animation
    '_timestamp': time.time()    # Forces unique value
}
```

### How It Works

1. **Viewport Property**: Dash Leaflet's `viewport` property is designed for programmatic control
2. **Timestamp Key**: Adding `_timestamp` ensures the dict is always unique
3. **Dash Recognition**: Dash compares viewport values and sees they differ (due to timestamp)
4. **Map Update**: Leaflet receives the new viewport and executes `flyTo(center, zoom)`

### Why This Works

- **Value Comparison**: Dash uses value equality to detect changes
- **Dict Uniqueness**: Two dicts with different timestamps are not equal
- **Force Update**: Even if center/zoom are the same, timestamp makes viewport unique
- **Leaflet Action**: `flyTo` method works even after user interaction

### Implementation

```python
# In callback that updates map
if triggered_id is None or triggered_id == 'landing-spots-store':
    bounds = calculate_map_bounds(landing_spots)
    center, zoom = calculate_center_and_zoom_from_bounds(bounds)
    
    viewport = {
        'center': center,
        'zoom': zoom,
        'transition': 'flyTo',
        '_timestamp': time.time()
    }
    return markers, viewport
else:
    return markers, no_update
```

## Testing

To verify this works:
1. Load the app - map should center on Sterling, MA (default CUP file)
2. Manually pan the map far away (e.g., to California)
3. Upload vero_beach_test.cup (Florida locations)
4. Map should smoothly fly to Florida and show all 52 landing spots

## Alternative Approaches Tried

1. **center/zoom properties**: Don't override user state reliably
2. **bounds property**: Caused JavaScript errors in Dash Leaflet 1.0.15
3. **viewport without timestamp**: Only worked on first update
4. **invalidateSize**: Only recalculates size, doesn't change position

## References

- Dash Leaflet documentation: https://dash-leaflet.herokuapp.com/
- Leaflet flyTo method: https://leafletjs.com/reference.html#map-flyto
- Dash property updates: https://dash.plotly.com/basic-callbacks
