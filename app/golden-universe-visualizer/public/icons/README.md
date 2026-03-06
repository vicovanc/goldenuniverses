# PWA Icons

This directory contains all PWA app icons for the Golden Universe Visualizer.

## Generated Icons

All icons have been **successfully generated** with a beautiful Golden Ratio spiral design!

### Available Icons:
- ✅ `icon-72x72.png` (72×72px)
- ✅ `icon-96x96.png` (96×96px)
- ✅ `icon-128x128.png` (128×128px)
- ✅ `icon-144x144.png` (144×144px)
- ✅ `icon-152x152.png` (152×152px)
- ✅ `icon-192x192.png` (192×192px)
- ✅ `icon-384x384.png` (384×384px)
- ✅ `icon-512x512.png` (512×512px)
- ✅ `apple-touch-icon.png` (180×180px) - iOS specific

### Additional Files:
- `favicon.ico` - Browser favicon (32x32, PNG format in .ico container)
- `favicon.png` - PNG favicon (32x32)
- `favicon.svg` - Vector favicon for modern browsers

## Icon Design

The icons feature a **Golden Ratio (φ) themed cosmic design**:
- **Background:** Purple-to-dark gradient (#2d1b4e to #1a1a1a to #0a0a0a)
- **Foreground:** Golden gradient (#FFD700 to #c9a84e to #B8860B)
- **Design Elements:**
  - Golden spiral using mathematical φ formula (2.5 turns)
  - Fibonacci rectangles pattern (subtle background)
  - Multiple decorative circles (outer cosmic, inner purple)
  - Central φ (phi) symbol with glow effect
  - Subtle "1.618" text at bottom
  - Animated twinkling stars/particles
  - Sophisticated glassmorphism theme matching the app

## Maskable Icons

All icons are designed with maskable icon support:
- Content within 76% safe area (38% radius)
- Works with circular, rounded square, and squircle masks
- Compatible with Android adaptive icons
- Test at: https://maskable.app/

## Regenerating Icons

To regenerate the icons (e.g., if you want to change the design):

```bash
npm run generate-icons
```

This runs the script at `scripts/generate-icons.js` which:
1. Uses the `sharp` library for high-quality PNG generation
2. Creates all required icon sizes (72-512px)
3. Generates PNG icons from SVG markup
4. Creates favicon.ico and favicon.png in the public directory
5. Includes Apple Touch Icon for iOS devices

## Manual Generation

If you need to customize the icons, edit `scripts/generate-icons.js`:

```javascript
// Customize the design in createIconSVG() function
// Available customizations:
// - Colors: golden gradient, purple background
// - Spiral: adjust turns, steps, radius
// - Stars: positions, sizes, animation speed
// - Fibonacci pattern: scale and rotation
```

Then run:
```bash
node scripts/generate-icons.js
```

## Testing Icons

### 1. Local Development:
```bash
npm run dev
# Visit http://localhost:3001
# Icons are served from /icons/ path
```

### 2. Chrome DevTools:
- Open DevTools (F12)
- Go to "Application" tab
- Check "Manifest" section
- Verify all icons load with 200 status

### 3. PWA Testing:
```bash
npm run build
npm run preview
# Test "Add to Home Screen" functionality
```

### 4. Real Devices:
- **Android:** Add to Home Screen, check adaptive icon
- **iOS:** Add to Home Screen, check apple-touch-icon
- **Desktop:** Install as PWA, check taskbar/dock icon

## Icon Usage

Icons are referenced in multiple places:

1. **manifest.json** (`public/manifest.json`)
   - All PWA icon sizes
   - Used for Android and desktop PWA

2. **index.html** (root `index.html`)
   - Apple touch icon: `/icons/apple-touch-icon.png`
   - Microsoft tile: `/icons/icon-144x144.png`

3. **Favicons** (`public/favicon.svg` and `public/favicon.png`)
   - Browser tab icons
   - Generated from same design

## Current Status

✅ **All icons generated and working!**

The icons are:
- ✅ Generated with proper sizes
- ✅ Served correctly from `/icons/` path
- ✅ Referenced in manifest.json
- ✅ Referenced in index.html
- ✅ Compatible with PWA requirements
- ✅ Maskable icon compatible
- ✅ No 404 errors

## Technical Details

- **Library:** sharp (Node.js image processing)
- **Format:** PNG with transparency
- **Compression:** Level 9 (maximum)
- **Color Space:** RGB
- **Design:** SVG-based, converted to PNG
- **Safe Area:** 76% (maskable compatible)
