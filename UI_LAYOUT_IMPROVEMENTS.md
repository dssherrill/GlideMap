# UI Layout Improvements

## Overview
This document describes the full-height map layout with sidebar controls implemented for the Python Dash version of GlideMap.

## Requirements
1. Map should occupy the full height of the window (leave room for header/footer)
2. Controls should be stacked on the left side
3. Initial instruction dialog should be smaller and centered on the map

## Implementation

### Layout Structure
The new layout uses CSS Flexbox to create a full-viewport-height application:

```
┌─────────────────────────────────────┐
│         Header (minimal)            │
├────────────┬────────────────────────┤
│            │                        │
│  Sidebar   │      Map Section       │
│  (350px)   │      (flex: 1)         │
│            │                        │
│  Controls  │      [Map fills        │
│  Stacked   │       100% height]     │
│            │                        │
│            │   [Instructions        │
│            │    Overlay Centered]   │
│            │                        │
├────────────┴────────────────────────┤
│         Footer (minimal)            │
└─────────────────────────────────────┘
```

### CSS Architecture
Custom CSS is injected via `app.index_string`:

```css
body {
    margin: 0;
    padding: 0;
    overflow: hidden;  /* Prevents scrollbars */
}

.app-container {
    display: flex;
    flex-direction: column;
    height: 100vh;  /* Full viewport height */
}

.content-section {
    display: flex;
    flex: 1;  /* Takes remaining space */
    overflow: hidden;
}

.sidebar {
    width: 350px;
    overflow-y: auto;  /* Scrollable if needed */
}

.map-section {
    flex: 1;  /* Takes remaining width */
    position: relative;
}
```

### Components

#### 1. Header Section
- Minimal height (~60px)
- Contains app title and subtitle
- Light gray background for visual separation

#### 2. Sidebar (Left)
- **Width**: 350px fixed
- **Content**: All glide parameter controls stacked vertically
- **Scrolling**: Independent scroll if content exceeds viewport
- **Styling**: Bootstrap card with clean borders
- **Features**:
  - Glide ratio input
  - Altitude input
  - Arrival height input
  - CUP file upload button (full width)
  - Upload status display

#### 3. Map Section (Right)
- **Size**: Fills remaining horizontal and vertical space
- **Map Component**: Set to 100% width and 100% height
- **Position**: Relative (for overlay positioning)

#### 4. Instructions Overlay
- **Position**: Absolutely positioned, centered on map
- **Centering**: CSS transform translate(-50%, -50%)
- **Size**: Max-width 400px, responsive to smaller screens
- **Z-index**: 1000 (floats above map)
- **Content**:
  - Quick guide with color-coded landing site types
  - Compact bullet points
  - Dismissable alert
  - Shadow for depth

#### 5. Footer
- Minimal height (~35px)
- Contains GitHub link and copyright
- Light gray background

## Benefits

### User Experience
1. **Maximum map visibility**: Map uses all available vertical space
2. **Always accessible controls**: Sidebar always visible, no scrolling needed
3. **Non-intrusive instructions**: Centered overlay can be dismissed
4. **Clean, modern appearance**: Professional layout with clear visual hierarchy
5. **Responsive**: Adapts to different viewport sizes

### Technical
1. **Pure CSS solution**: No JavaScript required for layout
2. **Flexbox reliability**: Works across all modern browsers
3. **Performance**: No layout calculations in render loop
4. **Maintainable**: Clear separation of concerns

## Code Changes

### Before (Container-based layout)
```python
app.layout = dbc.Container([
    dbc.Row([...]),  # Header
    dbc.Row([...]),  # Controls (full width)
    dbc.Row([...]),  # Map (600px fixed height)
], fluid=True)
```

### After (Flexbox layout)
```python
app.layout = html.Div([
    html.Div([...], className="header-section"),
    html.Div([
        html.Div([...], className="sidebar"),    # 350px
        html.Div([...], className="map-section") # flex: 1
    ], className="content-section"),
    html.Div([...], className="footer-section")
], className="app-container")
```

## Browser Compatibility
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari
- ✅ All modern browsers with Flexbox support

## Responsive Behavior
- **Large screens**: Full sidebar + map layout
- **Medium screens**: Sidebar may need scrolling for very tall content
- **Small screens**: Layout may need media queries for mobile (future enhancement)

## Future Enhancements
Possible improvements for mobile devices:
1. Collapsible sidebar on small screens
2. Hamburger menu for controls
3. Responsive breakpoints for different devices
4. Touch-optimized map controls

## Testing
To verify the layout works correctly:
1. Start the app: `python app.py`
2. Open browser to `http://localhost:8050`
3. Verify:
   - Map fills viewport height
   - Sidebar visible on left
   - Instructions centered on map
   - Controls accessible without scrolling
   - Resize window - layout adapts

## Screenshot
![Full-Height Layout](https://github.com/user-attachments/assets/ce1b0b47-cb6d-4815-a629-8164cd4ecd8a)

## Related Files
- `app.py`: Main application with layout and CSS
- `requirements.txt`: No new dependencies added
