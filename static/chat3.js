document.getElementById("predict-button").addEventListener("click", function(event) {
    const symptoms = document.getElementById("symptoms").value;
    const imageFile = document.getElementById("image").files[0];

    if (!symptoms && !imageFile) {
        alert("Please enter symptoms or upload an image.");
        event.preventDefault();
    }
});
