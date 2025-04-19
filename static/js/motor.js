document.addEventListener('DOMContentLoaded', () => {
    const MOTOR_BASE_PATH = '/api/gpio/motor';
    const forwardButton = document.getElementById('up');
    const leftButton = document.getElementById('left');
    const rightButton = document.getElementById('right');
    const backwardButton = document.getElementById('down');

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
            await fetch(`${MOTOR_BASE_PATH}/stop`, { method: 'POST' });
            activeRequest = null;
        }
    };

    forwardButton?.addEventListener('mousedown', () => sendMotorCommand(`${MOTOR_BASE_PATH}/forward`));
    forwardButton?.addEventListener('mouseup', stopMotor);

    leftButton?.addEventListener('mousedown', () => sendMotorCommand(`${MOTOR_BASE_PATH}/left`));
    leftButton?.addEventListener('mouseup', stopMotor);

    rightButton?.addEventListener('mousedown', () => sendMotorCommand(`${MOTOR_BASE_PATH}/right`));
    rightButton?.addEventListener('mouseup', stopMotor);

    backwardButton?.addEventListener('mousedown', () => sendMotorCommand(`${MOTOR_BASE_PATH}/backward`));
    backwardButton?.addEventListener('mouseup', stopMotor);
});

