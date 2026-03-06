import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import type { SidebarStore } from './types';

const initialState = {
  expandedSections: new Set<string>(['theory', 'derivations', 'calculations', 'visualizations']),
  expandedItems: new Set<string>([]),
  searchQuery: '',
  pinnedItems: [],
  recentItems: [],
  activeItemId: null,
};

export const useSidebarStore = create<SidebarStore>()(
  devtools(
    persist(
      (set, get) => ({
        ...initialState,

        toggleSection: (sectionId: string) =>
          set((state) => {
            const newExpanded = new Set(state.expandedSections);
            if (newExpanded.has(sectionId)) {
              newExpanded.delete(sectionId);
            } else {
              newExpanded.add(sectionId);
            }
            return { expandedSections: newExpanded };
          }),

        toggleItem: (itemId: string) =>
          set((state) => {
            const newExpanded = new Set(state.expandedItems);
            if (newExpanded.has(itemId)) {
              newExpanded.delete(itemId);
            } else {
              newExpanded.add(itemId);
            }
            return { expandedItems: newExpanded };
          }),

        setSearchQuery: (query: string) =>
          set({ searchQuery: query }),

        addPinnedItem: (itemId: string) =>
          set((state) => ({
            pinnedItems: state.pinnedItems.includes(itemId)
              ? state.pinnedItems
              : [...state.pinnedItems, itemId],
          })),

        removePinnedItem: (itemId: string) =>
          set((state) => ({
            pinnedItems: state.pinnedItems.filter((id) => id !== itemId),
          })),

        addRecentItem: (itemId: string) =>
          set((state) => {
            const filtered = state.recentItems.filter((id) => id !== itemId);
            const updated = [itemId, ...filtered].slice(0, 10); // Keep last 10 items
            return { recentItems: updated };
          }),

        setActiveItem: (itemId: string | null) =>
          set({ activeItemId: itemId }),

        expandAll: () => {
          const allSectionIds = ['theory', 'derivations', 'calculations', 'visualizations', 'explanations', 'results'];
          set({
            expandedSections: new Set(allSectionIds),
            expandedItems: new Set(get().expandedItems), // Keep items as they are
          });
        },

        collapseAll: () =>
          set({
            expandedSections: new Set(),
            expandedItems: new Set(),
          }),

        reset: () => set(initialState),
      }),
      {
        name: 'sidebar-storage',
        partialize: (state) => ({
          expandedSections: Array.from(state.expandedSections),
          expandedItems: Array.from(state.expandedItems),
          pinnedItems: state.pinnedItems,
          recentItems: state.recentItems,
        }),
        // Custom serializer for Set objects
        merge: (persistedState, currentState) => {
          const persisted = persistedState as Partial<{
            expandedSections: string[];
            expandedItems: string[];
            pinnedItems: string[];
            recentItems: string[];
          }>;

          return {
            ...currentState,
            expandedSections: new Set(persisted.expandedSections || []),
            expandedItems: new Set(persisted.expandedItems || []),
            pinnedItems: persisted.pinnedItems || [],
            recentItems: persisted.recentItems || [],
          };
        },
      }
    ),
    {
      name: 'SidebarStore',
    }
  )
);
