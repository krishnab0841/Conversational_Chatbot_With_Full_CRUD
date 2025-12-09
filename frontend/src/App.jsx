import React, { useState, useEffect, useRef } from 'react';
import Header from './components/Header';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import chatAPI from './services/api';
import './App.css';

function App() {
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [isConnected, setIsConnected] = useState(false);
    const messagesEndRef = useRef(null);

    // Check backend connection on mount
    useEffect(() => {
        checkConnection();
    }, []);

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const checkConnection = async () => {
        try {
            await chatAPI.checkHealth();
            setIsConnected(true);
        } catch (err) {
            setIsConnected(false);
            setError('Cannot connect to backend. Please ensure the backend server is running on http://localhost:8000');
        }
    };

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const handleSendMessage = async (message) => {
        if (!message.trim()) return;

        // Add user message to chat
        const userMessage = { text: message, isUser: true };
        setMessages(prev => [...prev, userMessage]);
        setIsLoading(true);
        setError(null);

        try {
            // Send message to backend
            const response = await chatAPI.sendMessage(message);

            // Add bot response to chat
            const botMessage = { text: response.response, isUser: false };
            setMessages(prev => [...prev, botMessage]);
        } catch (err) {
            setError('Failed to send message. Please try again.');
            console.error('Error:', err);

            // Add error message to chat
            const errorMessage = {
                text: '❌ Sorry, I encountered an error. Please try again.',
                isUser: false
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleClearChat = async () => {
        try {
            await chatAPI.clearConversation();
            setMessages([]);
            setError(null);
        } catch (err) {
            console.error('Error clearing chat:', err);
        }
    };

    const handleExampleClick = (example) => {
        handleSendMessage(example);
    };

    return (
        <div className="app">
            <Header />

            {/* Connection Status */}
            {!isConnected && (
                <div className="connection-error">
                    ⚠️ Backend not connected. Please run: <code>python backend.py</code>
                </div>
            )}

            {/* Info Section */}
            <div className="info-section">
                <details>
                    <summary>ℹ️ What can I do?</summary>
                    <div className="info-content">
                        <p>I'm your intelligent registration assistant powered by Google Gemini and LangGraph! I can help you with:</p>
                        <ul>
                            <li>🆕 <strong>Create</strong> a new registration</li>
                            <li>📖 <strong>Read</strong> your existing registration details</li>
                            <li>✏️ <strong>Update</strong> specific fields in your registration</li>
                            <li>🗑️ <strong>Delete</strong> your registration</li>
                        </ul>
                    </div>
                </details>
            </div>

            {/* Chat Messages */}
            <div className="chat-container">
                {messages.length === 0 ? (
                    <div className="welcome-message">
                        <h2>👋 Welcome!</h2>
                        <p>Start a conversation by typing a message below or try an example:</p>
                        <div className="example-buttons">
                            <button
                                onClick={() => handleExampleClick('I want to create a new registration')}
                                className="example-btn"
                            >
                                💡 Create Registration
                            </button>
                            <button
                                onClick={() => handleExampleClick('Show me my registration details')}
                                className="example-btn"
                            >
                                💡 View My Data
                            </button>
                        </div>
                    </div>
                ) : (
                    <div className="messages-list">
                        {messages.map((msg, index) => (
                            <ChatMessage
                                key={index}
                                message={msg.text}
                                isUser={msg.isUser}
                            />
                        ))}
                        {isLoading && (
                            <div className="loading-indicator">
                                <div className="typing-dots">
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>
                )}
            </div>

            {/* Error Display */}
            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            {/* Input Area */}
            <div className="input-area">
                <ChatInput
                    onSendMessage={handleSendMessage}
                    isLoading={isLoading}
                />
                {messages.length > 0 && (
                    <button
                        onClick={handleClearChat}
                        className="clear-btn"
                        disabled={isLoading}
                    >
                        🔄 Clear Chat
                    </button>
                )}
            </div>

            {/* Footer */}
            <div className="footer">
                <p>Powered by <strong>LangGraph</strong> + <strong>Google Gemini</strong> + <strong>PostgreSQL</strong></p>
                <p>All data is stored securely with full audit logging</p>
            </div>
        </div>
    );
}

export default App;
