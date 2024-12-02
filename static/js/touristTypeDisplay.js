document.addEventListener('DOMContentLoaded', function () {
    const instagramDataPlaceholder = document.getElementById('instagramData');
    const surveyDataPlaceholder = document.getElementById('surveyData');

    // Function to display session data
    function displaySessionData(data, placeholder) {
        text = JSON.stringify(data, null, 2);
        if (text && text !== '{}') {
            placeholder.textContent = text;
        } else {
            placeholder.textContent = '';
        }
    }

    // Fetch the Instagram data from the server
    fetch('/get-instagram-data')
        .then(response => response.json())
        .then(data => {
            displaySessionData(data, instagramDataPlaceholder);
        });

    // Fetch the survey data from the server
    fetch('/get-survey-data')
        .then(response => response.json())
        .then(data => {
            displaySessionData(data, surveyDataPlaceholder);
        });
});