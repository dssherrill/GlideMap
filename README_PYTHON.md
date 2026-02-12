# Glide Range Map - Python Dash Bootstrap Version

A Python Dash Bootstrap version of the Glide Range Map web application. This interactive tool helps glider pilots visualize their achievable range from their current position by displaying circles on a map representing potential landing areas.

## Features

- **Interactive Map Visualization**: Uses Dash Leaflet to display an interactive map with glide range circles
- **CUP File Support**: Import landing sites from SeeYou CUP files commonly used in soaring
- **Real-time Updates**: Map automatically updates when parameters change
- **Bootstrap UI**: Modern, responsive interface using Dash Bootstrap Components
- **Customizable Parameters**:
  - Glide Ratio (1-100)
  - Altitude MSL in feet (0-50,000 ft)
  - Arrival Height in feet (0-10,000 ft)
- **Landing Site Categories**: Displays airports, grass strips, and landable fields with different colored circles
  - Green: Airports and gliding airfields
  - Blue: Grass strips
  - Yellow: Landable fields

## Requirements

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/dssherrill/GlideMap.git
   cd GlideMap
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:8050
   ```

3. Adjust the glide parameters:
   - **Glide Ratio**: Your glider's glide ratio (e.g., 20:1, 30:1, etc.)
   - **Altitude MSL**: Your current altitude above mean sea level in feet
   - **Arrival Height**: Minimum safe arrival height above field elevation in feet

4. Load a CUP file containing your landing sites by clicking the "Upload CUP File" button

5. The map will display circles showing your glide range to each landing site

## CUP File Format

The application supports the SeeYou CUP waypoint file format, which is a standard format used by many soaring navigation systems. The file contains waypoint information including:
- Name
- Latitude and Longitude
- Elevation (in feet or meters)
- Landing site style (airport, grass strip, landable field)

A sample CUP file is included: `Sterling, Massachusetts 2021 SeeYou.cup`

## How It Works

The application calculates the glide range for each landing site using the following logic:

1. Takes your current altitude MSL
2. Subtracts the landing site elevation and required arrival height
3. Calculates the horizontal distance achievable using the glide ratio
4. Displays a circle on the map with radius equal to the calculated range

The circles help visualize which landing sites are within gliding distance based on your current position and altitude.

## Project Structure

```
GlideMap/
├── app.py                                        # Main Python Dash application
├── requirements.txt                              # Python dependencies
├── Dockerfile                                    # Docker configuration
├── .dockerignore                                 # Docker ignore file
├── .gitignore                                    # Git ignore file for Python
├── test_app.py                                   # Unit tests
├── Sterling, Massachusetts 2021 SeeYou.cup       # Sample CUP file
├── README_PYTHON.md                              # This file
├── QUICKSTART.md                                 # Quick start guide
└── [Original JavaScript/HTML files...]           # Original web app files
```

## Differences from JavaScript Version

This Python Dash Bootstrap version provides the same core functionality as the original JavaScript version, with some differences:

- **Modern Python Framework**: Built with Dash and Dash Bootstrap Components
- **Server-side Processing**: All calculations happen on the server
- **No Local Storage**: Settings are not persisted between sessions (can be added if needed)
- **OpenStreetMap Tiles**: Uses free OpenStreetMap tiles instead of Mapbox
- **Simplified UI**: Streamlined interface with Bootstrap styling

## Technologies Used

- [Dash](https://dash.plotly.com/) - Python web framework
- [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) - Bootstrap components for Dash
- [Dash Leaflet](https://dash-leaflet.herokuapp.com/) - Interactive mapping for Dash
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [NumPy](https://numpy.org/) - Numerical computing

## Development

To run in development mode with auto-reload:

```bash
python app.py
```

The application will run on `http://localhost:8050` with debug mode enabled.

## Deployment

### Local Network

To make the app accessible on your local network:

```bash
python app.py
```

The app will be accessible at `http://<your-ip>:8050`

### Production Deployment

For production deployment, consider using:

- **Gunicorn** (Linux/Mac):
  ```bash
  gunicorn app:server -b 0.0.0.0:8050
  ```
  Note: Gunicorn is already included in requirements.txt

- **Waitress** (Windows-friendly):
  ```bash
  pip install waitress
  waitress-serve --host=0.0.0.0 --port=8050 app:server
  ```

- **Docker**: A Dockerfile is included in the repository
  ```bash
  # Build the image
  docker build -t glidemap-dash .
  
  # Run the container
  docker run -p 8050:8050 glidemap-dash
  ```

- **Cloud Platforms**: Deploy to Heroku, AWS, Azure, or Google Cloud
  - The included `Dockerfile` makes deployment easy on any container platform
  - For Heroku, use the Heroku Python buildpack
  - For AWS, use Elastic Beanstalk or ECS
  - For Azure, use App Service or Container Instances

## Browser Compatibility

This application works in all modern web browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Security Features

- Input validation for all parameters
- File upload size limits (handled by Dash)
- Safe CSV parsing with error handling
- No execution of user-provided code

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

Copyright (c) David S. Sherrill

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Acknowledgments

- Created by David S. Sherrill
- Based on the original JavaScript version of Glide Range Map
- Uses OpenStreetMap data and tiles
- Built with open-source Python and JavaScript libraries

## Support

For issues, questions, or suggestions, please open an issue on the [GitHub repository](https://github.com/dssherrill/GlideMap/issues).

## Original Version

This is a Python port of the original JavaScript/HTML version. The original version can be found at:
- Repository: [https://github.com/dssherrill/GlideMap](https://github.com/dssherrill/GlideMap)
- Live Demo: [https://dssherrill.github.io/GlideRange.html](https://dssherrill.github.io/GlideRange.html)
