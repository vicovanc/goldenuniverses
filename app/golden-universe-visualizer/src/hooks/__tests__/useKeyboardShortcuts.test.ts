import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useKeyboardShortcuts, formatShortcut } from '../useKeyboardShortcuts';
import type { KeyboardShortcut } from '@/types/keyboard';

describe('useKeyboardShortcuts', () => {
  let mockAction: any;

  beforeEach(() => {
    mockAction = vi.fn();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('Basic functionality', () => {
    it('should register keyboard shortcuts', () => {
      const shortcuts: KeyboardShortcut[] = [
        {
          key: 's',
          ctrlKey: true,
          description: 'Save',
          action: mockAction,
        },
      ];

      renderHook(() => useKeyboardShortcuts(shortcuts));

      act(() => {
        const event = new KeyboardEvent('keydown', {
          key: 's',
          ctrlKey: true,
        });
        window.dispatchEvent(event);
      });

      expect(mockAction).toHaveBeenCalledTimes(1);
    });

    it('should not trigger shortcuts when disabled', () => {
      const shortcuts: KeyboardShortcut[] = [
        {
          key: 's',
          ctrlKey: true,
          description: 'Save',
          action: mockAction,
        },
      ];

      renderHook(() => useKeyboardShortcuts(shortcuts, { enabled: false }));

      act(() => {
        const event = new KeyboardEvent('keydown', {
          key: 's',
          ctrlKey: true,
        });
        window.dispatchEvent(event);
      });

      expect(mockAction).not.toHaveBeenCalled();
    });

    it('should cleanup event listeners on unmount', () => {
      const removeEventListener = vi.spyOn(window, 'removeEventListener');

      const shortcuts: KeyboardShortcut[] = [
        {
          key: 's',
          ctrlKey: true,
          description: 'Save',
          action: mockAction,
        },
      ];

      const { unmount } = renderHook(() => useKeyboardShortcuts(shortcuts));
      unmount();

      expect(removeEventListener).toHaveBeenCalledWith('keydown', expect.any(Function));
    });
  });

  describe('Modifier keys', () => {
    it('should handle ctrl key', () => {
      const shortcuts: KeyboardShortcut[] = [
        {
          key: 's',
          ctrlKey: true,
          description: 'Save',
          action: mockAction,
        },
      ];

      renderHook(() => useKeyboardShortcuts(shortcuts));

      act(() => {
        const event = new KeyboardEvent('keydown', { key: 's', ctrlKey: true });
        window.dispatchEvent(event);
      });

      expect(mockAction).toHaveBeenCalled();

      mockAction.mockClear();

      act(() => {
        const event = new KeyboardEvent('keydown', { key: 's', ctrlKey: false });
        window.dispatchEvent(event);
      });

      expect(mockAction).not.toHaveBeenCalled();
    });

    it('should handle shift key', () => {
      const shortcuts: KeyboardShortcut[] = [
        {
          key: 'k',
          ctrlKey: true,
          shiftKey: true,
          description: 'Command palette',
          action: mockAction,
        },
      ];

      renderHook(() => useKeyboardShortcuts(shortcuts));

      act(() => {
        const event = new KeyboardEvent('keydown', {
          key: 'k',
          ctrlKey: true,
          shiftKey: true,
        });
        window.dispatchEvent(event);
      });

      expect(mockAction).toHaveBeenCalled();
    });

    it('should handle alt key', () => {
      const shortcuts: KeyboardShortcut[] = [
        {
          key: 'f',
          altKey: true,
          description: 'Menu',
          action: mockAction,
        },
      ];

      renderHook(() => useKeyboardShortcuts(shortcuts));

      act(() => {
        const event = new KeyboardEvent('keydown', { key: 'f', altKey: true });
        window.dispatchEvent(event);
      });

      expect(mockAction).toHaveBeenCalled();
    });

    it('should handle meta key', () => {
      const shortcuts: KeyboardShortcut[] = [
        {
          key: 's',
          metaKey: true,
          description: 'Save (Mac)',
          action: mockAction,
        },
      ];

      renderHook(() => useKeyboardShortcuts(shortcuts));

      act(() => {
        const event = new KeyboardEvent('keydown', { key: 's', metaKey: true });
        window.dispatchEvent(event);
      });

      expect(mockAction).toHaveBeenCalled();
    });
  });

  describe('Input field handling', () => {
    it('should not trigger shortcuts in input fields', () => {
      const shortcuts: KeyboardShortcut[] = [
        {
          key: 's',
          ctrlKey: true,
          description: 'Save',
          action: mockAction,
        },
      ];

      renderHook(() => useKeyboardShortcuts(shortcuts));

      const input = document.createElement('input');
      document.body.appendChild(input);

      act(() => {
        const event = new KeyboardEvent('keydown', {
          key: 's',
          ctrlKey: true,
          bubbles: true,
        });
        Object.defineProperty(event, 'target', { value: input, enumerable: true });
        window.dispatchEvent(event);
      });

      expect(mockAction).not.toHaveBeenCalled();

      document.body.removeChild(input);
    });

    it('should not trigger shortcuts in textarea', () => {
      const shortcuts: KeyboardShortcut[] = [
        {
          key: 's',
          ctrlKey: true,
          description: 'Save',
          action: mockAction,
        },
      ];

      renderHook(() => useKeyboardShortcuts(shortcuts));

      const textarea = document.createElement('textarea');
      document.body.appendChild(textarea);

      act(() => {
        const event = new KeyboardEvent('keydown', {
          key: 's',
          ctrlKey: true,
          bubbles: true,
        });
        Object.defineProperty(event, 'target', { value: textarea, enumerable: true });
        window.dispatchEvent(event);
      });

      expect(mockAction).not.toHaveBeenCalled();

      document.body.removeChild(textarea);
    });

    it('should allow Escape key in input fields', () => {
      const shortcuts: KeyboardShortcut[] = [
        {
          key: 'Escape',
          description: 'Close',
          action: mockAction,
        },
      ];

      renderHook(() => useKeyboardShortcuts(shortcuts));

      const input = document.createElement('input');
      document.body.appendChild(input);

      act(() => {
        const event = new KeyboardEvent('keydown', {
          key: 'Escape',
          bubbles: true,
        });
        Object.defineProperty(event, 'target', { value: input, enumerable: true });
        window.dispatchEvent(event);
      });

      expect(mockAction).toHaveBeenCalled();

      document.body.removeChild(input);
    });
  });

  describe('preventDefault option', () => {
    it('should prevent default by default', () => {
      const shortcuts: KeyboardShortcut[] = [
        {
          key: 's',
          ctrlKey: true,
          description: 'Save',
          action: mockAction,
        },
      ];

      renderHook(() => useKeyboardShortcuts(shortcuts));

      act(() => {
        const event = new KeyboardEvent('keydown', {
          key: 's',
          ctrlKey: true,
        });
        const preventDefaultSpy = vi.spyOn(event, 'preventDefault');
        window.dispatchEvent(event);

        expect(preventDefaultSpy).toHaveBeenCalled();
      });
    });

    it('should not prevent default when disabled', () => {
      const shortcuts: KeyboardShortcut[] = [
        {
          key: 's',
          ctrlKey: true,
          description: 'Save',
          action: mockAction,
        },
      ];

      renderHook(() => useKeyboardShortcuts(shortcuts, { preventDefault: false }));

      act(() => {
        const event = new KeyboardEvent('keydown', {
          key: 's',
          ctrlKey: true,
        });
        const preventDefaultSpy = vi.spyOn(event, 'preventDefault');
        window.dispatchEvent(event);

        expect(preventDefaultSpy).not.toHaveBeenCalled();
      });
    });
  });

  describe('Disabled shortcuts', () => {
    it('should not trigger disabled shortcuts', () => {
      const shortcuts: KeyboardShortcut[] = [
        {
          key: 's',
          ctrlKey: true,
          description: 'Save',
          action: mockAction,
          enabled: false,
        },
      ];

      renderHook(() => useKeyboardShortcuts(shortcuts));

      act(() => {
        const event = new KeyboardEvent('keydown', { key: 's', ctrlKey: true });
        window.dispatchEvent(event);
      });

      expect(mockAction).not.toHaveBeenCalled();
    });
  });

  describe('Case insensitivity', () => {
    it('should match keys case-insensitively', () => {
      const shortcuts: KeyboardShortcut[] = [
        {
          key: 's',
          ctrlKey: true,
          description: 'Save',
          action: mockAction,
        },
      ];

      renderHook(() => useKeyboardShortcuts(shortcuts));

      act(() => {
        const event = new KeyboardEvent('keydown', { key: 'S', ctrlKey: true });
        window.dispatchEvent(event);
      });

      expect(mockAction).toHaveBeenCalled();
    });
  });
});

describe('formatShortcut', () => {
  const originalPlatform = navigator.platform;

  afterEach(() => {
    Object.defineProperty(navigator, 'platform', {
      value: originalPlatform,
      configurable: true,
    });
  });

  it('should format shortcut with Ctrl on non-Mac', () => {
    Object.defineProperty(navigator, 'platform', {
      value: 'Win32',
      configurable: true,
    });

    const shortcut: KeyboardShortcut = {
      key: 's',
      ctrlKey: true,
      description: 'Save',
      action: vi.fn(),
    };

    expect(formatShortcut(shortcut)).toBe('Ctrl + S');
  });

  it('should format shortcut with Command on Mac', () => {
    Object.defineProperty(navigator, 'platform', {
      value: 'MacIntel',
      configurable: true,
    });

    const shortcut: KeyboardShortcut = {
      key: 's',
      ctrlKey: true,
      description: 'Save',
      action: vi.fn(),
    };

    expect(formatShortcut(shortcut)).toBe('⌘ + S');
  });

  it('should format shortcut with Shift', () => {
    const shortcut: KeyboardShortcut = {
      key: 'k',
      ctrlKey: true,
      shiftKey: true,
      description: 'Command palette',
      action: vi.fn(),
    };

    const formatted = formatShortcut(shortcut);
    expect(formatted).toContain('Shift');
    expect(formatted).toContain('K');
  });

  it('should format shortcut with Alt', () => {
    const shortcut: KeyboardShortcut = {
      key: 'f',
      altKey: true,
      description: 'Menu',
      action: vi.fn(),
    };

    const formatted = formatShortcut(shortcut);
    expect(formatted).toContain('Alt');
    expect(formatted).toContain('F');
  });

  it('should capitalize single letter keys', () => {
    const shortcut: KeyboardShortcut = {
      key: 'a',
      description: 'Action',
      action: vi.fn(),
    };

    expect(formatShortcut(shortcut)).toBe('A');
  });

  it('should capitalize multi-letter keys', () => {
    const shortcut: KeyboardShortcut = {
      key: 'escape',
      description: 'Close',
      action: vi.fn(),
    };

    expect(formatShortcut(shortcut)).toBe('Escape');
  });
});
