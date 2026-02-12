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
    overflow: hidden;  /* Prevents scrollbars (caution: avoid on mobile) */
}

.app-container {
    display: flex;
    flex-direction: column;
    height: 100dvh;  /* Dynamic viewport height (Chrome/Edge 108+, Firefox 110+, Safari 15.4+) */
    height: 100vh;   /* Fallback for older browsers */
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

**⚠️ Mobile Viewport Considerations**:
- **`overflow: hidden` on body**: Can trap users on mobile where viewport resizing is common (browser UI appears/disappears). Consider applying `overflow: hidden` only to `.app-container` and specific containers instead.
- **`height: 100vh` issue**: Does not account for dynamic viewport (browser bars). Use `height: 100dvh` (supported in Chrome/Edge 108+, Firefox 110+, Safari 15.4+) with `100vh` as a fallback for older browsers.
- **Recommended fix**: Use `height: min(100dvh, 100vh)` or apply explicit double-rule: `height: 100dvh; height: 100vh;` (browsers ignore unknown properties and use fallback). Alternatively, detect and apply dynamic height via JavaScript if viewport resizing is detected.
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
5. **Responsive**: Optimized for desktop and tablet; mobile enhancements planned

### Accessibility
1. **Keyboard navigation**: All controls accessible via Tab navigation and keyboard shortcuts
2. **ARIA landmarks**: Semantic HTML (header, nav, main, footer) with ARIA regions for screen readers
3. **Focus management**: Clear focus indicators and logical tab order through interactive elements
4. **Dismissable overlays**: Alert overlay can be dismissed via Escape key or close button

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
- ✅ Chrome/Edge (Chromium) 108+ (dvh support); all versions (vh support)
- ✅ Firefox 110+ (dvh support); all versions (vh support)
- ✅ Safari 15.4+ (dvh support); all versions (vh support)
- ✅ All modern browsers with Flexbox support

**CSS Dynamic Viewport Height (dvh) Support**:
- **100dvh** (dynamic viewport height) is supported in Chrome/Edge 108+, Firefox 110+, and Safari 15.4+
- For older browser support, use CSS fallback: `height: min(100vh, 100dvh)` or provide a `100vh` fallback
- Example: `height: min(100vh, 100dvh)` will use the smaller value (more reliable on mobile)

## Responsive Behavior
- **Large screens (desktop)**: Full sidebar + full-height map layout
- **Medium screens (tablet)**: Sidebar may need scrolling for tall control panels; map remains full-height
- **Small screens (mobile)**: Layout requires workarounds for dynamic viewport height (address in future enhancement)

**⚠️ Viewport Height Concerns**:
- **100vh issue**: The `height: 100vh` on `.app-container` and `body { overflow: hidden }` can cause problems on mobile devices where the browser UI (address bar, navigation) appears and disappears, changing the viewport height dynamically.
  - **Mobile browser bars**: When address bar hides, 100vh may exceed the visible viewport, causing content to be clipped.
  - **Overflow trap**: Setting `overflow: hidden` globally can prevent scrolling and trap users when content overflows unexpectedly.
- **Recommended fixes**:
  1. Use CSS: `height: min(100vh, 100dvh)` to use the smaller of viewport height values (where 100dvh = dynamic viewport height)
  2. Or apply `overflow: hidden` only to specific containers (like `.content-section`), not globally on `body`
  3. Use JavaScript to detect viewport resize and adjust height dynamically if needed
  4. Consider media queries or `@supports` rules to apply mobile-specific viewport handling

**Current status**: Desktop and tablet layouts work well; mobile optimization is a future enhancement.

## Future Enhancements
Priority improvements:
1. **Mobile viewport height fix**: Use `100dvh` with `100vh` fallback (or `min(100dvh, 100vh)`) for cross-browser support, accounting for dynamic browser UI bars
2. **Conditional overflow**: Apply `overflow: hidden` only to specific containers on mobile, not globally
3. **Collapsible sidebar** on small screens (< 768px)
4. **Hamburger menu** for compact control access
5. **Touch-optimized** map controls and buttons
6. **Responsive breakpoints** with proper testing across devices

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
