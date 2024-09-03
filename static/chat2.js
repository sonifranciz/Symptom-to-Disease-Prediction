function validateCreateAccountForm() {
    const firstName = document.getElementById('first_name').value;
    const lastName = document.getElementById('last_name').value;
    const dob = document.getElementById('dob').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;

    // Check if any field is empty
    if (!firstName || !lastName || !dob || !password || !confirmPassword) {
        alert("Please fill in all the fields.");
        return false; // Prevent form submission
    }

    // Check if the password meets the specified criteria
    const passwordRegex = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}/;
    if (!passwordRegex.test(password)) {
        alert("Password must contain at least one digit, one lowercase letter, one uppercase letter, and be at least 8 characters long.");
        return false; // Prevent form submission
    }

    // Check if the password and confirm password match
    if (password !== confirmPassword) {
        alert("Passwords do not match. Please enter the same password in both fields.");
        return false; // Prevent form submission
    }

    return true; // Allow form submission
}
