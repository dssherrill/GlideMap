# Glide Range Map

An interactive web-based tool for visualizing glider range based on altitude, glide ratio, and landing site locations. This application helps glider pilots visualize their achievable range from their current position by displaying circles on a map representing potential landing areas.

## Features

- **Interactive Map Visualization**: Uses Leaflet.js to display an interactive map with glide range circles
- **CUP File Support**: Import landing sites from SeeYou CUP files commonly used in soaring
- **Real-time Updates**: Map automatically updates when parameters change
- **Customizable Parameters**:
  - Glide Ratio (1-100)
  - Altitude MSL in feet (0-50,000 ft)
  - Arrival Height in feet (0-10,000 ft)
- **Persistent Settings**: All user inputs are saved in local storage and restored on page reload
- **Location Search**: Built-in geocoding to find and center the map on specific locations
- **Landing Site Categories**: Displays airports, grass strips, and landable fields with different markers

## Demo

You can try the live application at: [https://dssherrill.github.io/GlideRange.html](https://dssherrill.github.io/GlideRange.html)

## Usage

### Online Usage

Simply visit the [live application](https://dssherrill.github.io/GlideRange.html) in your web browser.

### Local Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/dssherrill/GlideMap.git
   cd GlideMap
   ```

2. Open `GlideRange.html` in a modern web browser

3. Adjust the glide parameters:
   - **Glide Ratio**: Your glider's glide ratio (e.g., 20:1, 30:1, etc.)
   - **Altitude MSL**: Your current altitude above mean sea level in feet
   - **Arrival Height**: Minimum safe arrival height above field elevation in feet

4. Load a CUP file containing your landing sites (optional - a default file is included)

5. The map will display circles showing your glide range to each landing site

## File Structure

```
GlideMap/
├── GlideRange.html              # Main HTML application file
├── glideRange.js                # Core JavaScript logic
├── jquery.csv.js                # CSV parsing library for CUP files
├── Sterling, Massachusetts 2021 SeeYou.cup  # Sample CUP file
├── LICENSE                      # GNU GPL v3 License
├── SECURITY_IMPROVEMENTS.md     # Documentation of security enhancements
└── README.md                    # This file
```

## CUP File Format

The application supports the SeeYou CUP waypoint file format, which is a standard format used by many soaring navigation systems. The file contains waypoint information including:
- Name
- Latitude and Longitude
- Elevation (in feet or meters)
- Landing site style (airport, grass strip, landable field)

## How It Works

The application calculates the glide range for each landing site using the following logic:

1. Takes your current altitude MSL
2. Subtracts the landing site elevation and required arrival height
3. Calculates the horizontal distance achievable using the glide ratio
4. Displays a circle on the map with radius equal to the calculated range

The circles help visualize which landing sites are within gliding distance based on your current position and altitude.

## Security Features

Version 1.1.6 includes comprehensive security improvements:
- Content Security Policy (CSP) implementation
- Updated dependencies (jQuery 3.7.1, Lodash 4.17.21)
- Subresource Integrity (SRI) for CDN resources
- Input validation and sanitization
- File upload size limits (5MB max)
- Error handling for all operations

See [SECURITY_IMPROVEMENTS.md](SECURITY_IMPROVEMENTS.md) for detailed security documentation.

## Browser Compatibility

This application requires a modern web browser with support for:
- HTML5
- CSS3
- ES6 JavaScript
- localStorage API
- File API

Tested and working on:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Technologies Used

- [Leaflet.js](https://leafletjs.com/) - Interactive mapping library
- [jQuery](https://jquery.com/) - JavaScript library
- [Lodash](https://lodash.com/) - Utility library
- [esri-leaflet-geocoder](https://github.com/Esri/esri-leaflet-geocoder) - Geocoding plugin
- [jquery-csv](https://github.com/typeiii/jquery-csv) - CSV parsing

## Version History

### Version 1.1.6
- All user inputs are saved in local storage and restored when the page initializes
- Comprehensive security improvements
- Input validation and error handling
- Accessibility improvements

### Version 1.1.5
- Simplified circle management by using LayerGroups

### Version 1.1.4
- Landing sites displayed with proper layering (airports on top)

### Version 1.1.3
- Fixed inconsistent column labels in CUP files

### Version 1.1.2
- Loads a default CUP file during initialization

### Version 1.1.1
- Removed "Load file" and "Update" buttons
- Map automatically updates when inputs change

### Version 1.1
- Fixed problem with negative radius
- Support for CUP files with elevation in feet or meters
- Improved CUP file parsing

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

Copyright (c) David S. Sherrill

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Acknowledgments

- Created by David S. Sherrill
- Uses OpenStreetMap data and tiles
- Built with open-source mapping and JavaScript libraries

## Support

For issues, questions, or suggestions, please open an issue on the [GitHub repository](https://github.com/dssherrill/GlideMap/issues).
