// Toggle Slider Bar
function toggleSlider() {
    const slider = document.getElementById("slider-bar");
    const menuIcon = document.querySelector(".menu-icon");

    slider.classList.toggle("open"); // Toggle sidebar

    menuIcon.classList.toggle("active"); // Toggle menu icon animation
}

// Update Date and Time
function updateDateTime() {
    const now = new Date();
    const dateTime = document.getElementById("date-time");
    dateTime.textContent = now.toLocaleString();
}

// Update Date and Time Every Second
setInterval(updateDateTime, 1000);
updateDateTime();

let timeoutId; // Variable to track the timeout

// Function to show options and hide main circle
function showOptions() {
    const bottomCircle = document.getElementById("bottom-circle");
    const options = document.getElementById("options");

    bottomCircle.style.display = "none"; // Hide main circle
    options.style.display = "flex"; // Show options

    // Clear any previous timeout
    clearTimeout(timeoutId);

    // Set a timeout to reset after 10 seconds
    timeoutId = setTimeout(resetOptions, 10000);
}

// Function to reset to original position
function resetOptions() {
    const bottomCircle = document.getElementById("bottom-circle");
    const options = document.getElementById("options");

    bottomCircle.style.display = "flex"; // Show main circle
    options.style.display = "none"; // Hide options
}

// Add event listeners for hover effect
document.getElementById("bottom-circle").addEventListener("mouseenter", showOptions);
document.getElementById("options").addEventListener("mouseleave", resetOptions);

// Event listener for menu button
document.getElementById("menu-toggle").addEventListener("click", toggleSlider);


