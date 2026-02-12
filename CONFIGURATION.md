# Configuration Guide

This document explains how to configure the GlideMap application, including how to update API tokens and other settings.

## Table of Contents
- [Mapbox API Token](#mapbox-api-token)
- [Default Landing Sites File](#default-landing-sites-file)
- [Map Settings](#map-settings)

## Mapbox API Token

### Where is the Mapbox Token Stored?

The Mapbox API access token is currently stored directly in the `glideRange.js` file at **line 234**.

**Location:** `/glideRange.js` (line 234)

```javascript
let tiles = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=YOUR_TOKEN_HERE', {
```

### How to Update the Mapbox Token

To update the Mapbox API access token:

1. **Obtain a Mapbox Access Token:**
   - Go to [mapbox.com](https://www.mapbox.com/)
   - Sign in or create a free account
   - Navigate to your [Account page](https://account.mapbox.com/)
   - Go to the "Access tokens" section
   - Either use an existing token or create a new one
   - Copy the token (it will start with `pk.`)

2. **Update the Token in the Code:**
   - Open the `glideRange.js` file in a text editor
   - Navigate to line 234 (or search for `access_token=`)
   - Replace the existing token with your new token:
     ```javascript
     let tiles = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.YOUR_NEW_TOKEN_HERE', {
     ```
   - Save the file

3. **Test the Changes:**
   - Open `GlideRange.html` in your web browser
   - Verify that the map tiles load correctly
   - If the map doesn't load, check your browser's console for errors

### Why is the Token Hardcoded?

This is a client-side web application that runs entirely in the browser. For static GitHub Pages deployment, the token needs to be embedded in the code. 

**Important Security Notes:**
- Mapbox tokens used for map tiles are designed to be public and included in client-side code
- The token should have appropriate restrictions configured in your Mapbox account
- You can restrict the token to specific URLs (e.g., `https://dssherrill.github.io/*`)
- Mapbox provides usage monitoring and rate limiting to prevent abuse
- **Do not use a secret access token** - use only public tokens intended for client-side use

### Configuring Token Restrictions (Recommended)

To secure your Mapbox token:

1. Log in to your [Mapbox account](https://account.mapbox.com/)
2. Go to your Access Tokens
3. Click on the token you're using
4. Add URL restrictions:
   - For GitHub Pages: `https://dssherrill.github.io/*`
   - For local development: `http://localhost:*` or `file:///*`
5. Enable only the scopes needed (typically just `styles:read` for map tiles)
6. Set up usage alerts to monitor token usage

## Default Landing Sites File

The application loads a default CUP file on startup: `Sterling, Massachusetts 2021 SeeYou.cup`

### Changing the Default CUP File

To change which CUP file loads by default:

1. Open `glideRange.js`
2. Find the initialization code (around line 635-645)
3. Look for:
   ```javascript
   fetch('Sterling, Massachusetts 2021 SeeYou.cup')
   ```
4. Replace the filename with your desired CUP file
5. Ensure the new CUP file is in the same directory as `GlideRange.html`

## Map Settings

You can customize various map settings in `glideRange.js`:

### Map Style

To change the Mapbox map style (line 238):
```javascript
id: 'mapbox/streets-v11',  // Change to: satellite-v9, outdoors-v11, light-v10, dark-v10
```

Available Mapbox styles:
- `mapbox/streets-v11` - Street map (default)
- `mapbox/satellite-v9` - Satellite imagery
- `mapbox/outdoors-v11` - Outdoor/terrain map
- `mapbox/light-v10` - Light theme
- `mapbox/dark-v10` - Dark theme

### Maximum Zoom Level

Change the maximum zoom level (line 235):
```javascript
maxZoom: 18,  // Range: 0-22 (higher = more detailed)
```

### Initial Map View

Set the default map center and zoom (around lines 215-220):
```javascript
let map = L.map('map').setView([42.3601, -71.0589], 8);  // [latitude, longitude], zoom
```

### Default Glide Parameters

Default values are defined at the top of `glideRange.js` (lines 1-11):
```javascript
const GLIDE_RATIO_DEFAULT = 20;        // Default glide ratio
const ALTITUDE_DEFAULT = 3500;         // Default altitude MSL in feet
const ARRIVAL_HEIGHT_DEFAULT = 1000;   // Default arrival height in feet
```

## Deployment Configuration

When deploying changes with a new Mapbox token to GitHub Pages:

1. Update the token in `glideRange.js`
2. Commit and push to the `main` branch
3. The GitHub Actions workflow will automatically deploy to GitHub Pages
4. Verify the map loads correctly at https://dssherrill.github.io/GlideRange.html

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## Troubleshooting

### Map Doesn't Load
- **Check the browser console** for errors
- **Verify the token** is correctly formatted (starts with `pk.`)
- **Check token restrictions** in your Mapbox account
- **Verify token is active** and not expired
- **Check usage limits** - free tier has monthly request limits

### Token Errors in Console
Common errors:
- `401 Unauthorized` - Token is invalid or expired
- `403 Forbidden` - Token doesn't have required permissions or URL restrictions block access
- Rate limit errors - You've exceeded your usage quota

### Need Help?
- Check the [Mapbox documentation](https://docs.mapbox.com/)
- Open an issue on the [GitHub repository](https://github.com/dssherrill/GlideMap/issues)
- Verify your token at [Mapbox Account](https://account.mapbox.com/)

## Additional Resources

- [Mapbox Documentation](https://docs.mapbox.com/)
- [Mapbox GL JS API](https://docs.mapbox.com/mapbox-gl-js/api/)
- [Leaflet Documentation](https://leafletjs.com/reference.html)
- [How to Secure Your Mapbox Token](https://docs.mapbox.com/help/troubleshooting/how-to-use-mapbox-securely/)
