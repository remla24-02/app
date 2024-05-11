function sendRequest() {
    const inputURL = document.getElementById("inputURL").value;

    // Make a POST request to your Django backend
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
        // Display appropriate div based on response
        if (data.safe) {
            document.getElementById("result").innerHTML = '<div class="green-box"></div>';
        } else {
            document.getElementById("result").innerHTML = '<div class="red-box"></div>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
