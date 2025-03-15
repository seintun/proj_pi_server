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
                        drawBorder: false
                    },
                    ticks: { 
                        color: '#ffdb15',
                        font: {
                            family: 'Roboto Mono'
                        }
                    }
                }
            },
            layout: {
                padding: {
                    top: 20,
                    right: 10,
                    bottom: 10,
                    left: 10
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
                            min: 0,
                            max: 100,
                            ticks: {
                                ...commonOptions.scales.y.ticks,
                                callback: value => value + '%'
                            }
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
                            min: 0,
                            max: 100,
                            ticks: {
                                ...commonOptions.scales.y.ticks,
                                callback: value => value + '%'
                            }
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
                            min: 30,
                            max: 85,
                            ticks: {
                                ...commonOptions.scales.y.ticks,
                                callback: value => value + '°C'
                            }
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
        // Queue CPU updates
        this.pendingUpdates.set('cpuUsage', `${data.cpu.usage}%`);
        this.pendingUpdates.set('cpuTemp', `${data.temperature}°C`);
        this.pendingUpdates.set('cpuCores', data.cpu.cores);
        this.pendingUpdates.set('cpuThreads', data.cpu.threads);
        this.pendingUpdates.set('cpuFreq', `${data.cpu.frequency} MHz`);

        // Queue Memory updates with formatted values and validation
        const memPercent = data.memory?.percent ?? 0;
        const memTotal = data.memory?.total_formatted ?? '0 MB';
        const memUsed = data.memory?.used_formatted ?? '0 MB';
        const memFree = data.memory?.free_formatted ?? '0 MB';

        this.pendingUpdates.set('ramUsage', `${memPercent}%`);
        this.pendingUpdates.set('memTotal', memTotal);
        this.pendingUpdates.set('memUsed', memUsed);
        this.pendingUpdates.set('memFree', memFree);

        // Update RAM chart with validated percentage
        this.updateChart(this.charts.ram, memPercent, new Date().toLocaleTimeString());

        // Check for critical temperature (with default value)
        const tempElement = document.getElementById('cpuTemp');
        const temp = data.temperature ?? 0;
        
        if (tempElement) {
            if (temp > 80) {
                tempElement.classList.add('critical');
            } else {
                tempElement.classList.remove('critical');
            }
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
        this.updateChart(this.charts.cpu, data.cpu.usage, timestamp);


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
