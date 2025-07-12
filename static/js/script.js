document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    function appendMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender === 'user' ? 'user-message' : 'assistant-message');
        messageDiv.innerHTML = `<p>${message}</p>`;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to bottom
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;

        appendMessage('user', message);
        userInput.value = ''; // Clear input

        // Muestra un mensaje de carga
        const loadingMessageDiv = document.createElement('div');
        loadingMessageDiv.classList.add('message', 'assistant-message', 'loading-message');
        loadingMessageDiv.innerHTML = `<p>Asistente: Escribiendo...</p>`;
        chatBox.appendChild(loadingMessageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            // Elimina el mensaje de carga antes de añadir la respuesta real
            chatBox.removeChild(loadingMessageDiv);

            if (!response.ok) {
                const errorData = await response.json();
                appendMessage('assistant', `Error: ${errorData.response || response.statusText}`);
                return;
            }

            const data = await response.json();
            appendMessage('assistant', data.response);

        } catch (error) {
            console.error('Error al enviar mensaje:', error);
            // Asegúrate de eliminar el mensaje de carga si falla la petición
            if (chatBox.contains(loadingMessageDiv)) {
                chatBox.removeChild(loadingMessageDiv);
            }
            appendMessage('assistant', 'Lo siento, no pude conectar con el asistente. Inténtalo de nuevo más tarde.');
        }
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
