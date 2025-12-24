import React, { useEffect } from 'react';

const TextSelectionPlugin = () => {
  useEffect(() => {
    const handleMouseUp = () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText && selectedText.length > 10) { // Only show for meaningful selections
        showContextMenu(selectedText);
      }
    };

    const showContextMenu = (text) => {
      // Remove any existing context menu
      const existingMenu = document.getElementById('text-selection-context-menu');
      if (existingMenu) existingMenu.remove();

      // Create context menu
      const menu = document.createElement('div');
      menu.id = 'text-selection-context-menu';
      menu.innerHTML = `
        <div style="
          position: fixed;
          background: #25c2a0;
          color: white;
          padding: 8px 12px;
          border-radius: 4px;
          font-size: 14px;
          cursor: pointer;
          z-index: 10000;
          box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        " id="ask-ai-button">
          Ask AI
        </div>
      `;

      // Position the menu near the selection
      const selection = window.getSelection();
      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        menu.style.left = rect.left + 'px';
        menu.style.top = (rect.top - 40) + 'px';
      } else {
        // Fallback to mouse position
        const mouseEvent = window.event;
        if (mouseEvent) {
          menu.style.left = mouseEvent.clientX + 'px';
          menu.style.top = (mouseEvent.clientY - 40) + 'px';
        }
      }

      document.body.appendChild(menu);

      // Add click handler
      document.getElementById('ask-ai-button').onclick = () => {
        openChatWithText(selectedText);
        menu.remove();
      };

      // Remove menu when clicking elsewhere
      setTimeout(() => {
        document.addEventListener('click', removeMenuOnce);
      }, 100);
    };

    const removeMenuOnce = () => {
      const menu = document.getElementById('text-selection-context-menu');
      if (menu) {
        menu.remove();
        document.removeEventListener('click', removeMenuOnce);
      }
    };

    const openChatWithText = (text) => {
      // Store the selected text in sessionStorage to pass to chat
      sessionStorage.setItem('selectedTextForChat', text);
      // Navigate to chat page
      window.location.href = '/chat';
    };

    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, []);

  return null;
};

export default TextSelectionPlugin;