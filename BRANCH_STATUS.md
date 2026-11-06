# Bluestar-SMART — Redesign Branch Status & Review Guide

**Branch Name:** `redesign`  
**Base Branch:** `main`  
**Status:** In Review / Ready for Evaluation (Non-Destructive Staging)  
**Preview File:** [`web-dashboard/redesign.html`](file:///c:/Users/fizan/OneDrive/Documents/Bluestar-SMART/web-dashboard/redesign.html) / [`redesign.html`](file:///c:/Users/fizan/OneDrive/Documents/Bluestar-SMART/redesign.html)  
**Production File:** [`web-dashboard/index.html`](file:///c:/Users/fizan/OneDrive/Documents/Bluestar-SMART/web-dashboard/index.html) (Untouched & Pristine)  
**Detailed Specification:** [`web-dashboard/DESIGN.md`](file:///c:/Users/fizan/OneDrive/Documents/Bluestar-SMART/web-dashboard/DESIGN.md)  

---

## 1. Executive Summary

Per design direction ("minimalistic theme, keep dark and light modes, also swing animation needs to be revamped aswell. it should look like a really polished app from a big brand"), this branch implements a complete architectural visual overhaul modeled after **Apple Home**, **Dyson Link**, and **Nest**.

To ensure **zero risk** to your live production setup:
- The entire redesign lives in **`web-dashboard/redesign.html`** and root **`redesign.html`**.
- The production file **`web-dashboard/index.html`** remains completely untouched.
- Service workers from `localhost` are cleanly uncurbed to guarantee instant cache-free reloads.
- If you like the redesign, you can merge it directly into production with a single command.

---

## 2. Visual Architecture & Color Science

### 2.1 Obsidian Dark Mode ("Night Console")
- **Base Canvas**: Deep space obsidian (`#08090d`) with subtle zenith radial glow (`radial-gradient(ellipse 90% 60% at 50% -10%, #162032 0%, #08090d 80%)`).
- **Surface Elevation**: Layered frosted glass panels (`rgba(16, 20, 30, 0.72)`) with `28px` backdrop blur and hairline borders (`rgba(255, 255, 255, 0.08)`).
- **Accents**: Glacier Sky cyan (`#38bdf8`) with soft halo bloom (`rgba(56, 189, 248, 0.38)`).
- **Typography**: Crisp white `#ffffff` headlines, muted slate `#94a3b8` labels, and emerald `#10b981` live signals.

### 2.2 Ceramic Light Mode ("Daylight Studio")
- **Base Canvas**: Architectural gallery alabaster (`#f7f9fc`) with ambient light wash.
- **Surface Elevation**: Pure white ceramic panels (`#ffffff`) with micro-borders (`rgba(15, 23, 42, 0.07)`) and soft diffusion drop shadows (`0 6px 20px -6px rgba(15, 23, 42, 0.07)`).
- **Accents**: Blue Star Signature Azure (`#0066cc`).
- **Typography**: Deep onyx `#090e17` text and slate `#475569` labels meeting WCAG AAA contrast ($> 18:1$).

---

## 3. Revamped 3D Digital Twin & Louver Kinematics

### 3.1 3D Indoor Unit & Studio Lighting
1. **Seamless Infinity Studio Floor**: Replaced the previous circular cutoff plate with a soft-shadow receiver (`THREE.ShadowMaterial`), allowing the AC unit contact shadow to blend seamlessly into the background gradient.
2. **Hidden LED 7-Segment Display**: An offscreen canvas dynamically projects the current target temperature (`24°`) or technician mode (`C1`) directly through the white matte plastic of the front panel. When turned off, the digits disappear completely.
3. **Top Induction Slats**: 7 micro-slats representing the top intake grille.
4. **Discharge Cavity & Rotor**: Recessed dark air channel containing a rotating cross-flow blower wheel.

### 3.2 Revamped Stepper Louver Kinematics
- **Physical Unipolar Stepper Simulation**:
  - Auto-swing sweeps across $33.2^\circ$ to $74.5^\circ$ ($0.58\text{ to } 1.30\text{ rad}$) with constant angular velocity and smooth quintic smootherstep turnaround dwell at apex and nadir ($T = 5.2\text{ s}$).
  - Critically damped tracking ensures zero bounce or overshoot when switching positions.
  - Powering off smoothly glides the blade to $16.0^\circ$ flush dock.
- **Synchronized 2D Vector Cross-Section (Airflow & Louver Director)**:
  - Inside the control console, an animated architectural vector diagram displays the indoor unit cross-section.
  - The SVG motorized blade rotates in real-time synchronized with the 3D blade degrees.
  - Real-time digital angle badge: e.g. `56° · Harmonic Sweep`.
  - 5 tactile quick buttons: `Auto (Harmonic)`, `Top (Coanda)`, `Mid (Direct)`, `Floor (Downward)`, `4-Way (Horizontal)`.
- **Dynamic Aerodynamic Flow Particles**:
  - 700 radial glowing particles emit continuously from the discharge vent.
  - Trajectory curves dynamically matching instantaneous louver pitch and horizontal vane yaw.

---

## 4. UI Components & Control Deck

1. **Hero Climate Thermostat Dial**:
   - Circular gauge with 24 subtle tick marks.
   - Dynamic progress arc reflecting setpoint ($16^\circ\text{C}$ to $30^\circ\text{C}$).
   - Power capsule button with animated breathing ring.
   - Large $68\text{px}$ temperature readout with ambient delta badge (`↓ 3.0° Cooling to Target`).
   - Tactile `–` and `+` stepper circles.
2. **Segmented Mode & Velocity Switches**:
   - Liquid segmented controls with smooth sliding indicators.
   - Modes: `Cool`, `Dry`, `Fan`, `Auto`.
   - Fan Speeds: `Quiet`, `Low`, `Med`, `High`, `Turbo`, `Auto`.
   - Convertible Inverter Drive: `100%`, `80%`, `60%`, `40%`.
3. **Intelligent Features**:
   - `Turbo Cool (110% Boost)`, `Eco Mode`, `Comfort Sleep`, `Indoor LED Display`, `C1 Full Load Mode`.
4. **Bento Telemetry**:
   - Compressor Frequency ($Hz$), Evaporator Coil ($^\circ\text{C}$), Total Run Time ($h$), Filter Condition (`Clean` or `Check Filter`).
5. **Security PIN Screen**:
   - 4-digit PIN lock overlay (`1234` default demo) with keypad, dot indicators, and error shake animation.
6. **Web Audio Feedback**:
   - Real-time synthesized clicks, chimes, and beeps (no external audio assets).

---

## 5. Visual Verification Screenshots

Automated Playwright captures recorded and verified:
- **Desktop Dark**: `screenshots/redesign_desktop_dark.png` & `screenshots/redesign_desktop_dark_scrolled.png`
- **Desktop Light**: `screenshots/redesign_desktop_light.png` & `screenshots/redesign_desktop_light_scrolled.png`
- **Mobile Dark (390×844)**: `screenshots/redesign_mobile_dark.png`
- **Mobile Light (390×844)**: `screenshots/redesign_mobile_light.png`

---

## 6. How to Preview & Test

### Option 1: Browser (Direct Link)
```powershell
start web-dashboard/redesign.html
# or
start redesign.html
```

### Option 2: Local HTTP Server (Already Running on Port 3000)
Open in your browser:
**`http://localhost:3000/redesign.html`**

---

## 7. How to Merge to Production (When You Approve)

When you are satisfied with the redesign and want to replace `index.html`:

```powershell
git checkout main
Copy-Item web-dashboard/redesign.html web-dashboard/index.html -Force
Copy-Item redesign.html dashboard.html -Force
git commit -am "feat: promote luxury minimalist redesign to production dashboard"
git push origin main
```
