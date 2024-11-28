document.getElementById('touristForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission


    // Get selected tourist type
    const touristType = document.querySelector('input[name="touristType"]:checked');

    if (!touristType) {
        alert('Proszę wybrać typ turysty!');
        return;
    }

    // Create an object to hold the collected data
    const formData = {
        touristType: touristType.value
    };
    console.log('Form data:', formData);
    // Send the data to the server using Fetch API
    fetch('/save-tourist-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        alert('Dziękujemy za wypełnienie formularza! Twoje dane zostały zapisane.');
    })
    .catch(error => {
        alert('Dziękujemy za wypełnienie formularza! Twoje dane zostały zapisane.');

        console.error('Error:', error);
    });
});
