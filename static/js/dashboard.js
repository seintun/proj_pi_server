class DashboardUI {
    constructor() {
        this.pendingUpdates = new Map();
        this.frameRequested = false;
        this.charts = this.initializeCharts();
        this.setupEventSource();
    }

    initializeCharts() {
        const commonOptions = {
            animation: false,
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
            },
            scales: {
                x: {
                    display: false,
                    grid: { display: false }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 219, 21, 0.1)',
                        borderColor: '#ffdb15'
                    },
                    ticks: { color: '#ffdb15' }
                }
            },
            elements: {
                line: {
                    borderWidth: 2,
                    borderColor: '#ffdb15',
                    tension: 0.4
                },
                point: { radius: 0 }
            }
        };

        return {
            cpu: new Chart(document.getElementById('cpuChart'), {
                type: 'line',
                data: {
                    labels: Array(60).fill(''),
                    datasets: [{
                        data: Array(60).fill(0),
                        fill: {
                            target: 'origin',
                            above: 'rgba(255, 219, 21, 0.1)'
                        }
                    }]
                },
                options: {
                    ...commonOptions,
                    scales: {
                        ...commonOptions.scales,
                        y: {
                            ...commonOptions.scales.y,
                            max: 100,
                            min: 0
                        }
                    }
                }
            }),
            ram: new Chart(document.getElementById('ramChart'), {
                type: 'line',
                data: {
                    labels: Array(60).fill(''),
                    datasets: [{
                        data: Array(60).fill(0),
                        fill: {
                            target: 'origin',
                            above: 'rgba(255, 219, 21, 0.1)'
                        }
                    }]
                },
                options: {
                    ...commonOptions,
                    scales: {
                        ...commonOptions.scales,
                        y: {
                            ...commonOptions.scales.y,
                            max: 100,
                            min: 0
                        }
                    }
                }
            }),
            temp: new Chart(document.getElementById('tempChart'), {
                type: 'line',
                data: {
                    labels: Array(60).fill(''),
                    datasets: [{
                        data: Array(60).fill(0),
                        fill: {
                            target: 'origin',
                            above: 'rgba(255, 219, 21, 0.1)'
                        }
                    }]
                },
                options: {
                    ...commonOptions,
                    scales: {
                        ...commonOptions.scales,
                        y: {
                            ...commonOptions.scales.y,
                            max: 85,
                            min: 30
                        }
                    }
                }
            })
        };
    }

    setupEventSource() {
        const eventSource = new EventSource('/system-events');
        
        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.updateStats(data);
            this.updateCharts(data);
        };

        eventSource.onerror = (error) => {
            console.error('EventSource failed:', error);
            eventSource.close();
            // Attempt to reconnect after 5 seconds
            setTimeout(() => this.setupEventSource(), 5000);
        };
    }

    updateStats(data) {
        // Queue updates for next animation frame
        this.pendingUpdates.set('cpuTemp', `${data.temperature}°C`);
        this.pendingUpdates.set('cpuUsage', `${data.cpu_usage}%`);
        this.pendingUpdates.set('ramUsage', `${data.ram_usage}%`);

        // Check for critical temperature
        const tempElement = document.getElementById('cpuTemp');
        if (data.temperature > 80) {
            tempElement.classList.add('critical');
        } else {
            tempElement.classList.remove('critical');
        }

        if (!this.frameRequested) {
            this.frameRequested = true;
            requestAnimationFrame(() => this.updateUI());
        }
    }

    updateUI() {
        this.frameRequested = false;
        for (const [id, value] of this.pendingUpdates) {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        }
        this.pendingUpdates.clear();
    }

    updateCharts(data) {
        const timestamp = new Date().toLocaleTimeString();

        // Update CPU chart
        this.updateChart(this.charts.cpu, data.cpu_usage, timestamp);

        // Update RAM chart
        this.updateChart(this.charts.ram, data.ram_usage, timestamp);

        // Update Temperature chart
        this.updateChart(this.charts.temp, data.temperature, timestamp);
    }

    updateChart(chart, value, label) {
        chart.data.labels.push(label);
        chart.data.datasets[0].data.push(value);

        if (chart.data.labels.length > 60) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
        }

        chart.update('none'); // Update without animation
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new DashboardUI();
});
