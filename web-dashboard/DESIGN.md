# Blue Star Smart Climate — Pure Architecture Design System & Technical Specification

**Device Target:** Blue Star IC318QNU Inverter Split Air Conditioner  
**Interface:** Flagship 3D Digital Twin & Precision Climate Console  
**Design Paradigm:** Pure Architecture — Scandinavian Monolithic Minimalism meets High-Precision Japanese Climate Engineering (Apple Home / Dyson / Nest caliber)  
**Status:** Approved Specification & Isolated Branched Staging  
**Branched Preview Files:** [`web-dashboard/redesign.html`](file:///c:/Users/fizan/OneDrive/Documents/Bluestar-SMART/web-dashboard/redesign.html) / [`redesign.html`](file:///c:/Users/fizan/OneDrive/Documents/Bluestar-SMART/redesign.html)  
**Untouched Production File:** [`web-dashboard/index.html`](file:///c:/Users/fizan/OneDrive/Documents/Bluestar-SMART/web-dashboard/index.html)  

---

## 1. Executive Summary & Brand Principles

The Blue Star Smart Climate Dashboard is conceived as a luxury product console on par with **Apple Home**, **Dyson Link**, **Bang & Olufsen**, and **Nest Learning Thermostat**. It merges an interactive, hardware-accurate 3D digital twin with tactile, frosted-glass climate controls.

### Core Tenets

1. **The Product is the Hero**: The indoor unit floats serenely at the visual focal point with authentic studio lighting and seamless contact drop shadows—never placed on crude polygonal plates or cut-off floors.
2. **Kinematic Truth**: Louver flaps and airflow vanes do not oscillate with arbitrary decorative sine waves; their movement models real unipolar stepper motors, planetary gear reduction, and synchronized mechanical tie-bars.
3. **Dual Atmospheric Themes**:
   - **Obsidian Dark ("Night Console")**: Deep space obsidian surfaces (`#08090d`) with subtle translucent hairline dividers, glowing glacier sky accents (`#38bdf8`), and velvety glass cards.
   - **Ceramic Light ("Daylight Studio")**: Architectural gallery alabaster surfaces (`#f7f9fc`) with pure white ceramic floating panels (`#ffffff`), soft ambient diffusion drop shadows, and high-contrast onyx typography (`#090e17`).
4. **Immediate Tactile Feedback**: Every interaction (slider drag, temperature step, mode change, keypad stroke) provides instant visual confirmation, micro-haptics (where supported), and soft synthesizer feedback clicks.
5. **Zero Redundancy**: Every state attribute (temperature, mode, fan speed, louver angle) lives in one definitive place. Secondary clutter, duplicate labels, and noisy badges are strictly eliminated.
6. **Accessibility First**: Meets WCAG 2.1 AAA contrast for primary controls and AA for secondary telemetry in both dark and light modes. Fully respects `prefers-reduced-motion`.

---

## 2. Color Science & Design Tokens

Both themes share an identical semantic token structure. The active theme is toggled via `html[data-theme="dark" | "light"]` and initialized via an inline script before initial paint to prevent theme flash.

### 2.1 Complete Token Palette

| Token | Dark Mode (Obsidian) | Light Mode (Ceramic) | Semantic Role | Contrast (Dark / Light) |
| :--- | :--- | :--- | :--- | :--- |
| `--bg` | `#08090d` | `#f7f9fc` | Viewport & body background | Base Canvas |
| `--surface` | `#10141e` | `#ffffff` | Primary panels, nav bar, modals | 16.5:1 / 18.5:1 |
| `--surface-glass` | `rgba(16, 20, 30, 0.72)` | `rgba(255, 255, 255, 0.88)` | Floating frosted glass panels | High-diffusion backdrop |
| `--surface-2` | `#161c2b` | `#f1f4f9` | Control pills, inactive tracks, buttons | Structural containers |
| `--surface-3` | `#1f273b` | `#e2e8f0` | Hover fills, pressed states | Interactive feedback |
| `--well` | `#0b0e15` | `#e9eef5` | Inset screens, segmented track wells | Recessed visual plane |
| `--line` | `rgba(255, 255, 255, 0.08)` | `rgba(15, 23, 42, 0.07)` | Hairline dividers, card outlines | Sub-pixel division |
| `--line-strong`| `rgba(255, 255, 255, 0.16)` | `rgba(15, 23, 42, 0.16)` | Active outlines, focus rings | Emphasized division |
| `--text` | `#ffffff` | `#090e17` | Primary titles, hero readouts | 18.0:1 / 18.2:1 (AAA) |
| `--text-2` | `#94a3b8` | `#475569` | Secondary labels, pill text | 7.8:1 / 8.2:1 (AAA) |
| `--text-3` | `#64748b` | `#64748b` | Sub-labels, captions, units | 4.8:1 / 5.1:1 (AA) |
| `--accent` | `#38bdf8` (Glacier Sky) | `#0066cc` (Blue Star Azure) | Active pill fill, live dial arc, buttons | Signature brand tone |
| `--accent-ink` | `#041424` | `#ffffff` | Text/icons on solid accent surfaces | 12.4:1 / 5.2:1 (AA/AAA) |
| `--accent-soft`| `rgba(56, 189, 248, 0.12)` | `rgba(0, 102, 204, 0.09)` | Active pill background | Soft atmospheric tint |
| `--accent-glow`| `rgba(56, 189, 248, 0.38)` | `rgba(0, 102, 204, 0.22)` | Dial halo glow, live indicator pulse | Radiance layer |
| `--live` | `#10b981` | `#059669` | Online MQTT connection, filter clean | Emerald / Mint |
| `--warn` | `#f59e0b` | `#d97706` | Syncing, reconnecting, pending | Warm Amber |
| `--danger` | `#ef4444` | `#dc2626` | Error alert, PIN failed, filter dirty | Coral Red |

### 2.2 Elevation & Shadow Hierarchy

- **Dark Floating Surfaces** (`--shadow-float`):  
  `0 24px 60px -12px rgba(0, 0, 0, 0.75), 0 0 1px 1px rgba(255, 255, 255, 0.08)`
- **Light Floating Surfaces** (`--shadow-float`):  
  `0 20px 48px -10px rgba(15, 23, 42, 0.12), 0 0 1px 1px rgba(15, 23, 42, 0.06)`

---

## 3. Typography Scale & Optical Hierarchy

- **Display Font:** `Outfit` (Geometric, refined numerals, crisp letterforms).
- **Body & Controls:** `Plus Jakarta Sans` (Humanist sans-serif with high legibility at micro-sizes).
- **Telemetry Font:** `JetBrains Mono` (Monospaced precision tabular numerals).

| UI Element | Family | Size / Line-Height | Weight | Tracking | Lettercase |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hero Temperature Number** | Outfit | 68px / 62px | 500 (Medium) | −0.04em | Tabular Nums |
| **Degree Symbol (`°`)** | Outfit | 24px / 24px | 400 (Regular) | 0.00em | Standard |
| **Delta Status Badge** | Plus Jakarta Sans | 11px / 16px | 600 (SemiBold) | 0.00em | Sentence case |
| **Group Section Headings** | Outfit | 13px / 18px | 700 (Bold) | 0.05em | Uppercase |
| **Live Louver Angle Readout**| Outfit | 26px / 26px | 700 (Bold) | 0.00em | Tabular Nums |
| **Control Pill Labels** | Plus Jakarta Sans | 11px / 14px | 600 (SemiBold) | 0.01em | Sentence case |
| **Telemetry Values** | Outfit | 16px / 20px | 600 (SemiBold) | −0.01em | Tabular Nums |
| **Telemetry Labels** | Plus Jakarta Sans | 10px / 14px | 600 (SemiBold) | 0.04em | Uppercase |
| **PIN Keypad Digits** | Outfit | 20px / 26px | 600 (SemiBold) | 0.00em | Tabular Nums |

---

## 4. 3D Digital Twin Stage, Materials & Studio Lighting

The air conditioner digital twin is rendered in Three.js (WebGL with ACESFilmic tone mapping and soft shadow maps).

### 4.1 Studio Lighting Architecture

```mermaid
flowchart TD
    subgraph ThreePointLighting [Studio 3-Point Lighting Rig]
        Key[Key Light: Directional 0xffffff, Intensity 1.0-1.1<br/>Position: 3.5, 4.8, 4.2 | PCFSoftShadowMap 2048x2048]
        Fill[Fill Light: Directional<br/>Dark: 0x38bdf8 @ 0.32 | Light: 0xcce3f8 @ 0.40]
        Rim[Rim / Silhouette Light: Directional<br/>Dark: 0x7de9ff @ 0.70 | Light: 0xe2ecff @ 0.50]
        Ambient[Ambient & Hemi Light<br/>Dark: 0.28 + 0.45 | Light: 0.45 + 0.55]
    end
    Key --> AC[Blue Star Indoor Unit 3D Twin]
    Fill --> AC
    Rim --> AC
    Ambient --> AC
```

### 4.2 Chassis Geometry & Features
1. **Curved Matte Acrylic Casing**: Built with micro-beveled front fascia, realistic depth ($2.26\text{m} \times 0.76\text{m} \times 0.52\text{m}$ in unit space).
2. **Hidden LED 7-Segment Display**: An offscreen HTML5 2D canvas dynamically projects the current setpoint (e.g. `24°` or `C1`) right through the white plastic of the front panel using an emissive texture map. When power is toggled off or display light is muted, it turns invisible.
3. **Top Intake Grille Louvers**: 7 individual recessed intake slats representing the air induction array.
4. **Discharge Vent Cavity & Blower Rotor**: Deep recessed dark cavity hosting a motorized centrifugal blower wheel that rotates in real time proportional to the selected fan stage.
5. **Seamless Infinity Ground Shadow**: Uses a dedicated `THREE.ShadowMaterial` with soft shadow mapping. Eliminates ugly circular cutoff plates—the drop shadow blends seamlessly into the background gradient in both dark and light modes.

---

## 5. Revamped Louver Kinematics & Aerodynamic Physics

The louver mechanism models the real motorized unipolar stepper motor drive inside the Blue Star IC318QNU:

### 5.1 Mechanical Kinematics Equations

The louver angle $\theta(t)$ operates in two distinct modes:

#### 1. Auto Harmonic Oscillating Sweep
The louver sweeps between $\theta_{\min} = 33.2^\circ$ ($0.58\text{ rad}$) and $\theta_{\max} = 74.5^\circ$ ($1.30\text{ rad}$) with a cycle period $T = 5.2\text{ s}$.

To simulate the mechanical gear turnaround dwell of an unipolar stepper motor, we use an 8th-order quintic smootherstep acceleration envelope:

$$\phi(t) = \frac{1 - \cos\left(\frac{2\pi t}{T}\right)}{2}$$

$$\theta_{\text{target}}(t) = \theta_{\min} + (\theta_{\max} - \theta_{\min}) \cdot \left(6\phi^5 - 15\phi^4 + 10\phi^3\right)$$

#### 2. Fixed Step Positions
| Step | Nominal Angle | Aerodynamic Purpose |
| :--- | :--- | :--- |
| **Top (Step 1)** | $33.2^\circ$ ($0.58\text{ rad}$) | Coanda ceiling draft (indirect cooling) |
| **High-Mid (Step 2)** | $43.5^\circ$ ($0.76\text{ rad}$) | Long-distance room throw |
| **Mid (Step 3)** | $53.8^\circ$ ($0.94\text{ rad}$) | Balanced ambient circulation |
| **Mid-Low (Step 4)** | $64.1^\circ$ ($1.12\text{ rad}$) | Focused occupied zone throw |
| **Floor (Step 5)** | $74.5^\circ$ ($1.30\text{ rad}$) | Direct downward air blanket |
| **Standby / Docked** | $16.0^\circ$ ($0.28\text{ rad}$) | Vane closed flush with casing |

#### 3. Continuous Damped Tracking
```javascript
const trackSpeed = (state.power === 0) ? 4.5 : (state.vane === 0 ? 12.0 : 7.0);
currentLouverAngle = THREE.MathUtils.damp(currentLouverAngle, targetAngle, trackSpeed, delta);
louverPivot.rotation.x = currentLouverAngle;
```

### 5.2 Dual Aerofoil Louver Blade
The 3D model features:
1. **Primary Deflector Blade**: Molded white aerofoil blade with fine brushed metallic trailing edge trim.
2. **Inner Velocity Sub-Vane**: An articulated secondary guide vane that pivots in tandem inside the duct to prevent internal air vortexing.

### 5.3 Live Synchronized Vector Cross-Section (2D UI)
Inside the `Airflow & Louver Director` card:
- A technical SVG side-elevation diagram shows the intake vent, coil contour, blower rotor, and discharge duct.
- An animated SVG blade `<g id="svgBladePivot">` rotates in real-time matching the 3D unit's physical degrees:
  `svgBlade.style.transform = "rotate(" + (angleDeg * 0.65) + "deg)";`
- Flow streamlines `<g class="airflow-vector-rays">` ripple with an animated gradient path, showing the real throw direction of the air.

### 5.4 Fluid Dynamics Particle Streamlines
- 700 radial glowing particles emit continuously from the discharge vent.
- Particle trajectory is tightly coupled to the louver pitch $\theta$ and horizontal vane yaw $\psi$:
  $$v_x = \sin(\psi) \cdot v \cdot 0.85$$
  $$v_y = -v \cdot (0.35 + 0.95 \sin(\theta))$$
  $$v_z = v \cdot (0.55 + 0.45 \cos(\theta))$$
- In Light Mode, particles switch to `THREE.NormalBlending` with blue azure coloration.
- In Dark Mode, particles switch to `THREE.AdditiveBlending` with glacier sky luminescence.

---

## 6. Climate Control Master Deck (UI Components)

### 6.1 Hero Thermostat Dial
- Circular SVG gauge with 24 subtle tick marks.
- Tactile temperature arc calculating normalized setpoint ($16^\circ\text{C}$ to $30^\circ\text{C}$):
  $$\text{Arc Offset} = \text{Circumference} - (26 + \text{normalized} \cdot 312)$$
- Power capsule button with breathing LED ring.
- Large $68\text{px}$ temperature numeral with ambient delta badge:
  e.g. `↓ 3.0° Cooling to Target`.
- Dual tactile circular steppers (`–` and `+`) with scale-down spring feedback on click.

### 6.2 Airflow & Louver Director
- Vector cross-section screen with live degree readout (`54° Harmonic Sweep`).
- 5 tactile buttons with custom SVG icons:
  - `Auto` (Harmonic sweep)
  - `Top` (Coanda ceiling glide)
  - `Mid` (Room center throw)
  - `Floor` (Downward drop)
  - `4-Way` (Motorized horizontal tie-bar oscillation)

### 6.3 Segmented Climate & Fan Controls
- Segmented pill track with smooth active background indicators (macOS / iOS style).
- Climate Modes: `Cool`, `Dry`, `Fan`, `Auto`.
- Fan Velocity: 6-stage track (`Quiet`, `Low`, `Med`, `High`, `Turbo`, `Auto`).
- Inverter Capacity: 4-tier convertible buttons (`100%`, `80%`, `60%`, `40%`).

### 6.4 Intelligent Features
- `Turbo Cool (110% Boost)`
- `Eco Mode (Smart Saver)`
- `Comfort Sleep (+1°C/hr gradual ramp)`
- `Indoor LED Display (Toggle unit front digits)`
- `C1 Mode (Full Load Technician Test)`

### 6.5 Bento Hardware Diagnostics
- **Compressor Frequency**: Pulsing live indicator (`48 Hz`).
- **Coil Temperature**: Evaporator temperature (`7.8°C`).
- **Total Run Hours**: Tabular hour counter (`1,248 h`).
- **Self-Clean / Filter Alert**: Health indicator (`Clean` or `Check Filter`).

---

## 7. Responsive Viewport Adaptations

| Breakpoint | Target Devices | Layout Behavior |
| :--- | :--- | :--- |
| **Desktop ($\ge 960\text{px}$)** | Desktops, Laptops, Ultrawide | Balanced two-column split: 58% 3D digital twin stage, 42% fixed scrollable control console. |
| **Tablet ($701\text{--}959\text{px}$)** | iPad, Android Tablets | Single-column stacked layout: 3D stage fixed height ($320\text{px}$), control console below. |
| **Mobile ($\le 700\text{px}$)** | Phones (iOS / Android) | 3D stage $280\text{px}$ with touch-orbit; full scrollable bento console; floating bottom command dock (`[ - ]  24°C Cooling  [ + ]  [ Power ]`). |

---

## 8. Service Worker & Offline Isolation

To prevent service worker caching conflicts between the production `index.html` and the redesigned `redesign.html`:
```javascript
// Unregister any stale service workers from localhost to guarantee fresh asset loading
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.getRegistrations().then(function(regs) {
    for (var r of regs) { r.unregister(); }
  });
}
```
All Web Audio sound feedback (clicks, chimes, error beeps) is synthesized purely with the Web Audio API—zero external audio files or network latency required.
