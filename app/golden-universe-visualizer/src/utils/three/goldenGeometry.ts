/**
 * Golden Ratio Geometry Helpers
 * Utilities for creating golden ratio-based 3D geometries and calculations
 */

import * as THREE from 'three';

// Golden ratio constant
export const PHI = (1 + Math.sqrt(5)) / 2;
export const PHI_SQUARED = PHI * PHI;
export const INV_PHI = 1 / PHI;

/**
 * Create a torus geometry with golden ratio proportions
 */
export function createGoldenTorus(
  majorRadius: number = 2,
  minorRadius?: number,
  radialSegments: number = 64,
  tubularSegments: number = 128
): THREE.TorusGeometry {
  const minor = minorRadius ?? majorRadius / PHI;
  return new THREE.TorusGeometry(majorRadius, minor, radialSegments, tubularSegments);
}

/**
 * Calculate winding number path on torus surface
 * @param p - poloidal winding number
 * @param q - toroidal winding number
 * @param R - major radius
 * @param r - minor radius
 * @param samples - number of points on the path
 */
export function calculateWindingPath(
  p: number,
  q: number,
  R: number = 2,
  r: number = R / PHI,
  samples: number = 500
): THREE.Vector3[] {
  const points: THREE.Vector3[] = [];

  for (let i = 0; i <= samples; i++) {
    const t = (i / samples) * 2 * Math.PI * q;
    const theta = t; // toroidal angle
    const phi = (p / q) * t; // poloidal angle

    const x = (R + r * Math.cos(phi)) * Math.cos(theta);
    const y = (R + r * Math.cos(phi)) * Math.sin(theta);
    const z = r * Math.sin(phi);

    points.push(new THREE.Vector3(x, y, z));
  }

  return points;
}

/**
 * Calculate geodesic length of winding path
 * l_Ω = 2π√(p² + q²/φ²)
 */
export function calculateGeodesicLength(p: number, q: number): number {
  return 2 * Math.PI * Math.sqrt(p * p + (q * q) / PHI_SQUARED);
}

/**
 * Calculate resonance for given epoch N
 * k_res = round(N / φ²)
 */
export function calculateResonance(N: number): number {
  return Math.round(N / PHI_SQUARED);
}

/**
 * Check if resonance is resonant (even) or anti-resonant (odd)
 */
export function isResonant(k_res: number): boolean {
  return k_res % 2 === 0;
}

/**
 * Get winding numbers (p, q) for a given particle and epoch
 * Based on the Golden Universe paper's winding number assignments
 */
export function getWindingNumbers(particle: string, epoch: number): { p: number; q: number } {
  // Simplified mapping - in practice this would come from data tables
  const windingMap: Record<string, (N: number) => { p: number; q: number }> = {
    electron: (N) => ({ p: 1, q: Math.round(N / PHI_SQUARED) }),
    muon: (N) => ({ p: 2, q: Math.round(N / PHI_SQUARED) }),
    tau: (N) => ({ p: 3, q: Math.round(N / PHI_SQUARED) }),
    up: (N) => ({ p: 1, q: Math.round(N / (3 * PHI_SQUARED)) }),
    down: (N) => ({ p: 1, q: Math.round(N / (3 * PHI_SQUARED)) }),
    charm: (N) => ({ p: 2, q: Math.round(N / (3 * PHI_SQUARED)) }),
    strange: (N) => ({ p: 2, q: Math.round(N / (3 * PHI_SQUARED)) }),
    top: (N) => ({ p: 3, q: Math.round(N / (3 * PHI_SQUARED)) }),
    bottom: (N) => ({ p: 3, q: Math.round(N / (3 * PHI_SQUARED)) }),
  };

  const calculator = windingMap[particle.toLowerCase()];
  if (!calculator) {
    return { p: 1, q: 1 };
  }

  return calculator(epoch);
}

/**
 * Create a tube geometry following a path (for winding visualization)
 */
export function createTubePath(
  points: THREE.Vector3[],
  radius: number = 0.05,
  radialSegments: number = 8
): THREE.TubeGeometry {
  const curve = new THREE.CatmullRomCurve3(points);
  return new THREE.TubeGeometry(curve, points.length, radius, radialSegments, false);
}

/**
 * Create a golden spiral in 2D (for UI elements)
 */
export function createGoldenSpiral2D(
  turns: number = 3,
  samples: number = 200
): THREE.Vector2[] {
  const points: THREE.Vector2[] = [];
  const a = 0.1;
  const b = Math.log(PHI) / (Math.PI / 2);

  for (let i = 0; i <= samples; i++) {
    const theta = (i / samples) * turns * 2 * Math.PI;
    const r = a * Math.exp(b * theta);
    points.push(new THREE.Vector2(r * Math.cos(theta), r * Math.sin(theta)));
  }

  return points;
}

/**
 * Create a golden spiral in 3D
 */
export function createGoldenSpiral3D(
  turns: number = 3,
  samples: number = 200,
  zScale: number = 1
): THREE.Vector3[] {
  const points: THREE.Vector3[] = [];
  const a = 0.1;
  const b = Math.log(PHI) / (Math.PI / 2);

  for (let i = 0; i <= samples; i++) {
    const theta = (i / samples) * turns * 2 * Math.PI;
    const r = a * Math.exp(b * theta);
    const z = theta * zScale;
    points.push(new THREE.Vector3(r * Math.cos(theta), r * Math.sin(theta), z));
  }

  return points;
}

/**
 * Convert spherical coordinates to Cartesian
 */
export function sphericalToCartesian(r: number, theta: number, phi: number): THREE.Vector3 {
  return new THREE.Vector3(
    r * Math.sin(phi) * Math.cos(theta),
    r * Math.sin(phi) * Math.sin(theta),
    r * Math.cos(phi)
  );
}

/**
 * Create a color gradient based on golden ratio
 */
export function goldenGradientColor(t: number, startHue: number = 0.6): THREE.Color {
  const hue = (startHue + t * INV_PHI) % 1;
  return new THREE.Color().setHSL(hue, 0.8, 0.5);
}

/**
 * Create color based on resonance state
 */
export function resonanceColor(k_res: number): THREE.Color {
  return isResonant(k_res) ? new THREE.Color(0x00ff00) : new THREE.Color(0xff0000);
}
