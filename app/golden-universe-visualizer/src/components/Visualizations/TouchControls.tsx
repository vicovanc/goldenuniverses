import React, { useRef, useEffect } from 'react';
import { useTouchGestures } from '@/hooks/useTouchGestures';
import { useIsTouchDevice } from '@/hooks/useMediaQuery';
import './TouchControls.scss';

interface TouchControlsProps {
  onPinch?: (scale: number, delta: number) => void;
  onRotate?: (angle: number, delta: number) => void;
  onPan?: (deltaX: number, deltaY: number) => void;
  onSwipe?: (direction: 'up' | 'down' | 'left' | 'right', velocity: number) => void;
  onDoubleTap?: (x: number, y: number) => void;
  onLongPress?: (x: number, y: number) => void;
  children: React.ReactNode;
  className?: string;
  showHints?: boolean;
}

/**
 * Wrapper component that adds touch gesture controls to 3D visualizations
 */
const TouchControls: React.FC<TouchControlsProps> = ({
  onPinch,
  onRotate,
  onPan,
  onSwipe,
  onDoubleTap,
  onLongPress,
  children,
  className = '',
  showHints = true,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const isTouchDevice = useIsTouchDevice();
  const [showTouchHints, setShowTouchHints] = React.useState(false);

  useTouchGestures(containerRef, {
    onPinch,
    onRotate,
    onPan,
    onSwipe,
    onDoubleTap,
    onLongPress,
  });

  useEffect(() => {
    if (isTouchDevice && showHints) {
      const hasSeenHints = localStorage.getItem('touch-hints-seen');
      if (!hasSeenHints) {
        setShowTouchHints(true);
        setTimeout(() => {
          setShowTouchHints(false);
          localStorage.setItem('touch-hints-seen', 'true');
        }, 5000);
      }
    }
  }, [isTouchDevice, showHints]);

  return (
    <div
      ref={containerRef}
      className={`touch-controls ${className}`}
      style={{ touchAction: 'none', userSelect: 'none' }}
    >
      {children}

      {showTouchHints && isTouchDevice && (
        <div className="touch-hints">
          <div className="touch-hint">
            <span className="hint-icon">👆</span>
            <span className="hint-text">Drag to rotate</span>
          </div>
          <div className="touch-hint">
            <span className="hint-icon">🤏</span>
            <span className="hint-text">Pinch to zoom</span>
          </div>
          <div className="touch-hint">
            <span className="hint-icon">👆👆</span>
            <span className="hint-text">Two fingers to rotate</span>
          </div>
          <div className="touch-hint">
            <span className="hint-icon">👆✕2</span>
            <span className="hint-text">Double tap to reset</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default TouchControls;
