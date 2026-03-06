import './Skeleton.scss';

interface SkeletonProps {
  width?: string | number;
  height?: string | number;
  variant?: 'text' | 'circular' | 'rectangular' | 'rounded';
  animation?: 'pulse' | 'wave' | 'none';
  className?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({
  width,
  height,
  variant = 'rectangular',
  animation = 'pulse',
  className = '',
}) => {
  const style = {
    width: typeof width === 'number' ? `${width}px` : width,
    height: typeof height === 'number' ? `${height}px` : height,
  };

  return (
    <div
      className={`skeleton skeleton-${variant} skeleton-${animation} ${className}`}
      style={style}
      aria-busy="true"
      aria-live="polite"
    />
  );
};

// Pre-built skeleton patterns for common use cases
export const CardSkeleton: React.FC = () => (
  <div className="card-skeleton">
    <Skeleton height={200} variant="rounded" />
    <div className="card-skeleton-content">
      <Skeleton width="60%" height={24} />
      <Skeleton width="100%" height={16} />
      <Skeleton width="100%" height={16} />
      <Skeleton width="80%" height={16} />
    </div>
  </div>
);

export const ListSkeleton: React.FC<{ count?: number }> = ({ count = 5 }) => (
  <div className="list-skeleton">
    {Array.from({ length: count }).map((_, index) => (
      <div key={index} className="list-skeleton-item">
        <Skeleton variant="circular" width={40} height={40} />
        <div className="list-skeleton-text">
          <Skeleton width="70%" height={16} />
          <Skeleton width="40%" height={14} />
        </div>
      </div>
    ))}
  </div>
);

export const TableSkeleton: React.FC<{ rows?: number; cols?: number }> = ({
  rows = 5,
  cols = 4
}) => (
  <div className="table-skeleton">
    <div className="table-skeleton-header">
      {Array.from({ length: cols }).map((_, index) => (
        <Skeleton key={index} height={40} />
      ))}
    </div>
    {Array.from({ length: rows }).map((_, rowIndex) => (
      <div key={rowIndex} className="table-skeleton-row">
        {Array.from({ length: cols }).map((_, colIndex) => (
          <Skeleton key={colIndex} height={48} />
        ))}
      </div>
    ))}
  </div>
);

export const TheorySkeleton: React.FC = () => (
  <div className="theory-skeleton">
    <Skeleton width="40%" height={36} />
    <Skeleton width="100%" height={20} />
    <Skeleton width="100%" height={20} />
    <Skeleton width="90%" height={20} />
    <div className="theory-skeleton-section">
      <Skeleton width="30%" height={28} />
      <Skeleton width="100%" height={16} />
      <Skeleton width="100%" height={16} />
      <Skeleton width="95%" height={16} />
    </div>
    <div className="theory-skeleton-section">
      <Skeleton width="35%" height={28} />
      <Skeleton width="100%" height={16} />
      <Skeleton width="100%" height={16} />
    </div>
  </div>
);
