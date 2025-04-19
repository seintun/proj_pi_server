document.addEventListener('DOMContentLoaded', () => {
    const SERVO_BASE_PATH = '/api/gpio/servo';
    const raiseButton = document.getElementById('raiseArm');
    const lowerButton = document.getElementById('lowerArm');
    const openButton = document.getElementById('openGripper');
    const closeButton = document.getElementById('closeGripper');

    let activeRequest = null;

    const sendServoCommand = async (url) => {
        try {
            activeRequest = await fetch(url, { method: 'POST' });
        } catch (error) {
            console.error('Error sending servo command:', error);
        }
    };

    raiseButton?.addEventListener('mousedown', () => sendServoCommand(`${SERVO_BASE_PATH}/up`));

    lowerButton?.addEventListener('mousedown', () => sendServoCommand(`${SERVO_BASE_PATH}/down`));

    openButton?.addEventListener('mousedown', () => sendServoCommand(`${SERVO_BASE_PATH}/open`));

    closeButton?.addEventListener('mousedown', () => sendServoCommand(`${SERVO_BASE_PATH}/close`));
});
