import { lazy, Suspense, useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { UXProvider } from '@/components/UXEnhancements/UXProvider';
import { ErrorBoundary } from '@/components/Common/ErrorBoundary';
import { AppHeader } from '@/components/Layout/AppHeader';
import MainLayout from '@components/Layout/MainLayout';
import LoadingFallback from '@components/Common/LoadingFallback';
import './styles/globals.scss';
import './styles/accessibility.scss';
import './styles/unified-clean-design.scss';
import './styles/light-mode-overrides.scss'; // MUST be last!

// Lazy load page components for code splitting
const Home = lazy(() => import('@/pages/Home'));
const Theory = lazy(() => import('@/pages/Theory'));
const Derivations = lazy(() => import('@/pages/Derivations'));
const Calculations = lazy(() => import('@/pages/Calculations'));
const Visualizations = lazy(() => import('@/pages/Visualizations'));
const Results = lazy(() => import('@/pages/Results'));
const Explanations = lazy(() => import('@/pages/Explanations'));
const About = lazy(() => import('@/pages/About'));
const NotFound = lazy(() => import('@/pages/NotFound'));

function App() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    // Watch for theme changes on the HTML element
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
          const htmlElement = document.documentElement;
          if (htmlElement.classList.contains('light')) {
            setTheme('light');
          } else if (htmlElement.classList.contains('dark')) {
            setTheme('dark');
          }
        }
      });
    });

    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class']
    });

    // Initial check
    if (document.documentElement.classList.contains('light')) {
      setTheme('light');
    } else if (document.documentElement.classList.contains('dark')) {
      setTheme('dark');
    }

    return () => observer.disconnect();
  }, []);

  return (
    <ErrorBoundary>
      <BrowserRouter>
        <UXProvider>
          <div className={`app ${theme}`}>
            <AppHeader />
            <Suspense fallback={<LoadingFallback />}>
              <Routes>
                <Route path="/" element={<MainLayout />}>
                  <Route index element={<Home />} />
                  <Route path="theory/*" element={<Theory />} />
                  <Route path="derivations/*" element={<Derivations />} />
                  <Route path="calculations/*" element={<Calculations />} />
                  <Route path="visualizations/*" element={<Visualizations />} />
                  <Route path="results/*" element={<Results />} />
                  <Route path="explanations/*" element={<Explanations />} />
                  <Route path="about" element={<About />} />
                  <Route path="*" element={<NotFound />} />
                </Route>
              </Routes>
            </Suspense>
          </div>
        </UXProvider>
      </BrowserRouter>
    </ErrorBoundary>
  );
}

export default App;
