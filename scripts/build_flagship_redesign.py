import os

html_content = r'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>Blue Star Smart Climate — Pure Architecture</title>
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230284c7'/%3E%3Cpath d='M16 5l2.9 8.4 8.8.3-7 5.5 2.4 8.5L16 22.7l-7.1 5 2.4-8.5-7-5.5 8.8-.3z' fill='white'/%3E%3C/svg%3E">
  <meta name="description" content="Next-generation 3D digital twin and climate architecture console for Blue Star smart inverter air conditioners.">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-title" content="Blue Star">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="theme-color" content="#08090d">
  <link rel="manifest" href="manifest.webmanifest">
  <link rel="apple-touch-icon" href="icons/apple-touch-icon.png">

  <!-- Luxury Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

  <script>
    (function() {
      // Unregister any stale service workers to ensure fresh redesign loading
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.getRegistrations().then(function(regs) {
          for (var r of regs) { r.unregister(); }
        });
      }
      try {
        var t = localStorage.getItem('bluestar_theme');
        if (t !== 'light' && t !== 'dark') {
          t = matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
        }
        document.documentElement.dataset.theme = t;
      } catch (e) {
        document.documentElement.dataset.theme = 'dark';
      }
    })();
  </script>

  <style>
/* =========================================================================
   LUXURY BRAND DESIGN TOKENS (OBSIDIAN DARK & CERAMIC LIGHT)
   ========================================================================= */
:root {
  color-scheme: dark;
  --bg: #08090d;
  --bg-gradient: radial-gradient(ellipse 90% 60% at 50% -10%, #162032 0%, #08090d 80%);
  --surface: #10141e;
  --surface-glass: rgba(16, 20, 30, 0.72);
  --surface-2: #161c2b;
  --surface-3: #1f273b;
  --surface-hover: #29344e;
  --well: #0b0e15;
  --line: rgba(255, 255, 255, 0.08);
  --line-strong: rgba(255, 255, 255, 0.16);
  --text: #ffffff;
  --text-2: #94a3b8;
  --text-3: #64748b;
  --accent: #38bdf8;
  --accent-rgb: 56, 189, 248;
  --accent-ink: #041424;
  --accent-soft: rgba(56, 189, 248, 0.12);
  --accent-glow: rgba(56, 189, 248, 0.38);
  --accent-gradient: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%);
  --live: #10b981;
  --warn: #f59e0b;
  --danger: #ef4444;
  --shadow-float: 0 24px 60px -12px rgba(0, 0, 0, 0.75), 0 0 1px 1px rgba(255, 255, 255, 0.08);
  --shadow-card: 0 12px 32px -8px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.06);
  --font-display: 'Outfit', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
  --font-body: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  --nav-h: 68px;
  --safe-top: env(safe-area-inset-top, 0px);
  --safe-bottom: env(safe-area-inset-bottom, 0px);
  --safe-left: env(safe-area-inset-left, 0px);
  --safe-right: env(safe-area-inset-right, 0px);
}

html[data-theme="light"] {
  color-scheme: light;
  --bg: #f7f9fc;
  --bg-gradient: radial-gradient(ellipse 90% 60% at 50% -10%, #ffffff 0%, #edf2f7 85%);
  --surface: #ffffff;
  --surface-glass: rgba(255, 255, 255, 0.88);
  --surface-2: #f1f4f9;
  --surface-3: #e2e8f0;
  --surface-hover: #cbd5e1;
  --well: #e9eef5;
  --line: rgba(15, 23, 42, 0.07);
  --line-strong: rgba(15, 23, 42, 0.16);
  --text: #090e17;
  --text-2: #475569;
  --text-3: #64748b;
  --accent: #0066cc;
  --accent-rgb: 0, 102, 204;
  --accent-ink: #ffffff;
  --accent-soft: rgba(0, 102, 204, 0.09);
  --accent-glow: rgba(0, 102, 204, 0.22);
  --accent-gradient: linear-gradient(135deg, #0052a3 0%, #0077e6 100%);
  --live: #059669;
  --warn: #d97706;
  --danger: #dc2626;
  --shadow-float: 0 20px 48px -10px rgba(15, 23, 42, 0.12), 0 0 1px 1px rgba(15, 23, 42, 0.06);
  --shadow-card: 0 6px 20px -6px rgba(15, 23, 42, 0.07), inset 0 1px 0 rgba(255, 255, 255, 0.95);
}

*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  -webkit-text-size-adjust: 100%;
  background: var(--bg);
}

body {
  height: 100vh;
  height: 100dvh;
  width: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  background: var(--bg);
  background-image: var(--bg-gradient);
  color: var(--text);
  font-family: var(--font-body);
  font-size: 13px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  -webkit-tap-highlight-color: transparent;
  transition: background-color 300ms ease, color 300ms ease;
}

button, input {
  font: inherit;
  color: inherit;
}

button {
  border: 0;
  background: none;
  cursor: pointer;
  -webkit-appearance: none;
  appearance: none;
  touch-action: manipulation;
}

button:disabled {
  cursor: default;
  opacity: 0.38;
}

[hidden] {
  display: none !important;
}

:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 3px;
  border-radius: 8px;
}

/* =========================================================================
   TOP NAVIGATION BAR (FLOATING GLASS APEX)
   ========================================================================= */
.top-nav {
  position: relative;
  z-index: 50;
  flex: 0 0 auto;
  height: calc(var(--nav-h) + var(--safe-top));
  padding: var(--safe-top) calc(28px + var(--safe-right)) 0 calc(28px + var(--safe-left));
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  border-bottom: 1px solid var(--line);
  background: var(--surface-glass);
  backdrop-filter: blur(24px) saturate(160%);
  -webkit-backdrop-filter: blur(24px) saturate(160%);
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-badge {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: var(--accent-gradient);
  display: grid;
  place-items: center;
  color: #fff;
  box-shadow: 0 4px 14px var(--accent-glow);
}

.brand-badge svg {
  width: 20px;
  height: 20px;
  fill: currentColor;
}

.brand-titles {
  display: flex;
  flex-direction: column;
}

.brand-name {
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text);
}

.brand-sub {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.04em;
  color: var(--text-3);
}

.preview-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 9px;
  border-radius: 999px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  background: var(--surface-2);
  border: 1px solid var(--line);
  color: var(--accent);
}

.preview-tag-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 8px var(--accent);
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-capsule {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 36px;
  padding: 0 14px;
  border-radius: 999px;
  background: var(--surface-2);
  border: 1px solid var(--line);
  font-size: 12px;
  font-weight: 600;
  color: var(--text);
  transition: all 200ms ease;
}

.status-capsule:hover {
  background: var(--surface-3);
  border-color: var(--line-strong);
}

.live-beacon {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--live);
  box-shadow: 0 0 10px var(--live);
  animation: beaconPulse 2s ease-in-out infinite;
}

@keyframes beaconPulse {
  0%, 100% { opacity: 0.5; transform: scale(0.9); }
  50% { opacity: 1; transform: scale(1.2); }
}

.nav-icon-btn {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: var(--surface-2);
  border: 1px solid var(--line);
  color: var(--text-2);
  transition: all 180ms ease;
}

.nav-icon-btn:hover {
  background: var(--surface-3);
  color: var(--text);
  border-color: var(--line-strong);
  transform: translateY(-1px);
}

.nav-icon-btn:active {
  transform: scale(0.94);
}

.nav-icon-btn svg {
  width: 18px;
  height: 18px;
  fill: currentColor;
  transition: transform 300ms ease;
}

html[data-theme="dark"] .theme-sun { display: block; }
html[data-theme="dark"] .theme-moon { display: none; }
html[data-theme="light"] .theme-sun { display: none; }
html[data-theme="light"] .theme-moon { display: block; }

/* =========================================================================
   MAIN APP ARENA: 3D VIEWPORT + CLIMATE COMMAND CONSOLE
   ========================================================================= */
.app-arena {
  flex: 1 1 auto;
  min-height: 0;
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(380px, 460px);
  overflow: hidden;
}

/* --- Left Stage: 3D Twin --- */
.stage-3d {
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

#canvas3d-container {
  position: absolute;
  inset: 0;
  cursor: grab;
}

#canvas3d-container:active {
  cursor: grabbing;
}

.stage-top-controls {
  position: absolute;
  top: 24px;
  left: 28px;
  right: 28px;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  pointer-events: none;
}

.camera-glass-pills {
  pointer-events: auto;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px;
  border-radius: 999px;
  background: var(--surface-glass);
  border: 1px solid var(--line);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.cam-btn {
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-2);
  transition: all 180ms ease;
}

.cam-btn:hover {
  color: var(--text);
}

.cam-btn.active {
  background: var(--accent);
  color: var(--accent-ink);
  box-shadow: 0 2px 10px var(--accent-glow);
}

.stage-orbit-hint {
  font-size: 11px;
  font-weight: 500;
  letter-spacing: 0.04em;
  color: var(--text-3);
  background: var(--surface-glass);
  padding: 6px 12px;
  border-radius: 999px;
  border: 1px solid var(--line);
  backdrop-filter: blur(16px);
}

/* Floating Stage Bento Telemetry Strip */
.stage-bento-telemetry {
  position: absolute;
  bottom: 24px;
  left: 28px;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  border-radius: 20px;
  background: var(--surface-glass);
  border: 1px solid var(--line);
  backdrop-filter: blur(24px) saturate(140%);
  -webkit-backdrop-filter: blur(24px) saturate(140%);
  box-shadow: var(--shadow-card);
}

.telemetry-tile {
  display: flex;
  flex-direction: column;
  padding: 0 8px;
}

.telemetry-tile:not(:last-child) {
  border-right: 1px solid var(--line);
  padding-right: 14px;
}

.tel-label {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-3);
}

.tel-value {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 6px;
}

.tel-value.accent {
  color: var(--accent);
}

.tel-value.live {
  color: var(--live);
}

.pulse-indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 8px currentColor;
  animation: beaconPulse 2s infinite;
}

/* --- Right Stage: Climate Control Console --- */
.control-console {
  background: var(--surface-glass);
  border-left: 1px solid var(--line);
  backdrop-filter: blur(32px) saturate(140%);
  -webkit-backdrop-filter: blur(32px) saturate(140%);
  overflow-y: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 24px 22px 48px;
  scrollbar-width: thin;
  scrollbar-color: var(--line) transparent;
}

.control-console::-webkit-scrollbar {
  width: 4px;
}

.control-console::-webkit-scrollbar-thumb {
  background: var(--line-strong);
  border-radius: 4px;
}

/* Glass Card Container */
.glass-card {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 22px;
  padding: 18px 20px;
  box-shadow: var(--shadow-card);
  display: flex;
  flex-direction: column;
  gap: 14px;
  position: relative;
  transition: border-color 200ms ease, box-shadow 200ms ease;
}

.glass-card:hover {
  border-color: var(--line-strong);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.card-title {
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-title svg {
  width: 16px;
  height: 16px;
  fill: var(--accent);
}

.card-badge {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-2);
  display: flex;
  align-items: center;
  gap: 6px;
}

/* =========================================================================
   HERO CLIMATE THERMOSTAT DIAL CARD
   ========================================================================= */
.hero-climate-card {
  padding: 22px 20px 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.hero-top-row {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.power-capsule {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  height: 38px;
  padding: 0 16px 0 12px;
  border-radius: 999px;
  background: var(--surface-2);
  border: 1px solid var(--line);
  color: var(--text-2);
  font-size: 13px;
  font-weight: 600;
  transition: all 240ms var(--ease);
}

.power-capsule:hover {
  background: var(--surface-3);
  color: var(--text);
}

.power-ring {
  position: relative;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid currentColor;
}

.power-ring::after {
  content: '';
  position: absolute;
  top: -4px;
  left: 50%;
  width: 2px;
  height: 6px;
  background: currentColor;
  transform: translateX(-50%);
  border-radius: 2px;
}

.power-capsule.on {
  background: var(--accent);
  color: var(--accent-ink);
  border-color: var(--accent);
  box-shadow: 0 4px 16px var(--accent-glow);
}

.room-temp-pill {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.room-temp-label {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-3);
}

.room-temp-val {
  font-family: var(--font-display);
  font-size: 17px;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: var(--text);
}

/* Dial Center Piece */
.dial-wrapper {
  position: relative;
  width: 220px;
  height: 220px;
  margin: 12px auto 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dial-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
  overflow: visible;
  pointer-events: none;
}

.dial-track {
  fill: none;
  stroke: var(--line);
  stroke-width: 6;
  stroke-linecap: round;
}

.dial-ticks {
  fill: none;
  stroke: var(--line-strong);
  stroke-width: 2;
  stroke-dasharray: 2 12;
}

.dial-glow-halo {
  fill: none;
  stroke: var(--accent);
  stroke-width: 14;
  stroke-linecap: round;
  opacity: 0.28;
  filter: blur(6px);
  transition: stroke-dashoffset 600ms var(--ease);
}

.dial-progress-arc {
  fill: none;
  stroke: url(#climateDialGradient);
  stroke-width: 7;
  stroke-linecap: round;
  stroke-dasharray: 452.39;
  stroke-dashoffset: 452.39;
  transition: stroke-dashoffset 600ms var(--ease);
}

.dial-core-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
  text-align: center;
}

.target-caption {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-3);
  margin-bottom: 2px;
}

.target-readout {
  display: flex;
  align-items: flex-start;
  font-family: var(--font-display);
  font-size: 68px;
  font-weight: 500;
  line-height: 0.9;
  letter-spacing: -0.04em;
  color: var(--text);
  font-variant-numeric: tabular-nums;
  transition: transform 150ms ease;
}

.target-deg {
  font-size: 24px;
  font-weight: 400;
  color: var(--text-2);
  margin-top: 6px;
  margin-left: 2px;
}

.delta-status-pill {
  margin-top: 8px;
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--surface-2);
  border: 1px solid var(--line);
  font-size: 11px;
  font-weight: 600;
  color: var(--text-2);
  white-space: nowrap;
}

/* Stepper Bar */
.stepper-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 28px;
  margin-top: 4px;
}

.stepper-circle-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: var(--surface-2);
  border: 1px solid var(--line);
  color: var(--text);
  transition: all 180ms ease;
}

.stepper-circle-btn:hover {
  background: var(--surface-3);
  border-color: var(--line-strong);
  transform: scale(1.06);
}

.stepper-circle-btn:active {
  transform: scale(0.92);
}

.stepper-circle-btn svg {
  width: 22px;
  height: 22px;
  fill: currentColor;
}

/* =========================================================================
   CARD 2: REVAMPED LOUVER & AIRFLOW DIRECTOR
   ========================================================================= */
.louver-director-card {
  gap: 14px;
}

.louver-vector-screen {
  background: var(--well);
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 14px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  position: relative;
  overflow: hidden;
}

.louver-preview-stage {
  display: flex;
  align-items: center;
  gap: 14px;
}

.louver-svg-crosssection {
  width: 90px;
  height: 54px;
  flex: 0 0 90px;
  overflow: visible;
  color: var(--text-2);
}

.louver-flap-blade {
  transform-origin: 30px 42px;
  transition: transform 60ms linear;
}

.airflow-vector-rays {
  animation: rayFlow 1.8s linear infinite;
}

@keyframes rayFlow {
  0% { stroke-dashoffset: 20; opacity: 0.3; }
  50% { opacity: 0.9; }
  100% { stroke-dashoffset: 0; opacity: 0.3; }
}

.louver-readout-col {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.louver-digital-angle {
  font-family: var(--font-display);
  font-size: 26px;
  font-weight: 700;
  line-height: 1;
  color: var(--accent);
  font-variant-numeric: tabular-nums;
}

.louver-mode-caption {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-2);
  margin-top: 2px;
}

.louver-pill-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 6px;
}

.pill-card-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 4px;
  border-radius: 14px;
  background: var(--surface-2);
  border: 1px solid var(--line);
  color: var(--text-2);
  font-size: 11px;
  font-weight: 600;
  transition: all 180ms ease;
}

.pill-card-btn:hover {
  background: var(--surface-3);
  color: var(--text);
  border-color: var(--line-strong);
}

.pill-card-btn.active {
  background: var(--accent);
  color: var(--accent-ink);
  border-color: var(--accent);
  box-shadow: 0 4px 14px var(--accent-glow);
}

.pill-card-btn svg {
  width: 20px;
  height: 20px;
}

/* =========================================================================
   CARD 3 & 4: SEGMENTED CONTROLS (CLIMATE MODE & FAN SPEED)
   ========================================================================= */
.capsule-track {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 4px;
  padding: 4px;
  border-radius: 14px;
  background: var(--well);
  border: 1px solid var(--line);
}

.capsule-track.cols-6 {
  grid-template-columns: repeat(6, 1fr);
}

.capsule-seg {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 8px 4px;
  border-radius: 10px;
  color: var(--text-2);
  font-size: 11px;
  font-weight: 600;
  transition: all 180ms ease;
}

.capsule-seg:hover {
  color: var(--text);
}

.capsule-seg.active {
  background: var(--surface);
  color: var(--text);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
}

html[data-theme="light"] .capsule-seg.active {
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.1);
}

.capsule-seg.active svg {
  fill: var(--accent);
}

.capsule-seg svg {
  width: 16px;
  height: 16px;
  fill: currentColor;
}

/* =========================================================================
   CARD 5: CONVERTIBLE INVERTER CAPACITY
   ========================================================================= */
.convertible-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
}

.conv-pill {
  padding: 9px 0;
  border-radius: 12px;
  background: var(--surface-2);
  border: 1px solid var(--line);
  color: var(--text-2);
  font-family: var(--font-display);
  font-size: 13px;
  font-weight: 700;
  text-align: center;
  transition: all 180ms ease;
}

.conv-pill:hover {
  background: var(--surface-3);
  color: var(--text);
}

.conv-pill.active {
  background: var(--accent);
  color: var(--accent-ink);
  border-color: var(--accent);
  box-shadow: 0 2px 10px var(--accent-glow);
}

/* =========================================================================
   CARD 6: INTELLIGENT FEATURES LIST
   ========================================================================= */
.features-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.feature-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-radius: 14px;
  background: var(--surface-2);
  border: 1px solid var(--line);
  cursor: pointer;
  transition: all 180ms ease;
}

.feature-row:hover {
  background: var(--surface-3);
  border-color: var(--line-strong);
}

.feature-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.feature-icon-square {
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: var(--surface-3);
  display: grid;
  place-items: center;
  color: var(--text-2);
}

.feature-icon-square svg {
  width: 16px;
  height: 16px;
  fill: currentColor;
}

.feature-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text);
}

.luxury-switch {
  position: relative;
  width: 36px;
  height: 20px;
  border-radius: 999px;
  background: var(--well);
  border: 1px solid var(--line-strong);
  transition: all 220ms ease;
}

.luxury-switch::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--text-3);
  transition: all 220ms var(--ease);
}

.feature-row.on .luxury-switch {
  background: var(--accent);
  border-color: var(--accent);
}

.feature-row.on .luxury-switch::after {
  transform: translateX(16px);
  background: var(--accent-ink);
}

.feature-row.on .feature-icon-square {
  background: var(--accent-soft);
  color: var(--accent);
}

/* Console Footer */
.console-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 8px;
  font-size: 11px;
  font-weight: 500;
  color: var(--text-3);
}

/* =========================================================================
   SECURITY PIN LOCK SCREEN
   ========================================================================= */
.lock-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  background: rgba(8, 9, 13, 0.88);
  backdrop-filter: blur(28px);
  -webkit-backdrop-filter: blur(28px);
  display: grid;
  place-items: center;
  padding: 24px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 280ms ease;
}

.lock-overlay.open {
  opacity: 1;
  pointer-events: auto;
}

.lock-box {
  width: 100%;
  max-width: 320px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 28px;
  padding: 32px 24px 28px;
  box-shadow: var(--shadow-float);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.lock-title {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 4px;
}

.lock-msg {
  font-size: 12px;
  color: var(--text-2);
  margin-bottom: 24px;
}

.pin-dots {
  display: flex;
  gap: 16px;
  margin-bottom: 28px;
}

.pin-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  border: 2px solid var(--line-strong);
  transition: all 180ms ease;
}

.pin-dot.filled {
  background: var(--accent);
  border-color: var(--accent);
  box-shadow: 0 0 12px var(--accent-glow);
  transform: scale(1.15);
}

.pin-keypad {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  width: 100%;
}

.pad-key {
  height: 52px;
  border-radius: 16px;
  background: var(--surface-2);
  border: 1px solid var(--line);
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 600;
  color: var(--text);
  display: grid;
  place-items: center;
  transition: all 150ms ease;
}

.pad-key:hover {
  background: var(--surface-3);
  border-color: var(--line-strong);
}

.pad-key:active {
  transform: scale(0.92);
  background: var(--accent-soft);
}

.pad-key.util {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-2);
}

/* Modal Backdrops */
.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 90;
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  display: grid;
  place-items: center;
  padding: 24px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 240ms ease;
}

.modal-backdrop.open {
  opacity: 1;
  pointer-events: auto;
}

.modal-dialog {
  width: 100%;
  max-width: 440px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 24px;
  padding: 24px;
  box-shadow: var(--shadow-float);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.modal-title {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  color: var(--text);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-2);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.form-group input {
  height: 40px;
  padding: 0 14px;
  border-radius: 10px;
  background: var(--well);
  border: 1px solid var(--line);
  color: var(--text);
}

.form-group input:focus {
  border-color: var(--accent);
  outline: none;
}

.modal-btns {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
}

.btn-secondary {
  padding: 8px 16px;
  border-radius: 10px;
  background: var(--surface-2);
  border: 1px solid var(--line);
  color: var(--text-2);
  font-weight: 600;
}

.btn-primary {
  padding: 8px 18px;
  border-radius: 10px;
  background: var(--accent);
  color: var(--accent-ink);
  font-weight: 700;
  box-shadow: 0 2px 10px var(--accent-glow);
}

/* Toast Notifications */
.toast-shelf {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 110;
  display: flex;
  flex-direction: column;
  gap: 8px;
  pointer-events: none;
}

.toast {
  padding: 10px 16px;
  border-radius: 12px;
  background: var(--surface);
  border: 1px solid var(--line);
  box-shadow: var(--shadow-float);
  font-size: 12px;
  font-weight: 600;
  color: var(--text);
  display: flex;
  align-items: center;
  gap: 10px;
  transform: translateY(20px);
  opacity: 0;
  transition: all 260ms var(--ease);
}

.toast.show {
  transform: translateY(0);
  opacity: 1;
}

/* Responsive Breakpoints */
@media (max-width: 960px) {
  .app-arena {
    grid-template-columns: 1fr;
    grid-template-rows: 320px 1fr;
  }
  .stage-3d {
    min-height: 320px;
  }
  .control-console {
    border-left: 0;
    border-top: 1px solid var(--line);
  }
}

@media (max-width: 700px) {
  body {
    overflow-y: auto;
  }
  .top-nav {
    padding: var(--safe-top) 16px 0 16px;
  }
  .brand-sub, .preview-tag {
    display: none;
  }
  .app-arena {
    display: flex;
    flex-direction: column;
    height: auto;
    overflow: visible;
  }
  .stage-3d {
    height: 280px;
    flex: 0 0 280px;
  }
  .stage-top-controls {
    top: 12px;
    left: 12px;
    right: 12px;
  }
  .stage-orbit-hint {
    display: none;
  }
  .stage-bento-telemetry {
    left: 12px;
    bottom: 12px;
    padding: 6px 12px;
  }
  .control-console {
    padding: 16px 14px 100px;
    overflow: visible;
    height: auto;
  }
  .mobile-dock {
    position: fixed;
    left: 16px;
    right: 16px;
    bottom: calc(14px + var(--safe-bottom));
    z-index: 60;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
    padding: 8px 14px;
    border-radius: 22px;
    background: var(--surface-glass);
    border: 1px solid var(--line);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    box-shadow: var(--shadow-float);
  }
  .dock-btn {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: var(--surface-2);
    display: grid;
    place-items: center;
    color: var(--text);
  }
  .dock-btn svg { width: 18px; height: 18px; fill: currentColor; }
  .dock-readout {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .dock-temp {
    font-family: var(--font-display);
    font-size: 20px;
    font-weight: 700;
  }
  .dock-mode {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-3);
  }
  .dock-pwr.on {
    background: var(--accent);
    color: var(--accent-ink);
  }
}

@media (min-width: 701px) {
  .mobile-dock {
    display: none;
  }
}
  </style>
</head>
<body>

  <!-- Top Navigation Bar -->
  <header class="top-nav">
    <div class="brand">
      <div class="brand-badge" aria-hidden="true">
        <svg viewBox="0 0 24 24"><path d="M12 2.4l2.42 6.96 7.34.28-5.82 4.55 2.02 7.04L12 17.1l-5.96 4.13 2.02-7.04L2.24 9.64l7.34-.28z"/></svg>
      </div>
      <div class="brand-titles">
        <span class="brand-name">Blue Star</span>
        <span class="brand-sub">Pure Architecture · IC318QNU</span>
      </div>
      <span class="preview-tag"><span class="preview-tag-dot"></span>Redesign Preview</span>
    </div>

    <div class="nav-right">
      <button class="status-capsule" id="connPill" type="button" onclick="openConfigModal()" title="MQTT Live State">
        <span class="live-beacon"></span>
        <span id="connStatusText">Live Feed</span>
      </button>

      <button class="nav-icon-btn" id="themeBtn" type="button" title="Switch Theme" onclick="toggleTheme()">
        <svg class="theme-sun" viewBox="0 0 24 24"><path d="M12 4.5a1 1 0 0 1 1 1V7a1 1 0 1 1-2 0V5.5a1 1 0 0 1 1-1zm0 11a3.5 3.5 0 1 1 0-7 3.5 3.5 0 0 1 0 7zm7.5-3.5a1 1 0 0 1 1 1h0a1 1 0 1 1 0 0zM3.5 12a1 1 0 0 1 1-1H6a1 1 0 1 1 0 2H4.5a1 1 0 0 1-1-1zm13.27-6.27a1 1 0 0 1 1.42 0l1.06 1.06a1 1 0 1 1-1.42 1.42l-1.06-1.06a1 1 0 0 1 0-1.42zM5.7 17.73a1 1 0 0 1 1.42 0l1.06 1.06a1 1 0 0 1-1.42 1.42L5.7 19.15a1 1 0 0 1 0-1.42zm12.03 1.42a1 1 0 0 1 0-1.42l1.06-1.06a1 1 0 1 1 1.42 1.42l-1.06 1.06a1 1 0 0 1-1.42 0zM6.76 7.73a1 1 0 0 1-1.42 0L4.28 6.67a1 1 0 0 1 1.42-1.42l1.06 1.06a1 1 0 0 1 0 1.42z"/></svg>
        <svg class="theme-moon" viewBox="0 0 24 24"><path d="M20.5 14.2A8.5 8.5 0 0 1 9.8 3.5a8.5 8.5 0 1 0 10.7 10.7z"/></svg>
      </button>

      <button class="nav-icon-btn" id="lockNavBtn" type="button" title="Lock Console" onclick="lockConsole()">
        <svg viewBox="0 0 24 24"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>
      </button>

      <button class="nav-icon-btn" id="soundBtn" type="button" title="Audio Feedback" onclick="toggleSound()">
        <svg viewBox="0 0 24 24"><path d="M14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77zm-2.5-1.23L6.5 6.5H2v11h4.5l5 4.5V2z"/></svg>
      </button>

      <button class="nav-icon-btn" type="button" title="Settings" onclick="openConfigModal()">
        <svg viewBox="0 0 24 24"><path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"/></svg>
      </button>
    </div>
  </header>

  <!-- Main App Arena -->
  <main class="app-arena">

    <!-- 3D Digital Twin Viewport -->
    <section class="stage-3d" aria-label="3D Air Conditioner Model">
      <div id="canvas3d-container"></div>

      <!-- Stage Top Floating Controls -->
      <div class="stage-top-controls">
        <div class="camera-glass-pills" role="tablist">
          <button class="cam-btn active" id="camBtnHero" type="button" onclick="setCameraView('hero')">Studio</button>
          <button class="cam-btn" id="camBtnAirflow" type="button" onclick="setCameraView('airflow')">Airflow</button>
          <button class="cam-btn" id="camBtnLouver" type="button" onclick="setCameraView('louver')">Louver Detail</button>
          <button class="cam-btn" id="camBtnXray" type="button" onclick="setCameraView('xray')">X-Ray</button>
        </div>
        <span class="stage-orbit-hint">Drag to orbit · Scroll to zoom</span>
      </div>

      <!-- Stage Bottom Bento Telemetry Strip -->
      <div class="stage-bento-telemetry">
        <div class="telemetry-tile">
          <span class="tel-label">Compressor</span>
          <span class="tel-value accent"><span class="pulse-indicator"></span><span id="compHzVal">48 Hz</span></span>
        </div>
        <div class="telemetry-tile">
          <span class="tel-label">Coil Temp</span>
          <span class="tel-value" id="coilTempVal">7.8°C</span>
        </div>
        <div class="telemetry-tile">
          <span class="tel-label">Total Run</span>
          <span class="tel-value" id="compHoursVal">1,248 h</span>
        </div>
        <div class="telemetry-tile">
          <span class="tel-label">Self-Clean</span>
          <span class="tel-value live" id="filterConditionVal">Clean</span>
        </div>
      </div>
    </section>

    <!-- Climate Command Console -->
    <aside class="control-console" aria-label="Climate Controls">

      <!-- Card 1: Hero Thermostat Dial -->
      <section class="glass-card hero-climate-card" id="heroCard">
        <div class="hero-top-row">
          <button class="power-capsule on" id="mainPowerBtn" type="button" onclick="togglePower()">
            <span class="power-ring"></span>
            <span id="powerBtnText">System Running</span>
          </button>
          <div class="room-temp-pill">
            <span class="room-temp-label">Ambient Room</span>
            <span class="room-temp-val" id="ambientReadout">27.0°C</span>
          </div>
        </div>

        <div class="dial-wrapper">
          <svg class="dial-svg" viewBox="0 0 180 180">
            <defs>
              <linearGradient id="climateDialGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#38bdf8"/>
                <stop offset="100%" stop-color="#0284c7"/>
              </linearGradient>
            </defs>
            <circle class="dial-track" cx="90" cy="90" r="72"/>
            <circle class="dial-ticks" cx="90" cy="90" r="64"/>
            <circle class="dial-glow-halo" id="dialGlow" cx="90" cy="90" r="72"/>
            <circle class="dial-progress-arc" id="dialBar" cx="90" cy="90" r="72"/>
          </svg>
          <div class="dial-core-content">
            <span class="target-caption">Target Temperature</span>
            <div class="target-readout">
              <span id="targetTempNum">24</span>
              <span class="target-deg">°</span>
            </div>
            <span class="delta-status-pill" id="climateDeltaBadge">↓ 3.0° Cooling to Target</span>
          </div>
        </div>

        <div class="stepper-bar">
          <button class="stepper-circle-btn" type="button" aria-label="Decrease temperature" onclick="adjustTemp(-1)">
            <svg viewBox="0 0 24 24"><path d="M19 13H5v-2h14v2z"/></svg>
          </button>
          <button class="stepper-circle-btn" type="button" aria-label="Increase temperature" onclick="adjustTemp(+1)">
            <svg viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
          </button>
        </div>
      </section>

      <!-- Card 2: Interactive Airflow & Louver Director (STANDOUT FEATURE!) -->
      <section class="glass-card louver-director-card">
        <div class="card-header">
          <span class="card-title">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/></svg>
            Airflow & Louver Director
          </span>
          <span class="card-badge" id="vaneBadge">Auto Sweep · 54°</span>
        </div>

        <!-- Live Cross-Section Angle Visualizer -->
        <div class="louver-vector-screen">
          <div class="louver-preview-stage">
            <svg class="louver-svg-crosssection" viewBox="0 0 100 60">
              <!-- AC Body Cross-Section Profile -->
              <path d="M10 8 Q10 4 14 4 L65 4 Q70 4 72 8 L76 34 Q76 40 70 42 L28 42 L12 42 Q10 42 10 38 Z" fill="none" stroke="currentColor" stroke-width="2" opacity="0.4"/>
              <!-- Intake vent top -->
              <line x1="20" y1="8" x2="55" y2="8" stroke="currentColor" stroke-width="1.5" stroke-dasharray="2 2" opacity="0.3"/>
              <!-- Pivot point -->
              <circle cx="30" cy="42" r="2.5" fill="var(--accent)"/>
              <!-- Motorized Flap Blade (Rotates live with 3D unit!) -->
              <g id="svgBladePivot" class="louver-flap-blade">
                <line x1="30" y1="42" x2="58" y2="42" stroke="var(--accent)" stroke-width="3" stroke-linecap="round"/>
              </g>
              <!-- Airflow vector streamline rays -->
              <g class="airflow-vector-rays" stroke="var(--accent)" stroke-width="1.5" fill="none" opacity="0.75">
                <path id="svgAirRay1" d="M38 46 Q60 52 88 56"/>
                <path id="svgAirRay2" d="M44 43 Q68 47 94 48"/>
              </g>
            </svg>
            <div>
              <div style="font-size: 11px; font-weight: 700; color: var(--text); letter-spacing: 0.04em;">PHYSICAL KINEMATICS</div>
              <div style="font-size: 10px; color: var(--text-3);">Micro-stepper synchronized</div>
            </div>
          </div>
          <div class="louver-readout-col">
            <span class="louver-digital-angle" id="louverDegreeText">54°</span>
            <span class="louver-mode-caption" id="louverModeText">Harmonic Sweep</span>
          </div>
        </div>

        <!-- Louver 5-Button Grid -->
        <div class="louver-pill-grid" role="group" aria-label="Louver positions">
          <button class="pill-card-btn active" id="vaneBtn0" type="button" onclick="setVane(0)">
            <svg viewBox="0 0 24 24">
              <rect x="2" y="4" width="20" height="7" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/>
              <path d="M4 11c3 4 8 4 11 0" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
              <path d="M7 16c2.5 1.8 7.5 1.8 10 0" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="2 2" opacity="0.6"/>
            </svg>
            <span>Auto</span>
          </button>
          <button class="pill-card-btn" id="vaneBtn1" type="button" onclick="setVane(1)">
            <svg viewBox="0 0 24 24">
              <rect x="2" y="4" width="20" height="7" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/>
              <path d="M4 11l10-2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M15 8h4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity="0.6"/>
            </svg>
            <span>Top</span>
          </button>
          <button class="pill-card-btn" id="vaneBtn3" type="button" onclick="setVane(3)">
            <svg viewBox="0 0 24 24">
              <rect x="2" y="4" width="20" height="7" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/>
              <path d="M4 11h11" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M16 11h3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity="0.6"/>
            </svg>
            <span>Mid</span>
          </button>
          <button class="pill-card-btn" id="vaneBtn5" type="button" onclick="setVane(5)">
            <svg viewBox="0 0 24 24">
              <rect x="2" y="4" width="20" height="7" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/>
              <path d="M4 11l9 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M14 17l4 2" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity="0.6"/>
            </svg>
            <span>Floor</span>
          </button>
          <button class="pill-card-btn" id="hSwingBtn" type="button" onclick="toggleHSwing()">
            <svg viewBox="0 0 24 24">
              <path d="M7 8l-4 4 4 4M17 8l4 4-4 4M3 12h18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>4-Way</span>
          </button>
        </div>
      </section>

      <!-- Card 3: Operating Mode (Continuous Capsule Track) -->
      <section class="glass-card">
        <div class="card-header">
          <span class="card-title">Climate Mode</span>
          <span class="card-badge" id="modeBadge">Cooling</span>
        </div>
        <div class="capsule-track">
          <button class="capsule-seg active" id="modeBtn1" type="button" onclick="setMode(1)">
            <svg viewBox="0 0 24 24"><path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM17 13l-5 5-5-5h3V9h4v4h3z"/></svg>
            <span>Cool</span>
          </button>
          <button class="capsule-seg" id="modeBtn2" type="button" onclick="setMode(2)">
            <svg viewBox="0 0 24 24"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
            <span>Dry</span>
          </button>
          <button class="capsule-seg" id="modeBtn3" type="button" onclick="setMode(3)">
            <svg viewBox="0 0 24 24"><path d="M12 4c-4.41 0-8 3.59-8 8s3.59 8 8 8 8-3.59 8-8-3.59-8-8-8zm0 2c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6 2.69-6 6-6z"/></svg>
            <span>Fan</span>
          </button>
          <button class="capsule-seg" id="modeBtn4" type="button" onclick="setMode(4)">
            <svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 14.93V18h-2v-1.07A6 6 0 0 1 6.07 12H5v-2h1.07A6 6 0 0 1 11 6.07V5h2v1.07A6 6 0 0 1 17.93 11H19v2h-1.07A6 6 0 0 1 13 16.93z"/></svg>
            <span>Auto</span>
          </button>
        </div>
      </section>

      <!-- Card 4: Fan Velocity Track -->
      <section class="glass-card">
        <div class="card-header">
          <span class="card-title">Fan Velocity</span>
          <span class="card-badge" id="fanBadge">High · Stage 4</span>
        </div>
        <div class="capsule-track cols-6">
          <button class="capsule-seg" id="fanBtn1" type="button" onclick="setFan(1)"><span>Quiet</span></button>
          <button class="capsule-seg" id="fanBtn2" type="button" onclick="setFan(2)"><span>Low</span></button>
          <button class="capsule-seg" id="fanBtn3" type="button" onclick="setFan(3)"><span>Med</span></button>
          <button class="capsule-seg active" id="fanBtn4" type="button" onclick="setFan(4)"><span>High</span></button>
          <button class="capsule-seg" id="fanBtn5" type="button" onclick="setFan(5)"><span>Turbo</span></button>
          <button class="capsule-seg" id="fanBtn6" type="button" onclick="setFan(6)"><span>Auto</span></button>
        </div>
      </section>

      <!-- Card 5: Convertible Inverter Capacity -->
      <section class="glass-card">
        <div class="card-header">
          <span class="card-title">Inverter Capacity</span>
          <span class="card-badge" id="convBadge">100% · Full Ton</span>
        </div>
        <div class="convertible-grid">
          <button class="conv-pill active" id="convBtn1" type="button" onclick="setConvertible(1)">100%</button>
          <button class="conv-pill" id="convBtn2" type="button" onclick="setConvertible(2)">80%</button>
          <button class="conv-pill" id="convBtn3" type="button" onclick="setConvertible(3)">60%</button>
          <button class="conv-pill" id="convBtn4" type="button" onclick="setConvertible(4)">40%</button>
        </div>
      </section>

      <!-- Card 6: Intelligent Eco Features -->
      <section class="glass-card">
        <div class="card-header">
          <span class="card-title">Intelligent Features</span>
        </div>
        <div class="features-list">
          <div class="feature-row" id="cardTurbo" onclick="toggleFeature('turbo')">
            <div class="feature-left">
              <div class="feature-icon-square">
                <svg viewBox="0 0 24 24"><path d="M7 2v11h3v9l7-12h-4l4-8z"/></svg>
              </div>
              <span class="feature-label">Turbo Cool (110% Boost)</span>
            </div>
            <div class="luxury-switch"></div>
          </div>

          <div class="feature-row" id="cardEco" onclick="toggleFeature('eco')">
            <div class="feature-left">
              <div class="feature-icon-square">
                <svg viewBox="0 0 24 24"><path d="M12 2C6.5 2 2 6.5 2 12c0 3.58 2.5 7 6 8.5V18c-2.76 0-5-2.24-5-5 0-2.05 1.23-3.81 3-4.58V11c0 1.66 1.34 3 3 3h2v-2h-2c-.55 0-1-.45-1-1V7.1c3.55.77 6 3.65 6 6.9 0 1.1-.9 2-2 2h-1v2h1c2.21 0 4-1.79 4-4 0-4.41-3.59-8-8-8z"/></svg>
              </div>
              <span class="feature-label">Eco Mode (Smart Saver)</span>
            </div>
            <div class="luxury-switch"></div>
          </div>

          <div class="feature-row" id="cardSleep" onclick="toggleFeature('sleep')">
            <div class="feature-left">
              <div class="feature-icon-square">
                <svg viewBox="0 0 24 24"><path d="M12.3 2a10 10 0 0 0-1.9 20 10 10 0 0 0 11.5-11.5A10 10 0 0 0 12.3 2z"/></svg>
              </div>
              <span class="feature-label">Comfort Sleep (+1°C/hr)</span>
            </div>
            <div class="luxury-switch"></div>
          </div>

          <div class="feature-row on" id="cardLight" onclick="toggleFeature('light')">
            <div class="feature-left">
              <div class="feature-icon-square">
                <svg viewBox="0 0 24 24"><path d="M9 21c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H9v1zm3-19C8.14 2 5 5.14 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.86-3.14-7-7-7z"/></svg>
              </div>
              <span class="feature-label">Indoor LED Display</span>
            </div>
            <div class="luxury-switch"></div>
          </div>

          <div class="feature-row" id="cardC1" onclick="toggleFeature('c1')">
            <div class="feature-left">
              <div class="feature-icon-square">
                <svg viewBox="0 0 24 24"><path d="M20.38 8.57l-1.23 1.85a8 8 0 0 1-.22 7.58H5.07A8 8 0 0 1 15.58 6.85l1.85-1.23A10 10 0 0 0 3.35 19a2 2 0 0 0 1.72 1h13.85a2 2 0 0 0 1.74-1 10 10 0 0 0-.28-10.43zM10.59 15.41a2 2 0 0 0 2.83 0l5.66-8.49-8.49 5.66a2 2 0 0 0 0 2.83z"/></svg>
              </div>
              <span class="feature-label">C1 Mode (Full Load Test)</span>
            </div>
            <div class="luxury-switch"></div>
          </div>
        </div>
      </section>

      <!-- Console Footer -->
      <div class="console-foot">
        <span>Megmeet MD50BS Architecture</span>
        <span id="syncLabel">Synchronized · Pure Architecture</span>
      </div>

    </aside>
  </main>

  <!-- Mobile Floating Command Dock (Viewports < 700px) -->
  <nav class="mobile-dock" aria-label="Quick Climate Dock">
    <button class="dock-btn" type="button" aria-label="Decrease Temp" onclick="adjustTemp(-1)">
      <svg viewBox="0 0 24 24"><path d="M19 13H5v-2h14v2z"/></svg>
    </button>
    <div class="dock-readout">
      <span class="dock-temp" id="dockTemp">24°C</span>
      <span class="dock-mode" id="dockMode">Cooling</span>
    </div>
    <button class="dock-btn" type="button" aria-label="Increase Temp" onclick="adjustTemp(+1)">
      <svg viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
    </button>
    <button class="dock-btn dock-pwr on" id="dockPower" type="button" aria-label="Toggle Power" onclick="togglePower()">
      <svg viewBox="0 0 24 24"><path d="M13 3h-2v10h2V3zm4.83 2.17l-1.42 1.42C17.99 7.86 19 9.81 19 12c0 3.87-3.13 7-7 7s-7-3.13-7-7c0-2.19 1.01-4.14 2.58-5.42L6.17 5.17C4.23 6.82 3 9.26 3 12c0 4.97 4.03 9 9 9s9-4.03 9-9c0-2.74-1.23-5.18-3.17-6.83z"/></svg>
    </button>
  </nav>

  <!-- Security PIN Lock Screen -->
  <div class="lock-overlay" id="lockScreen" role="dialog" aria-modal="true">
    <div class="lock-box" id="lockBox">
      <div class="brand-badge" style="width:48px;height:48px;margin-bottom:8px;">
        <svg viewBox="0 0 24 24" style="width:26px;height:26px;"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>
      </div>
      <h2 class="lock-title">Blue Star Security</h2>
      <p class="lock-msg" id="lockStatusMsg">Enter device 4-digit PIN</p>
      <div class="pin-dots">
        <div class="pin-dot" id="dot0"></div>
        <div class="pin-dot" id="dot1"></div>
        <div class="pin-dot" id="dot2"></div>
        <div class="pin-dot" id="dot3"></div>
      </div>
      <div class="pin-keypad">
        <button class="pad-key" onclick="pressPin('1')">1</button>
        <button class="pad-key" onclick="pressPin('2')">2</button>
        <button class="pad-key" onclick="pressPin('3')">3</button>
        <button class="pad-key" onclick="pressPin('4')">4</button>
        <button class="pad-key" onclick="pressPin('5')">5</button>
        <button class="pad-key" onclick="pressPin('6')">6</button>
        <button class="pad-key" onclick="pressPin('7')">7</button>
        <button class="pad-key" onclick="pressPin('8')">8</button>
        <button class="pad-key" onclick="pressPin('9')">9</button>
        <button class="pad-key util" onclick="clearPin()">Clear</button>
        <button class="pad-key" onclick="pressPin('0')">0</button>
        <button class="pad-key util" onclick="backspacePin()">⌫</button>
      </div>
      <div style="font-size: 11px; color: var(--text-3); margin-top: 8px;">Demo default PIN: 1234</div>
    </div>
  </div>

  <!-- Settings Modal -->
  <div class="modal-backdrop" id="cfgModal" role="dialog">
    <div class="modal-dialog">
      <h3 class="modal-title">MQTT Bridge Configuration</h3>
      <div class="form-group">
        <label>Broker Host</label>
        <input type="text" id="cfgHost" value="io.adafruit.com">
      </div>
      <div class="form-group">
        <label>Port (WSS)</label>
        <input type="number" id="cfgPort" value="443">
      </div>
      <div class="form-group">
        <label>Username</label>
        <input type="text" id="cfgUser" value="">
      </div>
      <div class="form-group">
        <label>AIO Key / Password</label>
        <input type="password" id="cfgPass" value="">
      </div>
      <div class="modal-btns">
        <button class="btn-secondary" type="button" onclick="closeConfigModal()">Cancel</button>
        <button class="btn-primary" type="button" onclick="saveMqttConfig()">Connect</button>
      </div>
    </div>
  </div>

  <!-- Toast Shelf -->
  <div class="toast-shelf" id="toastShelf"></div>

  <!-- Scripts: Three.js & MQTT.js -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>

  <script>
    // =========================================================================
    // STATE ENGINE & HARDWARE TOPIC FIDELITY
    // =========================================================================
    const state = {
      power: 1,
      targetTemp: 24,
      roomTemp: 27.0,
      mode: 1,        // 1=Cool, 2=Dry, 3=Fan, 4=Auto
      fan: 4,         // 1=Quiet, 2=Low, 3=Med, 4=High, 5=Turbo, 6=Auto
      vane: 0,        // 0=Swing, 1=Top, 2=HighMid, 3=Mid, 4=MidLow, 5=Floor
      hSwing: 0,      // 0=Off, 1=4-Way Auto
      turbo: 0,
      eco: 0,
      sleep: 0,
      light: 1,       // 1=On (Indoor unit front LED active)
      convertible: 1, // 1=100%, 2=80%, 3=60%, 4=40%
      c1Mode: 0,
      compHz: 48,
      coilTemp: 7.8,
      compHours: 1248,
      filterAlert: 0
    };

    let audioContext = null;
    let isMuted = false;
    let enteredPin = "";
    const DEVICE_PIN = "1234";

    // Web Audio Synthesizer
    function getAudioCtx() {
      if (!audioContext) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (AudioCtx) audioContext = new AudioCtx();
      }
      if (audioContext && audioContext.state === 'suspended') {
        audioContext.resume();
      }
      return audioContext;
    }

    function playAudio(type) {
      if (isMuted) return;
      try {
        const ctx = getAudioCtx();
        if (!ctx) return;
        const now = ctx.currentTime;
        if (type === 'click') {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(1400, now);
          osc.frequency.exponentialRampToValueAtTime(400, now + 0.03);
          gain.gain.setValueAtTime(0.08, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.03);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now);
          osc.stop(now + 0.03);
        } else if (type === 'chime') {
          [880, 1174.66, 1760].forEach((freq, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(freq, now + i * 0.06);
            gain.gain.setValueAtTime(0.06, now + i * 0.06);
            gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.06 + 0.22);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now + i * 0.06);
            osc.stop(now + i * 0.06 + 0.22);
          });
        } else if (type === 'error') {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(180, now);
          gain.gain.setValueAtTime(0.12, now);
          gain.gain.exponentialRampToValueAtTime(0.001, now + 0.16);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now);
          osc.stop(now + 0.16);
        }
      } catch (e) {}
    }

    function toggleSound() {
      isMuted = !isMuted;
      showToast(isMuted ? "Sound feedback muted" : "Sound feedback enabled", "info");
      document.getElementById("soundBtn").style.opacity = isMuted ? "0.45" : "1";
    }

    function showToast(text, type = "info") {
      const shelf = document.getElementById("toastShelf");
      const toast = document.createElement("div");
      toast.className = "toast";
      toast.textContent = text;
      shelf.appendChild(toast);
      requestAnimationFrame(() => toast.classList.add("show"));
      setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 300);
      }, 2800);
    }

    // Security PIN Pad
    function lockConsole() {
      playAudio('chime');
      enteredPin = "";
      updatePinDots();
      document.getElementById("lockStatusMsg").textContent = "Enter device 4-digit PIN";
      document.getElementById("lockScreen").classList.add("open");
    }

    function pressPin(digit) {
      if (enteredPin.length >= 4) return;
      playAudio('click');
      enteredPin += digit;
      updatePinDots();
      if (enteredPin.length === 4) {
        setTimeout(verifyPin, 140);
      }
    }

    function clearPin() {
      playAudio('click');
      enteredPin = "";
      updatePinDots();
    }

    function backspacePin() {
      playAudio('click');
      enteredPin = enteredPin.slice(0, -1);
      updatePinDots();
    }

    function updatePinDots() {
      for (let i = 0; i < 4; i++) {
        const dot = document.getElementById(`dot${i}`);
        if (dot) dot.classList.toggle("filled", i < enteredPin.length);
      }
    }

    function verifyPin() {
      if (enteredPin === DEVICE_PIN || enteredPin === "1234") {
        playAudio('chime');
        document.getElementById("lockScreen").classList.remove("open");
        showToast("Console Unlocked", "success");
      } else {
        playAudio('error');
        const box = document.getElementById("lockBox");
        box.style.transform = "translateX(-8px)";
        setTimeout(() => box.style.transform = "translateX(8px)", 70);
        setTimeout(() => box.style.transform = "translateX(-4px)", 140);
        setTimeout(() => box.style.transform = "translateX(0)", 210);
        document.getElementById("lockStatusMsg").textContent = "Incorrect PIN. Try again.";
        enteredPin = "";
        updatePinDots();
      }
    }

    // =========================================================================
    // 3D DIGITAL TWIN & KINEMATICS ENGINE
    // =========================================================================
    let scene, camera, renderer, clock;
    let acGroup, facadeGroup, casingMesh, louverPivot, louverMesh, blowerDrum;
    let ventVanes = [];
    let airflowParticles;
    let particlePositions, particleVelocities, particleLifespans;
    let frontLedMesh, frontLedCanvas, frontLedCtx, frontLedTexture;

    let currentLouverAngle = 0.58; // Current physical pitch
    let currentVaneAngle = 0.0;   // Current yaw
    let currentHSwingAmp = 0.0;

    const LOUVER_CLOSED = 0.28;
    const LOUVER_SWING_MIN = 0.58; // 33.2°
    const LOUVER_SWING_MAX = 1.30; // 74.5°
    const LOUVER_SWING_PERIOD = 5.2; // seconds

    const LOUVER_STEPS = {
      1: 0.58, // Top (33.2°)
      2: 0.76, // High-Mid (43.5°)
      3: 0.94, // Mid (53.8°)
      4: 1.12, // Mid-Low (64.1°)
      5: 1.30, // Floor (74.5°)
      6: 0.94  // Auto fallback
    };

    const cameraOrbit = {
      target: new THREE.Vector3(0, -0.05, 0),
      radius: 3.4,
      targetRadius: 3.4,
      theta: 0.38,
      targetTheta: 0.38,
      phi: 1.25,
      targetPhi: 1.25,
      isDragging: false,
      lastX: 0,
      lastY: 0
    };

    function init3D() {
      const container = document.getElementById("canvas3d-container");
      scene = new THREE.Scene();

      // Atmospheric Studio Fog
      const bgHex = currentTheme() === "light" ? 0xf7f9fc : 0x08090d;
      scene.fog = new THREE.Fog(bgHex, 6, 16);

      camera = new THREE.PerspectiveCamera(38, container.clientWidth / container.clientHeight, 0.1, 30);
      clock = new THREE.Clock();

      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: "high-performance" });
      renderer.setSize(container.clientWidth, container.clientHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = currentTheme() === "light" ? 1.02 : 0.96;
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      container.appendChild(renderer.domElement);

      setupLighting();
      buildACModel();
      buildAirflowParticles();
      setupOrbitControls(container);

      window.addEventListener("resize", onWindowResize);
      animate();
    }

    function setupLighting() {
      const isLight = currentTheme() === "light";
      const ambLight = new THREE.AmbientLight(isLight ? 0xffffff : 0x90b4ce, isLight ? 0.45 : 0.28);
      scene.add(ambLight);

      const hemiLight = new THREE.HemisphereLight(
        isLight ? 0xffffff : 0xd0e8ff,
        isLight ? 0xd0dbe8 : 0x070b12,
        isLight ? 0.55 : 0.45
      );
      scene.add(hemiLight);

      // Studio Key Light
      const keyLight = new THREE.DirectionalLight(0xffffff, isLight ? 1.1 : 1.0);
      keyLight.position.set(3.5, 4.8, 4.2);
      keyLight.castShadow = true;
      keyLight.shadow.mapSize.set(2048, 2048);
      keyLight.shadow.camera.near = 0.5;
      keyLight.shadow.camera.far = 14;
      keyLight.shadow.bias = -0.0004;
      keyLight.shadow.radius = 3;
      scene.add(keyLight);

      // Fill Light
      const fillLight = new THREE.DirectionalLight(isLight ? 0xcce3f8 : 0x38bdf8, isLight ? 0.4 : 0.32);
      fillLight.position.set(-4.0, 1.6, 3.0);
      scene.add(fillLight);

      // Rim Light for Luxury Edge Glint
      const rimLight = new THREE.DirectionalLight(isLight ? 0xe2ecff : 0x7de9ff, isLight ? 0.5 : 0.7);
      rimLight.position.set(-2.0, 2.0, -4.0);
      scene.add(rimLight);
    }

    function buildACModel() {
      acGroup = new THREE.Group();
      scene.add(acGroup);
      facadeGroup = new THREE.Group();
      acGroup.add(facadeGroup);

      const AC_W = 2.26, AC_H = 0.76, AC_D = 0.52;
      const VENT_W = 2.00, VENT_H = 0.125, VENT_Y = -0.275, FRONT_Z = AC_D / 2;

      // 1. Main Casing Body (Pure Architectural White Matte)
      const casingMat = new THREE.MeshStandardMaterial({
        color: 0xf8fafc,
        roughness: 0.28,
        metalness: 0.08
      });
      const bodyGeom = new THREE.BoxGeometry(AC_W, AC_H, AC_D, 4, 4, 4);
      casingMesh = new THREE.Mesh(bodyGeom, casingMat);
      casingMesh.castShadow = true;
      casingMesh.receiveShadow = true;
      facadeGroup.add(casingMesh);

      // 2. Beveled Front Fascia Panel
      const panelMat = new THREE.MeshStandardMaterial({
        color: 0xffffff,
        roughness: 0.18,
        metalness: 0.05
      });
      const panelGeom = new THREE.BoxGeometry(AC_W + 0.02, AC_H * 0.78, 0.03);
      const frontPanel = new THREE.Mesh(panelGeom, panelMat);
      frontPanel.position.set(0, 0.065, FRONT_Z + 0.012);
      facadeGroup.add(frontPanel);

      // Blue Star Signature Emblem (Minimalist Badge)
      const logoGeom = new THREE.PlaneGeometry(0.24, 0.065);
      const logoCanvas = document.createElement("canvas");
      logoCanvas.width = 256; logoCanvas.height = 70;
      const ctx = logoCanvas.getContext("2d");
      ctx.fillStyle = "#0066cc";
      ctx.roundRect(0, 0, 256, 70, 14); ctx.fill();
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 32px 'Outfit', sans-serif";
      ctx.fillText("★ BLUE STAR", 22, 48);
      const logoTexture = new THREE.CanvasTexture(logoCanvas);
      const logoMesh = new THREE.Mesh(logoGeom, new THREE.MeshBasicMaterial({ map: logoTexture, transparent: true }));
      logoMesh.position.set(-0.80, 0.20, FRONT_Z + 0.03);
      facadeGroup.add(logoMesh);

      // Hidden Front LED Temperature Matrix (Glows through the front panel!)
      frontLedCanvas = document.createElement("canvas");
      frontLedCanvas.width = 128; frontLedCanvas.height = 64;
      frontLedCtx = frontLedCanvas.getContext("2d");
      frontLedTexture = new THREE.CanvasTexture(frontLedCanvas);
      const ledGeom = new THREE.PlaneGeometry(0.18, 0.09);
      const ledMat = new THREE.MeshBasicMaterial({ map: frontLedTexture, transparent: true, opacity: 0.92 });
      frontLedMesh = new THREE.Mesh(ledGeom, ledMat);
      frontLedMesh.position.set(0.72, 0.08, FRONT_Z + 0.03);
      facadeGroup.add(frontLedMesh);
      updateFrontLedTexture();

      // Top Air Intake Grille Louvers
      const grilleMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.5 });
      for (let i = 0; i < 7; i++) {
        const slat = new THREE.Mesh(new THREE.BoxGeometry(AC_W * 0.88, 0.006, 0.024), grilleMat);
        slat.position.set(0, AC_H / 2 + 0.002, -0.14 + i * 0.045);
        facadeGroup.add(slat);
      }

      // 3. Discharge Air Vent Mouth (Deep Recessed Cavity)
      const ventCavity = new THREE.Mesh(
        new THREE.BoxGeometry(VENT_W, VENT_H + 0.02, 0.16),
        new THREE.MeshStandardMaterial({ color: 0x080c14, roughness: 0.9 })
      );
      ventCavity.position.set(0, VENT_Y, FRONT_Z - 0.05);
      facadeGroup.add(ventCavity);

      // 4. Blower Wheel Rotor inside vent
      const drumGeom = new THREE.CylinderGeometry(0.045, 0.045, VENT_W - 0.06, 24);
      drumGeom.rotateZ(Math.PI / 2);
      blowerDrum = new THREE.Mesh(drumGeom, new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.7, roughness: 0.35 }));
      blowerDrum.position.set(0, VENT_Y - 0.005, FRONT_Z - 0.07);
      acGroup.add(blowerDrum);

      // 5. 13 Synchronized Vertical Airflow Deflector Vanes
      const vaneMat = new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.4, roughness: 0.5 });
      for (let i = 0; i < 13; i++) {
        const pivot = new THREE.Group();
        pivot.position.set(-0.84 + i * 0.14, VENT_Y - 0.002, FRONT_Z - 0.01);
        const vane = new THREE.Mesh(new THREE.BoxGeometry(0.004, VENT_H * 0.84, 0.075), vaneMat);
        pivot.add(vane);
        acGroup.add(pivot);
        ventVanes.push(pivot);
      }

      // 6. MOTORIZED HORIZONTAL LOUVER BLADE (PROMINENT SCULPTED AERODYNAMIC WING)
      louverPivot = new THREE.Group();
      louverPivot.position.set(0, VENT_Y - VENT_H / 2 + 0.004, FRONT_Z + 0.008);

      const bladeGeom = new THREE.BoxGeometry(VENT_W + 0.02, VENT_H + 0.02, 0.016);
      bladeGeom.translate(0, (VENT_H + 0.02) / 2, 0);
      const louverMat = new THREE.MeshStandardMaterial({
        color: 0xffffff,
        metalness: 0.22,
        roughness: 0.22
      });
      louverMesh = new THREE.Mesh(bladeGeom, louverMat);
      louverMesh.castShadow = true;
      louverPivot.add(louverMesh);

      // Metallic Brushed Chrome Accent Trim on Louver Trailing Edge
      const trimGeom = new THREE.BoxGeometry(VENT_W, 0.004, 0.02);
      trimGeom.translate(0, VENT_H + 0.018, 0.002);
      const trimMesh = new THREE.Mesh(trimGeom, new THREE.MeshStandardMaterial({ color: 0xc4cbd4, metalness: 0.85, roughness: 0.15 }));
      louverPivot.add(trimMesh);

      // Inner Sub-Vane (Tandem velocity blade)
      const subBladeGeom = new THREE.BoxGeometry(VENT_W - 0.06, 0.035, 0.006);
      subBladeGeom.translate(0, 0.04, -0.02);
      const subBlade = new THREE.Mesh(subBladeGeom, new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.5, roughness: 0.4 }));
      louverPivot.add(subBlade);

      facadeGroup.add(louverPivot);

      // 7. SEAMLESS INFINITY SHADOW RECEIVER (NO HARSH CUT-OFF PLATE!)
      const shadowPlane = new THREE.Mesh(
        new THREE.PlaneGeometry(24, 24),
        new THREE.ShadowMaterial({ opacity: currentTheme() === "light" ? 0.16 : 0.35 })
      );
      shadowPlane.rotation.x = -Math.PI / 2;
      shadowPlane.position.y = -0.58;
      shadowPlane.receiveShadow = true;
      scene.add(shadowPlane);
    }

    function updateFrontLedTexture() {
      if (!frontLedCtx || !frontLedTexture) return;
      frontLedCtx.clearRect(0, 0, 128, 64);
      if (state.power === 1 && state.light === 1) {
        frontLedCtx.fillStyle = currentTheme() === "light" ? "rgba(0, 102, 204, 0.88)" : "rgba(224, 242, 254, 0.92)";
        frontLedCtx.font = "bold 38px 'Outfit', sans-serif";
        frontLedCtx.textAlign = "center";
        frontLedCtx.textBaseline = "middle";
        const txt = state.c1Mode === 1 ? "C1" : `${Math.round(state.targetTemp)}°`;
        frontLedCtx.fillText(txt, 64, 32);
      }
      frontLedTexture.needsUpdate = true;
    }

    function buildAirflowParticles() {
      const count = 700;
      const geom = new THREE.BufferGeometry();
      particlePositions = new Float32Array(count * 3);
      particleVelocities = new Float32Array(count * 3);
      particleLifespans = new Float32Array(count);

      for (let i = 0; i < count; i++) {
        resetParticle(i, true);
      }

      geom.setAttribute("position", new THREE.BufferAttribute(particlePositions, 3));

      // Gaussian Radial Glow Particle Texture
      const canvas = document.createElement("canvas");
      canvas.width = 64; canvas.height = 64;
      const ctx = canvas.getContext("2d");
      const grad = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
      grad.addColorStop(0, "rgba(255, 255, 255, 1)");
      grad.addColorStop(0.28, currentTheme() === "light" ? "rgba(0, 102, 204, 0.7)" : "rgba(56, 189, 248, 0.7)");
      grad.addColorStop(1, "rgba(0, 102, 204, 0)");
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 64, 64);
      const texture = new THREE.CanvasTexture(canvas);

      const mat = new THREE.PointsMaterial({
        size: 0.075,
        map: texture,
        transparent: true,
        opacity: 0.44,
        blending: currentTheme() === "light" ? THREE.NormalBlending : THREE.AdditiveBlending,
        depthWrite: false,
        sizeAttenuation: true,
        color: new THREE.Color(currentTheme() === "light" ? 0x0066cc : 0x38bdf8)
      });

      airflowParticles = new THREE.Points(geom, mat);
      scene.add(airflowParticles);
    }

    function resetParticle(i, immediateSpread) {
      const offset = i * 3;
      const VENT_W = 2.00, VENT_Y = -0.275, FRONT_Z = 0.52 / 2;

      particlePositions[offset] = (Math.random() - 0.5) * (VENT_W - 0.16);
      particlePositions[offset + 1] = VENT_Y + (Math.random() - 0.5) * 0.04;
      particlePositions[offset + 2] = FRONT_Z + 0.015 + Math.random() * 0.04;

      const speeds = [0, 0.22, 0.34, 0.48, 0.70, 0.98, 0.48];
      const speed = speeds[state.fan] || 0.48;

      const pitch = Math.abs(currentLouverAngle);
      const yaw = currentVaneAngle;

      particleVelocities[offset] = Math.sin(yaw) * speed * 0.85 + (Math.random() - 0.5) * speed * 0.15;
      particleVelocities[offset + 1] = -speed * (0.35 + 0.95 * Math.sin(pitch)) * (0.8 + Math.random() * 0.4);
      particleVelocities[offset + 2] = speed * (0.55 + 0.45 * Math.cos(pitch)) * (0.8 + Math.random() * 0.5);

      particleLifespans[i] = immediateSpread ? Math.random() : 0;
    }

    function setupOrbitControls(container) {
      container.addEventListener("pointerdown", (e) => {
        cameraOrbit.isDragging = true;
        cameraOrbit.lastX = e.clientX;
        cameraOrbit.lastY = e.clientY;
      });
      window.addEventListener("pointermove", (e) => {
        if (!cameraOrbit.isDragging) return;
        const dx = e.clientX - cameraOrbit.lastX;
        const dy = e.clientY - cameraOrbit.lastY;
        cameraOrbit.lastX = e.clientX;
        cameraOrbit.lastY = e.clientY;

        cameraOrbit.targetTheta -= dx * 0.006;
        cameraOrbit.targetPhi = Math.max(0.65, Math.min(Math.PI / 2 - 0.08, cameraOrbit.targetPhi - dy * 0.006));
      });
      window.addEventListener("pointerup", () => cameraOrbit.isDragging = false);

      container.addEventListener("wheel", (e) => {
        e.preventDefault();
        cameraOrbit.targetRadius = Math.max(2.2, Math.min(5.2, cameraOrbit.targetRadius + e.deltaY * 0.0025));
      }, { passive: false });
    }

    function setCameraView(preset) {
      playAudio('click');
      document.querySelectorAll(".cam-btn").forEach(b => b.classList.remove("active"));
      if (preset === 'hero') {
        document.getElementById("camBtnHero").classList.add("active");
        cameraOrbit.targetRadius = 3.4; cameraOrbit.targetTheta = 0.38; cameraOrbit.targetPhi = 1.25;
        if (facadeGroup) facadeGroup.visible = true;
      } else if (preset === 'airflow') {
        document.getElementById("camBtnAirflow").classList.add("active");
        cameraOrbit.targetRadius = 3.8; cameraOrbit.targetTheta = 0.95; cameraOrbit.targetPhi = 1.38;
        if (facadeGroup) facadeGroup.visible = true;
      } else if (preset === 'louver') {
        document.getElementById("camBtnLouver").classList.add("active");
        cameraOrbit.targetRadius = 2.4; cameraOrbit.targetTheta = 0.12; cameraOrbit.targetPhi = 1.48;
        if (facadeGroup) facadeGroup.visible = true;
      } else if (preset === 'xray') {
        document.getElementById("camBtnXray").classList.add("active");
        cameraOrbit.targetRadius = 3.2; cameraOrbit.targetTheta = 0.38; cameraOrbit.targetPhi = 1.25;
        if (facadeGroup) facadeGroup.visible = !facadeGroup.visible;
      }
    }

    function onWindowResize() {
      const container = document.getElementById("canvas3d-container");
      if (!container || !renderer || !camera) return;
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    }

    function animate() {
      requestAnimationFrame(animate);
      const delta = Math.min(clock.getDelta(), 0.1);
      const time = clock.getElapsedTime();

      // 1. REVAMPED LOUVER STEPPER MOTOR KINEMATICS
      if (louverPivot) {
        let targetAngle = LOUVER_CLOSED;
        if (state.power === 1) {
          if (state.vane === 0) {
            // Auto Swing: Harmonic stepper cycle with quintic dwell turnaround
            const cycle = (time % LOUVER_SWING_PERIOD) / LOUVER_SWING_PERIOD;
            const cosPhase = 0.5 - 0.5 * Math.cos(cycle * Math.PI * 2);
            const smoothed = cosPhase * cosPhase * cosPhase * (cosPhase * (cosPhase * 6 - 15) + 10);
            targetAngle = LOUVER_SWING_MIN + (LOUVER_SWING_MAX - LOUVER_SWING_MIN) * smoothed;
          } else {
            targetAngle = LOUVER_STEPS[state.vane] || LOUVER_STEPS[3];
          }
        }

        // Critically damped tracking: zero overshoot, smooth motor glide
        const trackSpeed = (state.power === 0) ? 4.5 : (state.vane === 0 ? 12.0 : 7.0);
        currentLouverAngle = THREE.MathUtils.damp(currentLouverAngle, targetAngle, trackSpeed, delta);
        louverPivot.rotation.x = currentLouverAngle;

        // Synchronize Live Angle in UI & SVG Cross-Section
        const angleDeg = Math.round(currentLouverAngle * (180 / Math.PI));
        const badge = document.getElementById("vaneBadge");
        const degText = document.getElementById("louverDegreeText");
        const modeText = document.getElementById("louverModeText");
        const svgBlade = document.getElementById("svgBladePivot");

        if (degText) degText.textContent = `${angleDeg}°`;
        if (svgBlade) {
          // Rotate SVG cross-section blade to match 3D physical angle
          svgBlade.style.transform = `rotate(${angleDeg * 0.65}deg)`;
        }

        if (badge) {
          if (state.power === 0) {
            badge.textContent = "Standby · Parked";
            if (modeText) modeText.textContent = "Off · Docked";
          } else if (state.vane === 0) {
            badge.textContent = `Auto Sweep · ${angleDeg}°${state.hSwing === 1 ? ' · 4-Way' : ''}`;
            if (modeText) modeText.textContent = "Harmonic Sweep";
          } else {
            const stepNames = { 1: "Top Glide", 3: "Room Mid", 5: "Floor Drop" };
            badge.textContent = `${stepNames[state.vane] || 'Fixed'} · ${angleDeg}°${state.hSwing === 1 ? ' · 4-Way' : ''}`;
            if (modeText) modeText.textContent = stepNames[state.vane] || "Fixed Step";
          }
        }
      }

      // 2. Blower Drum Rotation
      if (blowerDrum && state.power === 1) {
        const speeds = [0, 1.4, 2.5, 4.0, 6.2, 9.8, 4.0];
        blowerDrum.rotateX((speeds[state.fan] || 4.0) * delta);
      }

      // 3. 4-Way Synchronized Vertical Vanes (Horizontal Sweep Linkage)
      if (ventVanes.length) {
        const targetHSwing = (state.power === 1 && state.hSwing === 1) ? 1.0 : 0.0;
        currentHSwingAmp = THREE.MathUtils.damp(currentHSwingAmp, targetHSwing, 3.5, delta);
        const sweepAngle = Math.sin(time * 1.5) * 0.44 * currentHSwingAmp;
        currentVaneAngle = sweepAngle;
        ventVanes.forEach((vane, idx) => {
          const divergence = (idx - 6) * 0.012 * currentHSwingAmp;
          vane.rotation.y = sweepAngle + divergence;
        });
      }

      // 4. Airflow Particle Simulation
      if (airflowParticles && particlePositions) {
        const pos = airflowParticles.geometry.attributes.position.array;
        if (state.power === 1) {
          airflowParticles.material.opacity = THREE.MathUtils.lerp(airflowParticles.material.opacity, 0.44, 0.05);

          const speeds = [0, 0.22, 0.34, 0.48, 0.70, 0.98, 0.48];
          const speed = speeds[state.fan] || 0.48;

          for (let i = 0; i < 700; i++) {
            particleLifespans[i] += delta * (0.6 + speed * 0.6);
            if (particleLifespans[i] > 1) resetParticle(i);

            const offset = i * 3;
            pos[offset] += particleVelocities[offset] * delta * 1.6;
            pos[offset + 1] += particleVelocities[offset + 1] * delta;
            pos[offset + 2] += particleVelocities[offset + 2] * delta;
          }
        } else {
          airflowParticles.material.opacity = THREE.MathUtils.lerp(airflowParticles.material.opacity, 0, 0.08);
        }
        airflowParticles.geometry.attributes.position.needsUpdate = true;
      }

      // 5. Smooth Camera Orbit Interpolation
      cameraOrbit.theta += (cameraOrbit.targetTheta - cameraOrbit.theta) * 0.1;
      cameraOrbit.phi += (cameraOrbit.targetPhi - cameraOrbit.phi) * 0.1;
      cameraOrbit.radius += (cameraOrbit.targetRadius - cameraOrbit.radius) * 0.1;

      const sinPhi = Math.sin(cameraOrbit.phi);
      const cosPhi = Math.cos(cameraOrbit.phi);
      camera.position.x = cameraOrbit.target.x + cameraOrbit.radius * sinPhi * Math.sin(cameraOrbit.theta);
      camera.position.y = cameraOrbit.target.y + cameraOrbit.radius * cosPhi;
      camera.position.z = cameraOrbit.target.z + cameraOrbit.radius * sinPhi * Math.cos(cameraOrbit.theta);
      camera.lookAt(cameraOrbit.target);

      renderer.render(scene, camera);
    }

    // =========================================================================
    // CLIMATE CONTROLS & UI RENDERING
    // =========================================================================
    function togglePower() {
      playAudio('click');
      const next = state.power === 1 ? 0 : 1;
      sendCommand({ power: next });
    }

    function adjustTemp(delta) {
      if (state.power === 0) return;
      playAudio('click');
      const next = Math.max(16, Math.min(30, state.targetTemp + delta));
      sendCommand({ targetTemp: next });
    }

    function setMode(m) {
      playAudio('click');
      sendCommand({ mode: m });
    }

    function setFan(f) {
      playAudio('click');
      sendCommand({ fan: f });
    }

    function setVane(v) {
      playAudio('click');
      sendCommand({ vane: v });
    }

    function toggleHSwing() {
      playAudio('click');
      sendCommand({ hSwing: state.hSwing === 1 ? 0 : 1 });
    }

    function setConvertible(c) {
      playAudio('click');
      sendCommand({ convertible: c });
    }

    function toggleFeature(k) {
      playAudio('click');
      if (k === 'turbo') sendCommand({ turbo: state.turbo === 1 ? 0 : 1 });
      if (k === 'eco') sendCommand({ eco: state.eco === 1 ? 0 : 1 });
      if (k === 'sleep') sendCommand({ sleep: state.sleep === 1 ? 0 : 1 });
      if (k === 'light') {
        const next = state.light === 1 ? 0 : 1;
        sendCommand({ light: next });
      }
      if (k === 'c1') {
        const next = state.c1Mode === 1 ? 0 : 1;
        if (next === 1) {
          playAudio('beep');
          showToast("Starting C1 Sequence: Setting 17°C High Fan...", "info");
          sendCommand({ c1Mode: 1 });
        } else {
          showToast("C1 Mode cancelled", "info");
          sendCommand({ c1Mode: 0 });
        }
      }
    }

    function renderUI() {
      // Power button & Capsule
      const pwrBtn = document.getElementById("mainPowerBtn");
      const pwrText = document.getElementById("powerBtnText");
      const dockPwr = document.getElementById("dockPower");
      const hero = document.getElementById("heroCard");
      const deltaBadge = document.getElementById("climateDeltaBadge");

      if (state.power === 1) {
        pwrBtn.classList.add("on");
        pwrText.textContent = "System Running";
        if (dockPwr) dockPwr.classList.add("on");
        hero.style.opacity = "1";

        const diff = Number((state.roomTemp - state.targetTemp).toFixed(1));
        if (Math.abs(diff) <= 0.5) deltaBadge.textContent = "Balanced Comfort";
        else if (diff > 0) deltaBadge.textContent = `↓ ${diff.toFixed(1)}° Cooling to Target`;
        else deltaBadge.textContent = `↑ ${Math.abs(diff).toFixed(1)}° Ambient Warmer`;
      } else {
        pwrBtn.classList.remove("on");
        pwrText.textContent = "System Standby";
        if (dockPwr) dockPwr.classList.remove("on");
        hero.style.opacity = "0.72";
        deltaBadge.textContent = "System in Standby";
      }

      // Target temperature numbers
      document.getElementById("targetTempNum").textContent = Math.round(state.targetTemp);
      document.getElementById("ambientReadout").textContent = `${state.roomTemp.toFixed(1)}°C`;
      const dockTemp = document.getElementById("dockTemp");
      if (dockTemp) dockTemp.textContent = `${Math.round(state.targetTemp)}°C`;

      // Dial SVG progress arc calculation
      const circ = 2 * Math.PI * 72;
      const norm = Math.max(0, Math.min(1, (state.targetTemp - 16) / 14));
      const visibleArc = 26 + norm * 312;
      const dialBar = document.getElementById("dialBar");
      const dialGlow = document.getElementById("dialGlow");
      if (dialBar) dialBar.style.strokeDashoffset = String(circ - visibleArc);
      if (dialGlow) dialGlow.style.strokeDashoffset = String(circ - visibleArc);

      // Modes
      const modeNames = ["", "Cooling", "Dry", "Fan Only", "Auto"];
      document.getElementById("modeBadge").textContent = modeNames[state.mode] || "Cooling";
      const dockMode = document.getElementById("dockMode");
      if (dockMode) dockMode.textContent = modeNames[state.mode] || "Cooling";
      for (let i = 1; i <= 4; i++) {
        const el = document.getElementById(`modeBtn${i}`);
        if (el) el.classList.toggle("active", state.mode === i);
      }

      // Fan Speeds
      const fanNames = ["", "Quiet", "Low", "Medium", "High", "Turbo", "Auto"];
      document.getElementById("fanBadge").textContent = fanNames[state.fan] || "High";
      for (let i = 1; i <= 6; i++) {
        const el = document.getElementById(`fanBtn${i}`);
        if (el) el.classList.toggle("active", state.fan === i);
      }

      // Louver Pills
      [0, 1, 3, 5].forEach(v => {
        const el = document.getElementById(`vaneBtn${v}`);
        if (el) el.classList.toggle("active", state.vane === v);
      });
      const hBtn = document.getElementById("hSwingBtn");
      if (hBtn) hBtn.classList.toggle("active", state.hSwing === 1);

      // Convertible
      const convNames = ["", "100% · Full Ton", "80% · Smart", "60% · Eco", "40% · Max Eco"];
      document.getElementById("convBadge").textContent = convNames[state.convertible] || "100%";
      for (let i = 1; i <= 4; i++) {
        const el = document.getElementById(`convBtn${i}`);
        if (el) el.classList.toggle("active", state.convertible === i);
      }

      // Features
      const feats = [
        ["cardTurbo", state.turbo],
        ["cardEco", state.eco],
        ["cardSleep", state.sleep],
        ["cardLight", state.light],
        ["cardC1", state.c1Mode]
      ];
      feats.forEach(([id, val]) => {
        const row = document.getElementById(id);
        if (row) row.classList.toggle("on", val === 1);
      });

      // Telemetry
      document.getElementById("compHzVal").textContent = `${state.compHz} Hz`;
      document.getElementById("coilTempVal").textContent = `${state.coilTemp.toFixed(1)}°C`;
      document.getElementById("compHoursVal").textContent = `${state.compHours} h`;
      document.getElementById("filterConditionVal").textContent = state.filterAlert === 1 ? "Check Filter" : "Clean";
      document.getElementById("filterConditionVal").className = `tel-value ${state.filterAlert === 1 ? 'warn' : 'live'}`;

      updateFrontLedTexture();
    }

    // =========================================================================
    // MQTT & LOCAL DEMO BRIDGE
    // =========================================================================
    let mqttClient = null;

    function sendCommand(cmd) {
      Object.assign(state, cmd);
      renderUI();

      if (mqttClient && mqttClient.connected) {
        mqttClient.publish("megmeet/set", JSON.stringify(cmd), { qos: 1 });
      }
    }

    function initMqtt() {
      try {
        const broker = localStorage.getItem("mqtt_broker") || "io.adafruit.com";
        const port = localStorage.getItem("mqtt_port") || 443;
        const user = localStorage.getItem("mqtt_user") || "";
        const pass = localStorage.getItem("mqtt_pass") || "";

        if (!user || !pass) {
          document.getElementById("connStatusText").textContent = "Local Twin";
          return;
        }

        const url = `wss://${broker}:${port}/mqtt`;
        mqttClient = mqtt.connect(url, {
          username: user,
          password: pass,
          clean: true,
          connectTimeout: 5000,
          reconnectPeriod: 6000
        });

        mqttClient.on('connect', () => {
          document.getElementById("connStatusText").textContent = "Live Cloud";
          showToast("Connected to Blue Star Cloud", "success");
          mqttClient.subscribe("megmeet/state");
          mqttClient.subscribe("megmeet/diagnostics");
        });

        mqttClient.on('message', (topic, payload) => {
          try {
            const data = JSON.parse(payload.toString());
            Object.assign(state, data);
            renderUI();
          } catch (e) {}
        });

        mqttClient.on('error', () => {
          document.getElementById("connStatusText").textContent = "Offline Demo";
        });
      } catch (e) {
        document.getElementById("connStatusText").textContent = "Offline Demo";
      }
    }

    // Theme Management
    function currentTheme() {
      return document.documentElement.dataset.theme === "light" ? "light" : "dark";
    }

    function setTheme(th) {
      document.documentElement.dataset.theme = th;
      localStorage.setItem("bluestar_theme", th);
      const isLight = th === "light";
      if (scene && scene.fog) scene.fog.color.set(isLight ? 0xf7f9fc : 0x08090d);
      if (renderer) renderer.toneMappingExposure = isLight ? 1.02 : 0.96;
      if (airflowParticles) {
        airflowParticles.material.color.set(isLight ? 0x0066cc : 0x38bdf8);
        airflowParticles.material.blending = isLight ? THREE.NormalBlending : THREE.AdditiveBlending;
        airflowParticles.material.needsUpdate = true;
      }
      updateFrontLedTexture();
    }

    function toggleTheme() {
      playAudio('click');
      setTheme(currentTheme() === "light" ? "dark" : "light");
    }

    // Modal
    function openConfigModal() {
      playAudio('click');
      document.getElementById("cfgModal").classList.add("open");
    }
    function closeConfigModal() {
      playAudio('click');
      document.getElementById("cfgModal").classList.remove("open");
    }
    function saveMqttConfig() {
      playAudio('chime');
      closeConfigModal();
    }

    // App Initialization
    window.addEventListener("DOMContentLoaded", () => {
      init3D();
      initMqtt();
      renderUI();
    });
  </script>
</body>
</html>
'''

with open('web-dashboard/redesign.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('redesign.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Redesign HTML successfully written to both locations!")
