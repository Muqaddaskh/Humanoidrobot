import React, { useState, useRef, useEffect } from 'react';
import Layout from '@theme/Layout';
import './chat.css';

// Define the structure of a chat message
type Message = {
  type: 'user' | 'bot';
  content: string;
};

const ChatPage = () => {
  // State to store all messages in the chat
  const [messages, setMessages] = useState<Message[]>([]);

  // State for the chat input (asking a question)
  const [inputValue, setInputValue] = useState('');

  // State for the placeholder text to be translated
  const [selectedText, setSelectedText] = useState('');

  // Loading state for async operations
  const [isLoading, setIsLoading] = useState(false);

  // Reference to scroll chat to the bottom automatically
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom whenever messages update
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // -----------------------
  // Handle sending a normal user question
  // -----------------------
  const handleUserSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user's message to chat
    setMessages(prev => [...prev, { type: 'user', content: inputValue }]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Simulate backend response (replace with Gemini API later)
      const response = await simulateBackendCall(inputValue);
      setMessages(prev => [...prev, { type: 'bot', content: response }]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { type: 'bot', content: 'Sorry, translation or answer failed.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // -----------------------
  // Handle Translate to Urdu button
  // -----------------------
  const handleTranslate = async () => {
    if (!selectedText.trim()) {
      alert('Please paste text first.');
      return;
    }

    setIsLoading(true);

    try {
      // Split text into sentences for sentence-wise translation
      const sentences = selectedText.match(/[^\.!\?]+[\.!\?]+/g) || [selectedText];

      // Simulate translation for each sentence
      const translatedSentences = sentences.map(sentence => `اردو ترجمہ: ${sentence}`);

      // Join translated sentences
      const translatedText = translatedSentences.join(' ');

      // Add translated text to chat messages
      setMessages(prev => [...prev, { type: 'bot', content: translatedText }]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { type: 'bot', content: 'Sorry, translation failed.' },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // -----------------------
  // Simulated backend call
  // Replace this function with Gemini API call for real translations
  // -----------------------
  const simulateBackendCall = async (text: string): Promise<string> => {
    return new Promise(resolve => {
      setTimeout(() => {
        resolve(`Simulated answer: ${text}`);
      }, 1000);
    });
  };

  return (
    <Layout title="AI Assistant" description="PhysicalAI Textbook AI Assistant">
      <div className="chat-container">
        <div className="chat-header">
          <h1>PhysicalAI Textbook AI Assistant</h1>
          <p>Ask questions or translate selected text</p>
        </div>

        {/* Chat messages display */}
        <div className="chat-box">
          {messages.map((msg, index) => (
            <div key={index} className={`msg ${msg.type}`}>
              {msg.content}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Placeholder input for text to translate */}
        <textarea
          value={selectedText}
          onChange={(e) => setSelectedText(e.target.value)}
          placeholder="Paste text here to translate..."
          rows={4}
          style={{
            width: '100%',
            padding: '0.5rem',
            marginTop: '1rem',
            borderRadius: '8px',
            border: '1px solid #ccc',
          }}
        />

        {/* Translate button */}
        <div className="chat-input" style={{ marginTop: '0.5rem' }}>
          <button onClick={handleTranslate} disabled={isLoading}>
            Translate to Urdu
          </button>
        </div>

        {/* Chat input for normal questions */}
        <form className="chat-input" onSubmit={handleUserSubmit}>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask a question about humanoid robotics..."
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading}>
            Send
          </button>
        </form>

        {isLoading && (
          <div style={{ marginTop: '0.5rem', fontStyle: 'italic' }}>Loading...</div>
        )}
      </div>
    </Layout>
  );
};

export default ChatPage;
