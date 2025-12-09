import React, { useState } from 'react';

function ChatInput({ onSendMessage, isLoading }) {
    const [message, setMessage] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (message.trim() && !isLoading) {
            onSendMessage(message);
            setMessage('');
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="chat-input-form">
            <div className="input-container">
                <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Type your message here... (e.g., 'I want to create a new registration')"
                    disabled={isLoading}
                    rows="2"
                />
                <button type="submit" disabled={isLoading || !message.trim()}>
                    {isLoading ? '⏳' : '📤'} {isLoading ? 'Sending...' : 'Send'}
                </button>
            </div>
        </form>
    );
}

export default ChatInput;
