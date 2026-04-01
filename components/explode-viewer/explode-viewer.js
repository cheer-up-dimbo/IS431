/**
 * Explodable 3D Model Viewer — Web Component
 * 
 * Uses Three.js to render a GLB/glTF model with an interactive
 * explode slider that separates assembly components outward from
 * the model's centre of mass.
 * 
 * Requires an importmap in the host HTML:
 *   <script type="importmap">
 *   { "imports": { "three": "https://cdn.jsdelivr.net/npm/three@0.164.0/build/three.module.js",
 *     "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.164.0/examples/jsm/" } }
 *   </script>
 * 
 * Usage:
 *   <explode-viewer src="path/to/model.glb" height="500" explode-scale="2.0">
 *   </explode-viewer>
 */

import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';

class ExplodeViewer extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._parts = [];
    this._animationId = null;
  }

  connectedCallback() {
    const height = parseInt(this.getAttribute('height') || '500', 10);
    const explodeScale = parseFloat(this.getAttribute('explode-scale') || '2.0');
    const src = this.getAttribute('src') || '';
    const alt = this.getAttribute('alt') || '3D Model';

    // Parse explode axis: 'x', 'y', 'z', or custom 'x,y,z' vector
    const axisAttr = (this.getAttribute('explode-axis') || 'z').trim().toLowerCase();
    let explodeAxis;
    if (axisAttr === 'x') explodeAxis = [1, 0, 0];
    else if (axisAttr === 'y') explodeAxis = [0, 1, 0];
    else if (axisAttr === 'z') explodeAxis = [0, 0, 1];
    else {
      const parts = axisAttr.split(',').map(Number);
      explodeAxis = parts.length === 3 ? parts : [0, 0, 1];
    }

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          width: 100%;
          border-radius: 12px;
          overflow: hidden;
          background: #f0f0f0;
          position: relative;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
          margin: 16px 0;
        }
        canvas {
          width: 100% !important;
          height: ${height}px !important;
          display: block;
          cursor: grab;
        }
        canvas:active { cursor: grabbing; }
        .controls-bar {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 12px 20px;
          background: linear-gradient(135deg, #e2e8f0 0%, #f0f0f0 100%);
          border-top: 1px solid rgba(0,0,0,0.08);
        }
        .controls-bar label {
          color: #475569;
          font-size: 0.82rem;
          font-weight: 600;
          letter-spacing: 0.5px;
          text-transform: uppercase;
          white-space: nowrap;
          min-width: 60px;
        }
        .slider-container {
          flex: 1;
          display: flex;
          align-items: center;
          gap: 10px;
        }
        input[type="range"] {
          -webkit-appearance: none;
          appearance: none;
          flex: 1;
          height: 6px;
          border-radius: 3px;
          background: linear-gradient(90deg, #cbd5e1 0%, #94a3b8 100%);
          outline: none;
        }
        input[type="range"]::-webkit-slider-thumb {
          -webkit-appearance: none;
          appearance: none;
          width: 18px;
          height: 18px;
          border-radius: 50%;
          background: linear-gradient(135deg, #3b82f6, #60a5fa);
          cursor: pointer;
          box-shadow: 0 0 8px rgba(59, 130, 246, 0.5);
          transition: transform 0.15s ease;
        }
        input[type="range"]::-webkit-slider-thumb:hover {
          transform: scale(1.2);
        }
        input[type="range"]::-moz-range-thumb {
          width: 18px;
          height: 18px;
          border-radius: 50%;
          background: linear-gradient(135deg, #3b82f6, #60a5fa);
          cursor: pointer;
          border: none;
          box-shadow: 0 0 8px rgba(59, 130, 246, 0.5);
        }
        .slider-value {
          color: #3b82f6;
          font-size: 0.85rem;
          font-weight: 600;
          min-width: 36px;
          text-align: right;
          font-variant-numeric: tabular-nums;
        }
        .reset-btn {
          background: transparent;
          border: 1px solid rgba(71, 85, 105, 0.3);
          color: #475569;
          padding: 4px 12px;
          border-radius: 6px;
          font-size: 0.78rem;
          cursor: pointer;
          transition: all 0.2s ease;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }
        .reset-btn:hover {
          border-color: #60a5fa;
          color: #60a5fa;
          background: rgba(96, 165, 250, 0.08);
        }
        .loading-overlay {
          position: absolute;
          inset: 0;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          background: #f0f0f0;
          z-index: 10;
          transition: opacity 0.4s ease;
        }
        .loading-overlay.hidden {
          opacity: 0;
          pointer-events: none;
        }
        .spinner {
          width: 40px;
          height: 40px;
          border: 3px solid rgba(96, 165, 250, 0.2);
          border-top-color: #60a5fa;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }
        .loading-text {
          color: #475569;
          font-size: 0.85rem;
          margin-top: 12px;
        }
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
        .part-count {
          color: #475569;
          font-size: 0.75rem;
          padding: 4px 20px 8px;
          background: #f0f0f0;
        }
        .caption {
          color: #475569;
          font-size: 0.85rem;
          text-align: center;
          padding: 8px 16px 12px;
          font-style: italic;
          background: #f0f0f0;
        }
      </style>

      <div class="loading-overlay" id="loader">
        <div class="spinner"></div>
        <div class="loading-text">Loading 3D Model…</div>
      </div>
      <canvas id="canvas"></canvas>
      <div class="controls-bar">
        <label for="exploder">Explode</label>
        <div class="slider-container">
          <input type="range" id="exploder" min="0" max="100" value="0" step="1">
          <span class="slider-value" id="sliderVal">0%</span>
        </div>
        <button class="reset-btn" id="resetBtn">Reset</button>
      </div>
      <div class="part-count" id="partCount"></div>
      <div class="caption">${alt}</div>
    `;

    this._initScene(height, explodeScale, src, explodeAxis);
  }

  _initScene(height, explodeScale, src, explodeAxis) {
    const canvas = this.shadowRoot.getElementById('canvas');
    const loaderEl = this.shadowRoot.getElementById('loader');
    const slider = this.shadowRoot.getElementById('exploder');
    const sliderVal = this.shadowRoot.getElementById('sliderVal');
    const resetBtn = this.shadowRoot.getElementById('resetBtn');
    const partCountEl = this.shadowRoot.getElementById('partCount');

    const width = this.offsetWidth || this.clientWidth || 800;

    // ─── Scene ───
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);

    // ─── Camera ───
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.01, 1000);
    camera.position.set(0, 0.3, 0.8);

    // ─── Renderer ───
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(width, height);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.0;

    this._renderer = renderer;
    this._camera = camera;
    this._scene = scene;

    // ─── Lighting ───
    scene.add(new THREE.AmbientLight(0xffffff, 0.6));
    const dirLight1 = new THREE.DirectionalLight(0xffffff, 1.2);
    dirLight1.position.set(5, 8, 5);
    scene.add(dirLight1);
    const dirLight2 = new THREE.DirectionalLight(0x8ec5fc, 0.4);
    dirLight2.position.set(-3, 2, -5);
    scene.add(dirLight2);

    // ─── Orbit Controls ───
    const controls = new OrbitControls(camera, canvas);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 1.0;
    controls.enablePan = true;
    this._controls = controls;

    // ─── Load Model ───
    const dracoLoader = new DRACOLoader();
    dracoLoader.setDecoderPath('https://cdn.jsdelivr.net/npm/three@0.164.0/examples/jsm/libs/draco/');
    const gltfLoader = new GLTFLoader();
    gltfLoader.setDRACOLoader(dracoLoader);
    gltfLoader.load(
      src,
      (gltf) => {
        const model = gltf.scene;

        // Centre and scale
        const box = new THREE.Box3().setFromObject(model);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);
        const scale = 0.5 / maxDim;
        model.scale.setScalar(scale);
        model.position.sub(center.clone().multiplyScalar(scale));
        scene.add(model);

        // ─── Collect Explodable Parts (axis-aligned) ───
        const axis = new THREE.Vector3(...explodeAxis).normalize();
        this._parts = [];

        // First pass: compute each mesh's signed distance along the axis
        const meshData = [];
        model.traverse((child) => {
          if (child.isMesh) {
            const worldPos = new THREE.Vector3();
            child.getWorldPosition(worldPos);
            // Signed projection onto axis (distance from model centre)
            const signedDist = worldPos.dot(axis);
            meshData.push({ mesh: child, signedDist });
          }
        });

        // Find the median distance to use as the explode centre
        if (meshData.length > 0) {
          const dists = meshData.map(d => d.signedDist).sort((a, b) => a - b);
          const medianDist = dists[Math.floor(dists.length / 2)];

          meshData.forEach(({ mesh, signedDist }) => {
            // Direction along axis: positive if above median, negative if below
            const offset = signedDist - medianDist;
            // Direction is just the axis, sign determined by offset
            const direction = axis.clone().multiplyScalar(offset >= 0 ? 1 : -1);
            // Magnitude proportional to distance from median
            const magnitude = Math.abs(offset) > 0.0001 ? Math.abs(offset) : 0.01;

            this._parts.push({
              mesh,
              originalPosition: mesh.position.clone(),
              explodeDirection: direction,
              explodeMagnitude: magnitude,
              name: mesh.name || mesh.parent?.name || 'unnamed'
            });
          });
        }

        partCountEl.textContent =
          `${this._parts.length} component${this._parts.length !== 1 ? 's' : ''} detected in scene graph`;

        // Fit camera
        const fov = camera.fov * (Math.PI / 180);
        const cameraZ = (0.5 / Math.tan(fov / 2)) * 1.5;
        camera.position.set(cameraZ * 0.7, cameraZ * 0.4, cameraZ);
        controls.target.set(0, 0, 0);
        controls.update();

        loaderEl.classList.add('hidden');
        console.log('[ExplodeViewer] Loaded:', this._parts.length, 'parts');
      },
      (progress) => {
        if (progress.total > 0) {
          const pct = Math.round((progress.loaded / progress.total) * 100);
          loaderEl.querySelector('.loading-text').textContent = `Loading… ${pct}%`;
        }
      },
      (error) => {
        console.error('[ExplodeViewer] Load error:', error);
        loaderEl.querySelector('.loading-text').textContent = 'Failed to load model.';
        loaderEl.querySelector('.spinner').style.display = 'none';
      }
    );

    // ─── Slider ───
    slider.addEventListener('input', () => {
      const factor = slider.value / 100;
      sliderVal.textContent = `${slider.value}%`;
      controls.autoRotate = false;
      this._parts.forEach((p) => {
        p.mesh.position.copy(p.originalPosition);
        p.mesh.position.addScaledVector(
          p.explodeDirection,
          factor * explodeScale * p.explodeMagnitude
        );
      });
    });

    resetBtn.addEventListener('click', () => {
      slider.value = 0;
      sliderVal.textContent = '0%';
      this._parts.forEach((p) => p.mesh.position.copy(p.originalPosition));
    });

    // ─── Animate ───
    const animate = () => {
      this._animationId = requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    // ─── Resize ───
    this._resizeObserver = new ResizeObserver(() => {
      const w = this.offsetWidth || this.clientWidth || 800;
      camera.aspect = w / height;
      camera.updateProjectionMatrix();
      renderer.setSize(w, height);
    });
    this._resizeObserver.observe(this);
  }

  disconnectedCallback() {
    if (this._animationId) cancelAnimationFrame(this._animationId);
    if (this._resizeObserver) this._resizeObserver.disconnect();
    if (this._renderer) this._renderer.dispose();
  }
}

customElements.define('explode-viewer', ExplodeViewer);
