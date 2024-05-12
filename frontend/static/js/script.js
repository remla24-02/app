// Update the version displayed on the frontend
fetch('/service/version')
.then(response => response.json())
.then(data => {
    // Update the <h1> element with the received data
    document.getElementById('app__header').textContent = 'URL Phishing Detection ' + data.version;
})
.catch(error => {
    console.error('Error:', error);
});

function sendRequest() {
    const inputURL = document.getElementById("inputURL").value;

    fetch('/service/detect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.CSRF_TOKEN
        },
        body: JSON.stringify({ url: inputURL }),
    })
    .then(response => response.json())
    .then(data => {
        // Prepare the correct url check results to display
        let resultClass;
        let resultLine;
        if (data.safe) {
            resultClass = "result--safe";
            resultLine = "This is a safe url! :)";
        } else {
            resultClass = "result--phishing";
            resultLine = "This is a phishing url! :(";
        }

        // Update the url check results
        document.getElementById("app__result").innerHTML = `<h3 class="${resultClass}">${resultLine}</h3>`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
