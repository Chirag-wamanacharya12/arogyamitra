document.addEventListener("DOMContentLoaded", function () {
    const secureTransaction = document.getElementById("secureTransaction");
    const tooltip = document.getElementById("tooltip");
    const closeButton = document.querySelector(".close-btn");

    // Show tooltip on click
    secureTransaction.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent default anchor behavior
        event.stopPropagation(); // Stop event from bubbling up
        tooltip.style.display = tooltip.style.display === "block" ? "none" : "block";
    });

    // Close tooltip when close button is clicked
    closeButton.addEventListener("click", function (event) {
        event.stopPropagation(); // Prevent closing when clicking the button itself
        tooltip.style.display = "none";
    });

    // Close tooltip when clicking outside
    document.addEventListener("click", function (event) {
        if (!secureTransaction.contains(event.target) && !tooltip.contains(event.target)) {
            tooltip.style.display = "none";
        }
    });
});
