# Scripts Directory

This directory contains utility scripts for the Golden Universe Visualizer project.

## Icon Generation Script

### `generate-icons.js`

Generates all PWA icons, favicons, and Apple touch icons for the application.

#### Features
- Programmatically creates icons using SVG-to-PNG conversion
- Uses Sharp library for high-quality image processing
- Generates mathematically accurate golden ratio spiral
- Includes Fibonacci rectangle patterns
- Adds cosmic visual effects (glow, stars, gradients)
- Creates all standard PWA icon sizes (72px - 512px)

#### Usage

**Via NPM script (recommended):**
```bash
npm run generate-icons
```

**Direct execution:**
```bash
node scripts/generate-icons.js
```

#### What Gets Generated

The script creates the following files:

**PWA Icons** (in `/public/icons/`):
- icon-72x72.png
- icon-96x96.png
- icon-128x128.png
- icon-144x144.png
- icon-152x152.png
- icon-192x192.png
- icon-384x384.png
- icon-512x512.png
- apple-touch-icon.png (180x180)

**Favicons** (in `/public/`):
- favicon.ico (32x32)
- favicon.png (32x32)

#### Design Specifications

**Colors:**
- Background: Purple-to-dark radial gradient (#2d1b4e → #1a1a1a → #0a0a0a)
- Primary: Golden linear gradient (#FFD700 → #c9a84e → #B8860B)
- Accent: Purple (#9b59b6)

**Elements:**
- Golden spiral (φ-based, 2.5 turns)
- Fibonacci rectangles pattern
- Cosmic circles (outer golden, inner purple)
- Central φ symbol with glow
- "1.618" value text
- 6 animated twinkling stars

**Technical:**
- Format: PNG with level 9 compression
- Color: 8-bit colormap (optimal size)
- Corners: 12% border radius
- Maskable: Safe area compatible

#### Customization

Edit the script to customize:

```javascript
// Spiral parameters
const spiralTurns = 2.5;     // Number of spiral turns
const spiralSteps = 200;     // Smoothness of spiral

// Colors (in createIconSVG function)
// Modify the gradient stop colors

// Stars
// Edit starPositions array in generateStars()

// Fibonacci pattern
// Adjust scale in generateFibonacciRectangles()
```

#### Requirements

- Node.js 18+
- Sharp library (installed via package.json)
- ES Modules support (configured in package.json)

#### Output

When run, you'll see:
```
Starting icon generation...

Theme: Golden Ratio / Cosmic / Purple-Gold

✓ Generated 72x72 icon
✓ Generated 96x96 icon
✓ Generated 128x128 icon
✓ Generated 144x144 icon
✓ Generated 152x152 icon
✓ Generated 192x192 icon
✓ Generated 384x384 icon
✓ Generated 512x512 icon
✓ Generated apple-touch-icon.png (180x180)
✓ Generated favicon.png (32x32)
✓ Generated favicon.ico

✨ All icons generated successfully!
📁 Icons saved to: /path/to/public/icons
```

#### Integration

The generated icons are automatically used by:
- `/public/manifest.json` - PWA manifest
- `/index.html` - Favicon and Apple touch icon references
- Service worker - For offline caching
- Browser - Tab icons and bookmarks

#### Troubleshooting

**Error: "sharp not installed"**
```bash
npm install
```

**Error: "Permission denied"**
```bash
chmod +x scripts/generate-icons.js
```

**Icons look wrong:**
1. Check the SVG generation in `createIconSVG()`
2. Verify gradient definitions
3. Ensure path data is correct

**File sizes too large:**
- Icons use optimal PNG compression (level 9)
- Consider reducing gradient complexity
- Simplify SVG filters if needed

## Other Scripts

### `parse-content.ts` / `quick-parse.js`
Content parsing scripts for indexing documentation and theory pages.

**Usage:**
```bash
npm run parse-content        # Quick parse
npm run parse-content:full   # Full parse with TypeScript
```

---

**For more information**, see `/public/icons/README.md` and `/ICON_GENERATION_SUMMARY.md`
