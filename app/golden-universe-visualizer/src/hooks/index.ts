export { useKeyboardShortcuts, formatShortcut } from './useKeyboardShortcuts';
export { useLocalStorage } from './useLocalStorage';
export { useTooltip } from './useTooltip';
export { useGuidedTour } from './useGuidedTour';
export { useFocusManagement } from './useFocusManagement';
export { useAnnouncer } from './useAnnouncer';
export { useTheme } from './useTheme';

// Media query hooks
export {
  useMediaQuery,
  useIsMobile,
  useIsTablet,
  useIsDesktop,
  useIsMobileOrTablet,
  useIsLandscape,
  useIsPortrait,
  useIsTouchDevice,
  useBreakpoint,
  useResponsiveValue,
  type Breakpoint,
} from './useMediaQuery';

// Touch gesture hooks
export { useTouchGestures, type TouchGestureHandlers } from './useTouchGestures';

// Performance hooks
export {
  useConnectionQuality,
  useReducedMotion,
  useAdaptiveLoading,
  useRenderTime,
  usePageVisibility,
  useIdleCallback,
  useIntersectionObserver,
  usePrefetch,
  useBatchedState,
} from './usePerformance';
