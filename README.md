# GlideMap

A web-based glider range calculator that visualizes reachable landing spots on an interactive map based on glide ratio, altitude, and arrival height parameters.

## Overview

GlideMap is a tool designed for glider pilots to visualize their glide range on a map. It reads CUP (SeeYou) format waypoint files and displays circles around each landing spot representing the reachable area based on configurable flight parameters.

## Features

- **Interactive Map**: Uses Leaflet.js with Mapbox tiles for smooth map navigation
- **CUP File Support**: Reads standard CUP format files with waypoint information
- **Configurable Parameters**:
  - Glide Ratio (typical values: 15-50)
  - Altitude Above Ground Level (AGL) in feet
  - Arrival Height (minimum safe altitude) in feet
- **Landing Spot Categories**:
  - Airports (green circles)
  - Grass Strips (blue circles)
  - Landable Fields (yellow circles)
  - Gliding Airfields (green circles)
- **Automatic Updates**: Map updates automatically when parameters change
- **Search Functionality**: Built-in geocoding search to navigate the map
- **Multi-unit Support**: Handles elevation data in both feet and meters

## Usage

1. Open `GlideRange.html` in a web browser
2. Click "Choose File" to load a CUP waypoint file
3. Adjust the glide ratio, altitude, and arrival height as needed
4. Use checkboxes to filter which types of landing spots to display
5. The map will automatically update to show your glide range

### Parameters Explained

- **Glide Ratio**: The distance you can glide horizontally for each unit of altitude lost (e.g., 20:1 means 20 feet forward for every 1 foot down)
- **Altitude AGL**: Your current altitude above ground level in feet
- **Arrival Height**: The minimum altitude you want to have when reaching a landing spot (safety margin)

The radius of each circle is calculated as:
```
radius = glideRatio × (altitude - arrivalHeight - fieldElevation)
```

## File Format

GlideMap supports CUP (SeeYou) format waypoint files, which are CSV files with specific columns for waypoint data including:
- Name
- Coordinates (latitude/longitude in degrees and decimal minutes)
- Elevation (in feet or meters)
- Style (airport type indicator)

## Default Location

The map is centered on Sterling, Massachusetts (42.426°N, 71.793°W) by default. Use the search box or pan the map to your desired location.

## Browser Compatibility

GlideMap requires a modern web browser with JavaScript enabled. It has been tested with:
- Chrome/Edge
- Firefox
- Safari

## Dependencies

- [Leaflet.js](https://leafletjs.com/) v1.9.4 - Interactive map library
- [jQuery](https://jquery.com/) v3.7.1 - JavaScript library
- [jQuery CSV](https://github.com/typeiii/jquery-csv) - CSV parsing
- [ESRI Leaflet](https://github.com/Esri/esri-leaflet) v0.0.1-beta.5 - Geocoding and search (using beta for compatibility)
- [ESRI Leaflet Geocoder](https://github.com/Esri/esri-leaflet-geocoder) v0.0.1-beta.5 - Geocoding control
- [Lodash](https://lodash.com/) v4.17.21 - Utility library
- [Mapbox](https://www.mapbox.com/) - Map tiles

## Version History

### Version 1.1.2
- **Code Quality Improvements**:
  - Standardized variable declarations (var → const/let)
  - Removed console.log statements from production code
  - Fixed missing variable declarations
- **Enhanced Input Validation**:
  - Added comprehensive validation for all numeric inputs
  - Added file size validation (max 5MB)
  - Added file format validation (.cup extension)
  - Added validation to ensure arrival height < altitude
  - Added real-time error/success feedback messages
- **Accessibility Enhancements**:
  - Added ARIA labels to all form inputs and checkboxes
  - Added required attributes where appropriate
  - Improved form label associations
- **Error Handling**:
  - Added try/catch blocks for file parsing
  - Added graceful handling of malformed waypoints
  - Added detailed error messages with context
  - Track and report skipped waypoints
- **Dependency Updates**:
  - Updated Leaflet to v1.9.4 (from 1.7.1)
  - Updated jQuery to v3.7.1 (from 3.3.1)
  - Kept ESRI Leaflet at v0.0.1-beta.5 for API compatibility
  - Updated Lodash to v4.17.21 (from 4.12.0)
- **Project Structure**:
  - Added package.json for dependency tracking
  - Added .gitignore file

### Version 1.1.1
- Removed "Load file" and "Update" buttons; map now automatically updates when inputs change

### Version 1.1
- Fixed problem with negative radius
- Now reads CUP files with field elevation in feet or meters
- Now discards tasks before parsing the CUP file by discarding everything that follows the "-----Related Tasks-----" line

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Safety Notice

⚠️ **Important**: This tool is for planning purposes only. Always maintain proper safety margins and follow all applicable aviation regulations. Weather conditions, wind, and other factors can significantly affect actual glide performance.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Author

Created by dssherrill
