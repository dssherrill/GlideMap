# Quick Start Guide

This guide will help you get started with either version of the Glide Range Map application.

## Which Version Should I Use?

### Use the **JavaScript/HTML Version** if you want:
- ✅ Simple setup with no installation required
- ✅ Runs entirely in the browser (no server needed)
- ✅ Can be deployed to GitHub Pages
- ✅ Works as a standalone HTML file

### Use the **Python Dash Version** if you want:
- ✅ Modern Python framework
- ✅ Server-side processing and control
- ✅ Bootstrap-based responsive UI
- ✅ Easy integration with Python tooling
- ✅ Extensibility with Python libraries

## JavaScript/HTML Version - Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dssherrill/GlideMap.git
   cd GlideMap
   ```

2. **Open the application**:
   - Simply double-click `GlideRange.html`
   - Or open it in any web browser

3. **That's it!** No installation required.

### Live Demo
Try it online: [https://dssherrill.github.io/GlideRange.html](https://dssherrill.github.io/GlideRange.html)

## Python Dash Version - Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dssherrill/GlideMap.git
   cd GlideMap
   ```

2. **Set up Python environment** (requires Python 3.8+):
   ```bash
   # Create a virtual environment (recommended)
   python -m venv venv
   
   # Activate it
   # On Linux/Mac:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** to:
   ```
   http://localhost:8050
   ```

6. **That's it!** The application is now running.

## Using the Application

### Both Versions Support:

1. **Adjust Glide Parameters**:
   - **Glide Ratio**: Your glider's glide ratio (e.g., 20:1, 30:1)
   - **Altitude MSL**: Your current altitude above sea level (feet)
   - **Arrival Height**: Minimum safe arrival height (feet)

2. **Upload a CUP File** (optional):
   - Click the file upload button
   - Select your SeeYou CUP waypoint file
   - The map will update with your landing sites

3. **View Glide Range**:
   - **Green circles**: Airports and gliding airfields
   - **Blue circles**: Grass strips
   - **Yellow circles**: Landable fields
   - Circle size shows maximum glide range to each site

### Sample CUP File Included
A sample file is included: `Sterling, Massachusetts 2021 SeeYou.cup`

## Common Questions

### Q: What is a CUP file?
A: CUP files are SeeYou waypoint files used by many soaring navigation systems. They contain landing site information including coordinates, elevation, and site type.

### Q: Do the circles account for terrain?
A: **No**, the range circles show theoretical glide range and do not account for blocking terrain. Always use proper aeronautical charts and planning tools for flight planning.

### Q: Can I use this for flight planning?
A: This tool is meant for visualization purposes. Always use approved flight planning tools and resources for actual flight operations.

### Q: Can I customize the map tiles?
A: Yes! 
- **JavaScript version**: Edit `glideRange.js` to change the Mapbox token or use different tile providers
- **Python version**: Edit `app.py` to use different tile URLs in the `dl.TileLayer` component

## Getting Help

- **Report issues**: [GitHub Issues](https://github.com/dssherrill/GlideMap/issues)
- **Contact**: glide@sherrill.in
- **Documentation**: 
  - [Main README](README.md)
  - [Python Version README](README_PYTHON.md)
  - [Configuration Guide](CONFIGURATION.md)
  - [Deployment Guide](DEPLOYMENT.md)

## License

Both versions are licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for details.
