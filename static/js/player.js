document.addEventListener('DOMContentLoaded', () => {
    const helloButton = document.getElementById('helloButton');

    let activeRequest = null;

    const sendPlayerCommand = async (url) => {
        try {
            activeRequest = await fetch(url, { method: 'POST' });
        } catch (error) {
            console.error('Error sending player command:', error);
        }
    };

    helloButton?.addEventListener('mousedown', () => sendPlayerCommand('/api/gpio/player/one'));
});
