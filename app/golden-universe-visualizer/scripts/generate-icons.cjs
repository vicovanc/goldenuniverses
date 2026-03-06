#!/usr/bin/env node

/**
 * Generate PWA icons for Golden Universe Visualizer
 * Creates beautiful icons with golden ratio spiral design using sharp
 */

const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const PHI = 1.618033988749895; // Golden ratio
const THEME_COLOR = '#c9a84e'; // Golden color
const BG_COLOR = '#0a0a0a'; // Dark background

const ICON_SIZES = [72, 96, 128, 144, 152, 192, 384, 512];
const APPLE_ICON_SIZE = 180;

const iconsDir = path.join(__dirname, '../public/icons');
const publicDir = path.join(__dirname, '../public');

// Ensure icons directory exists
if (!fs.existsSync(iconsDir)) {
  fs.mkdirSync(iconsDir, { recursive: true });
}

/**
 * Generate SVG content for icon with golden ratio design
 */
function generateIconSVG(size) {
  const center = size / 2;
  const maxRadius = size * 0.38; // Keep within 76% for maskable safety
  const strokeWidth = Math.max(2, size * 0.012);

  // Generate golden spiral coordinates
  const spiralPath = generateGoldenSpiral(center, center, maxRadius);

  // Generate Fibonacci rectangles
  const rectangles = generateFibonacciRectangles(center, center, maxRadius);

  return `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="goldenGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD700"/>
      <stop offset="50%" stop-color="${THEME_COLOR}"/>
      <stop offset="100%" stop-color="#B8860B"/>
    </linearGradient>
    <radialGradient id="bgGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#1a1a1a"/>
      <stop offset="100%" stop-color="${BG_COLOR}"/>
    </radialGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background with rounded corners -->
  <rect width="${size}" height="${size}" fill="url(#bgGrad)" rx="${size * 0.12}"/>

  <!-- Fibonacci rectangles (subtle background pattern) -->
  <g opacity="0.15">
    ${rectangles}
  </g>

  <!-- Outer circle -->
  <circle cx="${center}" cy="${center}" r="${maxRadius * 1.1}"
          fill="none" stroke="url(#goldenGrad)" stroke-width="${strokeWidth * 0.5}" opacity="0.3"/>

  <!-- Golden spiral -->
  <path d="${spiralPath}"
        stroke="url(#goldenGrad)"
        stroke-width="${strokeWidth}"
        fill="none"
        stroke-linecap="round"
        filter="url(#glow)"/>

  <!-- Central phi symbol -->
  <text x="${center}" y="${center + size * 0.15}"
        font-family="Georgia, serif"
        font-size="${size * 0.4}"
        font-weight="bold"
        fill="url(#goldenGrad)"
        text-anchor="middle"
        opacity="0.95"
        filter="url(#glow)">φ</text>

  <!-- Small golden ratio value -->
  <text x="${center}" y="${center + size * 0.35}"
        font-family="monospace"
        font-size="${size * 0.06}"
        fill="${THEME_COLOR}"
        text-anchor="middle"
        opacity="0.7">1.618</text>
</svg>`;
}

/**
 * Generate golden spiral path using parametric equations
 */
function generateGoldenSpiral(cx, cy, maxRadius) {
  const points = [];
  const turns = 2.2; // Number of spiral turns
  const steps = 150;

  for (let i = 0; i <= steps; i++) {
    const t = (i / steps) * turns * 2 * Math.PI;
    // Golden spiral: r = a * e^(b*θ) where b = ln(φ)/(π/2)
    const b = Math.log(PHI) / (Math.PI / 2);
    const a = maxRadius / Math.exp(b * turns * 2 * Math.PI);
    const r = a * Math.exp(b * t);

    const x = cx + r * Math.cos(t);
    const y = cy + r * Math.sin(t);

    points.push(`${i === 0 ? 'M' : 'L'} ${x.toFixed(2)} ${y.toFixed(2)}`);
  }

  return points.join(' ');
}

/**
 * Generate Fibonacci rectangles in a spiral pattern
 */
function generateFibonacciRectangles(cx, cy, maxSize) {
  const fib = [1, 1, 2, 3, 5, 8, 13];
  const scale = (maxSize * 1.4) / fib[fib.length - 1];
  let rects = '';

  let x = cx;
  let y = cy;
  let angle = 0;

  fib.forEach((num, i) => {
    const size = num * scale;
    const opacity = 0.3 + (i / fib.length) * 0.4;

    rects += `<rect x="${x - size / 2}" y="${y - size / 2}"
              width="${size}" height="${size}"
              fill="${THEME_COLOR}"
              opacity="${opacity}"
              rx="${size * 0.08}"
              transform="rotate(${angle} ${x} ${y})"/>\n    `;

    // Rotate for next rectangle
    angle += 90;
    const offset = size * 0.3;
    x += offset * Math.cos((angle * Math.PI) / 180);
    y += offset * Math.sin((angle * Math.PI) / 180);
  });

  return rects;
}

/**
 * Convert SVG to PNG using sharp
 */
async function convertSVGtoPNG(svgContent, size, outputPath) {
  try {
    const svgBuffer = Buffer.from(svgContent);

    await sharp(svgBuffer)
      .resize(size, size)
      .png({
        compressionLevel: 9,
        palette: false,
      })
      .toFile(outputPath);

    console.log(`✓ Generated ${path.basename(outputPath)} (${size}x${size})`);
  } catch (error) {
    console.error(`✗ Failed to generate ${path.basename(outputPath)}:`, error.message);
    throw error;
  }
}

/**
 * Generate favicon.ico using multiple sizes
 */
async function generateFavicon() {
  const faviconSizes = [16, 32, 48];
  const svgContent = generateIconSVG(48);
  const svgBuffer = Buffer.from(svgContent);

  // Generate PNG for favicon
  const faviconPath = path.join(publicDir, 'favicon.png');
  await sharp(svgBuffer)
    .resize(32, 32)
    .png()
    .toFile(faviconPath);

  // Also save SVG version
  const faviconSvgPath = path.join(publicDir, 'favicon.svg');
  fs.writeFileSync(faviconSvgPath, svgContent);

  console.log('✓ Generated favicon.png and favicon.svg');
}

/**
 * Main function to generate all icons
 */
async function generateAllIcons() {
  console.log('\n🎨 Generating Golden Universe PWA Icons...\n');
  console.log('Theme: Golden Ratio (φ = 1.618033988749895)');
  console.log('Colors: Golden (#c9a84e) on Dark (#0a0a0a)\n');

  try {
    // Generate standard PWA icons
    for (const size of ICON_SIZES) {
      const svgContent = generateIconSVG(size);
      const outputPath = path.join(iconsDir, `icon-${size}x${size}.png`);
      await convertSVGtoPNG(svgContent, size, outputPath);

      // Also save SVG version for reference
      const svgPath = path.join(iconsDir, `icon-${size}x${size}.svg`);
      fs.writeFileSync(svgPath, svgContent);
    }

    console.log('');

    // Generate Apple touch icon (non-transparent background)
    const appleSVG = generateIconSVG(APPLE_ICON_SIZE);
    const appleOutputPath = path.join(iconsDir, 'apple-touch-icon.png');
    await convertSVGtoPNG(appleSVG, APPLE_ICON_SIZE, appleOutputPath);
    console.log(`✓ Generated apple-touch-icon.png (${APPLE_ICON_SIZE}x${APPLE_ICON_SIZE})`);

    console.log('');

    // Generate favicon
    await generateFavicon();

    console.log('\n✅ All icons generated successfully!\n');
    console.log('📁 Location: public/icons/');
    console.log('📝 Formats: PNG (for browsers) + SVG (for reference)');
    console.log('🎯 Sizes:', ICON_SIZES.join(', '), '+ 180 (Apple)');
    console.log('');
    console.log('Next steps:');
    console.log('  1. Check icons in browser: http://localhost:3001');
    console.log('  2. Verify manifest: DevTools > Application > Manifest');
    console.log('  3. Test maskable icons: https://maskable.app\n');
  } catch (error) {
    console.error('\n❌ Error generating icons:', error);
    process.exit(1);
  }
}

// Run the generator
if (require.main === module) {
  generateAllIcons().catch((error) => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = { generateAllIcons, generateIconSVG };
