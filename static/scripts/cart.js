document.addEventListener("DOMContentLoaded", function () {
    // Stop browser from resetting scroll
    if ("scrollRestoration" in history) {
        history.scrollRestoration = "auto";
    }

    // Get scroll position
    let scrollPos = sessionStorage.getItem("scrollPosition");

    // Hide body to prevent flicker and restore scroll instantly
    document.documentElement.style.visibility = "hidden";
    
    if (scrollPos !== null) {
        window.scrollTo(0, parseInt(scrollPos));
    }

    // Show body after positioning to prevent flicker
    requestAnimationFrame(() => {
        document.documentElement.style.visibility = "visible";
    });

    // Store scroll position before the page unloads
    window.addEventListener("beforeunload", function () {
        sessionStorage.setItem("scrollPosition", window.scrollY);
    });

    // Prevent buttons from triggering reloads if not needed
    document.querySelectorAll("button").forEach((button) => {
        button.addEventListener("click", function (event) {
            // Only prevent default for non-submit buttons
            if (!this.closest("form")) {
                event.preventDefault();
            }

            // Save scroll position before any button action
            sessionStorage.setItem("scrollPosition", window.scrollY);
        });
    });
});


// ------------------------------------------------------------------------------------------------------------------------//

document.addEventListener("DOMContentLoaded", function () {
    function getAmount() {
        let integerPart = document.getElementById("amount").innerText || "0.00";
        let quantity = document.getElementById("quantitySelect").value;
        decimalPart = decimalPart.padEnd(2, "0");  // Ensure two decimal places

        // Calculate total price (price * quantity)
        let price = parseFloat(integerPart);
        let total = price * parseInt(quantity);
        
        console.log(total);
        return total.toFixed(2);
    }

    function initializePayPal() {
        paypal.Buttons({
            style: {
                layout: 'horizontal',
                color: 'blue',
                shape: 'rect',
                label: 'pay'
            },
            createOrder: function (data, actions) {
                let amount = getAmount();
                console.log(amount);
                if (amount === 0) {
                    console.error("Invalid amount, order creation aborted.");
                    return actions.reject();
                }
                return actions.order.create({
                    purchase_units: [{
                        amount: {
                            currency_code: "USD",
                            value: amount
                        }
                    }],
                    status: 'PENDING'
                });
            }
        }).render('#paypal-container');
        
    }

    document.getElementById("custom-pay-btn").addEventListener("click", function() {
        document.getElementById("paypal-container").style.display = "block";  
        document.getElementById("custom-pay-btn").style.display = "none"; 
        initializePayPal();  // Trigger PayPal UI
    });
});
