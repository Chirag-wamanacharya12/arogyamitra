document.addEventListener("DOMContentLoaded", function () {
    function handleFormSubmit(event) {
        event.preventDefault();
        let form = event.target;
        let formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCSRFToken(),  // Required for Django
            },
        })
        .then(response => response.json())
        .then(data => {
            alert("Profile updated successfully!");
        })
        .catch(error => {
            alert("Error updating profile.");
            console.error(error);
        });
    }

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    document.getElementById("personalForm").addEventListener("submit", handleFormSubmit);
    document.getElementById("addressForm").addEventListener("submit", handleFormSubmit);
    document.getElementById("medicalForm").addEventListener("submit", handleFormSubmit);
});
