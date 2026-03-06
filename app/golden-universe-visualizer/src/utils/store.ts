import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import type { AppState } from '@/types';

interface AppStore extends AppState {
  setCurrentSection: (section: string) => void;
  toggleSidebar: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

const initialState: AppState = {
  currentSection: 'home',
  sidebarCollapsed: false,
  theme: 'dark',
  loading: false,
  error: null,
};

export const useAppStore = create<AppStore>()(
  devtools(
    persist(
      (set) => ({
        ...initialState,

        setCurrentSection: (section: string) =>
          set({ currentSection: section, error: null }),

        toggleSidebar: () =>
          set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),

        setTheme: (theme: 'light' | 'dark') =>
          set({ theme }),

        setLoading: (loading: boolean) =>
          set({ loading }),

        setError: (error: string | null) =>
          set({ error, loading: false }),

        reset: () => set(initialState),
      }),
      {
        name: 'golden-universe-storage',
        partialize: (state) => ({
          theme: state.theme,
          sidebarCollapsed: state.sidebarCollapsed,
        }),
      }
    ),
    {
      name: 'GoldenUniverseStore',
    }
  )
);
