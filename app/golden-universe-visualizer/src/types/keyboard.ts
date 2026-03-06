export interface KeyboardShortcut {
  key: string;
  ctrlKey?: boolean;
  shiftKey?: boolean;
  altKey?: boolean;
  metaKey?: boolean;
  description: string;
  action: () => void;
  enabled?: boolean;
  category?: 'navigation' | 'search' | 'ui' | 'general';
}

export interface KeyboardShortcutGroup {
  category: string;
  shortcuts: KeyboardShortcut[];
}

export interface ShortcutContextValue {
  shortcuts: KeyboardShortcut[];
  registerShortcut: (shortcut: KeyboardShortcut) => void;
  unregisterShortcut: (key: string) => void;
  isShortcutsModalOpen: boolean;
  toggleShortcutsModal: () => void;
}
