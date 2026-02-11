        const sterling = L.latLng(42.426, -71.793);
        const map = L.map('map').setView(sterling, 8);

        const tiles = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
            maxZoom: 18,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
                'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            id: 'mapbox/streets-v11',
            tileSize: 512,
            zoomOffset: -1
        }).addTo(map);


        // Control 2: This add a scale to the map
        L.control.scale().addTo(map);

        // Control 3: This add a Search bar
        const searchControl = L.esri.Geocoding.geosearch().addTo(map);

        const results = new L.LayerGroup().addTo(map);

        searchControl.on('results', function (data) {
            results.clearLayers();
            for (let i = data.results.length - 1; i >= 0; i--) {
                results.addLayer(L.marker(data.results[i].latlng));
            }
        });


        let glideRatio = parseFloat(document.getElementById('glideRatioInput').value);
        let altitude = parseFloat(document.getElementById('altitudeInput').value);
        let arrivalHeight = parseFloat(document.getElementById('arrivalHeightInput').value);

        // Updates the radius of the circle for every landing spot using the parameters read from the form
        function drawLandingSpots(e) {
            let glideRatio = parseFloat(document.getElementById('glideRatioInput').value);
            let altitude = parseFloat(document.getElementById('altitudeInput').value);
            let arrivalHeight = parseFloat(document.getElementById('arrivalHeightInput').value);

            // Validate inputs
            if (isNaN(glideRatio) || glideRatio <= 0 || glideRatio > 100) {
                showError('Glide ratio must be between 1 and 100');
                return;
            }
            if (isNaN(altitude) || altitude < 0 || altitude > 50000) {
                showError('Altitude must be between 0 and 50,000 feet');
                return;
            }
            if (isNaN(arrivalHeight) || arrivalHeight < 0 || arrivalHeight > 10000) {
                showError('Arrival height must be between 0 and 10,000 feet');
                return;
            }
            if (arrivalHeight >= altitude) {
                showError('Arrival height must be less than altitude');
                return;
            }

            let inputElements = document.getElementsByClassName('messageCheckbox');
            let airport = inputElements[0].checked;
            let grassStrip = inputElements[1].checked;
            let landable = inputElements[2].checked;

            for (let a of landingSpots) {
                a.circle.removeFrom(map);

                let radius = glideRatio * (altitude - arrivalHeight - a.elevation);
                radius = Math.max(1.0, radius);
                a.circle.setRadius(feetToMeters(radius));

                if ((a.style == OUTLANDING && landable) ||
                    (a.style == GRASS_SURFACE && grassStrip) ||
                    (a.style == AIRPORT && airport) ||
                    (a.style == GLIDING_AIRFIELD && airport)) {
                    a.circle.addTo(map);
                }
            }
        }

        function feetToMeters(feet) {
            // one foot is exactly 0.3048 meters
            return feet * 0.3048;
        }

        function metersToFeet(meters) {
            return meters / 0.3048;
        }

        // Display error message to user
        function showError(message) {
            const statusElement = document.getElementById('fileStatus');
            if (statusElement) {
                statusElement.textContent = '❌ Error: ' + message;
                statusElement.style.color = 'red';
                setTimeout(() => {
                    statusElement.textContent = '';
                }, 5000);
            }
        }

        // Display success message to user
        function showSuccess(message) {
            const statusElement = document.getElementById('fileStatus');
            if (statusElement) {
                statusElement.textContent = '✓ ' + message;
                statusElement.style.color = 'green';
                setTimeout(() => {
                    statusElement.textContent = '';
                }, 3000);
            }
        }

        // map.on('click', onMapClick);

        let landingSpots = [];

        const myForm = document.getElementById("myForm");
        const csvFile = document.getElementById("csvFile");
        const GRASS_SURFACE = 2;
        const OUTLANDING = 3;
        const GLIDING_AIRFIELD = 4;
        const AIRPORT = 5;

        // Loads the CUP file when the "Load File" button is clicked.
        // Note that the CUP file format is a valid CSV file.
        myForm.addEventListener('change', loadCupFile);
        myForm.addEventListener("submit", loadCupFile);

        glideParameters.addEventListener('change', drawLandingSpots);

        function loadCupFile(e) {
            e.preventDefault();

            glideRatio = parseFloat(document.getElementById('glideRatioInput').value);
            altitude = parseFloat(document.getElementById('altitudeInput').value);
            arrivalHeight = parseFloat(document.getElementById('arrivalHeightInput').value);

            const input = csvFile.files[0];
            
            // Validate file is selected
            if (!input) {
                showError('Please select a CUP file');
                return;
            }

            // Validate file size (max 5MB)
            const maxSize = 5 * 1024 * 1024; // 5MB
            if (input.size > maxSize) {
                showError('File is too large. Maximum size is 5MB');
                return;
            }

            // Validate file extension
            if (!input.name.toLowerCase().endsWith('.cup')) {
                showError('Please select a valid CUP file');
                return;
            }

            const reader = new FileReader();

            let yellowOptions = { color: 'black', fillColor: 'yellow', opacity: 1, fillOpacity: 1 };
            let blueOptions = { color: 'black', fillColor: 'blue', opacity: 1, fillOpacity: 1 };
            let greenOptions = { color: 'black', fillColor: 'green', opacity: 1, fillOpacity: 1 };

            reader.onerror = function() {
                showError('Failed to read file. Please try again.');
            };

            reader.onload = function (e) {
                try {
                    const allText = e.target.result;

                    // delete tasks
                    let taskLocation = allText.indexOf("-----Related Tasks-----");

                    // correct taskLocation if string not found, or other error producing NaN or undefined
                    taskLocation = (~taskLocation) ? taskLocation : allText.length;

                    // parse the CUP file (which is formatted as a CSV file)
                    let result = $.csv.toObjects(allText.substring(0, taskLocation));

                    if (!result || result.length === 0) {
                        showError('No waypoints found in file');
                        return;
                    }

                    // Clear existing landing spots
                    for (let spot of landingSpots) {
                        if (spot.circle) {
                            spot.circle.removeFrom(map);
                        }
                    }
                    landingSpots = [];

                    let addedCount = 0;

                // add landables first
                for (let row of result) {
                    if (row.style == OUTLANDING) {
                        try {
                            let a = new LandingSpot(row, yellowOptions);
                            if (a.circle) {
                                landingSpots.push(a);
                                addedCount++;
                            }
                        } catch (err) {
                            // Skip invalid waypoints
                        }
                    }
                }

                // airports with grass surface will be layered above landable fields
                for (let row of result) {
                    if (row.style == GRASS_SURFACE) {
                        try {
                            let a = new LandingSpot(row, blueOptions);
                            if (a.circle) {
                                landingSpots.push(a);
                                addedCount++;
                            }
                        } catch (err) {
                            // Skip invalid waypoints
                        }
                    }
                }

                // load ordinary airports last so they will be layered above all others
                for (let row of result) {
                    if (row.style == GLIDING_AIRFIELD || row.style == AIRPORT) {
                        try {
                            let a = new LandingSpot(row, greenOptions);
                            if (a.circle) {
                                landingSpots.push(a);
                                addedCount++;
                            }
                        } catch (err) {
                            // Skip invalid waypoints
                        }
                    }
                }

                if (addedCount === 0) {
                    showError('No valid waypoints found in file');
                    return;
                }

                // Draw the landing spots according to the selected check boxes
                drawLandingSpots();
                showSuccess(`Loaded ${addedCount} waypoint${addedCount !== 1 ? 's' : ''}`);
            } catch (err) {
                showError('Failed to parse file: ' + err.message);
            }
            };

            // Parses an entry in a CUP file.
            function LandingSpot(csvRecord, options) {
                if (!csvRecord || !csvRecord.name || !csvRecord.lat || !csvRecord.lon || !csvRecord.elev) {
                    throw new Error('Invalid waypoint data');
                }

                this.name = csvRecord.name;
                this.style = csvRecord.style;

                // Parse elevation
                if (csvRecord.elev.endsWith("ft")) {
                    this.elevation = Number(csvRecord.elev.substr(0, csvRecord.elev.length - 2));
                }
                else if (csvRecord.elev.endsWith("m")) {
                    this.elevation = metersToFeet(Number(csvRecord.elev.substr(0, csvRecord.elev.length - 1)));
                }
                else {
                    throw new Error('Invalid elevation format');
                }

                if (isNaN(this.elevation)) {
                    throw new Error('Invalid elevation value');
                }

                // Parse latitude
                let s = csvRecord.lat;
                if (!s || s.length < 8) {
                    throw new Error('Invalid latitude format');
                }
                let degrees = Number(s.substring(0, 2));
                let minutes = Number(s.substring(2, 8));
                let sign = s.endsWith("N") ? 1 : -1;
                let lat = sign * (degrees + minutes / 60.0);

                // Parse longitude
                s = csvRecord.lon;
                if (!s || s.length < 9) {
                    throw new Error('Invalid longitude format');
                }
                degrees = Number(s.substring(0, 3));
                minutes = Number(s.substring(3, 9));
                sign = s.endsWith("E") ? 1 : -1;
                let lon = sign * (degrees + minutes / 60.0);

                if (isNaN(lat) || isNaN(lon)) {
                    throw new Error('Invalid coordinates');
                }

                this.latLng = L.latLng(lat, lon);
                let radius = glideRatio * (altitude - arrivalHeight - this.elevation);
                options.radius = feetToMeters(radius);

                if (!isNaN(radius)) {
                    this.circle = L.circle(this.latLng,
                        options).bindPopup(this.name + "<br>" + this.elevation.toFixed(0) + " ft");
                }
            }

            reader.readAsText(input);
        };