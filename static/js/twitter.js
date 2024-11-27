button = document.getElementById("submitBtn");
console.log(button);
button.addEventListener("click", () => {
    const username = document.getElementById("username").value;
    console.log("Username entered:", username);

    fetch('/save-username-twitter', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username })
    })
    .then(response => {
        console.log("Response status:", response.status);
        return response.text();
    })
    .then(data => {
        console.log("Response data:", data); // Log the response data
        alert(data);
    })
    .catch(error => {
        console.error('Error:', error); // Log any errors
        alert('An error occurred. Check the console for details.');
    });
});