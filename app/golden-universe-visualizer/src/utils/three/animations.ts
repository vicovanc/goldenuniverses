/**
 * Animation utilities for Three.js visualizations
 */

import * as THREE from 'three';

export interface AnimationState {
  isPlaying: boolean;
  progress: number;
  speed: number;
  time: number;
  loop: boolean;
}

export class AnimationController {
  private state: AnimationState;
  private callbacks: Map<string, (state: AnimationState) => void>;
  private lastTime: number;
  private animationId: number | null;

  constructor(initialState?: Partial<AnimationState>) {
    this.state = {
      isPlaying: false,
      progress: 0,
      speed: 1,
      time: 0,
      loop: true,
      ...initialState,
    };
    this.callbacks = new Map();
    this.lastTime = performance.now();
    this.animationId = null;
  }

  play(): void {
    if (!this.state.isPlaying) {
      this.state.isPlaying = true;
      this.lastTime = performance.now();
      this.animate();
    }
  }

  pause(): void {
    this.state.isPlaying = false;
    if (this.animationId !== null) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }

  reset(): void {
    this.state.progress = 0;
    this.state.time = 0;
    this.notifyCallbacks();
  }

  setSpeed(speed: number): void {
    this.state.speed = speed;
  }

  setProgress(progress: number): void {
    this.state.progress = Math.max(0, Math.min(1, progress));
    this.notifyCallbacks();
  }

  getState(): AnimationState {
    return { ...this.state };
  }

  on(event: string, callback: (state: AnimationState) => void): void {
    this.callbacks.set(event, callback);
  }

  off(event: string): void {
    this.callbacks.delete(event);
  }

  private animate = (): void => {
    if (!this.state.isPlaying) return;

    const currentTime = performance.now();
    const deltaTime = (currentTime - this.lastTime) / 1000;
    this.lastTime = currentTime;

    this.state.time += deltaTime * this.state.speed;
    this.state.progress += (deltaTime * this.state.speed) / 10;

    if (this.state.progress >= 1) {
      if (this.state.loop) {
        this.state.progress = 0;
      } else {
        this.state.progress = 1;
        this.pause();
      }
    }

    this.notifyCallbacks();
    this.animationId = requestAnimationFrame(this.animate);
  };

  private notifyCallbacks(): void {
    this.callbacks.forEach((callback) => callback(this.state));
  }

  dispose(): void {
    this.pause();
    this.callbacks.clear();
  }
}

/**
 * Easing functions for smooth animations
 */
export const easing = {
  linear: (t: number): number => t,

  easeInQuad: (t: number): number => t * t,

  easeOutQuad: (t: number): number => t * (2 - t),

  easeInOutQuad: (t: number): number =>
    t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t,

  easeInCubic: (t: number): number => t * t * t,

  easeOutCubic: (t: number): number => --t * t * t + 1,

  easeInOutCubic: (t: number): number =>
    t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1,

  easeInOutSine: (t: number): number => -(Math.cos(Math.PI * t) - 1) / 2,

  elastic: (t: number): number => {
    const c4 = (2 * Math.PI) / 3;
    return t === 0
      ? 0
      : t === 1
        ? 1
        : Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * c4) + 1;
  },
};

/**
 * Camera animation presets
 */
export interface CameraPreset {
  position: THREE.Vector3;
  target: THREE.Vector3;
  duration: number;
}

export const cameraPresets = {
  default: {
    position: new THREE.Vector3(5, 3, 5),
    target: new THREE.Vector3(0, 0, 0),
    duration: 1.5,
  },
  top: {
    position: new THREE.Vector3(0, 8, 0),
    target: new THREE.Vector3(0, 0, 0),
    duration: 1.5,
  },
  side: {
    position: new THREE.Vector3(8, 0, 0),
    target: new THREE.Vector3(0, 0, 0),
    duration: 1.5,
  },
  front: {
    position: new THREE.Vector3(0, 0, 8),
    target: new THREE.Vector3(0, 0, 0),
    duration: 1.5,
  },
  closeup: {
    position: new THREE.Vector3(3, 2, 3),
    target: new THREE.Vector3(0, 0, 0),
    duration: 1.5,
  },
};

/**
 * Animate camera to preset position
 */
export function animateCameraToPreset(
  camera: THREE.Camera,
  preset: CameraPreset,
  onUpdate?: () => void
): Promise<void> {
  return new Promise((resolve) => {
    const startPosition = camera.position.clone();
    const startTime = performance.now();

    const animate = () => {
      const elapsed = (performance.now() - startTime) / 1000;
      const progress = Math.min(elapsed / preset.duration, 1);
      const t = easing.easeInOutCubic(progress);

      camera.position.lerpVectors(startPosition, preset.position, t);

      if (onUpdate) onUpdate();

      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        resolve();
      }
    };

    animate();
  });
}

/**
 * Rotate object smoothly
 */
export function createRotationAnimation(
  object: THREE.Object3D,
  axis: 'x' | 'y' | 'z',
  speed: number = 1
): (deltaTime: number) => void {
  return (deltaTime: number) => {
    object.rotation[axis] += speed * deltaTime;
  };
}

/**
 * Pulse scale animation
 */
export function createPulseAnimation(
  object: THREE.Object3D,
  minScale: number = 0.9,
  maxScale: number = 1.1,
  speed: number = 2
): (time: number) => void {
  return (time: number) => {
    const scale = minScale + (maxScale - minScale) * (0.5 + 0.5 * Math.sin(time * speed));
    object.scale.setScalar(scale);
  };
}

/**
 * Orbit animation
 */
export function createOrbitAnimation(
  object: THREE.Object3D,
  radius: number,
  speed: number = 1,
  axis: 'x' | 'y' | 'z' = 'y'
): (time: number) => void {
  return (time: number) => {
    const angle = time * speed;
    if (axis === 'y') {
      object.position.x = radius * Math.cos(angle);
      object.position.z = radius * Math.sin(angle);
    } else if (axis === 'x') {
      object.position.y = radius * Math.cos(angle);
      object.position.z = radius * Math.sin(angle);
    } else {
      object.position.x = radius * Math.cos(angle);
      object.position.y = radius * Math.sin(angle);
    }
  };
}
