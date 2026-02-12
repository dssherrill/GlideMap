# Map Height Stability Fix

## Problem Description

The map initially appeared at full height when the page loaded, but then changed to a more rectangular shape (wider than tall) approximately when the Quick Guide box appeared. This caused an unpleasant visual jump and reduced the usable map area.

## Root Cause

The issue was caused by insufficient CSS constraints on the flex layout:

1. **Parent container** (`.map-section`) used `flex: 1` but didn't explicitly establish itself as a flex container
2. **Map container** (`#map-container`) used `height: 100%` but lacked proper flex properties
3. **Overlay rendering** triggered a layout recalculation that exposed these layout weaknesses
4. The flex item's natural sizing behavior caused the map to shrink when content appeared

## Technical Analysis

### Flex Layout Gotchas

When using nested flex layouts with `height: 100%`, you must:
- Explicitly set `display: flex` on the parent
- Use `min-height: 0` on flex children to prevent overflow
- Combine `flex: 1` with `height: 100%` for reliable sizing

### The `min-height: 0` Mystery

By default, flex items have `min-height: auto`, which means they won't shrink below their content size. When combined with `height: 100%`, this can cause the item to:
1. Try to take 100% of parent height
2. Also try to fit its content
3. Result in unpredictable sizing during layout calculations

Setting `min-height: 0` allows the flex item to properly respect the `height: 100%` directive.

## Solution Implemented

### CSS Changes

```css
.map-section {
    flex: 1;
    position: relative;
    overflow: hidden;
    display: flex;              /* NEW: Establish flex container */
    flex-direction: column;     /* NEW: Stack children vertically */
}

#map-container {
    flex: 1;                    /* NEW: Take all available space */
    height: 100%;               /* EXISTING: Fill parent height */
    min-height: 0;              /* NEW: Allow proper flex sizing */
}

.instructions-overlay {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 1000;
    max-width: 400px;
    width: 90%;
    pointer-events: none;       /* NEW: Don't block clicks */
}

.instructions-overlay > * {
    pointer-events: auto;       /* NEW: But allow clicking the alert */
}
```

### Key Improvements

1. **Explicit Flex Container**: `.map-section` now explicitly declares `display: flex` and `flex-direction: column`, creating a proper flex context for its children.

2. **Flex Child Sizing**: `#map-container` uses `flex: 1` to take all available space within the flex container, combined with `height: 100%` for explicit sizing.

3. **Min-Height Fix**: Adding `min-height: 0` prevents the flex item from expanding beyond its allocated space when content appears.

4. **Pointer Events**: The overlay now uses `pointer-events: none` on the container but `auto` on children, ensuring it truly "floats" above the map without affecting layout.

## Before and After

### Before
```
- Map loads at full height
- Quick Guide appears
- Layout recalculates
- Map shrinks to rectangular shape
- User sees annoying visual jump
```

### After
```
- Map loads at full height
- Quick Guide appears
- Layout remains stable
- Map maintains full height
- Smooth, professional appearance
```

## Testing

### Visual Tests
1. ✅ Map loads at full height initially
2. ✅ Map stays at full height when Quick Guide appears
3. ✅ Map fills vertical space from header to footer
4. ✅ No visual jumps or layout shifts
5. ✅ Quick Guide is dismissable

### Responsive Tests
1. ✅ Resize browser window - map adapts smoothly
2. ✅ Very tall windows - map fills height properly
3. ✅ Very wide windows - map maintains proportions
4. ✅ Quick Guide remains centered

### Interaction Tests
1. ✅ Click map - map responds normally
2. ✅ Click Quick Guide - alert dismisses
3. ✅ Click outside Quick Guide - map responds
4. ✅ Pan/zoom map - smooth interaction

## Browser Compatibility

This solution uses standard CSS Flexbox properties supported by all modern browsers:
- Chrome 29+ (2013)
- Firefox 28+ (2014)
- Safari 9+ (2015)
- Edge (all versions)

## Future Considerations

### If Issues Persist

If map height issues reappear, consider:

1. **Absolute Positioning Alternative**
   ```css
   .map-section {
       position: relative;
   }
   #map-container {
       position: absolute;
       top: 0;
       right: 0;
       bottom: 0;
       left: 0;
   }
   ```

2. **CSS Grid Alternative**
   ```css
   .app-container {
       display: grid;
       grid-template-rows: auto 1fr auto;
   }
   .content-section {
       display: grid;
       grid-template-columns: 350px 1fr;
   }
   ```

3. **JavaScript Height Calculation**
   Use Dash callbacks to calculate and set explicit pixel heights based on window size (less elegant but more reliable).

## Related Issues

This fix also resolves:
- Potential scrollbar appearance issues
- Map rendering artifacts during initial load
- Inconsistent behavior across different browsers
- Layout shifts when other UI elements load

## References

- [CSS Flexbox Spec](https://www.w3.org/TR/css-flexbox-1/)
- [A Complete Guide to Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [Flexbox min-height gotcha](https://stackoverflow.com/questions/36247140/why-dont-flex-items-shrink-past-content-size)
