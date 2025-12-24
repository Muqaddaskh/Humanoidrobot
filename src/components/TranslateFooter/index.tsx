// src/components/Translatefooter/Footer/index.tsx
import React from 'react';

type ChatFooterProps = {
  onTranslate: (selectedText: string) => void; // keep function type
};

const ChatFooter: React.FC<ChatFooterProps> = ({ onTranslate }) => {
  const handleButtonClick = () => {
    const selectedText = window.getSelection()?.toString() || '';
    if (!selectedText) {
      alert('Please select some text first.');
      return;
    }
    onTranslate(selectedText);
  };

  // ✅ Keep your original UI styling intact
  return (
    <div style={{ marginTop: '1rem', textAlign: 'right' }}>
      <button
        onClick={handleButtonClick}
        style={{
          padding: '8px 12px',
          borderRadius: '6px',
          background: '#0ca031',
          color: 'white',
          border: 'none',
          cursor: 'pointer',
        }}
      >
        Translate to Urdu
      </button>
    </div>
  );
};

export default ChatFooter;
