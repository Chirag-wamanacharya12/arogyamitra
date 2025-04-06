const videos = document.querySelectorAll(".short video");

videos.forEach(video => {
    video.addEventListener("mouseenter", () => {
        video.play();
    });

    video.addEventListener("mouseleave", () => {
        video.pause();
        video.currentTime = 0; // Reset video to the start when hover ends
    });
});
