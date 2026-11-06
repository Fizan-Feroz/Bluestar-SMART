# Bluestar-SMART — Redesign Branch Status & Review Guide

**Branch Name:** `redesign`  
**Base Branch:** `main`  
**Status:** In Review / Ready for Evaluation (Non-Destructive Staging)  
**Preview File:** [`web-dashboard/redesign.html`](file:///c:/Users/fizan/OneDrive/Documents/Bluestar-SMART/web-dashboard/redesign.html) / [`redesign.html`](file:///c:/Users/fizan/OneDrive/Documents/Bluestar-SMART/redesign.html)  
**Production File:** [`web-dashboard/index.html`](file:///c:/Users/fizan/OneDrive/Documents/Bluestar-SMART/web-dashboard/index.html) (Untouched & Pristine)

---

## 1. Executive Summary

Per design direction, this branch implements an Apple/Dyson/Nest-grade minimalist UI revamp for the Blue Star Smart AC controller. To ensure zero risk to your live setup, the redesign is isolated in dedicated files:
- **`web-dashboard/redesign.html`** (served at `/redesign` on Vercel)
- **`redesign.html`** (root mirror for local offline testing)
- The production file **`web-dashboard/index.html`** remains completely untouched.
- If you like the design, it can be merged directly into `index.html` and `main` with a single command.

---

## 2. Key Features Implemented in the Redesign

### 2.1 Minimalist Brand-Grade Design System (Dark & Light)
- **Dark Mode**:
  - Deep space obsidian background (`#080a0f`) with soft multilayered ink surfaces (`#0f131c`, `#151b26`, `#1d2535`).
  - Ultra-thin translucent hairline borders (`rgba(255, 255, 255, 0.07)`).
  - Vibrant precision electric sky accent (`#38bdf8`) with soft ambient luminescence (`--accent-glow`).
- **Light Mode**:
  - Clean architectural gallery alabaster (`#f8fafc`) with crisp white panels (`#ffffff`).
  - High-contrast slate-900 typography (`#0f172a`) meeting WCAG AAA contrast requirements.
  - Deep electric azure active states (`#0284c7`).
  - Studio-grade three-point lighting in the 3D scene that illuminates the unit with natural contact shadows.
- **Theme Persistence**:
  - Single-click theme toggle with smooth rotating sun/moon icon transition.
  - Saved to `localStorage` (`bluestar_theme`) with zero-flash inline initialization.

### 2.2 Revamped Louver Kinematics & Swing Motion Model
- **Motorized Stepper Kinematics**:
  - Replaced the previous erratic spring tracking with an authentic **unipolar stepper motor simulation**.
  - **Auto Swing**: Sweeps across $40.1^\circ$ to $69.9^\circ$ with constant-velocity travel and smooth quintic smootherstep turnaround dwells at apex and nadir ($T = 4.2\text{ s}$).
  - **Fixed Steps**: Transitions to Top ($41.2^\circ$), Middle ($53.8^\circ$), or Low ($67.6^\circ$) with a critically damped mechanical tracker (zero overshoot, no bouncy oscillations).
  - **Power Off Docking**: When turned off, the flap glides smoothly to $0.00\text{ rad}$ and docks flush with the housing.
- **4-Way Motorized Horizontal Vane Sweep**:
  - Replaced the undulating snake wave with a **synchronized tie-rod linkage**: all 13 internal vertical vanes pivot in unison from $-24^\circ$ to $+24^\circ$, with subtle aerodynamic edge divergence.
  - Smooth envelope damping prevents snapping when toggled on/off.
- **Fluid Dynamics & Particle Coupling**:
  - Airflow particles emerge directly behind the louver blade.
  - Particle pitch dynamically couples to the instantaneous louver angle $\theta_{\text{louver}}(t)$.
  - Particle lateral yaw couples to the 4-way vane angle $\theta_{\text{vane}}(t)$.
  - You visibly see the cold air plume sweeping across the room in rhythm with the 3D louvers!

### 2.3 Interactive Louver UI & Live Angle Badge
- **Live Degree Readout**:
  - The Louver section header features a real-time badge (`• Auto sweep · 54°` or `Top · 41°` or `Standby · Parked`) dynamically synchronized every frame with the 3D blade.
- **Bespoke SVG Segmented Pill Icons**:
  - **Swing**: Flap outline with active CSS oscillating blade animation (`@keyframes louverOscillate`).
  - **Top**: Coanda ceiling draft profile.
  - **Middle**: Horizontal room air throw profile.
  - **Low**: Floor cooling cascade profile.
  - **4-Way**: Dual lateral sweep arrows with active pulsing animation (`@keyframes lateralPulse`).

### 2.4 Ergonomics & Responsive Breakpoints
- **Desktop ($\ge 1100\text{px}$)**:
  - 3D stage on the left, fixed scrollable 400px control panel on the right.
- **Tablet ($700\text{--}1099\text{px}$)**:
  - Responsive vertical stack with bounded 3D viewport height and centered controls.
- **Mobile ($< 700\text{px}$)**:
  - Floating bottom command dock (`[ - ]  Cooling 24°C  [ + ]  [ Power ]`) with safe-area insets.
  - Cleaned navigation header with auto-collapsed badges for zero clutter.

---

## 3. How to Preview & Test

### Option A: Local Browser (Zero Setup)
Simply open the redesign file directly in your browser:
```powershell
start web-dashboard/redesign.html
# or
start redesign.html
```

### Option B: Local HTTP Server
```powershell
npx serve web-dashboard
# Open http://localhost:3000/redesign.html
```

### Option C: Vercel Preview
When pushed, Vercel automatically deploys the branch:
- Production URL: `https://<your-project>.vercel.app/` (serves `index.html`)
- Redesign Preview URL: `https://<your-project>.vercel.app/redesign` (serves `redesign.html`)

---

## 4. How to Merge (When You Approve)

When you are satisfied with the redesign and want to promote it to the default dashboard:

```powershell
# 1. Overwrite production files with the redesign
cp web-dashboard/redesign.html web-dashboard/index.html
cp redesign.html dashboard.html

# 2. Commit and push on redesign branch
git add web-dashboard/index.html dashboard.html
git commit -m "feat(dashboard): promote minimalist brand-grade redesign to production"
git push origin redesign

# 3. Merge into main
git checkout main
git merge redesign
git push origin main
```
