// package import
const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 9876;
const WINDOW_SIZE = 10;

let windowNumbers = [];

// Fetch numbers from the test server
async function fetchNumbers(qualifier) {
    let response;
    try {
        response = await axios.get(`http://localhost:9876/test/${qualifier}`);
        return response.data.numbers;
    } catch (error) {
        console.error('Error fetching numbers:', error);
        return [];
    }
}

// Calculate average of numbers in the window
function calculateAverage() {
    const sum = windowNumbers.reduce((acc, num) => acc + num, 0);
    return windowNumbers.length === 0 ? 0 : sum / windowNumbers.length;
}

// Middleware
app.get('/numbers/:qualifier', async (req, res) => {
    const { qualifier } = req.params;
    const numbers = await fetchNumbers(qualifier);

    // update the window state
    if (numbers.length > 0) {
        const prevWindowState = windowNumbers.slice();
        windowNumbers = [...windowNumbers.slice(-(WINDOW_SIZE - numbers.length)), ...numbers];
        const avg = calculateAverage();

        // Send response
        res.json({
            numbers,
            windowPrevState: prevWindowState,
            windowCurrState: windowNumbers,
            avg
        });
    } else {
        res.json({
            numbers: [],
            windowPrevState: windowNumbers.slice(),
            windowCurrState: windowNumbers.slice(),
            avg: calculateAverage()
        });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
