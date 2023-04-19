
            // Get the form element
            const form = document.querySelector('form');
            
            // Add a listener for the form submission event
            form.addEventListener('submit', (event) => {
                // Prevent the default form submission behavior
                event.preventDefault();
            
                // Get the form fields values
                const name = document.getElementById('name').value;
                const email = document.getElementById('email').value;
                const seminar = document.getElementById('seminar').value;
            
                // Validate the form fields
                if (name === '' || email === '' || seminar === '') {
                    alert('Please fill out all the fields!');
                    return;
                }
            
                // Send the form data to the server
                // Replace the URL with your server endpoint
                fetch('https://example.com/register', {
                    method: 'POST',
                    body: JSON.stringify({ name, email, seminar }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    // Handle the response from the server
                    alert('Registration successful!');
                })
                .catch(error => {
                    // Handle the error from the server
                    alert('Registration failed!');
                });
            });
            
            // Add a listener for the form reset event
            form.addEventListener('reset', (event) => {
                // Confirm the user wants to cancel the registration
                if (!confirm('Are you sure you want to cancel the registration?')) {
                    event.preventDefault();
                }
            });
            
            function redirectToForm() {
                window.location.href = "your-form-url-here";
              }