document.addEventListener('DOMContentLoaded', function () {
    const resultsPlaceholder = document.getElementById('resultingType');
    const descriptionPlaceholder = document.getElementById('description');
    let chatbotData = {};
    let instagramData = {};
    let surveyData = {};

     // Function to determine the tourist type
    function determineTouristType(chatbotData, instagramData, surveyData) {
        // Count the number of responses for each type
        const scores = {cultural: 0, sport: 0, entertainment: 0};

         if (surveyData.type) {
            scores[surveyData.type] += 2; // weight 2
        }
        if (chatbotData.type) {
            scores[chatbotData.type]++;
        }
        if (instagramData.type) {
            scores[instagramData.type]++;
        }

        // Determine the tourist type with the highest score
        const maxType = Object.keys(scores).reduce((a, b) => scores[a] > scores[b] ? a : b);

        // Message based on the result
        let resultMessage = '';
        let description = '';
        if (maxType === 'cultural') {
            resultMessage += 'Kulturalny'
            description+= 'Lubisz zwiedzać i poznawać historię.';
        } else if (maxType === 'sport') {
            resultMessage += 'Sportowy'
            description += 'Aktywność fizyczna to Twoja pasja.';
        } else if (maxType === 'entertainment') {
            resultMessage += 'Rozrywkowy'
            description+='Życie nocne i zabawa to Twój żywioł.';
        }
        resultsPlaceholder.innerHTML = `<p>${resultMessage}</p>`;
        descriptionPlaceholder.innerHTML = `<p>${description}</p>`;

    }


    // Fetch the Instagram data from the server
    fetch('/get-chatbot-data')
        .then(response => response.json())
        .then(data => {
            chatbotData = data;
        });
    // Fetch the Instagram data from the server
    fetch('/get-instagram-data')
        .then(response => response.json())
        .then(data => {
            instagramData = data;
        });

    // Fetch the survey data from the server
    fetch('/get-survey-data')
        .then(response => response.json())
        .then(data => {
            surveyData = data;

        });
    determineTouristType(chatbotData, instagramData, surveyData);
});