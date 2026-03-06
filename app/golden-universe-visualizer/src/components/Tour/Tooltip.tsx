import React from 'react';
import './Tooltip.scss';

interface TooltipProps {
  content: string;
  isVisible: boolean;
  position: { top: number; left: number };
}

export function Tooltip({ content, isVisible, position }: TooltipProps) {
  if (!isVisible || !content) return null;

  return (
    <div
      className="custom-tooltip"
      style={{
        top: `${position.top}px`,
        left: `${position.left}px`,
      }}
      role="tooltip"
    >
      {content}
    </div>
  );
}
