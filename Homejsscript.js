document.addEventListener("DOMContentLoaded", ()=> {
    const loginForm = document.querySelector("#log-in-account");
    const signupForm = document.querySelector("#sign-up-account");
    
    document.querySelector("#sign-up-form-link").addEventListener("click", e => {
        e.preventDefault();
        signupForm.classList.remove("form-hidden");
        loginForm.classList.add("form-hidden");
    });

    document.querySelector("#linkbacktologin").addEventListener("click", e => {
        e.preventDefault();
        signupForm.classList.add("form-hidden");
        loginForm.classList.remove("form-hidden");
    });


});