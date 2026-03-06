import { useEffect, useRef, useState } from 'react';
import './AnimatedCounter.scss';

interface AnimatedCounterProps {
  end: number;
  duration?: number;
  decimals?: number;
  suffix?: string;
  prefix?: string;
  start?: number;
}

export const AnimatedCounter: React.FC<AnimatedCounterProps> = ({
  end,
  duration = 2000,
  decimals = 0,
  suffix = '',
  prefix = '',
  start = 0,
}) => {
  const [count, setCount] = useState(start);
  const countRef = useRef<HTMLSpanElement>(null);
  const observerRef = useRef<IntersectionObserver | null>(null);
  const hasAnimatedRef = useRef(false);

  useEffect(() => {
    if (!countRef.current) return;

    observerRef.current = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !hasAnimatedRef.current) {
          hasAnimatedRef.current = true;
          animateCount();
        }
      },
      { threshold: 0.1 }
    );

    observerRef.current.observe(countRef.current);

    return () => {
      if (observerRef.current) {
        observerRef.current.disconnect();
      }
    };
  }, []);

  const animateCount = () => {
    const startTime = Date.now();
    const startValue = start;
    const endValue = end;
    const diff = endValue - startValue;

    const updateCount = () => {
      const now = Date.now();
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);

      // Easing function (easeOutCubic)
      const easedProgress = 1 - Math.pow(1 - progress, 3);
      const currentValue = startValue + diff * easedProgress;

      setCount(currentValue);

      if (progress < 1) {
        requestAnimationFrame(updateCount);
      } else {
        setCount(endValue);
      }
    };

    requestAnimationFrame(updateCount);
  };

  const formattedValue = count.toFixed(decimals);

  return (
    <span ref={countRef} className="animated-counter">
      {prefix}
      {formattedValue}
      {suffix}
    </span>
  );
};
