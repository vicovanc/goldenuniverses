import React, { useState, useMemo } from 'react';
import { theoryLaws, categories } from '@/data/theoryLaws';
import { TheoryLaw, BookmarkState, ReadingProgress } from '@/types/theory';

interface LawsBrowserProps {
  onSelectLaw: (law: TheoryLaw) => void;
  selectedLawId?: number;
}

const LawsBrowser: React.FC<LawsBrowserProps> = ({ onSelectLaw, selectedLawId }) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [jumpToNumber, setJumpToNumber] = useState('');
  const [hoveredLaw, setHoveredLaw] = useState<TheoryLaw | null>(null);
  const [hoverPosition, setHoverPosition] = useState({ x: 0, y: 0 });
  const [bookmarks, setBookmarks] = useState<BookmarkState[]>([]);
  const [readingProgress, setReadingProgress] = useState<ReadingProgress[]>([]);
  const [showBookmarksOnly, setShowBookmarksOnly] = useState(false);

  // Filter laws based on category, search, and bookmarks
  const filteredLaws = useMemo(() => {
    let laws = theoryLaws;

    // Filter by category
    if (selectedCategory !== 'all') {
      laws = laws.filter((law) => law.category === selectedCategory);
    }

    // Filter by search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      laws = laws.filter(
        (law) =>
          law.title.toLowerCase().includes(query) ||
          law.statement.toLowerCase().includes(query) ||
          law.id.toString().includes(query)
      );
    }

    // Filter by bookmarks
    if (showBookmarksOnly) {
      const bookmarkedIds = bookmarks.map((b) => b.lawId);
      laws = laws.filter((law) => bookmarkedIds.includes(law.id));
    }

    return laws;
  }, [selectedCategory, searchQuery, showBookmarksOnly, bookmarks]);

  // Get progress for a law
  const getProgress = (lawId: number): number => {
    const progress = readingProgress.find((p) => p.lawId === lawId);
    return progress?.progress || 0;
  };

  // Check if law is bookmarked
  const isBookmarked = (lawId: number): boolean => {
    return bookmarks.some((b) => b.lawId === lawId);
  };

  // Toggle bookmark
  const toggleBookmark = (lawId: number, event: React.MouseEvent) => {
    event.stopPropagation();
    if (isBookmarked(lawId)) {
      setBookmarks(bookmarks.filter((b) => b.lawId !== lawId));
    } else {
      setBookmarks([...bookmarks, { lawId, timestamp: Date.now() }]);
    }
  };

  // Handle law hover
  const handleLawHover = (law: TheoryLaw, event: React.MouseEvent) => {
    setHoveredLaw(law);
    setHoverPosition({ x: event.clientX, y: event.clientY });
  };

  // Handle jump to law
  const handleJumpTo = () => {
    const lawId = parseInt(jumpToNumber);
    if (!isNaN(lawId) && lawId >= 0 && lawId <= 38) {
      const law = theoryLaws.find((l) => l.id === lawId);
      if (law) {
        onSelectLaw(law);
        setJumpToNumber('');
      }
    }
  };

  // Mark progress when selecting a law
  const handleSelectLaw = (law: TheoryLaw) => {
    onSelectLaw(law);
    // Update reading progress
    const existingProgress = readingProgress.find((p) => p.lawId === law.id);
    if (!existingProgress) {
      setReadingProgress([...readingProgress, { lawId: law.id, progress: 50, lastRead: Date.now() }]);
    } else {
      setReadingProgress(
        readingProgress.map((p) => (p.lawId === law.id ? { ...p, lastRead: Date.now(), progress: 100 } : p))
      );
    }
  };

  return (
    <div className="laws-browser">
      <div className="browser-header">
        <h2>Theory Laws Browser</h2>
        <p className="laws-count">
          {filteredLaws.length} of {theoryLaws.length} laws
        </p>
      </div>

      {/* Search and Quick Navigation */}
      <div className="browser-controls">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search laws..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          <button className="search-clear" onClick={() => setSearchQuery('')} aria-label="Clear search">
            ×
          </button>
        </div>

        <div className="jump-to-box">
          <input
            type="number"
            placeholder="Jump to law #"
            value={jumpToNumber}
            onChange={(e) => setJumpToNumber(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleJumpTo()}
            min="0"
            max="38"
            className="jump-input"
          />
          <button onClick={handleJumpTo} className="jump-button" aria-label="Jump to law">
            Go
          </button>
        </div>

        <button
          className={`bookmark-filter ${showBookmarksOnly ? 'active' : ''}`}
          onClick={() => setShowBookmarksOnly(!showBookmarksOnly)}
          title={showBookmarksOnly ? 'Show all laws' : 'Show bookmarks only'}
        >
          {showBookmarksOnly ? '★' : '☆'} Bookmarks ({bookmarks.length})
        </button>
      </div>

      {/* Category Filter */}
      <div className="category-filter">
        <button
          className={`category-button ${selectedCategory === 'all' ? 'active' : ''}`}
          onClick={() => setSelectedCategory('all')}
        >
          All Laws (0-38)
        </button>
        {categories.map((category) => (
          <button
            key={category.id}
            className={`category-button ${selectedCategory === category.id ? 'active' : ''}`}
            onClick={() => setSelectedCategory(category.id)}
            title={category.description}
          >
            {category.name} ({category.range})
          </button>
        ))}
      </div>

      {/* Laws List */}
      <div className="laws-list">
        {filteredLaws.map((law) => {
          const progress = getProgress(law.id);
          const bookmarked = isBookmarked(law.id);

          return (
            <div
              key={law.id}
              className={`law-item ${selectedLawId === law.id ? 'selected' : ''} ${bookmarked ? 'bookmarked' : ''}`}
              onClick={() => handleSelectLaw(law)}
              onMouseEnter={(e) => handleLawHover(law, e)}
              onMouseLeave={() => setHoveredLaw(null)}
            >
              <div className="law-item-header">
                <div className="law-item-number">Law {law.id}</div>
                <button
                  className={`bookmark-button ${bookmarked ? 'active' : ''}`}
                  onClick={(e) => toggleBookmark(law.id, e)}
                  aria-label={bookmarked ? 'Remove bookmark' : 'Add bookmark'}
                >
                  {bookmarked ? '★' : '☆'}
                </button>
              </div>
              <div className="law-item-title">{law.title}</div>
              <div className="law-item-status">
                <span className={`status-indicator status-${law.status}`}></span>
                {law.status.replace('-', ' ')}
              </div>
              {progress > 0 && (
                <div className="law-item-progress">
                  <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${progress}%` }}></div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Hover Preview */}
      {hoveredLaw && (
        <div
          className="law-preview"
          style={{
            position: 'fixed',
            left: `${hoverPosition.x + 20}px`,
            top: `${hoverPosition.y}px`,
            pointerEvents: 'none',
          }}
        >
          <div className="preview-header">
            <strong>Law {hoveredLaw.id}</strong>: {hoveredLaw.title}
          </div>
          <div className="preview-statement">{hoveredLaw.statement}</div>
          {hoveredLaw.equations && hoveredLaw.equations.length > 0 && (
            <div className="preview-equations">
              <em>Key equation:</em>
              <code>{hoveredLaw.equations[0]}</code>
            </div>
          )}
          <div className="preview-meta">
            <span className={`preview-status status-${hoveredLaw.status}`}>{hoveredLaw.status}</span>
            <span className={`preview-category category-${hoveredLaw.category}`}>{hoveredLaw.category}</span>
          </div>
        </div>
      )}

      {/* Overall Progress Indicator */}
      <div className="overall-progress">
        <div className="progress-header">
          <span>Reading Progress</span>
          <span>
            {readingProgress.length} / {theoryLaws.length} laws started
          </span>
        </div>
        <div className="progress-bar overall">
          <div
            className="progress-fill"
            style={{ width: `${(readingProgress.length / theoryLaws.length) * 100}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default LawsBrowser;
