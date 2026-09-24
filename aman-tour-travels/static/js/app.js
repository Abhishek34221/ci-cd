// Aman Tour & Travels Enterprise JavaScript
document.addEventListener("DOMContentLoaded", () => {
    console.log("Aman Tour & Travels Enterprise UI initialized successfully.");

    // Auto-dismiss flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.fixed.top-20');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(el => el.remove());
        }, 5000);
    }
});