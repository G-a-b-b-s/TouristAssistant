const form = document.getElementById('formularz');
document.getElementById('touristTypeForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const responses = new FormData(this);
    const scores = {cultural: 0, sport: 0, entertainment: 0};

    // Count responses
    for (let value of responses.values()) {
        scores[value]++;
    }

    // Determine the tourist type with the highest score
    const maxType = Object.keys(scores).reduce((a, b) => scores[a] > scores[b] ? a : b);

    // Message based on the result
    let resultMessage = '';
    if (maxType === 'cultural') {
        resultMessage += 'Twój profil to: Kulturalny. Lubisz zwiedzać i poznawać historię.';
    } else if (maxType === 'sport') {
        resultMessage += 'Twój profil to: Sportowy. Aktywność fizyczna to Twoja pasja.';
    } else if (maxType === 'entertainment') {
        resultMessage += 'Twój profil to: Rozrywkowy. Życie nocne i zabawa to Twój żywioł.';
    }

    form.innerHTML += `<p>${resultMessage}</p>`;

    // Update dataState in localStorage
    const dataState = JSON.parse(localStorage.getItem('dataState')) || {};
    dataState.survey = true;
    localStorage.setItem('dataState', JSON.stringify(dataState));

    // Send the data to the server using Fetch API
    // Send the data to the server using Fetch API
    const formData = {touristType: maxType}; // Ensure key is 'touristType'
    fetch('/save-survey-data', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(formData),
    })
        .then(response => response.json())
        .then(data => {
            alert('Dziękujemy za wypełnienie formularza! Twoje dane zostały zapisane.');
            window.location.href = '/formSelectDataOrigin';
        })
        .catch(error => {
            alert('Dziękujemy za wypełnienie formularza! Twoje dane zostały zapisane.');
            console.error('Error:', error);
        });
});