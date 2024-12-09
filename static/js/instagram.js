const button = document.getElementById("submitBtn");
const progressContainer = document.getElementById("progressContainer");
const progressBar = document.getElementById("progressBar");

button.addEventListener("click", () => {
    const username = document.getElementById("username").value;
    console.log("Username entered:", username);

    // Show the progress bar
    progressContainer.style.display = "block";

    // Simulate progress: reset to 0
    progressBar.style.width = "0%";
    progressBar.setAttribute("aria-valuenow", 0);

    // Start fetching data
    let progress = 0;
    const interval = setInterval(() => {
        progress += 10;
        progressBar.style.width = `${progress}%`;
        progressBar.setAttribute("aria-valuenow", progress);

        if (progress >= 100) {
            clearInterval(interval);
        }
    }, 100); // Update progress every 100ms

    fetch('/save-instagram-username', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username })
    })
        .then(response => {
            console.log("Response status:", response.status);

            if (response.status === 404) {
                alert('Nie znaleziono użytkownika. Spróbuj ponownie.');
                throw new Error('404 Not Found');
            } else {
                return response.json();
            }
        })
        .then(data => {
            console.log("Response data:", data);

            // Complete the progress bar
            progressBar.style.width = "100%";
            progressBar.setAttribute("aria-valuenow", 100);
            progressBar.classList.remove("progress-bar-animated");

            // Process with model

            window.location.href = '/formSelectDataOrigin';

        })
        .catch(error => {
            console.error('Error:', error);

            // Hide the progress bar in case of an error
            progressContainer.style.display = "none";

            alert('Wystąpił błąd. Sprawdź szczegóły w konsoli.');
        });
});
