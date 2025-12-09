import React from 'react';

function ChatMessage({ message, isUser }) {
    return (
        <div className={`message ${isUser ? 'user-message' : 'bot-message'}`}>
            <div className="message-avatar">
                {isUser ? '👤' : '🤖'}
            </div>
            <div className="message-content">
                <div className="message-text">{message}</div>
            </div>
        </div>
    );
}

export default ChatMessage;
