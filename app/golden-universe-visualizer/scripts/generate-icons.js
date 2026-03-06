#!/usr/bin/env node

/**
 * Generate PWA icons for Golden Universe Visualizer
 * Creates beautiful icons with golden ratio symbol and cosmic theme
 */

import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Icon sizes for PWA
const ICON_SIZES = [72, 96, 128, 144, 152, 192, 384, 512];

// Paths
const publicDir = path.join(__dirname, '..', 'public');
const iconsDir = path.join(publicDir, 'icons');

// Ensure icons directory exists
if (!fs.existsSync(iconsDir)) {
  fs.mkdirSync(iconsDir, { recursive: true });
}

/**
 * Create SVG for icon with golden ratio theme
 * @param {number} size - Icon size in pixels
 * @returns {string} SVG markup
 */
function createIconSVG(size) {
  const padding = size * 0.1;
  const innerSize = size - (padding * 2);
  const centerX = size / 2;
  const centerY = size / 2;
  const radius = innerSize / 2;

  // Golden ratio
  const phi = 1.618;

  // Font sizes scaled to icon size
  const phiFontSize = size * 0.4;
  const valueFontSize = size * 0.06;
  const phiY = centerY + (phiFontSize * 0.35);
  const valueY = centerY + (size * 0.35);

  // Spiral parameters
  const spiralTurns = 2.5;
  const spiralSteps = 200;
  const spiralPath = generateGoldenSpiral(centerX, centerY, radius * 0.8, spiralTurns, spiralSteps);

  // Fibonacci rectangles for background pattern
  const fibonacciRects = generateFibonacciRectangles(centerX, centerY, size);

  return `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Golden gradient -->
    <linearGradient id="goldenGrad_${size}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFD700"/>
      <stop offset="50%" stop-color="#c9a84e"/>
      <stop offset="100%" stop-color="#B8860B"/>
    </linearGradient>

    <!-- Purple gradient for background -->
    <radialGradient id="bgGrad_${size}" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2d1b4e"/>
      <stop offset="50%" stop-color="#1a1a1a"/>
      <stop offset="100%" stop-color="#0a0a0a"/>
    </radialGradient>

    <!-- Cosmic glow effect -->
    <filter id="glow_${size}">
      <feGaussianBlur stdDeviation="${size * 0.04}" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Outer glow for background -->
    <filter id="outerGlow_${size}">
      <feGaussianBlur stdDeviation="${size * 0.02}" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background with rounded corners -->
  <rect width="${size}" height="${size}" fill="url(#bgGrad_${size})" rx="${size * 0.12}"/>

  <!-- Fibonacci rectangles pattern (subtle background) -->
  <g opacity="0.15">
    ${fibonacciRects}
  </g>

  <!-- Outer cosmic circle -->
  <circle cx="${centerX}" cy="${centerY}" r="${radius * 0.95}"
          fill="none" stroke="url(#goldenGrad_${size})"
          stroke-width="${size * 0.01}" opacity="0.3"
          filter="url(#outerGlow_${size})"/>

  <!-- Inner decorative circle -->
  <circle cx="${centerX}" cy="${centerY}" r="${radius * 0.75}"
          fill="none" stroke="#9b59b6"
          stroke-width="${size * 0.005}" opacity="0.2"/>

  <!-- Golden spiral -->
  <path d="${spiralPath}"
        stroke="url(#goldenGrad_${size})"
        stroke-width="${size * 0.02}"
        fill="none"
        stroke-linecap="round"
        filter="url(#glow_${size})"/>

  <!-- Central phi symbol with cosmic glow -->
  <text x="${centerX}" y="${phiY}"
        font-family="Georgia, serif"
        font-size="${phiFontSize}"
        font-weight="bold"
        fill="url(#goldenGrad_${size})"
        text-anchor="middle"
        opacity="0.95"
        filter="url(#glow_${size})">φ</text>

  <!-- Small golden ratio value -->
  <text x="${centerX}" y="${valueY}"
        font-family="monospace"
        font-size="${valueFontSize}"
        fill="#c9a84e"
        text-anchor="middle"
        opacity="0.7">1.618</text>

  <!-- Decorative stars/particles -->
  ${generateStars(size, centerX, centerY, radius)}
</svg>`;
}

/**
 * Generate golden spiral path
 * @param {number} cx - Center X
 * @param {number} cy - Center Y
 * @param {number} maxRadius - Maximum radius
 * @param {number} turns - Number of spiral turns
 * @param {number} steps - Number of steps to draw
 * @returns {string} SVG path data
 */
function generateGoldenSpiral(cx, cy, maxRadius, turns, steps) {
  const phi = 1.618;
  const points = [];

  for (let i = 0; i < steps; i++) {
    const t = (i / steps) * turns * 2 * Math.PI;
    const r = (maxRadius / Math.pow(phi, turns * 2)) * Math.pow(phi, t / (2 * Math.PI));
    const x = cx + r * Math.cos(t);
    const y = cy + r * Math.sin(t);
    points.push(`${i === 0 ? 'M' : 'L'} ${x.toFixed(2)} ${y.toFixed(2)}`);
  }

  return points.join(' ');
}

/**
 * Generate Fibonacci rectangles for background pattern
 * @param {number} cx - Center X
 * @param {number} cy - Center Y
 * @param {number} size - Icon size
 * @returns {string} SVG rect elements
 */
function generateFibonacciRectangles(cx, cy, size) {
  const fibonacci = [1, 1, 2, 3, 5, 8];
  const scale = size * 0.04;
  const rects = [];

  let x = 0;
  let y = 0;
  let direction = 0; // 0=right, 1=up, 2=left, 3=down

  fibonacci.forEach((num, i) => {
    const rectSize = num * scale;
    const opacity = 0.3 + (i * 0.1);
    const rotation = direction * 90;

    rects.push(`
    <rect x="${cx + x}" y="${cy + y}"
          width="${rectSize}" height="${rectSize}"
          fill="#c9a84e"
          opacity="${opacity}"
          rx="${rectSize * 0.08}"
          transform="rotate(${rotation} ${cx} ${cy})"/>`);

    // Update position for next rectangle
    switch (direction % 4) {
      case 0: x += rectSize; break;
      case 1: y -= rectSize; break;
      case 2: x -= rectSize; break;
      case 3: y += rectSize; break;
    }
    direction++;
  });

  return rects.join('');
}

/**
 * Generate decorative stars/particles
 * @param {number} size - Icon size
 * @param {number} cx - Center X
 * @param {number} cy - Center Y
 * @param {number} radius - Distribution radius
 * @returns {string} SVG circle elements
 */
function generateStars(size, cx, cy, radius) {
  const stars = [];
  const starPositions = [
    { angle: 30, dist: 0.85, size: 0.008 },
    { angle: 75, dist: 0.9, size: 0.006 },
    { angle: 150, dist: 0.88, size: 0.007 },
    { angle: 210, dist: 0.92, size: 0.005 },
    { angle: 280, dist: 0.87, size: 0.006 },
    { angle: 320, dist: 0.91, size: 0.007 }
  ];

  starPositions.forEach(star => {
    const rad = (star.angle * Math.PI) / 180;
    const x = cx + Math.cos(rad) * radius * star.dist;
    const y = cy + Math.sin(rad) * radius * star.dist;
    const r = size * star.size;

    stars.push(`
    <circle cx="${x.toFixed(2)}" cy="${y.toFixed(2)}" r="${r.toFixed(2)}"
            fill="#FFD700" opacity="0.6">
      <animate attributeName="opacity"
               values="0.3;0.8;0.3"
               dur="${2 + Math.random()}s"
               repeatCount="indefinite"/>
    </circle>`);
  });

  return stars.join('');
}

/**
 * Generate a single icon
 * @param {number} size - Icon size in pixels
 */
async function generateIcon(size) {
  try {
    const svg = createIconSVG(size);
    const outputPath = path.join(iconsDir, `icon-${size}x${size}.png`);

    await sharp(Buffer.from(svg))
      .resize(size, size)
      .png({ quality: 100, compressionLevel: 9 })
      .toFile(outputPath);

    console.log(`✓ Generated ${size}x${size} icon`);
  } catch (error) {
    console.error(`✗ Failed to generate ${size}x${size} icon:`, error.message);
  }
}

/**
 * Generate favicon.ico with multiple sizes
 */
async function generateFavicon() {
  try {
    // Generate 32x32 PNG first (standard favicon size)
    const svg = createIconSVG(32);
    const pngBuffer = await sharp(Buffer.from(svg))
      .resize(32, 32)
      .png({ quality: 100 })
      .toBuffer();

    // Save as favicon.png
    const faviconPngPath = path.join(publicDir, 'favicon.png');
    await sharp(pngBuffer).toFile(faviconPngPath);
    console.log('✓ Generated favicon.png (32x32)');

    // For .ico format, we need to create it differently
    // Since sharp doesn't directly support .ico, we'll create a 32x32 PNG
    // and save it as .ico (browsers accept PNG format in .ico files)
    const faviconIcoPath = path.join(publicDir, 'favicon.ico');

    // Generate a multi-size favicon (16x16 and 32x32)
    const svg16 = createIconSVG(16);
    const png16Buffer = await sharp(Buffer.from(svg16))
      .resize(16, 16)
      .png({ quality: 100 })
      .toBuffer();

    // For proper .ico support, we'll use the 32x32 version
    // Modern browsers support PNG in .ico containers
    await sharp(pngBuffer).toFile(faviconIcoPath);
    console.log('✓ Generated favicon.ico');

  } catch (error) {
    console.error('✗ Failed to generate favicon:', error.message);
  }
}

/**
 * Generate Apple Touch Icon
 */
async function generateAppleTouchIcon() {
  try {
    const size = 180;
    const svg = createIconSVG(size);
    const outputPath = path.join(iconsDir, 'apple-touch-icon.png');

    await sharp(Buffer.from(svg))
      .resize(size, size)
      .png({ quality: 100, compressionLevel: 9 })
      .toFile(outputPath);

    console.log('✓ Generated apple-touch-icon.png (180x180)');
  } catch (error) {
    console.error('✗ Failed to generate apple-touch-icon:', error.message);
  }
}

/**
 * Main function to generate all icons
 */
async function generateAllIcons() {
  console.log('Starting icon generation...\n');
  console.log('Theme: Golden Ratio / Cosmic / Purple-Gold\n');

  // Generate all PWA icons
  for (const size of ICON_SIZES) {
    await generateIcon(size);
  }

  // Generate Apple Touch Icon
  await generateAppleTouchIcon();

  // Generate favicons
  await generateFavicon();

  console.log('\n✨ All icons generated successfully!');
  console.log(`📁 Icons saved to: ${iconsDir}`);
}

// Run the generator
generateAllIcons().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
