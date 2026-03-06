/**
 * AchievementCards - Breakthrough results display
 * GU-037: Achievement Overview
 * - Cards for breakthrough results
 * - Animated counters for key metrics
 * - Precision badges (gold, silver, bronze)
 * - Timeline view
 */

import React, { useState, useEffect } from 'react';
import type { AchievementData } from './types';
import { getStatistics } from './resultsData';

interface AchievementCardsProps {
  achievements: AchievementData[];
  onShare?: (achievement: AchievementData) => void;
}

export const AchievementCards: React.FC<AchievementCardsProps> = ({
  achievements,
  onShare,
}) => {
  const [animatedStats, setAnimatedStats] = useState({
    subPpm: 0,
    sub10Ppm: 0,
    sub100Ppm: 0,
    breakthroughs: 0,
  });

  const stats = getStatistics();

  // Animate counters on mount
  useEffect(() => {
    const duration = 1500; // 1.5 seconds
    const steps = 60;
    const interval = duration / steps;

    let currentStep = 0;
    const timer = setInterval(() => {
      currentStep++;
      const progress = currentStep / steps;

      setAnimatedStats({
        subPpm: Math.floor(stats.subPpm * progress),
        sub10Ppm: Math.floor(stats.sub10Ppm * progress),
        sub100Ppm: Math.floor(stats.sub100Ppm * progress),
        breakthroughs: Math.floor(stats.breakthroughs * progress),
      });

      if (currentStep >= steps) {
        clearInterval(timer);
        setAnimatedStats({
          subPpm: stats.subPpm,
          sub10Ppm: stats.sub10Ppm,
          sub100Ppm: stats.sub100Ppm,
          breakthroughs: stats.breakthroughs,
        });
      }
    }, interval);

    return () => clearInterval(timer);
  }, [stats]);

  const getBadgeEmoji = (badge: 'gold' | 'silver' | 'bronze'): string => {
    const badges = {
      gold: '🥇',
      silver: '🥈',
      bronze: '🥉',
    };
    return badges[badge];
  };

  const getBadgeColor = (badge: 'gold' | 'silver' | 'bronze'): string => {
    const colors = {
      gold: '#FFD700',
      silver: '#C0C0C0',
      bronze: '#CD7F32',
    };
    return colors[badge];
  };

  const formatDate = (dateStr: string): string => {
    const [year, month] = dateStr.split('-');
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return `${monthNames[parseInt(month) - 1]} ${year}`;
  };

  // Sort by date (most recent first)
  const sortedAchievements = [...achievements].sort((a, b) =>
    b.date.localeCompare(a.date)
  );

  return (
    <div className="achievement-cards-container">
      {/* Key Metrics */}
      <div className="metrics-overview">
        <h3>Key Achievements</h3>
        <div className="metrics-grid">
          <div className="metric-card highlight">
            <div className="metric-value">{animatedStats.subPpm}</div>
            <div className="metric-label">Sub-1 ppm</div>
            <div className="metric-subtitle">Ultra-precision</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{animatedStats.sub10Ppm}</div>
            <div className="metric-label">Sub-10 ppm</div>
            <div className="metric-subtitle">High precision</div>
          </div>
          <div className="metric-card">
            <div className="metric-value">{animatedStats.sub100Ppm}</div>
            <div className="metric-label">Sub-100 ppm</div>
            <div className="metric-subtitle">Excellent match</div>
          </div>
          <div className="metric-card highlight">
            <div className="metric-value">{animatedStats.breakthroughs}</div>
            <div className="metric-label">Breakthroughs</div>
            <div className="metric-subtitle">Major discoveries</div>
          </div>
        </div>
      </div>

      {/* Achievement Cards */}
      <div className="achievements-section">
        <h3>Breakthrough Results</h3>
        <div className="achievements-grid">
          {sortedAchievements.map((achievement, idx) => (
            <div
              key={idx}
              className={`achievement-card ${achievement.badge}`}
              style={{ animationDelay: `${idx * 0.1}s` }}
            >
              <div className="achievement-header">
                <div
                  className="badge-icon"
                  style={{ backgroundColor: getBadgeColor(achievement.badge) }}
                >
                  {getBadgeEmoji(achievement.badge)}
                </div>
                <div className="achievement-meta">
                  <span className={`category-tag ${achievement.category}`}>
                    {achievement.category}
                  </span>
                  <span className="date-tag">{formatDate(achievement.date)}</span>
                </div>
              </div>

              <div className="achievement-content">
                <h4 className="achievement-title">{achievement.title}</h4>
                <p className="achievement-description">{achievement.description}</p>

                <div className="precision-display">
                  <div className="precision-value">
                    {achievement.precision < 1
                      ? `${achievement.precision.toFixed(3)} ppm`
                      : `${achievement.precision.toFixed(1)} ppm`}
                  </div>
                  <div className="precision-label">Precision</div>
                </div>
              </div>

              {onShare && (
                <div className="achievement-footer">
                  <button
                    className="share-btn"
                    onClick={() => onShare(achievement)}
                    title="Share this achievement"
                  >
                    Share
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Timeline View */}
      <div className="timeline-section">
        <h3>Discovery Timeline</h3>
        <div className="timeline">
          {sortedAchievements.map((achievement, idx) => (
            <div key={idx} className="timeline-item">
              <div className="timeline-marker">
                <div
                  className="marker-dot"
                  style={{ backgroundColor: getBadgeColor(achievement.badge) }}
                />
              </div>
              <div className="timeline-content">
                <div className="timeline-date">{formatDate(achievement.date)}</div>
                <div className="timeline-title">{achievement.title}</div>
                <div className="timeline-precision">
                  {achievement.precision < 1
                    ? `${achievement.precision.toFixed(3)} ppm`
                    : `${achievement.precision.toFixed(1)} ppm`}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
