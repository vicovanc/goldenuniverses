import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import type { KeyboardShortcut, ShortcutContextValue } from '@/types/keyboard';

const KeyboardShortcutsContext = createContext<ShortcutContextValue | undefined>(undefined);

export function KeyboardShortcutsProvider({ children }: { children: ReactNode }) {
  const [shortcuts, setShortcuts] = useState<KeyboardShortcut[]>([]);
  const [isShortcutsModalOpen, setIsShortcutsModalOpen] = useState(false);

  const registerShortcut = useCallback((shortcut: KeyboardShortcut) => {
    setShortcuts((prev) => {
      // Remove existing shortcut with same key combination
      const filtered = prev.filter(
        (s) =>
          !(
            s.key === shortcut.key &&
            s.ctrlKey === shortcut.ctrlKey &&
            s.shiftKey === shortcut.shiftKey &&
            s.altKey === shortcut.altKey &&
            s.metaKey === shortcut.metaKey
          )
      );
      return [...filtered, shortcut];
    });
  }, []);

  const unregisterShortcut = useCallback((key: string) => {
    setShortcuts((prev) => prev.filter((s) => s.key !== key));
  }, []);

  const toggleShortcutsModal = useCallback(() => {
    setIsShortcutsModalOpen((prev) => !prev);
  }, []);

  const value: ShortcutContextValue = {
    shortcuts,
    registerShortcut,
    unregisterShortcut,
    isShortcutsModalOpen,
    toggleShortcutsModal,
  };

  return (
    <KeyboardShortcutsContext.Provider value={value}>
      {children}
    </KeyboardShortcutsContext.Provider>
  );
}

export function useKeyboardShortcutsContext() {
  const context = useContext(KeyboardShortcutsContext);
  if (!context) {
    throw new Error(
      'useKeyboardShortcutsContext must be used within KeyboardShortcutsProvider'
    );
  }
  return context;
}
