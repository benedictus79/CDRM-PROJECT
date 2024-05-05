// Define decrypt function

function sendCache() {

    // Declare PSSH variable
    let pssh = document.getElementById("cache_pssh");

    // Declare JSON dictionary and add the values
    let json_dict = {
        'PSSH': pssh.value,
    }

    // Reset all the fields
    pssh.value = ''

    // Set request options
    let requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(json_dict)
    }

    // Send post request
    fetch('/cache', requestOptions)

        // Process return object
        .then(response => {
            return response.json()

                // Access JSON info
                .then(data => {

                    // Grab the message
                    let message = data['Message']

                    // Make fields visible and update with message
                    document.getElementById("cache_results").style.display = 'Grid'
                    document.getElementById("cache_results").textContent = message
                })
        })
}