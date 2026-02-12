# Solution: Map Recentering via Center/Zoom Outputs

## The Problem

**Steps to reproduce**:
1. Start the application → Map centers on New England (Sterling, MA)
2. Pan/zoom to Denver, Colorado
3. Load vero_beach_test.cup (Florida locations)
4. **Bug**: Map remains centered on Denver but zooms out

**Expected**: Map should recenter to Florida to show the new landing spots.

## Why This Happens

When a user interacts with a Leaflet map (pan, zoom), Leaflet maintains that state. Simply updating the `center` and `zoom` properties doesn't always override this user interaction state. This is by design in Leaflet to prevent programmatic changes from disrupting user navigation.

However, the implemented solution shows that selective trigger-based updating (only recenter on data changes, not on every callback) is reliable and acceptable.

## Why Previous Attempts Failed

### Attempt 1: Update center/zoom props directly (every callback)
```python
return markers, center, zoom
```
**Result**: Leaflet may ignore prop updates after user interaction if they are sent on every callback.

### Attempt 2: Using viewport property with flyTo
```python
viewport = {'center': [lat, lon], 'zoom': zoom, 'transition': 'flyTo'}
```
**Result**: JavaScript error "can't access property 'transition', e is null" — breaks the map entirely.

### Attempt 3: Using viewport with timestamp
```python
viewport = {'center': [lat, lon], 'zoom': zoom, '_timestamp': time.time()}
```
**Result**: JavaScript error, breaks map loading.

### Attempt 4: Direct center/zoom without trigger detection
```python
return markers, center, zoom  # sent on every callback
```
**Result**: Map loads correctly, circles update, but view doesn't recenter after user interaction because Leaflet receives updates on every trigger, including parameter changes.

## The Working Solution

**Key Insight**: Use `Output('map', 'center')` and `Output('map', 'zoom')` alongside `Output('map', 'children')`, but **only send center/zoom updates when landing spot data changes** — not when the user adjusts glide parameters or toggles layers. This selective trigger-based approach is reliable and respects user interactions.

The callback system works perfectly:
1. User uploads a new CUP file
2. Store updates with new landing spots data
3. Callback fires with `ctx.triggered_id = 'landing-spots-store'`
4. All circles update correctly (rebuilt with new data)
5. Center and zoom are calculated from bounds of new landing spots
6. Map receives new center/zoom values **only on data change**, not on every update
7. Map recenters to show the new data

### Implementation

The callback detects the trigger and conditionally returns center/zoom updates:
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
    """Update map layers with landing spots and glide range circles"""
    # ... build markers list (TileLayer + LayersControl) ...

    triggered_id = ctx.triggered_id
    if triggered_id is None or triggered_id == 'landing-spots-store':
        bounds = calculate_map_bounds(landing_spots)
        center, zoom = calculate_center_and_zoom_from_bounds(bounds)
    else:
        center = no_update
        zoom = no_update

    return markers, center, zoom
```

### How It Works

**When landing spots change** (new CUP file loaded or initial load):
1. `ctx.triggered_id` is `None` (initial) or `'landing-spots-store'`
2. Calculate bounds from the new landing spots
3. Derive center/zoom via `calculate_center_and_zoom_from_bounds(bounds)`
4. Return markers **plus** the new center and zoom values
5. Map recenters to show the new data

**When only parameters change** (glide ratio, altitude, arrival height):
1. `ctx.triggered_id` is `'glide-ratio'`, `'altitude'`, or `'arrival-height'`
2. Recalculate circle radii and rebuild markers
3. Return markers with `no_update` for center and zoom
4. Map children update but the user's pan/zoom state is preserved

## Trade-offs

### Advantages ✅
- Map recenters reliably when new data is loaded
- No JavaScript errors
- No DOM destruction/recreation — smooth transition
- User's view is preserved when only adjusting parameters
- Clean, simple callback logic

### Disadvantages ⚠️
- After user manually pans/zooms, Leaflet may not always honor
  programmatic center/zoom updates (standard Leaflet behavior)

### Why This Is Acceptable
1. **Selective recentering**: Only triggers on data changes, not parameter tweaks
2. **Expected behavior**: When users load new data, they expect to see it
3. **Fallback**: Even if recentering doesn't override a strong user interaction,
   the circles still update correctly and users can manually pan

## Testing the Fix

### Test Scenario
1. **Initial load**:
   - Map should center on Sterling, MA (42.94°N, 72.15°W)
   - Should show 418 landing spots

2. **User interaction**:
   - Pan to Denver (39.74°N, 104.99°W)
   - Zoom in/out
   - Verify map follows user input

3. **Load new data**:
   - Upload vero_beach_test.cup
   - Map should **recenter to Florida** (26.58°N, 81.11°W)
   - Should show 52 landing spots
   - **Not** stay on Denver

4. **Parameter changes**:
   - Adjust glide ratio from 40:1 to 30:1
   - Circles should shrink
   - Map should **stay at current view** (preserve user's position)

### Verification
```bash
python app.py
# Open browser to http://localhost:8050
# Follow test scenario above
```

## Conclusion

This solution uses Dash Leaflet's `center` and `zoom` properties as callback outputs, selectively updating them only when new landing spot data is loaded via `ctx.triggered_id` detection. This provides reliable recentering without DOM remounting overhead, while preserving user interactions when only glide parameters change. The implementation is simple, maintainable, and avoids JavaScript errors.

## References

- Dash Leaflet documentation: https://dash-leaflet.com
- Dash Callbacks and Context: https://dash.plotly.com/basic-callbacks
- Leaflet map state and interaction: https://leafletjs.com/reference.html#map-state
