import React from 'react';
import { useKeyboardShortcutsContext } from '@/contexts/KeyboardShortcutsContext';
import { formatShortcut } from '@/hooks/useKeyboardShortcuts';
import type { KeyboardShortcutGroup } from '@/types/keyboard';
import './KeyboardShortcutsModal.scss';

export function KeyboardShortcutsModal() {
  const { shortcuts, isShortcutsModalOpen, toggleShortcutsModal } =
    useKeyboardShortcutsContext();

  if (!isShortcutsModalOpen) return null;

  // Group shortcuts by category
  const groupedShortcuts: Record<string, KeyboardShortcutGroup> = {};
  shortcuts.forEach((shortcut) => {
    const category = shortcut.category || 'general';
    if (!groupedShortcuts[category]) {
      groupedShortcuts[category] = {
        category: category.charAt(0).toUpperCase() + category.slice(1),
        shortcuts: [],
      };
    }
    groupedShortcuts[category].shortcuts.push(shortcut);
  });

  const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      toggleShortcutsModal();
    }
  };

  return (
    <div
      className="keyboard-shortcuts-modal-backdrop"
      onClick={handleBackdropClick}
      role="dialog"
      aria-modal="true"
      aria-labelledby="shortcuts-modal-title"
    >
      <div className="keyboard-shortcuts-modal">
        <div className="modal-header">
          <h2 id="shortcuts-modal-title">Keyboard Shortcuts</h2>
          <button
            className="close-button"
            onClick={toggleShortcutsModal}
            aria-label="Close shortcuts modal"
          >
            ×
          </button>
        </div>
        <div className="modal-content">
          {Object.values(groupedShortcuts).map((group) => (
            <div key={group.category} className="shortcut-group">
              <h3 className="group-title">{group.category}</h3>
              <div className="shortcuts-list">
                {group.shortcuts.map((shortcut, index) => (
                  <div key={index} className="shortcut-item">
                    <span className="shortcut-description">{shortcut.description}</span>
                    <kbd className="shortcut-keys">{formatShortcut(shortcut)}</kbd>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
        <div className="modal-footer">
          <p className="footer-hint">Press ? to toggle this dialog</p>
        </div>
      </div>
    </div>
  );
}
