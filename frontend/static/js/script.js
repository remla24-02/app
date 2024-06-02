// Update the version displayed on the frontend
fetch('/service/version')
.then(response => response.json())
.then(data => {
    // Update the <h1> element with the received data
    document.getElementById('app__version').textContent = data.version;
})
.catch(error => {
    console.error('Error:', error);
});

// Add an "Enter" listener on the url input field to fire the send request method
document.getElementById("inputURL").addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
      sendRequest();
    }
});

// Send a detection check request (when the submit button is clicked or via the listener)
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
        document.getElementById("app__result").innerHTML = `
            <h3 class="${resultClass}">${resultLine}</h3>
            <span>With your feedback we can improve our model!</span>
            <div id="result__feedback" class="result__feedback">
                <span>Was this prediction correct?</span>
                <div class="result__feedback--buttons">
                    <button class="submit-buttons correct-button" 
                        onclick="sendFeedback('${inputURL}', 'correct')">Correct</button>
                    <button class="submit-buttons incorrect-button" 
                        onclick="sendFeedback('${inputURL}', 'incorrect')">Incorrect</button>
                    <button class="submit-buttons unknown-button" 
                        onclick="sendFeedback('${inputURL}', 'unknown')">Unknown</button>
                </div>
            </div>`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function sendFeedback(url, feedback) {
    fetch('/service/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.CSRF_TOKEN
        },
        body: JSON.stringify({ url: url, feedback: feedback }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result__feedback").innerHTML =
            `<p>Thank you for your help! (Reported ${feedback})</p>`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
