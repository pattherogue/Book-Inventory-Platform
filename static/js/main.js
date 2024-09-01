// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to flash messages for dismissal
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(flash => {
        flash.addEventListener('click', function() {
            this.style.display = 'none';
        });
    });

    // Add any other client-side functionality here
});