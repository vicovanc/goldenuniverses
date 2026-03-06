import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { UXProvider } from '@/components/UXEnhancements/UXProvider';
import { ErrorBoundary } from '@/components/Common/ErrorBoundary';
import { AppHeader } from '@/components/Layout/AppHeader';
import MainLayout from '@components/Layout/MainLayout';
import LoadingFallback from '@components/Common/LoadingFallback';
import './styles/globals.scss';
import './styles/accessibility.scss';

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
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <UXProvider>
          <div className="app">
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
