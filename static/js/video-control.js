class VideoController {
    constructor() {
        this.isStreaming = true;
        this.feedImage = document.querySelector('#camera-feed img');
        this.toggleBtn = document.querySelector('.video-toggle-btn');
        this.statusIcon = document.querySelector('.status-icon');
        this.statusText = document.querySelector('.status-text');
        this.setupControls();
    }

    setupControls() {
        if (this.toggleBtn) {
            this.toggleBtn.addEventListener('click', () => this.toggleStream());
        }

        // Handle video feed errors
        if (this.feedImage) {
            this.feedImage.addEventListener('error', () => {
                this.handleVideoError();
            });
        }
    }

    async toggleStream() {
        try {
            this.toggleBtn.disabled = true; // Prevent double-clicks
            
            const response = await fetch('/video/toggle', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.status === 'success') {
                this.isStreaming = data.streaming;
                this.updateUI();
                
                // Update video source if streaming is enabled
                if (this.isStreaming) {
                    // Add timestamp to prevent caching
                    this.feedImage.src = `/video_feed?t=${Date.now()}`;
                }
            } else {
                throw new Error(data.message || 'Failed to toggle video stream');
            }
        } catch (error) {
            console.error('Error toggling video stream:', error);
            this.showError(error.message);
        } finally {
            this.toggleBtn.disabled = false;
        }
    }

    updateUI() {
        const cameraStatusIcon = document.getElementById('camera-status-icon');
        
        if (cameraStatusIcon) {
            cameraStatusIcon.style.display = this.isStreaming ? 'block' : 'none';
        }

        if (this.statusIcon) {
            this.statusIcon.classList.toggle('off', !this.isStreaming);
        }
        if (this.statusText) {
            this.statusText.textContent = this.isStreaming ? 'Stop Stream' : 'Start Stream';
        }
        
        if (this.toggleBtn) {
            this.toggleBtn.classList.toggle('streaming', this.isStreaming);
            this.toggleBtn.classList.remove('error');
        }
    }

    handleVideoError() {
        // If the video feed fails to load, show error state
        this.isStreaming = false;
        this.updateUI();
        this.showError('Video feed unavailable');
    }

    showError(message) {
        this.toggleBtn.classList.add('error');
        console.error(message);
        
        // Remove error class after animation completes
        setTimeout(() => {
            this.toggleBtn.classList.remove('error');
        }, 500);
    }
}

// Initialize video controls when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VideoController();
});
