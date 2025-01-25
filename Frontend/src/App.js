import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false); // Loading state

  const handleSend = async () => {
    if (input.trim() === '') return;

    const userMessage = { sender: 'user', text: input };
    setMessages([...messages, userMessage]);
    setInput('');
    setIsLoading(true); // Start loading spinner
    const API = process.env.REACT_APP_API_URL;
    console.log(API)
    try {
      const response = await fetch(API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: input }),
      });

      const data = await response.json();
      console.log(data)
      const botMessage = { sender: 'bot', text: data.message };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { sender: 'bot', text: 'Something went wrong!' };
      console.log(error)
      setMessages((prev) => [...prev, errorMessage]);
    }

    setIsLoading(false); // Stop loading spinner
  };

  return (
    <div className="chat-container">
      <header className="chat-header">AI Chat</header>
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`chat-message ${
              msg.sender === 'user' ? 'message-user' : 'message-bot'
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleSend()}
          disabled={isLoading} // Disable input while loading
        />
        <button onClick={handleSend} disabled={isLoading}>
          {isLoading ? <div className="spinner"></div> : 'Send'}
        </button>
      </div>
    </div>
  );
};

export default App;
