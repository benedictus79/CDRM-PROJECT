// Define decrypt function

function sendDecryption() {

    // Declare PSSH variable
    let pssh = document.getElementById("index_pssh");

    // Declare License URL variable
    let license_url = document.getElementById("license_url");

    // Declare Headers variable
    let headers = document.getElementById("headers");

    // Declare JSON variable
    let json = document.getElementById("json");

    // Declare JSON dictionary and add the values
    let json_dict = {
        'PSSH': pssh.value,
        'License URL': license_url.value,
        'Headers': headers.value,
        'JSON': json.value
    }

    // Reset all the fields
    pssh.value = ''
    license_url.value = ''
    headers.value = ''
    json.value = ''

    // Set request options
    let requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(json_dict)
    }

    // Send post request
    fetch('/', requestOptions)

        // Process return object
        .then(response => {
            return response.json()

                // Access JSON info
                .then(data => {

                    // Grab the message
                    let message = data['Message']

                    // Make fields visible and update with message
                    document.getElementById("keys_paragraph").style.display = 'Grid'
                    document.getElementById("decrypt_results").style.display = 'Grid'
                    document.getElementById("decrypt_results").textContent = message
                })
        })
}