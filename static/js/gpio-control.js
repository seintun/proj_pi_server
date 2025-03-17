document.addEventListener('DOMContentLoaded', () => {
    const gpioButton = document.getElementById('gpioButton');
    const ledIndicator = document.getElementById('ledIndicator');

    // Button click handler
    gpioButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/gpio/led/toggle', {
                method: 'POST',
            });
            const data = await response.json();

            if (data.status === 'success') {
                updateLedIndicator(data.led_state);
                alert(data.state.message || 'LED state toggled'); // Show alert popup with message
            } else {
                alert('Error: ' + (data.state.message || 'Unknown error occurred')); // Show error alert
            }
        } catch (error) {
            alert('Error: ' + error.message); // Show error alert
        }
    });

    // Update LED indicator UI
    function updateLedIndicator(state) {
        if (ledIndicator) {
            if (state) {
                ledIndicator.classList.add('on');
            } else {
                ledIndicator.classList.remove('on');
            }
        }
    }

});
