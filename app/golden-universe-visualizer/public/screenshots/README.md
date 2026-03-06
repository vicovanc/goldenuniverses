# PWA Screenshots

This directory should contain screenshots for the PWA app store listings.

## Required Screenshots

1. **Desktop Screenshot** (`desktop.png`)
   - Size: 1280×720px (16:9 ratio)
   - Shows main desktop interface
   - Used in Chrome Web Store

2. **Mobile Screenshot** (`mobile.png`)
   - Size: 750×1334px (iPhone 8 ratio)
   - Shows main mobile interface
   - Used for mobile app listings

## How to Capture

### Desktop Screenshot:
1. Open app in browser
2. Resize window to 1280×720
3. Navigate to best showcase screen
4. Use browser DevTools screenshot or screen capture tool
5. Save as `desktop.png`

### Mobile Screenshot:
1. Open Chrome DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select iPhone 8 (375×667) or similar
4. Set zoom to 2x for retina
5. Capture screenshot (1280×720 minimum)
6. Save as `mobile.png`

## Screenshot Guidelines

### Content:
- Show key features of the app
- Use real data (not placeholder)
- Ensure good visual quality
- Avoid any sensitive information

### Quality:
- Format: PNG (preferred) or JPEG
- No compression artifacts
- Clear, readable text
- Proper lighting/contrast

### Best Practices:
1. Show the most engaging screen first
2. Include interactive elements
3. Display actual functionality
4. Use consistent theme (light or dark)

## Testing

After adding screenshots:
1. Build app: `npm run build`
2. Check manifest: `http://localhost:4173/manifest.json`
3. Verify screenshots load in Application tab
4. Test PWA install to see screenshots displayed

## Current Status

⚠️ **Action Required:** Capture and add screenshot files to this directory.

The app will work without screenshots, but they enhance the install experience and are required for app store submissions.

## Tools

### Recommended Screenshot Tools:
- **Chrome DevTools:** Built-in screenshot capture
- **Firefox Screenshots:** Built-in tool (Shift+F2, screenshot --fullpage)
- **Lightshot:** Desktop screenshot tool
- **Snagit:** Professional screenshot tool
- **Browser Extensions:** Awesome Screenshot, FireShot

### Online Tools:
- **Responsive Screenshot Generator:** https://www.responsivescreenshotgenerator.com/
- **Browser Frame:** https://browserframe.com/ (adds device frames)

## Example Command

Using Chrome DevTools Protocol:
```bash
# Install puppeteer
npm install -g puppeteer

# Create screenshot script
node capture-screenshots.js
```

Create `capture-screenshots.js`:
```javascript
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Desktop screenshot
  await page.setViewport({ width: 1280, height: 720 });
  await page.goto('http://localhost:3000');
  await page.screenshot({ path: 'public/screenshots/desktop.png' });

  // Mobile screenshot
  await page.setViewport({ width: 375, height: 667, deviceScaleFactor: 2 });
  await page.goto('http://localhost:3000');
  await page.screenshot({ path: 'public/screenshots/mobile.png' });

  await browser.close();
})();
```
