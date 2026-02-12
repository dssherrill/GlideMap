# Solution: Force Map Recentering by Component Remounting

## The Problem

**Steps to reproduce**:
1. Start the application → Map centers on New England (Sterling, MA)
2. Pan/zoom to Denver, Colorado
3. Load vero_beach_test.cup (Florida locations)
4. **Bug**: Map remains centered on Denver but zooms out

**Expected**: Map should recenter to Florida to show the new landing spots.

## Why Previous Attempts Failed

### Attempt 1: Update center/zoom props directly
```python
return markers, center, zoom
```
**Result**: Leaflet ignores prop updates after user interaction

### Attempt 2: Use viewport property
```python
viewport = {'center': center, 'zoom': zoom, 'transition': 'flyTo'}
```
**Result**: JavaScript error - breaks the map entirely

### Why These Failed
Leaflet maintains internal state about user interactions. Simply updating React props doesn't override this state. Leaflet is designed this way to prevent programmatic changes from disrupting user navigation.

## The Working Solution

**Key Insight**: Force React to completely remount the component, creating a fresh Leaflet map instance.

### Implementation

1. **Wrap map in a container**:
```python
html.Div(
    id="map-container",
    children=[dl.Map(...)]
)
```

2. **Output entire map component from callback**:
```python
@callback(
    [Output('landing-spots-layer', 'children'),
     Output('map-container', 'children')],
    ...
)
```

3. **Create new map when data changes**:
```python
if triggered_id is None or triggered_id == 'landing-spots-store':
    # Data changed - create completely new map
    new_map = dl.Map(
        id="map",
        key=f"map-{map_key}",  # Unique key forces remount
        center=center,
        zoom=zoom,
        children=[
            dl.TileLayer(...),
            dl.LayerGroup(id="landing-spots-layer", children=markers)
        ]
    )
    return [], new_map
else:
    # Only parameters changed - update markers only
    return markers, no_update
```

### How It Works

**When landing spots change**:
1. Calculate new center/zoom from bounds
2. Create entirely new Map component with:
   - Unique `key` (forces React remount)
   - New center/zoom values
   - Markers embedded in LayerGroup
3. React sees different key → unmounts old map → mounts new map
4. Fresh Leaflet instance has no user interaction state
5. Map appears at specified center/zoom

**When only parameters change** (glide ratio, altitude):
1. Calculate new circle radii
2. Update markers in existing LayerGroup
3. Don't touch map component (preserves user's view)
4. User's pan/zoom state maintained

## Why This Works

### React's Key Property
React uses `key` to identify components. When `key` changes:
1. React unmounts the old component (destroys old Leaflet map)
2. React mounts a new component (creates new Leaflet map)
3. New map has no memory of user interactions
4. New map respects center/zoom props

### Counter-Based Keys
```python
# Store tracks counter
dcc.Store(id='map-key-store', data=0)

# Callback increments on data change
def update_map_key(landing_spots, current_key):
    return current_key + 1

# Map uses counter in key
key=f"map-{map_key}"
```

Each data change gets unique key: `map-0`, `map-1`, `map-2`, etc.

## Trade-offs

### Advantages ✅
- Map reliably recenters after user interaction
- No JavaScript errors
- Clean, understandable code
- Stable behavior

### Disadvantages ⚠️
- Brief flicker when map remounts
- User loses zoom/pan state when loading new data
- More expensive (destroys/recreates DOM)

### Why This Is Acceptable
1. **Remounting only on data change**: Parameters (glide ratio, altitude) still preserve view
2. **Expected behavior**: When user loads new data, they expect to see it
3. **Flicker is brief**: Modern browsers remount quickly
4. **Alternative is worse**: Map stuck on wrong location is confusing

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

## Comparison with JavaScript Version

The original JavaScript/HTML version likely:
1. Reloads the entire page, or
2. Uses Leaflet's `flyToBounds()` method directly, or
3. Also has this issue but wasn't noticed

Dash Leaflet doesn't expose `flyToBounds()` directly, so we use component remounting instead.

## Conclusion

This solution trades a brief visual flicker for reliable recentering behavior. The flicker is acceptable because:
- It only happens when loading new data (rare)
- Users expect to see new data when they load it
- Alternative (broken recentering) is worse

The implementation is clean, maintainable, and works reliably across all scenarios.
