document.addEventListener('DOMContentLoaded', () => {
    const savingButton = document.querySelector('.saving-toggle-btn');
    const savingIcon = savingButton.querySelector('.saving-status-icon');
    const savingText = savingButton.querySelector('.saving-status-text');

    savingButton.addEventListener('click', () => {
        const isRecording = savingButton.classList.contains('recording');

        // Toggle button state
        if (isRecording) {
            savingButton.classList.remove('recording');
            savingIcon.textContent = '⚪';
            savingText.textContent = 'Start Recording';
        } else {
            savingButton.classList.add('recording');
            savingIcon.textContent = '🔴';
            savingText.textContent = 'Stop Recording';
        }

        // Send request to backend to toggle recording
        fetch('/api/recording/toggle', {
            method: 'POST'
        }).then(response => {
            if (!response.ok) {
                console.error('Failed to toggle recording state');
            }
        }).catch(error => {
            console.error('Error toggling recording state:', error);
        });
    });
});
