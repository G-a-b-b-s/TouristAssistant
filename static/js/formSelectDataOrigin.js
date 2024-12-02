document.addEventListener('DOMContentLoaded', function () {
    // Function to update the UI
    function updateUI(dataState) {
        // Update checkmarks
        for (const key in dataState) {
            const tickElement = document.getElementById(`${key}-tick`);
            if (dataState[key]) {
                tickElement.style.display = 'inline';
            } else {
                tickElement.style.display = 'none';
            }
        }

        // Show or hide the button
        const button = document.getElementById('checkNowButton');
        const isAnyDataCollected = Object.values(dataState).some(value => value);
        button.style.display = isAnyDataCollected ? 'inline-block' : 'none';
    }

    // Fetch the data state from the server
    fetch('/get-data-state')
        .then(response => response.json())
        .then(dataState => {
            updateUI(dataState);
        });

    // Simulate data collection on click
    document.querySelectorAll('.page-link').forEach(link => {
        link.addEventListener('click', function (event) {
            const page = event.target.dataset.page;
            if (page) {
                fetch('/get-data-state')
                    .then(response => response.json())
                    .then(dataState => {
                        dataState[page] = true; // Simulate data collection
                        fetch('/save-data-state', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify(dataState),
                        })
                        .then(() => {
                            updateUI(dataState);
                        });
                    });
            }
        });
    });
});