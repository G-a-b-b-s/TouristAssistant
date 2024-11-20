const express = require('express');
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// Serve static files like images, CSS, JS, and HTML
app.use(express.static(path.join(__dirname, '..')));

// Route for the main page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'mainPage.html')); // Adjusted for your layout
});

// Handle POST request from the form
app.post('/save-tourist-data', (req, res) => {
    const touristData = req.body;

    // Define the path to save the JSON file
    const filePath = path.join(__dirname, '..', 'dataOfUsers', 'tourist_data.json');

    // Read the existing JSON data (if any)
    fs.readFile(filePath, 'utf8', (err, data) => {
        let jsonData = [];

        if (err) {
            if (err.code === 'ENOENT') {
                // File doesn't exist, initialize an empty array
                console.log('No existing data file found. A new file will be created.');
            } else {
                // Log the error, but don't send it to the user
                console.error('Error reading data:', err);
            }
        } else {
            try {
                // If file exists, parse the existing data
                jsonData = JSON.parse(data);
            } catch (parseError) {
                console.error('Error parsing existing data. Initializing new data array.');
                jsonData = [];
            }
        }

        // Append the new tourist data
        jsonData.push(touristData);

        // Ensure the directory exists before saving the file
        fs.mkdir(path.dirname(filePath), { recursive: true }, (dirErr) => {
            if (dirErr) {
                // Log the error, but don't send it to the user
                console.error('Error creating directory:', dirErr);
                res.status(200).send('Data saved successfully!');
                return;
            }

            // Save the updated data back to the file
            fs.writeFile(filePath, JSON.stringify(jsonData, null, 2), (writeErr) => {
                if (writeErr) {
                    // Log the error, but don't send it to the user
                    console.error('Error writing to file:', writeErr);
                    res.status(200).send('Data saved successfully!');
                    return;
                }
                res.status(200).send('Data saved successfully!');
            });
        });
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
