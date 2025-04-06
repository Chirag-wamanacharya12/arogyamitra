document.querySelectorAll(".widgetContainer button").forEach(button => {
    button.addEventListener("click", () => {
        alert(`You clicked on "${button.parentElement.querySelector("h2").innerText}"`);
    });
});

const socket = new WebSocket('ws://' + window.location.host + '/ws/notifications/');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    showToast(data.message);
};

function showToast(message) {
    const toastContainer = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.classList.add('toast');
    toast.innerHTML = `${message} <button onclick="closeToast(this)">✖</button>`;
    toastContainer.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        closeToast(toast);
    }, 3000);
}

function closeToast(toast) {
    toast.classList.add('hide');
    setTimeout(() => {
        toast.remove();
    }, 400);
}
