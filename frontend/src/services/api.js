import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

class ChatAPI {
    constructor() {
        this.sessionId = null;
    }

    async sendMessage(message) {
        try {
            const response = await axios.post(`${API_BASE_URL}/api/chat`, {
                message,
                session_id: this.sessionId
            });

            // Store session ID from response
            if (response.data.session_id) {
                this.sessionId = response.data.session_id;
            }

            return response.data;
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    }

    async clearConversation() {
        if (!this.sessionId) return;

        try {
            await axios.post(`${API_BASE_URL}/api/clear`, {
                session_id: this.sessionId
            });

            this.sessionId = null;
        } catch (error) {
            console.error('Error clearing conversation:', error);
            throw error;
        }
    }

    async checkHealth() {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/health`);
            return response.data;
        } catch (error) {
            console.error('Error checking health:', error);
            throw error;
        }
    }
}

export default new ChatAPI();
