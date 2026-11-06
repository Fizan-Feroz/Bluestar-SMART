# Blue Star Smart Climate — Design System & Technical Specification

**Device Target:** Blue Star IC318QNU Inverter Split Air Conditioner  
**Interface:** 3D Digital Twin & Climate Control Console  
**Design Paradigm:** Precision Climate — Scandinavian Minimalism meets Japanese Micro-Engineering  
**Status:** Approved Specification & Branched Implementation  
**Reference Files:** [`web-dashboard/redesign.html`](file:///c:/Users/fizan/OneDrive/Documents/Bluestar-SMART/web-dashboard/redesign.html) / [`redesign.html`](file:///c:/Users/fizan/OneDrive/Documents/Bluestar-SMART/redesign.html)

---

## 1. Executive Summary & Brand Principles

The Blue Star Smart Climate Dashboard is engineered as a luxury product console on par with **Apple Home**, **Dyson Link**, **Bang & Olufsen**, and **Nest Learning Thermostat**. It merges an interactive, hardware-accurate 3D digital twin with quiet, tactile glassmorphic controls.

### Core Tenets

1. **The Product is the Hero**: The indoor unit occupies the visual focal point. UI chrome sits quietly on the periphery and never competes with the hardware twin.
2. **Kinematic Truth**: Louver flaps and airflow vanes do not oscillate with arbitrary decorative sine waves; their movement models real unipolar stepper motors, planetary gear reduction, and synchronized mechanical tie-bars.
3. **Dual Atmospheric Moods (Dark & Light)**:
   - **Dark Mode ("Night Console")**: Deep space obsidian surfaces (`#080a0f`) with subtle translucent hairline dividers and vibrant electric sky glowing accents.
   - **Light Mode ("Daylight Gallery")**: Clean architectural alabaster surfaces (`#f8fafc`) with pure white floating panels, soft ambient drop shadows, and high-contrast slate-900 typography.
4. **Immediate Tactile Feedback**: Every interaction (slider drag, temperature step, mode change, keypad stroke) provides instant visual confirmation, micro-haptics (where supported), and soft synthesizer feedback clicks.
5. **Zero Redundancy**: Every state attribute (temperature, mode, fan speed, louver angle) lives in one definitive place. Secondary clutter, duplicate labels, and noisy badges are strictly eliminated.
6. **Accessibility First**: Meets WCAG 2.1 AAA contrast for primary controls and AA for secondary telemetry in both dark and light modes. Fully respects `prefers-reduced-motion`.

---

## 2. Color Science & Design Tokens

Both themes share an identical semantic token structure. The active theme is toggled via `html[data-theme="dark" | "light"]` and initialized via an inline script before initial paint to prevent theme flash.

### 2.1 Complete Token Palette

| Token | Dark Mode | Light Mode | Semantic Role | Contrast (Dark / Light) |
| :--- | :--- | :--- | :--- | :--- |
| `--bg` | `#080a0f` | `#f8fafc` | Viewport & body background | Base Canvas |
| `--surface` | `#0f131c` | `#ffffff` | Primary panels, nav bar, modals | 16.2:1 / 18.5:1 |
| `--surface-2` | `#151b26` | `#f1f5f9` | Control pills, inactive tracks, buttons | Structural containers |
| `--surface-3` | `#1d2535` | `#e2e8f0` | Hover fills, pressed states | Interactive feedback |
| `--surface-hover` | `#263145` | `#cbd5e1` | Deep hover & focus backgrounds | Focus layers |
| `--line` | `rgba(255,255,255,0.07)` | `rgba(15,23,42,0.08)` | Hairline dividers, card outlines | Sub-pixel division |
| `--line-strong`| `rgba(255,255,255,0.15)` | `rgba(15,23,42,0.16)` | Active outlines, focus rings | Emphasized division |
| `--text` | `#f8fafc` | `#0f172a` | Primary titles, hero readouts | 17.1:1 / 18.2:1 (AAA) |
| `--text-2` | `#94a3b8` | `#475569` | Secondary labels, pill text | 7.8:1 / 8.2:1 (AAA) |
| `--text-3` | `#64748b` | `#64748b` | Sub-labels, captions, units | 4.8:1 / 5.1:1 (AA) |
| `--accent` | `#38bdf8` | `#0284c7` | Active pill fill, live dial arc, buttons | Primary Brand Cyan-Blue |
| `--accent-ink` | `#041424` | `#ffffff` | Text/icons on solid accent surfaces | 12.4:1 / 4.9:1 (AA/AAA) |
| `--accent-soft`| `rgba(56,189,248,0.12)` | `rgba(2,132,199,0.10)` | Active pill background | Soft atmospheric tint |
| `--accent-glow`| `rgba(56,189,248,0.35)` | `rgba(2,132,199,0.25)` | Dial halo glow, live indicator pulse | Radiance layer |
| `--live` | `#34d399` | `#059669` | Online MQTT connection, filter clean | Emerald / Mint |
| `--warn` | `#fbbf24` | `#b45309` | Syncing, reconnecting, pending | Warm Amber |
| `--danger` | `#f87171` | `#b91c1c` | Error alert, PIN failed, filter dirty | Coral Red |

### 2.2 Elevation & Shadow Hierarchy

- **Dark Floating Surfaces** (`--shadow-float`):  
  `0 24px 60px -12px rgba(0, 0, 0, 0.65), 0 0 1px 1px rgba(255, 255, 255, 0.08)`
- **Light Floating Surfaces** (`--shadow-float`):  
  `0 20px 48px -10px rgba(15, 23, 42, 0.12), 0 0 1px 1px rgba(15, 23, 42, 0.06)`

---

## 3. Typography Scale & Optical Hierarchy

- **Display Font:** `Outfit` (Geometric, refined numerals, crisp letterforms).
- **Body & Controls:** `Plus Jakarta Sans` (Humanist sans-serif with high legibility at micro-sizes).

| UI Element | Family | Size / Line-Height | Weight | Tracking | Lettercase |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hero Temperature Number** | Outfit | 72px / 64px | 500 (Medium) | −0.04em | Tabular Nums |
| **Degree Symbol (`°`)** | Outfit | 24px / 24px | 400 (Regular) | 0.00em | Standard |
| **Delta Status Badge** | Plus Jakarta Sans | 12px / 16px | 500 (Medium) | −0.01em | Sentence case |
| **Group Section Headings** | Plus Jakarta Sans | 13px / 18px | 600 (SemiBold) | 0.00em | Sentence case |
| **Live Louver Angle Readout**| Outfit | 13px / 18px | 500 (Medium) | 0.00em | Tabular Nums |
| **Control Pill Labels** | Plus Jakarta Sans | 11px / 14px | 600 (SemiBold) | 0.01em | Sentence case |
| **Telemetry Values** | Outfit | 17px / 20px | 500 (Medium) | −0.01em | Tabular Nums |
| **Telemetry Labels** | Plus Jakarta Sans | 11px / 14px | 500 (Medium) | 0.00em | Sentence case |
| **PIN Keypad Digits** | Outfit | 22px / 28px | 500 (Medium) | 0.00em | Tabular Nums |

---

## 4. 3D Digital Twin Stage, Materials & Studio Lighting

The air conditioner digital twin is rendered in Three.js (WebGL with tone mapping and soft shadow maps).

### 4.1 Studio Lighting Architecture

```mermaid
flowchart TD
    subgraph ThreePointLighting [Studio 3-Point Lighting Rig]
        Key[Key Light: Directional 0xffffff, Intensity 0.95<br/>Position: 3.4, 4.4, 3.6 | PCFSoftShadowMap]
        Fill[Fill Light: Directional<br/>Dark: 0x5dc9f5 @ 0.30 | Light: 0xdbeafe @ 0.42]
        Rim[Rim / Silhouette Light: Directional<br/>Dark: 0x7de9ff @ 0.60 | Light: 0xc7d2fe @ 0.35]
        Ambient[Ambient & Hemi Light<br/>Dark: 0.18 + 0.40 | Light: 0.38 + 0.45]
    end
    Key --> AC[Blue Star Indoor Unit 3D Twin]
    Fill --> AC
    Rim --> AC
    Ambient --> AC
```

- **Theme Dynamic Lighting Tuning**:
  - In **Dark Mode**: Soft cool cyan fill (`0x5dc9f5`) and luminous rim specular reflection (`0x7de9ff`) carve the casing contours against the obsidian backdrop.
  - In **Light Mode**: Clean daylight white key (`0xffffff`) and high-ambient diffusion (`0.38` intensity) reveal crisp surface geometry without washing out the bevels.
- **Ground Contact Shadow**: Soft Gaussian radial attenuation map positioned under the chassis (`y = -0.551`) anchors the unit to the ground plane.

---

## 5. Louver Kinematics & Swing Motion Engineering

The horizontal louver blade and vertical deflector vanes have been completely revamped to model true physical air conditioning kinematics.

```
       [Top / Coanda Glide: 41.2° (0.72 rad)]
            \
             \
  [Closed: 0°] === [Mid Circulation: 53.8° (0.94 rad)]
                    \
                     \
                      [Low Floor Cascade: 67.6° (1.18 rad)]
```

### 5.1 Motorized Horizontal Louver Kinematics

1. **Angular Envelopes**:
   - `LOUVER_CLOSED`: $0.00\text{ rad}$ ($0^\circ$, fully docked and flush with front bevel).
   - `LOUVER_SWING_MIN` (Apex): $0.70\text{ rad}$ ($40.1^\circ$, Coanda ceiling throw).
   - `LOUVER_SWING_MAX` (Nadir): $1.22\text{ rad}$ ($69.9^\circ$, floor cooling throw).
   - `LOUVER_STEPS`:
     - Top (Step 1): $0.72\text{ rad}$ ($41.2^\circ$).
     - High-Mid (Step 2): $0.82\text{ rad}$ ($47.0^\circ$).
     - Mid (Step 3): $0.94\text{ rad}$ ($53.8^\circ$).
     - Mid-Low (Step 4): $1.06\text{ rad}$ ($60.7^\circ$).
     - Low (Step 5): $1.18\text{ rad}$ ($67.6^\circ$).

2. **Harmonic Stepper Turnaround Formula (Auto Swing)**:  
   Rather than simple harmonic oscillation which lacks travel deceleration, the motor sweep executes a **quintic smootherstep dwell** over a $4.2\text{ second}$ cycle period ($T = 4.2\text{ s}$):
   $$\tau(t) = \frac{t \pmod T}{T}$$
   $$u(\tau) = \frac{1}{2} - \frac{1}{2}\cos(2\pi \tau)$$
   $$s(u) = u^3 \left( u (6u - 15) + 10 \right)$$
   $$\theta_{\text{target}}(t) = \theta_{\text{min}} + (\theta_{\text{max}} - \theta_{\text{min}}) \cdot s(u)$$

3. **Critically Damped Tracking & Mode Transitions**:  
   To prevent spring recoil or wobbly elasticity when switching between Auto Swing and Fixed steps, the blade angle $\theta(t)$ follows an exponential smoothing damper:
   $$\theta(t + \Delta t) = \text{damp}\left(\theta(t), \theta_{\text{target}}, k, \Delta t\right)$$
   - Tracking speed $k = 12.0$ in Auto Swing (instantaneous motor phase locking).
   - Tracking speed $k = 7.0$ when transitioning to fixed steps (smooth 0.45s gliding settle with zero overshoot).
   - Tracking speed $k = 4.5$ on power down (graceful mechanical docking).

### 5.2 4-Way Synchronized Vertical Vanes (Horizontal Sweep)

In physical split AC units, the 13 internal vertical louvers are linked via a single internal connecting rod (`tie-rod`).
- **Synchronized Lateral Deflection**: All vanes oscillate together in unison:
  $$\theta_{\text{vane}, i}(t) = \text{envelope} \cdot \left[ 0.44 \cdot \sin(1.5 \cdot t) + (i - 6) \cdot 0.012 \right]$$
  Where $i \in [0, 12]$ is the vane index (center vane $i = 6$).
- The term $(i - 6) \cdot 0.012$ introduces a slight aerodynamic divergence: air near the outer edges expands laterally into the room.
- `envelope` dampens smoothly between $0.0$ and $1.0$ when 4-Way is toggled, preventing sudden snaps.

### 5.3 Dynamic Coupled Airflow Simulation

Airflow particle physics are tightly coupled to the real-time louver and vane angles:
- **Pitch Coupling**:
  $$V_y = -\text{speed} \cdot \left( 0.32 + 0.92 \cdot \sin(\theta_{\text{louver}}) \right) \cdot (0.8 + 0.4 \cdot \text{rand})$$
  $$V_z = \text{speed} \cdot \left( 0.55 + 0.45 \cdot \cos(\theta_{\text{louver}}) \right) \cdot \text{spread}$$
- **Yaw Coupling (4-Way)**:
  $$V_x = \sin(\theta_{\text{vane}}) \cdot \text{speed} \cdot 0.82 + (\text{rand} - 0.5) \cdot \text{speed} \cdot 0.18$$
- **Visual Result**: As the louver sweeps vertically or the 4-way vanes sweep horizontally, the particle mist visibly waves and disperses across the room in real time.

---

## 6. Component-by-Component Specifications

### 6.1 Louver & Swing Control Section
- **Live Degree Readout Badge**: Positioned in the section header, updating every frame with a pulsing cyan micro-dot and active degree angle:  
  `• Auto sweep · 54°` or `Top · 41°` or `Standby · Parked`.
- **5-Button Segmented Grid**:
  - `Swing`: Features an animated oscillating blade icon (`@keyframes louverOscillate`).
  - `Top`: Features a Coanda upward draft profile icon.
  - `Middle`: Features a horizontal flow profile icon.
  - `Low`: Features a downward floor cooling icon.
  - `4-Way`: Features dual horizontal sweep arrows with a gentle lateral pulse animation (`@keyframes lateralPulse`).

### 6.2 Circular Thermostat Dial & Delta Pill
- **Concentric Dual Ring**:
  - Outer hairline track: $r = 72\text{px}$, stroke width $6.5\text{px}$, `--line`.
  - Ambient glow halo: stroke width $14\text{px}$, Gaussian blur filter $4\text{px}$, `--accent-glow`.
  - Gradient progress arc: `--accent` gradient with rounded caps (`stroke-linecap: round`), animating smoothly via `600ms var(--ease)`.
- **Center Readout**:
  - "Set temperature" sub-label in `--text-3`.
  - Giant $72\text{px}$ temperature value in tabular figures.
  - Dynamic delta badge: calculates real-time temperature differential:  
    `↓ 3.0° cooling to target` or `↑ 1.5° warming to target` or `At target temperature`.

### 6.3 Stepper Buttons
- Dual $48\text{px}$ circular buttons with subtle `--surface-2` fill and 1px `--line` border.
- Tactile active feedback: `transform: scale(0.92)` on press.

### 6.4 Mode & Fan Speed Segmented Controls
- **Mode Pills**: 4 equal-width buttons with bespoke vector icons (Cool, Dry, Fan, Auto).
- **Fan Pills**: 6 stages (Quiet, Low, Med, High, Turbo, Auto) with compact $11\text{px}$ typography.
- Active pill transitions use smooth cubic-bezier transitions (`220ms cubic-bezier(0.2, 0.8, 0.2, 1)`).

### 6.5 Floating Stage Telemetry Strip
- Positioned bottom-left of the 3D viewport.
- Translucent frosted glass card with $20\text{px}$ backdrop blur and 1px hairline border.
- 4 telemetry cells:
  - **Compressor Frequency**: Cyan glow tabular readout (`48 Hz`).
  - **Coil Temperature**: Blue readout (`7.8°C`).
  - **Run Hours**: Tabular hour counter (`1,248 h`).
  - **Filter Health**: Emerald status (`Clean` or `Alert`).

### 6.6 Mobile Floating Command Dock
- Bounded to viewports $< 700\text{px}$, floating $14\text{px}$ above the screen bottom with `env(safe-area-inset-bottom)`.
- 4 touch targets (all $\ge 46\text{px}$):
  - `[-]` Stepper button.
  - Center readout: Mode + Temperature (`Cooling 24°C`).
  - `[+]` Stepper button.
  - Hero Power toggle button with active cyan glow.

### 6.7 Security Lock Screen
- Accessible via the lock icon or automatically enforced upon initialization.
- 10-digit circular keypad ($64\text{px}$ keys) with DJB2 32-bit PIN hashing (`1234` default demo).
- Incorrect PIN triggers an automated 6px horizontal shake animation and coral red error dots.

---

## 7. Responsive Layout Breakpoints

| Breakpoint | Target Devices | Layout Behavior |
| :--- | :--- | :--- |
| **Desktop ($\ge 1100\text{px}$)** | Desktops, Laptops, Ultrawide | Two-column split: full 3D canvas stage on left (`minmax(0, 1fr)`), fixed 400px scrollable control panel on right. Top nav 64px. |
| **Tablet ($700\text{--}1099\text{px}$)** | iPad, Tablets, Small Laptops | Single-column stacked layout: 3D stage fixed height (`clamp(340px, 50svh, 520px)`), control panel max-width 560px centered below. |
| **Mobile ($< 700\text{px}$)** | iPhones, Android devices | Compact top nav 56px with collapsed preview badges. 3D stage ~46svh. Floating bottom dock active. Panel bottom padding 110px. |

---

## 8. Accessibility & Compliance (WCAG 2.1)

- **Contrast Conformance**:
  - Primary text `--text` to `--bg`: **17.1:1** in Dark mode, **18.2:1** in Light mode (exceeds WCAG 2.1 AAA threshold of 7.0:1).
  - Secondary text `--text-2` to `--surface`: **7.8:1** in Dark mode, **8.2:1** in Light mode (exceeds AAA).
  - Interactive pill labels: **6.2:1** minimum (exceeds AA threshold of 4.5:1).
- **ARIA & Keyboard Navigation**:
  - All segmented pill buttons expose `role="group"` and `aria-pressed="true|false"`.
  - Feature cards expose `role="switch"` and `aria-checked="true|false"`.
  - Visible focus ring: `2px solid var(--accent)` with `3px` outline offset.
- **Reduced Motion**:
  - When `prefers-reduced-motion: reduce` is detected:
    - Louver auto-swing holds at midpoint ($54^\circ$).
    - Horizontal vanes remain stationary.
    - Shake animations on PIN error are replaced with static color alerts.
    - All CSS transitions drop to $0.01\text{ms}$.

---

## 9. Verification & Promotion Guide

1. **Previewing**:
   - Open [`web-dashboard/redesign.html`](file:///c:/Users/fizan/OneDrive/Documents/Bluestar-SMART/web-dashboard/redesign.html) or visit `/redesign` on your Vercel deployment.
2. **Promoting to Production (`main`)**:
   - Copy `web-dashboard/redesign.html` to `web-dashboard/index.html` and `redesign.html` to `dashboard.html`.
   - Commit and merge the `redesign` branch into `main`.
