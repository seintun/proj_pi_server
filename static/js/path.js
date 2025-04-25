class PathGraph {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) {
            console.error(`Canvas with id "${canvasId}" not found.`);
            return;
        }

        this.ctx = this.canvas.getContext('2d');
        this.path = [];
        this.scale = 1; // Each grid cell represents 1 meter
        this.gridSize = 3; // Half of 6x6 grid (3 meters in each direction)

        // Set fixed canvas size
        this.canvas.width = 450; // Fixed width in pixels
        this.canvas.height = 450; // Fixed height in pixels

        // Set initial styles
        this.ctx.strokeStyle = '#ffdb15';
        this.ctx.lineWidth = 2;

        // Draw the initial grid and legend
        this.draw();
    }

    addPoint(point) {
        this.path.push(point);
        this.draw();
    }

    draw() {
        const ctx = this.ctx;
        const canvas = this.canvas;
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const cellSize = canvas.width / (this.gridSize * 2);

        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw grid
        ctx.strokeStyle = 'rgba(255, 219, 21, 0.1)';
        ctx.lineWidth = 1;

        // Draw vertical grid lines
        for (let i = -this.gridSize; i <= this.gridSize; i++) {
            const x = centerX + i * cellSize;
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
            ctx.stroke();
        }

        // Draw horizontal grid lines
        for (let i = -this.gridSize; i <= this.gridSize; i++) {
            const y = centerY + i * cellSize;
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
            ctx.stroke();
        }

        // Draw axes
        ctx.strokeStyle = '#ffdb15';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(centerX, 0);
        ctx.lineTo(centerX, canvas.height);
        ctx.moveTo(0, centerY);
        ctx.lineTo(canvas.width, centerY);
        ctx.stroke();

        // Draw legend
        const legendX = 10;
        const legendY = 20;

        // Path line legend
        ctx.strokeStyle = '#fcc303';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(legendX, legendY);
        ctx.lineTo(legendX + 30, legendY);
        ctx.stroke();

        ctx.fillStyle = '#ffdb15';
        ctx.font = '15px "Roboto Mono", monospace';
        ctx.fillText('Robot Path', legendX + 40, legendY + 5);

        // Current position legend
        ctx.fillStyle = '#ff0000';
        ctx.beginPath();
        ctx.arc(legendX + 15, legendY + 25, 5, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#ffdb15';
        ctx.fillText('Current Position', legendX + 40, legendY + 30);

        // Draw path
        if (this.path.length > 0) {
            ctx.strokeStyle = '#fcc303';
            ctx.lineWidth = 2;
            ctx.beginPath();

            this.path.forEach((point, index) => {
                const x = centerX + point.x * cellSize;
                const y = centerY - point.y * cellSize;

                if (index === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            });

            ctx.stroke();

            // Draw current position marker
            const lastPoint = this.path[this.path.length - 1];
            const x = centerX + lastPoint.x * cellSize;
            const y = centerY - lastPoint.y * cellSize;

            ctx.fillStyle = '#ff0000';
            ctx.beginPath();
            ctx.arc(x, y, 5, 0, Math.PI * 2);
            ctx.fill();
        }
    }
}

// Initialize path graph when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const pathGraph = new PathGraph('pathCanvas');

    function fetchEncoderPath() {
        const eventSource = new EventSource('/api/encoder/path');
        
        eventSource.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data.error) {
                    console.error('Error in encoder data:', data.error);
                    eventSource.close();
                } else if (data.x !== undefined && data.y !== undefined) {
                    pathGraph.addPoint(data);
                    console.log('Updated position:', data);  // Debug output
                }
            } catch (e) {
                console.error('Error parsing encoder data:', e);
            }
        };

        eventSource.onerror = () => {
            console.error('Connection to /api/encoder/path lost.');
            eventSource.close();
            // Attempt to reconnect after 5 seconds
            setTimeout(fetchEncoderPath, 5000);
        };
    }

    fetchEncoderPath();
});
