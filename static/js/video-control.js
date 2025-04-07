class VideoController {
    constructor() {
        this.isStreaming = true;
        this.feedImage = document.querySelector('#camera-feed img');
        this.toggleBtn = document.querySelector('.video-toggle-btn');
        this.statusIcon = document.querySelector('.status-icon');
        this.statusText = document.querySelector('.status-text');
        this.cameraTypeIndicator = document.querySelector('.camera-type-indicator');

        // Video metrics elements
        this.resolutionElement = document.getElementById('resolution');
        this.bitrateElement = document.getElementById('bitrate');
        this.fpsElement = document.getElementById('video-fps');
        this.qualityElement = document.getElementById('quality');

        this.lastStatUpdate = 0;
        this.statUpdateInterval = 1000; // Update stats every second

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

        // Initial stats update
        this.updateStats();

        // Update stats periodically
        setInterval(() => {
            if (this.isStreaming) {
                this.updateStats();
            }
        }, this.statUpdateInterval);
    }

    async updateStats() {
        try {
            const now = Date.now();
            if (now - this.lastStatUpdate < this.statUpdateInterval) {
                return; // Prevent too frequent updates
            }
            this.lastStatUpdate = now;

            const response = await fetch('/video/stats');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            if (data.status === 'success') {
                const stats = data.stats?.stats || {};

                // Update metrics display with fallback values
                if (this.resolutionElement) {
                    this.resolutionElement.textContent = stats.resolution || '--x--';
                }
                if (this.bitrateElement) {
                    const bitrate = stats.bitrate || 0;
                    this.bitrateElement.textContent = `${bitrate.toFixed(1)} kbps`;
                }
                if (this.fpsElement) {
                    const fps = stats.fps || 0;
                    this.fpsElement.textContent = fps.toFixed(1);
                }
                if (this.qualityElement) {
                    const quality = stats.quality || 0;
                    this.qualityElement.textContent = `${quality}%`;
                }

                // Update camera type indicator
                if (this.cameraTypeIndicator) {
                    this.cameraTypeIndicator.textContent = data.stats.display_name;
                }
            }
        } catch (error) {
            console.error('Error updating video stats:', error);
            this.resetMetrics();
        }
    }

    resetMetrics() {
        if (this.resolutionElement) this.resolutionElement.textContent = '--x--';
        if (this.bitrateElement) this.bitrateElement.textContent = '-- kbps';
        if (this.fpsElement) this.fpsElement.textContent = '--';
        if (this.qualityElement) this.qualityElement.textContent = '--%';
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

        // Update video source based on streaming state
        if (!this.isStreaming) {
            this.feedImage.src = '/static/img/no-camera.png';
            this.resetMetrics();
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
