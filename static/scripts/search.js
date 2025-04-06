let debounceTimer;
document.getElementById("search-box").addEventListener("keyup", function () {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        performSearch(this.value.trim());
    }, 300); // Debounce to prevent excessive API calls
});

function performSearch(query) {
    if (query.length < 1) {
        document.getElementById("search-results").innerHTML = "";
        return;
    }

    fetch(`/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            let resultsContainer = document.getElementById("search-results");
            resultsContainer.innerHTML = ""; // Clear previous results

            console.log("Received data:", data);

            if (!data.products || data.products.length === 0) {
                resultsContainer.innerHTML = "<p>No results found</p>";
                return;
            }

            let resultsHtml = "<div class='prodlist'>";

            data.products.forEach(product => {
                let productName = product.name || "Unknown Product";
                let productTitle = product.title || "no title";
                let productId = product.id || "#";
                let quantity = product.quantity || "";
                let avgRating = product.rating || 0;
                
                // Fetch Image using product ID, name, or title
                let imageEntry = data.prodImage.find(img => 
                    img.product__name === productName
                );
                let imageUrl = imageEntry ? `/media/${imageEntry.image1}` : '/static/images/default-image.jpg';
                
                // Fetch Pricing using product ID, name, or title
                let priceEntry = data.pricing.find(price => 
                    price.product__id === productId || price.product__name === productName || price.product__title === productTitle
                );
                let originalPrice = priceEntry?.price || "0";
                let discount = priceEntry?.offer || 0;
                let discountedPrice = (originalPrice - (originalPrice * (discount / 100))).toFixed(2); // Limited to 2 decimal places

                // Fetch Important Info using product ID, name, or title
                let infoEntry = data.important_info.find(info => 
                    info.product__id === productId || info.product__name === productName || info.product__name === productTitle
                );
                let directionsUse = infoEntry?.direction_to_use || "No usage info available.";
                let directionsStore = infoEntry?.direction_to_store || "No storage info available.";

                // Fetch Reviews using product ID, name, or title
                let reviews = data.reviews.filter(review => 
                    review.product__id === productId || review.product__name === productName || review.product__name === productTitle
                );
                

                resultsHtml += `
                    <a href="/viewDetails/${productId}" >
                        <div class="product-card">
                            ${discount > 0 ? `<div class="flag">${discount}% <p>Off</p></div>` : ""}
                            <div class="productImage">
                                <img src="${imageUrl}" alt="${productName}">
                            </div>
                            <div class="description">${productName}</div>
                            <div class="quantity">${quantity}</div>
                            <br>
                            <div class="price">
                                <div class="PriceValue">
                                    <p class="discountedPriceValue">₹${discountedPrice}</p>
                                    <p class="originalPriceValue">₹${originalPrice}</p>
                                </div>
                            </div>
                            <div class="reviews">
                                <p><strong>Rating:</strong> ${avgRating} ⭐</p>
                            </div>
                            <div class="card-footer">
                                <a class="button" href="/addToCart/${productId}">Add to cart</a>
                            </div>
                        </div>
                    </a>
                `;
            });

            resultsHtml += "</div>";
            resultsContainer.innerHTML = resultsHtml;
        })
        .catch(error => console.error("Error fetching data:", error));

}