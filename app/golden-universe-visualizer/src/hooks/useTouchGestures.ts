import { useEffect, useRef, useCallback } from 'react';

export interface TouchGestureHandlers {
  onPinch?: (scale: number, delta: number) => void;
  onRotate?: (angle: number, delta: number) => void;
  onPan?: (deltaX: number, deltaY: number) => void;
  onSwipe?: (direction: 'up' | 'down' | 'left' | 'right', velocity: number) => void;
  onDoubleTap?: (x: number, y: number) => void;
  onLongPress?: (x: number, y: number) => void;
}

interface TouchPoint {
  x: number;
  y: number;
  identifier: number;
}

interface GestureState {
  touches: TouchPoint[];
  lastDistance: number;
  lastAngle: number;
  lastCenter: { x: number; y: number };
  initialTap: { x: number; y: number; time: number } | null;
  lastTapTime: number;
  longPressTimer: NodeJS.Timeout | null;
}

const DOUBLE_TAP_DELAY = 300; // ms
const LONG_PRESS_DELAY = 500; // ms
const SWIPE_THRESHOLD = 50; // pixels
const SWIPE_VELOCITY_THRESHOLD = 0.3; // pixels per ms

/**
 * Custom hook for handling touch gestures on 3D visualizations
 */
export function useTouchGestures(
  elementRef: React.RefObject<HTMLElement>,
  handlers: TouchGestureHandlers
) {
  const stateRef = useRef<GestureState>({
    touches: [],
    lastDistance: 0,
    lastAngle: 0,
    lastCenter: { x: 0, y: 0 },
    initialTap: null,
    lastTapTime: 0,
    longPressTimer: null,
  });

  const getDistance = useCallback((touch1: TouchPoint, touch2: TouchPoint): number => {
    const dx = touch2.x - touch1.x;
    const dy = touch2.y - touch1.y;
    return Math.sqrt(dx * dx + dy * dy);
  }, []);

  const getAngle = useCallback((touch1: TouchPoint, touch2: TouchPoint): number => {
    return Math.atan2(touch2.y - touch1.y, touch2.x - touch1.x) * (180 / Math.PI);
  }, []);

  const getCenter = useCallback((touch1: TouchPoint, touch2: TouchPoint) => {
    return {
      x: (touch1.x + touch2.x) / 2,
      y: (touch1.y + touch2.y) / 2,
    };
  }, []);

  const getTouches = useCallback((event: TouchEvent): TouchPoint[] => {
    const touches: TouchPoint[] = [];
    for (let i = 0; i < event.touches.length; i++) {
      const touch = event.touches[i];
      touches.push({
        x: touch.clientX,
        y: touch.clientY,
        identifier: touch.identifier,
      });
    }
    return touches;
  }, []);

  const handleTouchStart = useCallback(
    (event: TouchEvent) => {
      const state = stateRef.current;
      const touches = getTouches(event);
      state.touches = touches;

      if (touches.length === 1) {
        const touch = touches[0];
        const now = Date.now();

        // Check for double tap
        if (
          state.lastTapTime &&
          now - state.lastTapTime < DOUBLE_TAP_DELAY &&
          handlers.onDoubleTap
        ) {
          handlers.onDoubleTap(touch.x, touch.y);
          state.lastTapTime = 0;
          state.initialTap = null;
        } else {
          state.lastTapTime = now;
          state.initialTap = { x: touch.x, y: touch.y, time: now };

          // Start long press timer
          if (handlers.onLongPress) {
            state.longPressTimer = setTimeout(() => {
              if (handlers.onLongPress) {
                handlers.onLongPress(touch.x, touch.y);
              }
              state.initialTap = null;
            }, LONG_PRESS_DELAY);
          }
        }
      } else if (touches.length === 2) {
        // Clear single touch timers
        if (state.longPressTimer) {
          clearTimeout(state.longPressTimer);
          state.longPressTimer = null;
        }
        state.initialTap = null;

        // Initialize two-finger gestures
        state.lastDistance = getDistance(touches[0], touches[1]);
        state.lastAngle = getAngle(touches[0], touches[1]);
        state.lastCenter = getCenter(touches[0], touches[1]);
      }
    },
    [handlers, getTouches, getDistance, getAngle, getCenter]
  );

  const handleTouchMove = useCallback(
    (event: TouchEvent) => {
      event.preventDefault();
      const state = stateRef.current;
      const touches = getTouches(event);

      if (touches.length === 1 && state.touches.length === 1) {
        // Pan gesture
        const deltaX = touches[0].x - state.touches[0].x;
        const deltaY = touches[0].y - state.touches[0].y;

        if (handlers.onPan) {
          handlers.onPan(deltaX, deltaY);
        }

        // Clear long press if moved significantly
        if (
          state.longPressTimer &&
          state.initialTap &&
          (Math.abs(deltaX) > 10 || Math.abs(deltaY) > 10)
        ) {
          clearTimeout(state.longPressTimer);
          state.longPressTimer = null;
        }
      } else if (touches.length === 2 && state.touches.length === 2) {
        // Pinch gesture
        const distance = getDistance(touches[0], touches[1]);
        const deltaDistance = distance - state.lastDistance;

        if (handlers.onPinch && Math.abs(deltaDistance) > 1) {
          const scale = distance / state.lastDistance;
          handlers.onPinch(scale, deltaDistance);
          state.lastDistance = distance;
        }

        // Rotate gesture
        const angle = getAngle(touches[0], touches[1]);
        const deltaAngle = angle - state.lastAngle;

        if (handlers.onRotate && Math.abs(deltaAngle) > 1) {
          handlers.onRotate(angle, deltaAngle);
          state.lastAngle = angle;
        }

        // Update center
        state.lastCenter = getCenter(touches[0], touches[1]);
      }

      state.touches = touches;
    },
    [handlers, getTouches, getDistance, getAngle, getCenter]
  );

  const handleTouchEnd = useCallback(
    (event: TouchEvent) => {
      const state = stateRef.current;

      // Clear long press timer
      if (state.longPressTimer) {
        clearTimeout(state.longPressTimer);
        state.longPressTimer = null;
      }

      // Check for swipe gesture
      if (
        state.touches.length === 1 &&
        state.initialTap &&
        handlers.onSwipe
      ) {
        const touch = state.touches[0];
        const deltaX = touch.x - state.initialTap.x;
        const deltaY = touch.y - state.initialTap.y;
        const deltaTime = Date.now() - state.initialTap.time;
        const absX = Math.abs(deltaX);
        const absY = Math.abs(deltaY);

        if (absX > SWIPE_THRESHOLD || absY > SWIPE_THRESHOLD) {
          const velocity = Math.max(absX, absY) / deltaTime;

          if (velocity > SWIPE_VELOCITY_THRESHOLD) {
            let direction: 'up' | 'down' | 'left' | 'right';

            if (absX > absY) {
              direction = deltaX > 0 ? 'right' : 'left';
            } else {
              direction = deltaY > 0 ? 'down' : 'up';
            }

            handlers.onSwipe(direction, velocity);
          }
        }
      }

      // Reset state
      state.touches = getTouches(event);
      state.initialTap = null;

      if (state.touches.length === 0) {
        state.lastDistance = 0;
        state.lastAngle = 0;
      }
    },
    [handlers, getTouches]
  );

  useEffect(() => {
    const element = elementRef.current;
    if (!element) return;

    element.addEventListener('touchstart', handleTouchStart, { passive: false });
    element.addEventListener('touchmove', handleTouchMove, { passive: false });
    element.addEventListener('touchend', handleTouchEnd);
    element.addEventListener('touchcancel', handleTouchEnd);

    return () => {
      element.removeEventListener('touchstart', handleTouchStart);
      element.removeEventListener('touchmove', handleTouchMove);
      element.removeEventListener('touchend', handleTouchEnd);
      element.removeEventListener('touchcancel', handleTouchEnd);

      // Clean up any remaining timer
      const state = stateRef.current;
      if (state.longPressTimer) {
        clearTimeout(state.longPressTimer);
      }
    };
  }, [elementRef, handleTouchStart, handleTouchMove, handleTouchEnd]);
}
