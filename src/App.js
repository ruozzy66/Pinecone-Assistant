import React, { useState } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: updatedMessages })
      });

      const data = await response.json();
      if (data.error) {
        throw new Error(data.details);
      }

      const assistantMessage = data.choices[0].message;
      assistantMessage.content = processLinks(assistantMessage.content);

      setMessages([...updatedMessages, assistantMessage]);
    } catch (error) {
      setMessages([...updatedMessages, { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !isLoading) {
      sendMessage();
    }
  };

  const processLinks = (text) => {
    const urlRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
    return text.replace(urlRegex, '<a href="$2" target="_blank">$1</a>');
  };

  return (
    <div className="App">
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.role}`}>
            <div dangerouslySetInnerHTML={{ __html: msg.content }} />
          </div>
        ))}
        {isLoading && <div className="loading">Loading...</div>}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type a message..."
      />
      <button onClick={sendMessage} disabled={isLoading}>Send</button>
    </div>
  );
}

export default App;
