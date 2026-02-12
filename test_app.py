"""
Test script for the Glide Range Map Dash application
"""

import sys
import os

# Test imports
print("Testing imports...")
try:
    from app import (
        feet_to_meters,
        meters_to_feet,
        calculate_radius,
        parse_cup_coordinate,
        parse_cup_elevation,
        parse_cup_file,
        calculate_map_bounds,
    )

    print("✓ All imports successful")
except Exception as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test conversion functions
print("\nTesting conversion functions...")
assert abs(feet_to_meters(1000) - 304.8) < 0.1, "feet_to_meters failed"
assert abs(meters_to_feet(304.8) - 1000) < 0.1, "meters_to_feet failed"
print("✓ Conversion functions work correctly")

# Test coordinate parsing
print("\nTesting coordinate parsing...")
lat = parse_cup_coordinate("5107.830N", is_longitude=False)
assert abs(lat - 51.1305) < 0.001, f"Latitude parsing failed: got {lat}"
lon = parse_cup_coordinate("01410.467E", is_longitude=True)
assert abs(lon - 14.1744) < 0.001, f"Longitude parsing failed: got {lon}"
print(f"✓ Coordinate parsing works: lat={lat:.4f}, lon={lon:.4f}")

# Test elevation parsing
print("\nTesting elevation parsing...")
elev_ft = parse_cup_elevation("1234ft")
assert elev_ft == 1234, f"Feet parsing failed: got {elev_ft}"
elev_m = parse_cup_elevation("100m")
assert abs(elev_m - 328.08) < 0.1, f"Meters parsing failed: got {elev_m}"
print(f"✓ Elevation parsing works: {elev_ft}ft, {elev_m:.1f}ft")

# Test radius calculation
print("\nTesting radius calculation...")
radius = calculate_radius(20, 3500, 1000, 500)
expected = feet_to_meters(20 * (3500 - 1000 - 500))
assert (
    abs(radius - expected) < 0.1
), f"Radius calculation failed: got {radius}, expected {expected}"
print(f"✓ Radius calculation works: {radius:.1f}m ({radius/1000:.1f}km)")

# Test CUP file loading with committed fixture
print("\nTesting CUP file loading with fixture...")
fixture_path = os.path.join(os.path.dirname(__file__), "vero_beach_test.cup")
assert os.path.exists(fixture_path), (
    f"Test fixture missing: {fixture_path}. "
    "Ensure vero_beach_test.cup is committed to the repository."
)
with open(fixture_path, "r", encoding="utf-8") as f:
    fixture_content = f.read()
from app import parse_cup_file

spots = parse_cup_file(fixture_content)
assert len(spots) > 0, "No landing spots loaded from fixture file"
assert "name" in spots[0], "Landing spot missing 'name' field"
assert "lat" in spots[0], "Landing spot missing 'lat' field"
assert "lon" in spots[0], "Landing spot missing 'lon' field"
print(f"✓ CUP file loading works: loaded {len(spots)} spots from vero_beach_test.cup")

# Test map bounds calculation
print("\nTesting map bounds calculation...")
bounds = calculate_map_bounds(spots)
assert bounds is not None, "Bounds should not be None for valid spots"
assert isinstance(bounds, list) and len(bounds) == 2, "Bounds should be [[sw], [ne]]"
assert len(bounds[0]) == 2 and len(bounds[1]) == 2, "Each corner should have [lat, lon]"
# Verify bounds format: [[min_lat, min_lon], [max_lat, max_lon]]
assert bounds[0][0] < bounds[1][0], "South lat should be less than north lat"
assert bounds[0][1] < bounds[1][1], "West lon should be less than east lon"
print(f"✓ Map bounds calculation works: SW={bounds[0]}, NE={bounds[1]}")

# Test app structure
print("\nTesting app structure...")
from app import app

assert app is not None, "App not initialized"
assert hasattr(app, "layout"), "App has no layout"
print("✓ App structure is valid")

print("\n✅ All tests passed!")
print("\nTo run the application:")
print("  python app.py")
print("\nThen open http://localhost:8050 in your browser")
print("\nNew features:")
print("  - Default CUP file loaded on startup")
print("  - Map automatically recenters when CUP file is loaded")
