# Layers Control Implementation

## Overview

The Python Dash version now includes a layers control feature that matches the JavaScript version's functionality. Users can toggle different types of landing spots on/off to customize their map view.

## Landing Spot Categories

The application categorizes landing spots into three groups based on their CUP file style field:

### 1. Airports (Style 4 & 5)
- **Color**: Green (#AAC896)
- **Includes**: 
  - Airports (style 5)
  - Gliding Airfields (style 4)
- **Description**: Paved runways suitable for powered aircraft and gliders

### 2. Grass Strips (Style 2)
- **Color**: Blue (#AAAADC)
- **Includes**: Grass surface landing areas
- **Description**: Unpaved grass runways, typically shorter than airports

### 3. Landable Fields (Style 3)
- **Color**: Yellow (#E6E696)
- **Includes**: Outlanding fields
- **Description**: Open fields suitable for emergency landings

## User Interface

### Layer Control Position
- Located at **top-left** corner of the map
- Consistent with JavaScript version placement
- Easily accessible without obstructing map view

### Control Features
- **Toggle visibility**: Click layer name or checkbox to show/hide
- **Color legend**: Colored squares match circle colors on map
- **Default state**: All layers enabled/visible on startup
- **Persistent during session**: Layer selections maintained while adjusting parameters

### Visual Design
```
┌─────────────────────────┐
│ Layers                  │
├─────────────────────────┤
│ ☑ ▪ Airports            │
│ ☑ ▪ Grass Strips        │
│ ☑ ▪ Landable Fields     │
└─────────────────────────┘
```

## Technical Implementation

### Component Structure

```python
dl.Overlay(
    dl.LayerGroup(children=airports_markers),
    name='<span style="...">...</span>Airports',
    checked=True,
    id="airports-layer"
)
```

### Marker Separation

Landing spots are filtered into three separate lists during callback processing:

```python
if spot['style'] in [AIRPORT, GLIDING_AIRFIELD]:
    airports_markers.append(circle)
elif spot['style'] == GRASS_SURFACE:
    grass_strips_markers.append(circle)
elif spot['style'] == OUTLANDING:
    landables_markers.append(circle)
```

### Layer Control Component

```python
dl.LayersControl(
    position="topleft",
    id="layers-control"
)
```

## Behavior

### Initial Load
1. Map loads with default CUP file
2. All three layers visible
3. Layer control displays at top-left
4. All checkboxes checked

### Toggling Layers
1. User clicks layer name or checkbox
2. Dash Leaflet toggles layer visibility
3. Circles for that category show/hide
4. Other layers unaffected
5. Selection persists while adjusting parameters

### Loading New CUP File
1. Spots recategorized by style
2. All layers remain in previously selected state
3. Map recenters to show new data
4. Layer control updates with new counts

### Adjusting Parameters
1. Glide ratio, altitude, or arrival height changes
2. Circle radii recalculate
3. Layer visibility states preserved
4. Map view (center/zoom) preserved

## Comparison with JavaScript Version

### Similarities
✅ Three categories (Airports, Grass Strips, Landables)
✅ Same color scheme
✅ Same positioning (top-left)
✅ Toggle on/off functionality
✅ Colored legend squares

### Differences
- Python uses `dl.Overlay` + `dl.LayerGroup`
- JavaScript uses `L.featureGroup()` + `L.control.layers()`
- Python: Overlays defined in Map children
- JavaScript: Overlays added to map after creation
- Both achieve same user experience

## Code Style Constants

Matching the JavaScript version's style constants:

```python
GRASS_SURFACE = 2
OUTLANDING = 3
GLIDING_AIRFIELD = 4
AIRPORT = 5
```

These map directly to the CUP file style field values.

## Troubleshooting

### Layers Control Not Visible
- Check that `dl.LayersControl` is in Map children
- Verify position="topleft" is set
- Ensure Dash Leaflet version supports LayersControl

### Circles Not Appearing
- Check that spots are being categorized correctly
- Verify style field is being read from CUP file
- Check browser console for JavaScript errors

### Layers Not Toggling
- Verify each Overlay has unique id
- Check that LayerGroup has children (markers)
- Ensure Dash Leaflet callbacks are working

### Wrong Colors
- Verify style_colors dict matches expected values:
  - AIRPORT/GLIDING_AIRFIELD: '#AAC896' (green)
  - GRASS_SURFACE: '#AAAADC' (blue)
  - OUTLANDING: '#E6E696' (yellow)

## Future Enhancements

Potential improvements:

1. **Layer Counts**: Show number of spots in each category
2. **Custom Styles**: Allow users to customize colors
3. **Additional Categories**: Support more landing spot types
4. **Filtering**: Add distance or elevation filters
5. **Layer Persistence**: Save layer states to local storage
6. **Keyboard Shortcuts**: Toggle layers with hotkeys

## References

- Dash Leaflet Documentation: https://dash-leaflet.herokuapp.com/
- Leaflet Layers Control: https://leafletjs.com/reference.html#control-layers
- Original JavaScript Implementation: See `glideRange.js` lines with `L.featureGroup()` and `L.control.layers()`
