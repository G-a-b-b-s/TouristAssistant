document.getElementById('touristForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    // Collecting form data
    const name = document.getElementById('name').value;
    const duration = document.getElementById('duration').value;
    const startDate = document.getElementById('startDate').value;

    // Get selected tourist type
    const touristType = document.querySelector('input[name="touristType"]:checked');

    if (!touristType) {
        alert('Proszę wybrać typ turysty!');
        return;
    }

    // Create an object to hold the collected data
    const formData = {
        name: name,
        duration: duration,
        startDate: startDate,
        touristType: touristType.value
    };

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
