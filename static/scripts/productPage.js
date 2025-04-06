
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

// ----------------------------------------------------------------------------------------------------------------------//

document.addEventListener("DOMContentLoaded", function () {
    let select = document.getElementById("quantitySelect");

    // Get the current quantity from the server-side variable
    let currentQuantity = parseInt(select.getAttribute("data-current-quantity")) || 0;
    let maxQuantity = 10;
    let availableQuantity = maxQuantity - currentQuantity;



    // Create options dynamically based on available quantity
    for (let i = 1; i <= availableQuantity; i++) {
        let option = document.createElement("option");
        option.value = i;
        option.textContent = i;
        select.appendChild(option);
    }
});


// ----------------------------------------------------------------------------------------------------------------------//


document.querySelector(".addToCartButton").addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default link behavior
    let quantity = document.getElementById("quantitySelect").value;
    let url = this.href + "?quantity=" + quantity; // Append quantity to URL
    window.location.href = url; // Redirect with quantity
});

// ------------------------------------------------------------------------------------------------------------------------//

let currentIndex = 0;
let thumbnails = document.querySelectorAll('.thumbnail img');
let images = Array.from(thumbnails).map(img => img.src);
let interval = 3000; // Change image every 3 seconds
let autoChangeTimeout;
let isPaused = false; // Track whether the slideshow is paused

function changeImage(imageUrl) {
    document.getElementById('mainImage').src = imageUrl;
    thumbnails.forEach(img => img.classList.remove('active'));
    let activeImg = [...thumbnails].find(img => img.src === imageUrl);
    if (activeImg) activeImg.classList.add('active');

    // Update index for auto-change
    currentIndex = images.indexOf(imageUrl);
}

// Function to switch to the next image automatically
function autoChangeImage() {
    if (!isPaused) {
        currentIndex = (currentIndex + 1) % images.length;
        changeImage(images[currentIndex]);
    }
    autoChangeTimeout = setTimeout(autoChangeImage, interval);
}

// Start automatic image change
autoChangeTimeout = setTimeout(autoChangeImage, interval);

// Pause on hover and resume on mouse leave
let mainImage = document.getElementById('mainImage');
mainImage.addEventListener('mouseenter', () => {
    isPaused = true;
    clearTimeout(autoChangeTimeout);
});

mainImage.addEventListener('mouseleave', () => {
    isPaused = false;
    autoChangeTimeout = setTimeout(autoChangeImage, interval);
});


// ------------------------------------------------------------------------------------------------------------------------// old
// document.addEventListener("DOMContentLoaded", function () {
//     function getAmount() {
//         let integerPart = document.getElementById("integer_part").innerText || "0";
//         let decimalPart = document.getElementById("decimal_part").innerText || "00";
//         let quantity = document.getElementById("quantitySelect").value;
//         decimalPart = decimalPart.padEnd(2, "0");  // Ensure two decimal places

//         // Calculate total price (price * quantity)
//         let price = parseFloat(integerPart + "." + decimalPart);
//         let total = price * parseInt(quantity);
        
//         return total.toFixed(2);
//     }

//     function initializePayPal() {
//         paypal.Buttons({
//             style: {
//                 layout: 'horizontal',
//                 color: 'blue',
//                 shape: 'rect',
//                 label: 'pay'
//             },
//             createOrder: function (data, actions) {
//                 let amount = getAmount();
//                 console.log(amount);
//                 if (amount === 0) {
//                     console.error("Invalid amount, order creation aborted.");
//                     return actions.reject();
//                 }
//                 return actions.order.create({
//                     purchase_units: [{
//                         amount: {
//                             currency_code: "USD",
//                             value: amount
//                         }
//                     }],
//                     status: 'PENDING'
//                 });
//             }
//         }).render('#paypal-container');
        
//     }

//     document.getElementById("custom-pay-btn").addEventListener("click", function() {
//         document.getElementById("paypal-container").style.display = "block";  
//         document.getElementById("custom-pay-btn").style.display = "none"; 
//         initializePayPal();  // Trigger PayPal UI
//     });
// });

// ------------------------------------------------------------------------------------------------------------------------// New

// document.addEventListener("DOMContentLoaded", function () {
//     function getAmount() {
//         let integerPart = document.getElementById("integer_part").innerText || "0";
//         let decimalPart = document.getElementById("decimal_part").innerText || "00";
//         let quantity = document.getElementById("quantitySelect").value;
        
//         decimalPart = decimalPart.padEnd(2, "0");
//         let price = parseFloat(integerPart + "." + decimalPart);
//         let total = price * parseInt(quantity);

//         let productInfo = document.getElementById("product_info");
//         let productID = productInfo.dataset.productId;
//         let pricingID = productInfo.dataset.pricingId;

//         return {
//             amount: total.toFixed(2),
//             productID: productID,
//             pricingID: pricingID,
//             quantity: quantity
//         };
//     }

//     function initializePayPal() {
//         paypal.Buttons({
//             style: {
//                 layout: 'horizontal',
//                 color: 'blue',
//                 shape: 'rect',
//                 label: 'pay'
//             },
//             createOrder: function (data, actions) {
//                 let { amount } = getAmount();
//                 if (amount === "0.00") {
//                     console.error("Invalid amount, order creation aborted.");
//                     return actions.reject();
//                 }
//                 return actions.order.create({
//                     purchase_units: [{
//                         amount: {
//                             currency_code: "USD",
//                             value: amount
//                         }
//                     }]
//                 });
//             },
//             onApprove: function (data, actions) {
//                 return actions.order.capture().then(function (details) {
//                     let { amount, productID, pricingID, quantity } = getAmount();

//                     fetch('/process_order/', {
//                         method: 'POST',
//                         headers: {
//                             'Content-Type': 'application/json',
//                             'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
//                         },
//                         body: JSON.stringify({
//                             orderID: data.orderID,
//                             payerID: data.payerID,
//                             transactionID: details.id,
//                             amount: amount,
//                             product_id: productID,
//                             pricing_id: pricingID,
//                             quantity: quantity
//                         })
//                     }).then(response => response.json())
//                       .then(data => {
//                           if (data.success) {
//                               alert("Payment successful and order placed!");
//                           } else {
//                               alert("Payment was successful, but there was an issue placing the order.");
//                           }
//                       })
//                       .catch(error => console.error('Error:', error));
//                 });
//             }
//         }).render('#paypal-container');
//     }

//     document.getElementById("custom-pay-btn").addEventListener("click", function() {
//         document.getElementById("paypal-container").style.display = "block";  
//         document.getElementById("custom-pay-btn").style.display = "none"; 
//         initializePayPal();
//     });
// });
