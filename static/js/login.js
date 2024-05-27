// Login function

function sendLogin() {

    // Declare Username variable
    let username = document.getElementById("username");

    // Declare Password variable
    let password = document.getElementById("password");

    // Declare JSON dictionary and add the values
    let json_dict = {
        'Username': username.value,
        'Password': password.value,
    }

    // Set request options
    let requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(json_dict)
    }

    // Send post request
    fetch('/login', requestOptions)

        // Process return object
        .then(response => {
            return response.json()

                // Access JSON info
                .then(data => {

                    // Grab the message
                    let message = data['Message']

                    if (message === 'Failed to Login') {
                        document.getElementById("error_message_holder").textContent = "Failed to Login"
                    }

                    if (message === 'Username does not exist') {
                        document.getElementById("error_message_holder").textContent = "Username does not exist"
                    }

                    if (message === 'Success') {
                        window.location.href = '/profile'
                    }
                })
        })
}

// Login function

function sendRegister() {

    // Declare Username variable
    let username = document.getElementById("username");

    // Declare Password variable
    let password = document.getElementById("password");

    // Declare JSON dictionary and add the values
    let json_dict = {
        'Username': username.value,
        'Password': password.value,
    }

    // Set request options
    let requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(json_dict)
    }

    // Send post request
    fetch('/register', requestOptions)

        // Process return object
        .then(response => {
            return response.json()

                // Access JSON info
                .then(data => {

                    // Grab the message
                    let message = data['Message']

                    if (message === 'Username already taken') {
                        document.getElementById("error_message_holder").textContent = "Username already taken"
                        document.getElementById("error_message_holder").style.display = 'grid'
                        document.getElementById("error_message_holder").style.justifyContent = 'center'
                    }

                    if (message === 'Username cannot be empty') {
                        document.getElementById("error_message_holder").textContent = "Username cannot be empty"
                        document.getElementById("error_message_holder").style.display = 'grid'
                        document.getElementById("error_message_holder").style.justifyContent = 'center'
                    }

                    if (message === 'Success') {
                        window.location.href = "/profile"
                    }
                })
        })
}