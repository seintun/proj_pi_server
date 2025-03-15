class VideoFeedController {
    constructor() {
        this.feedImage = document.querySelector('#camera-feed img');
        this.isActive = true;
        this.setupControls();
    }

    setupControls() {
        // Add video control button to the camera feed container
        const controlButton = document.createElement('button');
        controlButton.className = 'video-control-btn';
        controlButton.textContent = 'Stop Feed';
        controlButton.onclick = () => this.toggleFeed();
        
        const container = document.querySelector('#camera-feed');
        container.appendChild(controlButton);
    }

    async toggleFeed() {
        const button = document.querySelector('.video-control-btn');
        try {
            if (this.isActive) {
                const response = await fetch('/video_feed/stop');
                if (response.ok) {
                    this.isActive = false;
                    button.textContent = 'Start Feed';
                    // Save the current src
                    this.lastSrc = this.feedImage.src;
                    // Show "feed stopped" message or image
                    this.feedImage.src = '/static/img/no-camera.png';
                }
            } else {
                const response = await fetch('/video_feed/start');
                if (response.ok) {
                    this.isActive = true;
                    button.textContent = 'Stop Feed';
                    // Restore the video feed
                    this.feedImage.src = '/video_feed?' + new Date().getTime();
                }
            }
        } catch (error) {
            console.error('Error toggling video feed:', error);
            // Visual feedback of the error
            button.classList.add('error');
            setTimeout(() => button.classList.remove('error'), 2000);
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VideoFeedController();
});
