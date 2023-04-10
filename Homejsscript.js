Zdocument.addEventListener("DOMContentLoaded", ()=> { //Function that toggles between log in and sign up forms
    const loginForm = document.querySelector("#log-in-account");
    const signupForm = document.querySelector("#sign-up-account");
    
    document.querySelector("#sign-up-form-link").addEventListener("click", e => {
        e.preventDefault(); //display sign up form
        signupForm.classList.remove("form-hidden"); //
        loginForm.classList.add("form-hidden");
    });

    document.querySelector("#linkbacktologin").addEventListener("click", e => {
        e.preventDefault(); //returns to log in form
        signupForm.classList.add("form-hidden");
        loginForm.classList.remove("form-hidden");
    });


});