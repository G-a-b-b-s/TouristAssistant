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
        button.style.display = 'inline-block'; // Always make it visible
        button.disabled = !isAnyDataCollected;
    }

    // Fetch the data state from the server
    fetch('/get-data-state')
        .then(response => response.json())
        .then(dataState => {
            updateUI(dataState);
        });

    // Handle click events on links
    document.querySelectorAll('.page-link').forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault(); // Temporarily prevent navigation
            const page = this.dataset.page; // Use `this` to get the correct element
            if (page) {
                fetch('/get-data-state')
                    .then(response => response.json())
                    .then(dataState => {
                        dataState[page] = true; // Update the clicked page state
                        fetch('/save-data-state', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(dataState),
                        }).then(() => {
                            updateUI(dataState);
                            // Navigate to the page after saving the state
                            window.location.href = this.href; // Use the `href` attribute of the link
                        });
                    });
            }
        });
    });
});
