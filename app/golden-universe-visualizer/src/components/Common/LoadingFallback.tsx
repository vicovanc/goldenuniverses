/**
 * Loading fallback component for lazy-loaded routes
 * Displays during code-split chunk loading
 */

import './LoadingFallback.scss';

interface LoadingFallbackProps {
  message?: string;
}

const LoadingFallback: React.FC<LoadingFallbackProps> = ({
  message = 'Loading...'
}) => {
  return (
    <div className="loading-fallback">
      <div className="loading-spinner">
        <div className="spinner-ring"></div>
        <div className="spinner-ring"></div>
        <div className="spinner-ring"></div>
      </div>
      <p className="loading-message">{message}</p>
    </div>
  );
};

export default LoadingFallback;
