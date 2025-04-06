document.addEventListener("DOMContentLoaded", function () {
    const subCategory = document.querySelector(".subCategory");
    const leftButton = document.querySelector(".scrollButton.left");
    const rightButton = document.querySelector(".scrollButton.right");

    let scrollAmount = 150; // Normal scroll step
    let longPressTimeout;

    function scrollLeft() {
        subCategory.scrollBy({ left: -scrollAmount, behavior: "smooth" });
    }

    function scrollRight() {
        subCategory.scrollBy({ left: scrollAmount, behavior: "smooth" });
    }

    function longPressScrollLeft() {
        subCategory.scrollTo({ left: 0, behavior: "smooth" });
    }

    function longPressScrollRight() {
        subCategory.scrollTo({ left: subCategory.scrollWidth, behavior: "smooth" });
    }

    function handleMouseDown(button, shortPressFn, longPressFn) {
        longPressTimeout = setTimeout(longPressFn, 600); // 600ms long press

        button.addEventListener("mouseup", () => clearTimeout(longPressTimeout));
        button.addEventListener("mouseleave", () => clearTimeout(longPressTimeout));
        button.addEventListener("touchend", () => clearTimeout(longPressTimeout));
    }

    leftButton.addEventListener("mousedown", () => handleMouseDown(leftButton, scrollLeft, longPressScrollLeft));
    rightButton.addEventListener("mousedown", () => handleMouseDown(rightButton, scrollRight, longPressScrollRight));

    leftButton.addEventListener("click", scrollLeft);
    rightButton.addEventListener("click", scrollRight);
});

