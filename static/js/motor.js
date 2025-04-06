document.addEventListener('DOMContentLoaded', () => {
    const forwardButton = document.getElementById('forward_button');
    const leftButton = document.getElementById('left_button');
    const rightButton = document.getElementById('right_button');
    const backwardButton = document.getElementById('backward_button');

    let activeRequest = null;

    const sendMotorCommand = async (url) => {
        try {
            activeRequest = await fetch(url, { method: 'POST' });
        } catch (error) {
            console.error('Error sending motor command:', error);
        }
    };

    const stopMotor = async () => {
        if (activeRequest) {
            await fetch('/api/gpio/motor/stop', { method: 'POST' });
            activeRequest = null;
        }
    };

    forwardButton?.addEventListener('mousedown', () => sendMotorCommand('/api/gpio/motor/forward'));
    forwardButton?.addEventListener('mouseup', stopMotor);

    leftButton?.addEventListener('mousedown', () => sendMotorCommand('/api/gpio/motor/left'));
    leftButton?.addEventListener('mouseup', stopMotor);

    rightButton?.addEventListener('mousedown', () => sendMotorCommand('/api/gpio/motor/right'));
    rightButton?.addEventListener('mouseup', stopMotor);

    backwardButton?.addEventListener('mousedown', () => sendMotorCommand('/api/gpio/motor/backward'));
    backwardButton?.addEventListener('mouseup', stopMotor);
});