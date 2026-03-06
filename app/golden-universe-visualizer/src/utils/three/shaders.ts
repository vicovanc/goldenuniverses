/**
 * Custom shaders for field visualization
 * GLSL shaders for rendering quantum fields and energy densities
 */

/**
 * Vertex shader for field visualization
 */
export const fieldVertexShader = `
  varying vec3 vPosition;
  varying vec3 vNormal;
  varying vec2 vUv;

  void main() {
    vPosition = position;
    vNormal = normalize(normalMatrix * normal);
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

/**
 * Fragment shader for energy density visualization
 */
export const energyDensityShader = `
  uniform float time;
  uniform float energy;
  uniform vec3 colorStart;
  uniform vec3 colorEnd;

  varying vec3 vPosition;
  varying vec3 vNormal;
  varying vec2 vUv;

  void main() {
    // Energy-based color interpolation
    float energyNorm = clamp(energy, 0.0, 1.0);
    vec3 color = mix(colorStart, colorEnd, energyNorm);

    // Add pulsing effect
    float pulse = 0.5 + 0.5 * sin(time * 2.0 + vPosition.x + vPosition.y);
    color *= (0.8 + 0.2 * pulse);

    // Fresnel effect for edges
    float fresnel = pow(1.0 - abs(dot(vNormal, vec3(0.0, 0.0, 1.0))), 2.0);
    color += fresnel * 0.3;

    gl_FragColor = vec4(color, 1.0);
  }
`;

/**
 * Fragment shader for phase space visualization
 */
export const phaseSpaceShader = `
  uniform float time;
  uniform float phiValue;
  uniform vec3 baseColor;

  varying vec3 vPosition;
  varying vec3 vNormal;
  varying vec2 vUv;

  const float PHI = 1.618033988749895;

  void main() {
    // Golden ratio-based pattern
    float pattern = sin(vPosition.x * PHI) * cos(vPosition.y / PHI);
    pattern = 0.5 + 0.5 * pattern;

    // Color based on position and golden ratio
    vec3 color = baseColor;
    color *= (0.7 + 0.3 * pattern);

    // Add time-based animation
    float wave = sin(time + length(vPosition) * PHI);
    color += wave * 0.1;

    gl_FragColor = vec4(color, 0.9);
  }
`;

/**
 * Fragment shader for winding path visualization
 */
export const windingPathShader = `
  uniform float time;
  uniform float progress;
  uniform vec3 pathColor;
  uniform float resonance;

  varying vec3 vPosition;
  varying vec2 vUv;

  void main() {
    // Fade based on progress along path
    float fade = smoothstep(progress - 0.1, progress, vUv.x);

    // Pulsing effect for resonance
    float pulse = 0.8 + 0.2 * sin(time * 3.0);

    vec3 color = pathColor * pulse;
    float alpha = fade * 0.9;

    // Highlight resonant points
    if (resonance > 0.5) {
      color += vec3(0.2, 0.2, 0.0) * sin(time * 5.0);
    }

    gl_FragColor = vec4(color, alpha);
  }
`;

/**
 * Vertex shader for particle systems
 */
export const particleVertexShader = `
  uniform float time;
  uniform float size;

  attribute float particleSize;
  attribute vec3 particleColor;

  varying vec3 vColor;

  void main() {
    vColor = particleColor;

    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);

    // Size attenuation with distance
    gl_PointSize = particleSize * size * (300.0 / -mvPosition.z);
    gl_Position = projectionMatrix * mvPosition;
  }
`;

/**
 * Fragment shader for particle systems
 */
export const particleFragmentShader = `
  uniform float time;

  varying vec3 vColor;

  void main() {
    // Circular particle shape
    vec2 center = gl_PointCoord - vec2(0.5);
    float dist = length(center);

    if (dist > 0.5) {
      discard;
    }

    // Soft edges
    float alpha = 1.0 - smoothstep(0.3, 0.5, dist);

    // Pulsing glow
    float glow = 0.8 + 0.2 * sin(time * 2.0);

    gl_FragColor = vec4(vColor * glow, alpha);
  }
`;

/**
 * Fragment shader for field lines
 */
export const fieldLineShader = `
  uniform float time;
  uniform vec3 lineColor;
  uniform float intensity;

  varying vec3 vPosition;
  varying vec2 vUv;

  void main() {
    // Flow animation along the line
    float flow = fract(vUv.x * 5.0 - time * 0.5);
    float pulse = smoothstep(0.0, 0.2, flow) * smoothstep(0.4, 0.2, flow);

    vec3 color = lineColor * (0.7 + 0.3 * pulse);
    float alpha = intensity * (0.6 + 0.4 * pulse);

    gl_FragColor = vec4(color, alpha);
  }
`;

/**
 * Create shader material for energy density
 */
export function createEnergyDensityMaterial(params?: {
  energy?: number;
  colorStart?: [number, number, number];
  colorEnd?: [number, number, number];
}): THREE.ShaderMaterialParameters {
  return {
    uniforms: {
      time: { value: 0 },
      energy: { value: params?.energy ?? 0.5 },
      colorStart: {
        value: new THREE.Vector3(...(params?.colorStart ?? [0.1, 0.2, 0.8])),
      },
      colorEnd: {
        value: new THREE.Vector3(...(params?.colorEnd ?? [0.8, 0.2, 0.1])),
      },
    },
    vertexShader: fieldVertexShader,
    fragmentShader: energyDensityShader,
  };
}

/**
 * Create shader material for phase space
 */
export function createPhaseSpaceMaterial(params?: {
  phiValue?: number;
  baseColor?: [number, number, number];
}): THREE.ShaderMaterialParameters {
  return {
    uniforms: {
      time: { value: 0 },
      phiValue: { value: params?.phiValue ?? 1.618 },
      baseColor: {
        value: new THREE.Vector3(...(params?.baseColor ?? [0.3, 0.6, 0.9])),
      },
    },
    vertexShader: fieldVertexShader,
    fragmentShader: phaseSpaceShader,
    transparent: true,
  };
}

// Add THREE import for type checking
import * as THREE from 'three';
