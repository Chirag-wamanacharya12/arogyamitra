document.querySelectorAll(".size-option").forEach(option => {
    option.addEventListener("click", () => {
      const checkbox = option.querySelector("input");
      checkbox.checked = !checkbox.checked; // Toggle checkbox state
      option.classList.addClass("selected", checkbox.checked); // Toggle class
    });
  });
  

document.addEventListener('DOMContentLoaded', function () {
    const imageInput = document.getElementById('imageInput');
    const mainPreview = document.getElementById('mainPreview');
    const mainPreviewContainer = document.getElementById('mainPreviewContainer');
    const thumbnailContainer = document.getElementById('thumbnailContainer');
    const addImage = document.getElementById('addImage');

    let imageList = [];

    addImage.addEventListener('click', function () {
        imageInput.click();
    });

    imageInput.addEventListener('change', function (event) {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const imageUrl = e.target.result;

                // Set main preview if it's the first image
                if (imageList.length === 0) {
                    mainPreview.src = imageUrl;
                    mainPreviewContainer.style.display = 'block';
                }

                // Add to image list
                imageList.push(imageUrl);
                updateThumbnails();
            };
            reader.readAsDataURL(file);
        }
    });

    function updateThumbnails() {
        // Clear existing thumbnails except the add button
        document.querySelectorAll('.thumbnail:not(.add-image)').forEach(el => el.remove());

        // Update thumbnails
        imageList.forEach((imageUrl, index) => {
            const thumb = document.createElement('div');
            thumb.classList.add('thumbnail');
            
            const img = document.createElement('img');
            img.src = imageUrl;

            thumb.appendChild(img);

            thumb.addEventListener('click', function () {
                mainPreview.src = imageUrl;
            });

            // Add double-click event to delete the thumbnail
            thumb.addEventListener('dblclick', function () {
                // Remove the image from the list and update the thumbnails
                imageList.splice(index, 1);
                updateThumbnails();  // Rebuild the thumbnails
            });

            thumbnailContainer.insertBefore(thumb, addImage);
        });

        // Automatically update the main preview to the last image in the list
        if (imageList.length > 0) {
            mainPreview.src = imageList[imageList.length - 1];
        } else {
            mainPreviewContainer.style.display = 'none';
        }
    }
});


$(document).ready(function() {
    // Listen for changes on the primary category dropdown
    $('#category').change(function() {
        var primaryCategoryId = $(this).val();  // Get selected primary category ID

        // Clear the subcategory dropdown
        $('#sub_category').html('<option value="">Select a Subcategory</option>');

        if (primaryCategoryId) {
            // Make AJAX request to fetch subcategories based on the selected primary category
            $.ajax({
                url: '{% url "get_subcategories" %}',  // Django URL to the get_subcategories view
                data: {
                    'primary_category_id': primaryCategoryId
                },
                dataType: 'json',
                success: function(response) {
                    if (response.subcategories) {
                        // Populate the subcategory dropdown with the fetched subcategories
                        $.each(response.subcategories, function(index, subcategory) {
                            $('#sub_category').append(
                                `<option value="${subcategory.id}">${subcategory.name}</option>`
                            );
                        });
                    }
                },
                error: function() {
                    alert('Failed to fetch subcategories.');
                }
            });
        }
    });
});