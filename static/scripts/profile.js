let navLinks = document.querySelectorAll(".sidebar .sidenav a.nav-link");
let sections = document.querySelectorAll(".main section");

// Function to activate the clicked link and store in localStorage
const setActiveLink = (id) => {
    navLinks.forEach(link => {
        link.classList.remove("active");
        let img = link.querySelector("img");
        if (img) img.classList.remove("active");
    });

    let activeLink = document.querySelector(`.sidenav a[href="#${id}"]`);
    if (activeLink) {
        activeLink.classList.add("active");
        let img = activeLink.querySelector("img");
        if (img) img.classList.add("active");
    }

    // Store active section ID
    localStorage.setItem("activeSection", id);
};

// Add click event listeners to navigation links
navLinks.forEach(link => {
    link.addEventListener("click", (event) => {
        event.preventDefault(); // Prevent default anchor jump
        let targetId = link.getAttribute("href").substring(1);
        let targetSection = document.getElementById(targetId);
        
        if (targetSection) {
            targetSection.scrollIntoView({ behavior: "smooth" });
            setActiveLink(targetId);
        }
    });
});

// Restore active section after refresh
document.addEventListener("DOMContentLoaded", () => {
    let savedSection = localStorage.getItem("activeSection");
    if (savedSection) {
        let targetSection = document.getElementById(savedSection);
        if (targetSection) {
            targetSection.scrollIntoView(); // Keep the position after refresh
            setActiveLink(savedSection);
        }
    }
});

//  ----------------------------  ---------------------------------------------//

// document.addEventListener("DOMContentLoaded", function () {
//     const navLinks = document.querySelectorAll(".sidenav a");

//     // Load active state from localStorage
//     const activePage = localStorage.getItem("activeNav");
//     if (activePage) {
//         const activeLink = document.querySelector(`.sidenav a[href="${activePage}"]`);
//         if (activeLink) {
//             activateNavItem(activeLink);
//         }
//     }

//     navLinks.forEach(link => {
//         link.addEventListener("click", function () {
//             activateNavItem(this);
//             localStorage.setItem("activeNav", this.getAttribute("href")); // Save active item
//         });
//     });

//     function activateNavItem(selectedLink) {
//         navLinks.forEach(link => link.classList.remove("active")); // Remove from all
//         selectedLink.classList.add("active"); // Add to clicked one
//     }
// });


//  ---------------------------- Profile image submit form ---------------------------------------------//

function previewAndSubmit() {
    var input = document.getElementById('profileUpload');
    var profilePicture = document.getElementById('profilePicture');

    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            profilePicture.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
        input.form.submit();  // Auto-submit form after selecting an image
    }
}