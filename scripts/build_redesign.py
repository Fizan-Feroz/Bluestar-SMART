import os
import re

def create_redesign():
    with open('web-dashboard/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Title and Add subtle Redesign Preview Banner indicator
    content = content.replace(
        '<title>Blue Star Smart Climate — 3D Digital Twin</title>',
        '<title>Blue Star Smart Climate — Redesign Preview</title>'
    )

    # 2. Refine Theme Variables in CSS
    old_root = """:root {
  color-scheme: dark;
  --bg: #0a0c10;
  --surface: #11151c;
  --surface-2: #181d26;
  --surface-3: #202632;
  --line: rgba(255, 255, 255, 0.08);
  --line-strong: rgba(255, 255, 255, 0.16);
  --text: #f2f5f9;
  --text-2: #a7b1bf;
  --text-3: #7f8a9a;
  --accent: #4aa8ea;
  --accent-ink: #06121d;
  --accent-soft: rgba(74, 168, 234, 0.14);
  --live: #4ade80;
  --warn: #fbbf24;
  --danger: #f87171;
  --shadow-float: 0 24px 64px rgba(0, 0, 0, 0.45);"""

    new_root = """:root {
  color-scheme: dark;
  --bg: #080a0f;
  --surface: #0f131c;
  --surface-2: #151b26;
  --surface-3: #1d2535;
  --surface-hover: #263145;
  --line: rgba(255, 255, 255, 0.07);
  --line-strong: rgba(255, 255, 255, 0.15);
  --text: #f8fafc;
  --text-2: #94a3b8;
  --text-3: #64748b;
  --accent: #38bdf8;
  --accent-ink: #041424;
  --accent-soft: rgba(56, 189, 248, 0.12);
  --accent-glow: rgba(56, 189, 248, 0.35);
  --live: #34d399;
  --warn: #fbbf24;
  --danger: #f87171;
  --shadow-float: 0 24px 60px -12px rgba(0, 0, 0, 0.65), 0 0 1px 1px rgba(255, 255, 255, 0.08);"""

    content = content.replace(old_root, new_root)

    old_light = """html[data-theme="light"] {
  color-scheme: light;
  --bg: #f3f5f8;
  --surface: #ffffff;
  --surface-2: #eef2f6;
  --surface-3: #e4eaf1;
  --line: rgba(15, 23, 42, 0.08);
  --line-strong: rgba(15, 23, 42, 0.16);
  --text: #0e1620;
  --text-2: #4a5565;
  --text-3: #66717f;
  --accent: #0b6fc2;
  --accent-ink: #ffffff;
  --accent-soft: rgba(11, 111, 194, 0.09);
  --live: #15803d;
  --warn: #b45309;
  --danger: #b91c1c;
  --shadow-float: 0 20px 48px rgba(15, 23, 42, 0.12);
}"""

    new_light = """html[data-theme="light"] {
  color-scheme: light;
  --bg: #f8fafc;
  --surface: #ffffff;
  --surface-2: #f1f5f9;
  --surface-3: #e2e8f0;
  --surface-hover: #cbd5e1;
  --line: rgba(15, 23, 42, 0.08);
  --line-strong: rgba(15, 23, 42, 0.16);
  --text: #0f172a;
  --text-2: #475569;
  --text-3: #64748b;
  --accent: #0284c7;
  --accent-ink: #ffffff;
  --accent-soft: rgba(2, 132, 199, 0.10);
  --accent-glow: rgba(2, 132, 199, 0.25);
  --live: #059669;
  --warn: #b45309;
  --danger: #b91c1c;
  --shadow-float: 0 20px 48px -10px rgba(15, 23, 42, 0.12), 0 0 1px 1px rgba(15, 23, 42, 0.06);
}"""

    content = content.replace(old_light, new_light)

    # 3. CSS Enhancements for Louver Icons, Wave Animation, Badge & Dial
    louver_css_additions = """
/* Louver Icons and Animations */
.pill-icon {
  width: 17px;
  height: 17px;
  display: block;
  flex: 0 0 auto;
}

@keyframes louverOscillate {
  0%, 100% {
    transform: rotate(0deg);
  }
  50% {
    transform: rotate(-16deg);
  }
}

.seg-btn.active .swing-animated-blade {
  animation: louverOscillate 2.4s ease-in-out infinite;
  transform-origin: 4px 11px;
}

@keyframes lateralPulse {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-2.5px);
  }
  75% {
    transform: translateX(2.5px);
  }
}

.seg-btn.active .lateral-arrows {
  animation: lateralPulse 2.0s ease-in-out infinite;
}

/* Dynamic Live Louver Badge */
.louver-angle-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-display);
  font-variant-numeric: tabular-nums;
  font-size: 13px;
  font-weight: 500;
  color: var(--accent);
}

.louver-angle-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 8px var(--accent);
  animation: pulseDot 2s ease-in-out infinite;
}

@keyframes pulseDot {
  0%, 100% { opacity: 0.4; transform: scale(0.9); }
  50% { opacity: 1; transform: scale(1.2); }
}

/* Preview Banner */
.preview-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 8px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.02em;
  background: var(--surface-2);
  border: 1px solid var(--line);
  color: var(--text-2);
}

.preview-badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
}

@media (max-width: 700px) {
  .preview-badge {
    display: none;
  }
}
"""
    content = content.replace('.seg-btn svg {', louver_css_additions + '\n.seg-btn svg {')

    # 4. Update the Louver Section in HTML with bespoke SVG icons
    old_louver_html = """      <section class="group">
        <div class="group-head">
          <span class="group-title">Louver</span>
          <span class="group-value" id="vaneBadge">Auto swing</span>
        </div>
        <div class="pills cols-5" role="group" aria-label="Louver direction">
          <button class="seg-btn active" id="vaneBtn0" type="button" aria-pressed="true" onclick="setVane(0)"><span>Swing</span></button>
          <button class="seg-btn" id="vaneBtn1" type="button" aria-pressed="false" onclick="setVane(1)"><span>Top</span></button>
          <button class="seg-btn" id="vaneBtn3" type="button" aria-pressed="false" onclick="setVane(3)"><span>Middle</span></button>
          <button class="seg-btn" id="vaneBtn5" type="button" aria-pressed="false" onclick="setVane(5)"><span>Low</span></button>
          <button class="seg-btn" id="hSwingBtn" type="button" aria-pressed="false" onclick="toggleHSwing()"><span>4-way</span></button>
        </div>
      </section>"""

    new_louver_html = """      <section class="group">
        <div class="group-head">
          <span class="group-title">Louver & Swing</span>
          <span class="group-value" id="vaneBadge">Auto sweep · 54°</span>
        </div>
        <div class="pills cols-5" role="group" aria-label="Louver and swing controls">
          <button class="seg-btn active" id="vaneBtn0" type="button" aria-pressed="true" onclick="setVane(0)">
            <svg viewBox="0 0 24 24" class="pill-icon swing-icon" aria-hidden="true">
              <rect x="2" y="4" width="20" height="7" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/>
              <path class="swing-animated-blade" d="M4 11c3 4 8 4 11 0" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
              <path d="M7 16c2.5 1.8 7.5 1.8 10 0" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-dasharray="2 2" opacity="0.6"/>
            </svg>
            <span>Swing</span>
          </button>
          <button class="seg-btn" id="vaneBtn1" type="button" aria-pressed="false" onclick="setVane(1)">
            <svg viewBox="0 0 24 24" class="pill-icon" aria-hidden="true">
              <rect x="2" y="4" width="20" height="7" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/>
              <path d="M4 11l10-2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M15 8h4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity="0.6"/>
            </svg>
            <span>Top</span>
          </button>
          <button class="seg-btn" id="vaneBtn3" type="button" aria-pressed="false" onclick="setVane(3)">
            <svg viewBox="0 0 24 24" class="pill-icon" aria-hidden="true">
              <rect x="2" y="4" width="20" height="7" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/>
              <path d="M4 11h11" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M16 11h3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity="0.6"/>
            </svg>
            <span>Middle</span>
          </button>
          <button class="seg-btn" id="vaneBtn5" type="button" aria-pressed="false" onclick="setVane(5)">
            <svg viewBox="0 0 24 24" class="pill-icon" aria-hidden="true">
              <rect x="2" y="4" width="20" height="7" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/>
              <path d="M4 11l9 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M14 17l4 2" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity="0.6"/>
            </svg>
            <span>Low</span>
          </button>
          <button class="seg-btn" id="hSwingBtn" type="button" aria-pressed="false" onclick="toggleHSwing()">
            <svg viewBox="0 0 24 24" class="pill-icon lateral-arrows" aria-hidden="true">
              <path d="M7 8l-4 4 4 4M17 8l4 4-4 4M3 12h18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>4-Way</span>
          </button>
        </div>
      </section>"""
    content = content.replace(old_louver_html, new_louver_html)

    # Add preview badge in header
    old_brand = """        <span class="brand-model">IC318QNU · Smart inverter</span>
      </div>"""
    new_brand = """        <span class="brand-model">IC318QNU · Smart inverter</span>
      </div>
      <span class="preview-badge"><span class="preview-badge-dot"></span>Redesign Preview</span>"""
    content = content.replace(old_brand, new_brand)

    # 5. Revamp Kinematics & Three.js Lighting
    old_kinematics_vars = """    let ventVanes = [];
    const LOUVER_CLOSED = 0;
    const LOUVER_CYCLE = 3.2;
    const LOUVER_SWEEP_MIN = 0.80;
    const LOUVER_SWEEP_MAX = 1.24;
    const LOUVER_STEPS = { 1: 0.72, 2: 0.82, 3: 0.92, 4: 1.0, 5: 1.1, 6: 0.92 };
    const louverSpring = { x: 0, v: 0 };
    const swingEnvelope = { x: 0, v: 0 };

    function springStep(spring, target, dt) {
      const stiffness = 60;
      const damping = 2 * Math.sqrt(stiffness);
      const accel = stiffness * (target - spring.x) - damping * spring.v;
      spring.v += accel * dt;
      spring.x += spring.v * dt;
    }"""

    new_kinematics_vars = """    let ventVanes = [];
    let keyLight, fillLight, rimLight, ambientLight, hemiLight;

    // Kinematic Stepper Motor Model
    let currentLouverAngle = 0; // Current physical angle in radians
    let currentVaneAngle = 0;   // Current horizontal vane sweep in radians
    let currentHSwingAmp = 0;   // Eased envelope for 4-way horizontal sweep (0..1)

    const LOUVER_CLOSED = 0.00;
    const LOUVER_SWING_PERIOD = 4.2; // 4.2s smooth full oscillation cycle
    const LOUVER_SWING_MIN = 0.70;   // ~40.1 deg (Coanda / ceiling glide)
    const LOUVER_SWING_MAX = 1.22;   // ~69.9 deg (Floor comfort throw)
    const LOUVER_STEPS = {
      1: 0.72, // Top (41.2°)
      2: 0.82, // High-Mid (47.0°)
      3: 0.94, // Mid (53.8°)
      4: 1.06, // Mid-Low (60.7°)
      5: 1.18, // Low (67.6°)
      6: 0.94  // Auto fallback
    };"""
    content = content.replace(old_kinematics_vars, new_kinematics_vars)

    # In setupLighting(), assign to variables
    old_lighting = """    function setupLighting() {
      scene.add(new THREE.AmbientLight(0xa9c8df, 0.18));
      scene.add(new THREE.HemisphereLight(0xe8f9ff, 0x07111b, 0.4));

      const keyLight = new THREE.DirectionalLight(0xffffff, 0.95);
      keyLight.position.set(3.4, 4.4, 3.6);
      keyLight.castShadow = true;
      keyLight.shadow.mapSize.set(2048, 2048);
      keyLight.shadow.camera.near = 0.5;
      keyLight.shadow.camera.far = 14;
      keyLight.shadow.camera.left = -3.2;
      keyLight.shadow.camera.right = 3.2;
      keyLight.shadow.camera.top = 3.2;
      keyLight.shadow.camera.bottom = -3.2;
      keyLight.shadow.bias = -0.0007;
      keyLight.shadow.radius = 4;
      scene.add(keyLight);

      const fillLight = new THREE.DirectionalLight(0x5dc9f5, 0.3);
      fillLight.position.set(-4.0, 1.0, 3.0);
      scene.add(fillLight);

      const rimLight = new THREE.DirectionalLight(0x7de9ff, 0.55);
      rimLight.position.set(-1.8, 1.6, -3.8);
      scene.add(rimLight);"""

    new_lighting = """    function setupLighting() {
      ambientLight = new THREE.AmbientLight(0xa9c8df, 0.18);
      scene.add(ambientLight);
      hemiLight = new THREE.HemisphereLight(0xe8f9ff, 0x07111b, 0.4);
      scene.add(hemiLight);

      keyLight = new THREE.DirectionalLight(0xffffff, 0.95);
      keyLight.position.set(3.4, 4.4, 3.6);
      keyLight.castShadow = true;
      keyLight.shadow.mapSize.set(2048, 2048);
      keyLight.shadow.camera.near = 0.5;
      keyLight.shadow.camera.far = 14;
      keyLight.shadow.camera.left = -3.2;
      keyLight.shadow.camera.right = 3.2;
      keyLight.shadow.camera.top = 3.2;
      keyLight.shadow.camera.bottom = -3.2;
      keyLight.shadow.bias = -0.0007;
      keyLight.shadow.radius = 4;
      scene.add(keyLight);

      fillLight = new THREE.DirectionalLight(0x5dc9f5, 0.3);
      fillLight.position.set(-4.0, 1.0, 3.0);
      scene.add(fillLight);

      rimLight = new THREE.DirectionalLight(0x7de9ff, 0.55);
      rimLight.position.set(-1.8, 1.6, -3.8);
      scene.add(rimLight);"""
    content = content.replace(old_lighting, new_lighting)

    # In applyStageTheme(), adjust lights
    old_apply_stage = """    function applyStageTheme(theme) {
      if (typeof THREE === "undefined") return;
      const light = theme === "light";
      if (renderer) renderer.toneMappingExposure = light ? 1.0 : 0.9;
      if (scene && scene.fog) scene.fog.color.set(light ? 0xf3f5f8 : 0x0a0c10);
      if (stageFloor) stageFloor.material.color.set(light ? 0xdfe6ee : 0x0c1119);
      if (scene) {
        scene.traverse((object) => {
          if (object.isMesh && object.geometry && object.geometry.type === "RingGeometry") {
            const inner = object.geometry.parameters.innerRadius < 2;
            object.material.color.set(light ? 0x0b6fc2 : 0x2e8db4);
            object.material.opacity = inner ? (light ? 0.14 : 0.2) : (light ? 0.05 : 0.085);
          }
        });
      }
      if (airflowParticles) {
        airflowParticles.material.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
        airflowParticles.material.needsUpdate = true;
      }
    }"""

    new_apply_stage = """    function applyStageTheme(theme) {
      if (typeof THREE === "undefined") return;
      const light = theme === "light";
      if (renderer) renderer.toneMappingExposure = light ? 1.04 : 0.92;
      if (scene && scene.fog) scene.fog.color.set(light ? 0xf8fafc : 0x080a0f);
      if (stageFloor) stageFloor.material.color.set(light ? 0xf1f5f9 : 0x0c1017);

      if (ambientLight) {
        ambientLight.intensity = light ? 0.38 : 0.18;
        ambientLight.color.setHex(light ? 0xffffff : 0xa9c8df);
      }
      if (hemiLight) {
        hemiLight.intensity = light ? 0.45 : 0.4;
        hemiLight.color.setHex(light ? 0xffffff : 0xe8f9ff);
      }
      if (fillLight) {
        fillLight.intensity = light ? 0.42 : 0.3;
        fillLight.color.setHex(light ? 0xdbeafe : 0x5dc9f5);
      }
      if (rimLight) {
        rimLight.intensity = light ? 0.35 : 0.6;
        rimLight.color.setHex(light ? 0xc7d2fe : 0x7de9ff);
      }

      if (scene) {
        scene.traverse((object) => {
          if (object.isMesh && object.geometry && object.geometry.type === "RingGeometry") {
            const inner = object.geometry.parameters.innerRadius < 2;
            object.material.color.set(light ? 0x0284c7 : 0x38bdf8);
            object.material.opacity = inner ? (light ? 0.12 : 0.18) : (light ? 0.04 : 0.07);
          }
        });
      }
      if (airflowParticles) {
        airflowParticles.material.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
        airflowParticles.material.needsUpdate = true;
      }
    }"""
    content = content.replace(old_apply_stage, new_apply_stage)

    # In animate(), replace louver and 4-way vane animation
    old_animate_louver = """      // Louver: sweep with dwell at the ends, or settle to a fixed step with a damped spring
      if (louverPivot) {
        let targetAngle = LOUVER_CLOSED;
        if (state.power === 1) {
          if (state.vane === 0) {
            const cycle = REDUCED_MOTION ? 0.5 : (time % LOUVER_CYCLE) / LOUVER_CYCLE;
            const phase = 0.5 - 0.5 * Math.cos(cycle * Math.PI * 2);
            const eased = phase * phase * phase * (phase * (phase * 6 - 15) + 10);
            targetAngle = LOUVER_SWEEP_MIN + (LOUVER_SWEEP_MAX - LOUVER_SWEEP_MIN) * eased;
          } else {
            targetAngle = LOUVER_STEPS[state.vane] || LOUVER_STEPS[3];
          }
        }
        springStep(louverSpring, targetAngle, delta);
        louverPivot.rotation.x = louverSpring.x;
      }

      // Blower drum
      if (blowerDrum && state.power === 1) {
        const fanSpeeds = [0, 1.4, 2.5, 4.0, 6.0, 9.4, 3.8];
        blowerDrum.rotateY((fanSpeeds[state.fan] || 4.0) * delta);
      }

      // 4-way vanes: an eased envelope gates a phase-offset wave, so toggling never pops
      if (ventVanes.length) {
        const swingOn = state.power === 1 && state.hSwing === 1 && !REDUCED_MOTION ? 1 : 0;
        springStep(swingEnvelope, swingOn, delta);
        const envelope = Math.min(1, Math.max(0, swingEnvelope.x));
        ventVanes.forEach((vane, index) => {
          vane.rotation.y = envelope * 0.42 * Math.sin(time * 1.6 - index * 0.46);
        });
      }"""

    new_animate_louver = """      // Revamped Louver Stepper Kinematics
      if (louverPivot) {
        let targetAngle = LOUVER_CLOSED;
        if (state.power === 1) {
          if (state.vane === 0) {
            // Auto swing: Harmonic stepper curve with cushioned dwell at extremes
            if (REDUCED_MOTION) {
              targetAngle = (LOUVER_SWING_MIN + LOUVER_SWING_MAX) / 2;
            } else {
              const cycle = (time % LOUVER_SWING_PERIOD) / LOUVER_SWING_PERIOD;
              const cosPhase = 0.5 - 0.5 * Math.cos(cycle * Math.PI * 2);
              // Quintic smootherstep for soft cushioned turnaround
              const smoothed = cosPhase * cosPhase * cosPhase * (cosPhase * (cosPhase * 6 - 15) + 10);
              targetAngle = LOUVER_SWING_MIN + (LOUVER_SWING_MAX - LOUVER_SWING_MIN) * smoothed;
            }
          } else {
            targetAngle = LOUVER_STEPS[state.vane] || LOUVER_STEPS[3];
          }
        }

        // Smooth, critically damped stepper tracking (no bouncy spring overshoot)
        const trackSpeed = (state.power === 0) ? 4.5 : (state.vane === 0 ? 12.0 : 7.0);
        currentLouverAngle = THREE.MathUtils.damp(currentLouverAngle, targetAngle, trackSpeed, delta);
        louverPivot.rotation.x = currentLouverAngle;

        // Real-time angle readout in UI
        const angleDeg = Math.round(currentLouverAngle * (180 / Math.PI));
        const louverBadge = document.getElementById("vaneBadge");
        if (louverBadge) {
          if (state.power === 0) {
            louverBadge.textContent = "Standby · Parked";
          } else if (state.vane === 0) {
            louverBadge.innerHTML = `<span class="louver-angle-badge"><span class="louver-angle-dot"></span>Auto sweep · ${angleDeg}°${state.hSwing === 1 ? ' · 4-Way' : ''}</span>`;
          } else {
            const stepNames = { 1: "Top", 3: "Middle", 5: "Low" };
            louverBadge.textContent = `${stepNames[state.vane] || 'Manual'} · ${angleDeg}°${state.hSwing === 1 ? ' · 4-Way' : ''}`;
          }
        }
      }

      // Blower drum
      if (blowerDrum && state.power === 1) {
        const fanSpeeds = [0, 1.4, 2.5, 4.0, 6.0, 9.4, 3.8];
        blowerDrum.rotateY((fanSpeeds[state.fan] || 4.0) * delta);
      }

      // 4-way vanes: Synchronized motorized lateral sweep with aerodynamic outward divergence
      if (ventVanes.length) {
        const targetHSwing = (state.power === 1 && state.hSwing === 1 && !REDUCED_MOTION) ? 1.0 : 0.0;
        currentHSwingAmp = THREE.MathUtils.damp(currentHSwingAmp, targetHSwing, 3.5, delta);
        const sweepAngle = Math.sin(time * 1.5) * 0.44 * currentHSwingAmp;
        currentVaneAngle = sweepAngle;
        ventVanes.forEach((vane, index) => {
          const aerodynamicSpread = (index - 6) * 0.012 * currentHSwingAmp;
          vane.rotation.y = sweepAngle + aerodynamicSpread;
        });
      }"""
    content = content.replace(old_animate_louver, new_animate_louver)

    # In resetParticle(), couple with louver and vane angle
    old_reset_particle = """    function resetParticle(index, immediateSpread) {
      const offset = index * 3;
      particlePositions[offset] = (Math.random() - 0.5) * (VENT_W - 0.14);
      particlePositions[offset + 1] = VENT_Y + (Math.random() - 0.2) * 0.06;
      particlePositions[offset + 2] = FRONT_Z + 0.05 + Math.random() * 0.04;

      const speeds = [0, 0.15, 0.24, 0.36, 0.52, 0.8, 0.34];
      const speed = speeds[state.fan] || 0.36;
      const spread = 0.7 + Math.random() * 0.7;

      particleVelocities[offset] = (Math.random() - 0.5) * speed * 0.36;
      const pitch = Math.abs(louverPivot ? louverPivot.rotation.x : 0.9);
      particleVelocities[offset + 1] = -speed * (0.35 + 0.9 * Math.sin(pitch)) * (0.8 + Math.random() * 0.4);
      particleVelocities[offset + 2] = speed * (0.5 + 0.5 * Math.cos(pitch)) * spread;

      particleLifespans[index] = immediateSpread ? Math.random() : 0;
    }"""

    new_reset_particle = """    function resetParticle(index, immediateSpread) {
      const offset = index * 3;
      particlePositions[offset] = (Math.random() - 0.5) * (VENT_W - 0.16);
      particlePositions[offset + 1] = VENT_Y + (Math.random() - 0.5) * 0.04;
      particlePositions[offset + 2] = FRONT_Z + 0.02 + Math.random() * 0.03;

      const speeds = [0, 0.16, 0.25, 0.38, 0.54, 0.82, 0.36];
      const speed = speeds[state.fan] || 0.38;
      const spread = 0.75 + Math.random() * 0.65;

      const pitch = Math.abs(currentLouverAngle);
      const yaw = currentVaneAngle;

      particleVelocities[offset] = Math.sin(yaw) * speed * 0.82 + (Math.random() - 0.5) * speed * 0.18;
      particleVelocities[offset + 1] = -speed * (0.32 + 0.92 * Math.sin(pitch)) * (0.8 + Math.random() * 0.4);
      particleVelocities[offset + 2] = speed * (0.55 + 0.45 * Math.cos(pitch)) * spread;

      particleLifespans[index] = immediateSpread ? Math.random() : 0;
    }"""
    content = content.replace(old_reset_particle, new_reset_particle)

    # In renderUI(), prevent overriding vaneBadge with static text if louverPivot is active
    old_render_vane = """      // Louver direction
      const vaneNames = { 0: "Auto swing", 1: "Top / 1", 3: "Middle / 3", 5: "Low / 5" };
      document.getElementById("vaneBadge").textContent = vaneNames[state.vane] || "Custom vane";"""
    new_render_vane = """      // Louver direction
      const vaneNames = { 0: "Auto sweep", 1: "Top", 3: "Middle", 5: "Low" };
      if (!louverPivot) {
        document.getElementById("vaneBadge").textContent = vaneNames[state.vane] || "Custom vane";
      }"""
    content = content.replace(old_render_vane, new_render_vane)

    # Write web-dashboard/redesign.html
    with open('web-dashboard/redesign.html', 'w', encoding='utf-8') as f:
        f.write(content)

    # Also mirror to root redesign.html
    with open('redesign.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully built web-dashboard/redesign.html and redesign.html!")

if __name__ == '__main__':
    create_redesign()
