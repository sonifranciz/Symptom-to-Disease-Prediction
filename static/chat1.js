function validateLogin() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const digitRegex = /\d/;
    const lowercaseRegex = /[a-z]/;
    const uppercaseRegex = /[A-Z]/;
  
    
    
    if (!email || email.indexOf('@') === -1) {
        alert("Please enter a valid email address.");
        return false; // Prevent form submission
    }

    
    if (password.length < 8 || !digitRegex.test(password) || !lowercaseRegex.test(password) || !uppercaseRegex.test(password)) {
        alert("Enter a valid password")    
        return false;
    // Check if the password is empty or doesn't meet specific criteria
    
    }
    

    return  window.location.href = "chat3.html";
        
            // Redirect to the next page (e.g., dashboard.html)
    
    
        
    
}
