// Video stream control functions
async function toggleStream() {
    try {
        const response = await fetch('/toggle_stream', { method: 'POST' });
        const data = await response.json();
        const videoElement = document.getElementById('video');
        videoElement.src = data.streaming ? "/video_feed" : "";
    } catch (error) {
        console.error('Error toggling video stream:', error);
        alert('Failed to toggle video stream');
    }
}

// Raspberry Pi action functions
async function performAction() {
    try {
        const response = await fetch('/action');
        const data = await response.json();
        alert(data.message);
    } catch (error) {
        console.error('Error performing action:', error);
        alert('Failed to perform action');
    }
}

// Initialize video stream when page loads
document.addEventListener('DOMContentLoaded', () => {
    const videoElement = document.getElementById('video');
    if (videoElement) {
        videoElement.onerror = () => {
            console.error('Error loading video stream');
        };
    }
});
