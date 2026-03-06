import React, { useEffect, useState } from 'react';
import { promptInstall, isAppInstalled } from '@/utils/pwa';
import './InstallPrompt.scss';

interface InstallPromptProps {
  className?: string;
}

/**
 * Component to prompt users to install the PWA
 */
const InstallPrompt: React.FC<InstallPromptProps> = ({ className = '' }) => {
  const [showPrompt, setShowPrompt] = useState(false);
  const [isInstalling, setIsInstalling] = useState(false);

  useEffect(() => {
    // Check if app is already installed
    if (isAppInstalled()) {
      setShowPrompt(false);
      return;
    }

    // Check if user has dismissed the prompt before
    const dismissed = localStorage.getItem('install-prompt-dismissed');
    if (dismissed) {
      const dismissedTime = parseInt(dismissed, 10);
      const daysSinceDismissed = (Date.now() - dismissedTime) / (1000 * 60 * 60 * 24);

      // Show again after 7 days
      if (daysSinceDismissed < 7) {
        return;
      }
    }

    // Listen for installable event
    const handleInstallable = (event: Event) => {
      const customEvent = event as CustomEvent;
      if (customEvent.detail.canInstall) {
        setShowPrompt(true);
      }
    };

    window.addEventListener('pwa:installable', handleInstallable);

    return () => {
      window.removeEventListener('pwa:installable', handleInstallable);
    };
  }, []);

  const handleInstall = async () => {
    setIsInstalling(true);
    const outcome = await promptInstall();

    if (outcome === 'accepted') {
      setShowPrompt(false);
    } else if (outcome === 'dismissed') {
      handleDismiss();
    }

    setIsInstalling(false);
  };

  const handleDismiss = () => {
    setShowPrompt(false);
    localStorage.setItem('install-prompt-dismissed', Date.now().toString());
  };

  if (!showPrompt) {
    return null;
  }

  return (
    <div className={`install-prompt ${className}`} role="dialog" aria-label="Install app">
      <div className="install-prompt__content">
        <div className="install-prompt__icon">📱</div>
        <div className="install-prompt__text">
          <h3 className="install-prompt__title">Install Golden Universe</h3>
          <p className="install-prompt__description">
            Install the app for a better experience with offline access
          </p>
        </div>
        <div className="install-prompt__actions">
          <button
            className="install-prompt__button install-prompt__button--primary"
            onClick={handleInstall}
            disabled={isInstalling}
          >
            {isInstalling ? 'Installing...' : 'Install'}
          </button>
          <button
            className="install-prompt__button install-prompt__button--secondary"
            onClick={handleDismiss}
            disabled={isInstalling}
          >
            Not Now
          </button>
        </div>
      </div>
    </div>
  );
};

export default InstallPrompt;
