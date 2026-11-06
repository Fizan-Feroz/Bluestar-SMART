# Blue Star Smart Climate — Design System & UI Revamp Spec

Scope: `web-dashboard/index.html` (also mirrored to `dashboard.html`).
Status: Approved direction — minimal, dark + light themes, brand-grade swing animation.

---

## 1. Design principles

1. **The unit is the hero.** The 3D twin owns the left stage. Controls sit quietly on the right and never compete with it.
2. **One value, one place.** Each piece of state (mode, fan, temperature) is shown once, at the control that changes it. Duplicate badges and footer text are removed.
3. **Quiet surfaces.** Flat panels, hairline dividers, no decorative gradients, no glow except on live status.
4. **Calm motion.** Motion explains a change (a louver moves, a value settles). Nothing loops for decoration, except the swing itself, which is the product's signature behaviour.
5. **Readable first.** Minimum body text 13px, controls 13–14px, all text meets WCAG AA contrast in both themes.
6. **Same product, two moods.** Dark is the default "night console". Light is a clean "daylight" version. Layout, spacing and motion are identical; only tokens change.

---

## 2. Colour tokens

Both themes use the same token names. The theme is switched with `html[data-theme="dark" | "light"]`.

| Token | Dark | Light | Use |
|---|---|---|---|
| `--bg` | `#0a0c10` | `#f3f5f8` | Page background |
| `--surface` | `#11151c` | `#ffffff` | Panels, nav |
| `--surface-2` | `#181d26` | `#eef2f6` | Pills, inputs, tracks |
| `--surface-3` | `#202632` | `#e4eaf1` | Pressed / hover fill |
| `--line` | `rgba(255,255,255,.08)` | `rgba(15,23,42,.08)` | Dividers, borders |
| `--line-strong` | `rgba(255,255,255,.16)` | `rgba(15,23,42,.16)` | Focus-adjacent borders |
| `--text` | `#f2f5f9` | `#0e1620` | Primary text (15.9:1 dark / 16.4:1 light) |
| `--text-2` | `#a7b1bf` | `#4a5565` | Secondary labels (≥7:1) |
| `--text-3` | `#7f8a9a` | `#66717f` | Tertiary, hints (≥4.6:1) |
| `--accent` | `#4aa8ea` | `#0b6fc2` | Active state, primary action |
| `--accent-ink` | `#06121d` | `#ffffff` | Text on accent fills |
| `--accent-soft` | `rgba(74,168,234,.14)` | `rgba(11,111,194,.09)` | Active pill background |
| `--live` | `#4ade80` | `#15803d` | Connection live, filter clean |
| `--warn` | `#fbbf24` | `#b45309` | Connecting / syncing |
| `--danger` | `#f87171` | `#b91c1c` | Filter alert, PIN error |

Rules:
- Cyan is no longer a general accent. It is only used by the 3D display and the LED.
- No gradients in UI chrome. The only gradient is the temperature arc, which fades from `--accent` to a lighter tint.

---

## 3. Typography

Families: **Outfit** (display numbers, headings) and **Plus Jakarta Sans** (UI text). Both are already loaded.

| Role | Size / line | Weight | Tracking |
|---|---|---|---|
| Hero temperature | 72 / 72px (desktop), 60 / 60 (mobile) | 500 | −0.04em |
| Screen title (lock, modal) | 22 / 28px | 600 | −0.01em |
| Group title | 13 / 18px | 600 | 0 |
| Body / labels | 13 / 20px | 500 | 0 |
| Control pill | 13 / 18px | 600 | 0 |
| Caption / hint | 12 / 16px | 500 | 0 |
| Telemetry value | 17 / 20px | 500 | −0.01em |
| Telemetry label | 11 / 14px | 500 | 0 |

Rules:
- No uppercase tracked labels anywhere. Sentence case throughout.
- Numbers use `font-variant-numeric: tabular-nums`.

---

## 4. Space, shape, elevation

- Spacing scale (px): 4, 8, 12, 16, 20, 24, 32, 40.
- Radii: pill controls `12px`, panels `20px`, hero `24px`, dock `24px`, dots `999px`.
- Borders: 1px `--line`. No double borders.
- Elevation: one shadow only, used for floating surfaces (dock, modal):
  - dark: `0 24px 64px rgba(0,0,0,.45)`
  - light: `0 20px 48px rgba(15,23,42,.12)`

---

## 5. Layout

### Desktop (≥ 1100px)
- Top bar 64px tall, full width, `--surface`, bottom hairline.
- Body grid: `minmax(0,1fr)` stage + `400px` control panel.
- Stage: unit centred, camera tabs top-left, hint top-right, telemetry as a single row bottom-left.
- Panel: 28px padding, vertical rhythm 28px between groups, scroll inside the panel only.

### Tablet (700–1099px)
- Stage on top at `clamp(340px, 50svh, 520px)`.
- Panel below, single column, max width 560px, centred.

### Phone (< 700px)
- Compact top bar 56px with status dot only.
- Stage ~46svh.
- Panel: 16px side padding, bottom padding reserves space for the dock.
- Bottom dock: floating, 16px inset, safe-area aware.
- The hero −/+ stepper is hidden on phones, because the dock is the single temperature control there.

---

## 6. Components

### 6.1 Top bar
- Left: small brand mark, "Blue Star" (13px, 600), model line (12px, `--text-3`).
- Right: status (dot + word), theme toggle, lock (when unlocked), sound, settings. All icon buttons are 40px circles, transparent, `--surface-2` on hover.
- Status words: `Live`, `Syncing`, `Offline`, `Retrying`.

### 6.2 Theme toggle
- Single icon button. Shows a sun in dark mode and a moon in light mode (the icon shows the mode you will switch to).
- Choice saved in `localStorage` as `bluestar_theme`.
- First visit follows `prefers-color-scheme`.
- Set before first paint with an inline script to avoid a flash.

### 6.3 Camera tabs (stage)
- Text tabs, 13px, `--text-2`. Active tab: `--text` with a 2px accent underline, no fill.
- Hint text at 12px, `--text-3`, top right. Hidden on phones.

### 6.4 Telemetry strip (stage)
- Four values in one row with 1px dividers, no individual boxes.
- Background: `--surface` at 72% with 16px blur, 16px radius, only for legibility over the 3D floor.
- Label 11px `--text-3`, value 17px `--text`.
- Live numbers use `--live` for filter "Clean", `--danger` for "Alert".

### 6.5 Hero thermostat
- No card. The dial sits directly on the panel background.
- Row: power button (left) and room temperature (right).
- Dial: 200px, 6px track in `--line`, 6px arc in the accent gradient, round caps. The arc animates with a 600ms ease-out when the target changes.
- Centre: "Set" caption, large temperature, delta caption (e.g. "3.0° to target").
- Stepper: two 52px outlined circles, −/+, below the dial. Disabled in standby.

### 6.6 Control groups (Mode, Fan, Louver, Capacity)
- Header row: title (left, 13px, `--text`), current value (right, 13px, `--text-2`). Value is the only place the state is written.
- Pill row: equal-width pills, 40px tall, 12px radius, `--surface-2` fill, 1px `--line` border.
- Active pill: `--accent-soft` fill, `--accent` border at 40% opacity, text `--text`. The active state moves with a 220ms slide indicator, not a snap.
- Mode pills carry a 16px icon above the label. Other groups are text only.
- Fan pills: six pills (Quiet, Low, Med, High, Turbo, Auto).
- Louver pills: Swing, Top, Mid, Low, 4-Way.
- Capacity pills: 100%, 80%, 60%, 40%.

### 6.7 Smart features
- A list, not a grid. Rows 56px tall, separated by hairlines.
- Left: 32px icon in a `--surface-2` square. Label 14px, `--text`.
- Right: switch 40×24px. Off: track `--surface-3`, knob `--text-3`. On: track `--accent`, knob `--accent-ink`.
- The whole row is the hit target.

### 6.8 Panel footer
- One line, 12px, `--text-3`: status dot, "Megmeet MD50BS", and sync text.

### 6.9 Mobile dock
- Floating bar at the bottom of the phone: `[ − ]  temperature + mode  [ + ]  [ power ]`.
- Surface: `--surface` at 94%, 16px blur, 24px radius, shadow, 1px `--line`.
- Buttons 44px. Power button uses the accent when on.

### 6.10 Lock screen
- Full-screen background `--bg`. Centred column, max width 320px. No card border.
- Brand mark, title "Enter PIN", four dots, 3×4 keypad with 64px round keys, no fill until pressed.
- Keys: 22px numerals in `--text`. Clear and backspace in `--text-2`.
- "Remember this device" toggle at the bottom.
- Error: dots turn `--danger`, a 6px horizontal shake (respects reduced motion).

### 6.11 Settings sheet
- Bottom sheet on phones, centred dialog on desktop. 20px radius, `--surface`, shadow.
- Title 18px, description 13px `--text-2`.
- Fields 44px tall, `--surface-2`, 1px `--line`, focus ring 2px `--accent` at 40%.
- Buttons: primary solid `--accent` with `--accent-ink` text, secondary outlined.
- "Install app" appears as a full-width outlined button only when the browser offers installation.

---

## 7. Motion

Principles: motion is short, purposeful and interruptible. Everything respects `prefers-reduced-motion`.

| Motion | Duration | Easing | Notes |
|---|---|---|---|
| Pill active indicator | 220ms | `cubic-bezier(.2,.8,.2,1)` | Slides between active pills |
| Dial arc change | 600ms | `cubic-bezier(.2,.8,.2,1)` | On target change |
| Switch knob | 180ms | `cubic-bezier(.2,.8,.2,1)` | — |
| Press feedback | 120ms | `ease-out` | Scale 0.97 |
| Sheet / modal in | 280ms | `cubic-bezier(.2,.8,.2,1)` | Fade + 12px rise |
| Theme change | 240ms | `ease` | Colour tokens only |
| Lock shake | 360ms | `ease-in-out` | Error only |

No looping decorative animation in the UI. The only continuous motion is the airflow and the louver swing in the 3D stage.

---

## 8. Swing animation (3D unit)

This replaces the current sine-based louver motion with physically inspired motion.

### 8.1 Louver (vertical flap)
- Range: closed `0.00 rad`, Top `0.72`, Mid `0.92`, Low `1.10`, auto sweep `0.80 → 1.24`.
- **Auto swing:** the flap moves on a smoothed cycle (`0.5 − 0.5·cos`, then smootherstep). It dwells briefly at each end and moves fastest in the middle, like a real louver. Full cycle ≈ 3.2s.
- **Fixed step:** moves to the target with a critically damped spring (stiffness 60, damping 2·√60 ≈ 15.5). Settles in about 0.5s with no overshoot.
- **Power off:** eases to closed with the same spring.
- Motion is driven by real frame delta, clamped to 50ms so tab switches do not jump.

### 8.2 Horizontal vanes (4-Way)
- 13 vertical vanes, one per slot, each with its own phase offset (`index × 0.42` rad).
- A global envelope `swingAmount` (0 → 1) eases in and out with the spring, so turning 4-Way on or off never pops.
- Vane angle = `envelope × 0.42 × sin(t × 1.5 + index × 0.42)`.

### 8.3 Airflow coupling
- Particle direction follows the flap angle: a more open flap sends air further down and forward.
- Particle emission eases when the power state changes instead of switching on or off.

### 8.4 Reduced motion
- Louver holds at the middle position. Vanes do not oscillate. Particles still stream because they show state.

---

## 9. 3D stage per theme

| Element | Dark | Light |
|---|---|---|
| Fog colour | `#0a0c10` | `#f3f5f8` |
| Floor colour | `#0c1119` | `#dfe6ee` |
| Floor rings | `#2e8db4` @ 20% | `#0b6fc2` @ 14% |
| Particle blending | Additive | Normal |
| Particle colour | Sky / mint / cyan by state | Deeper blue / teal by state |
| Tone-map exposure | 0.9 | 1.0 |

The casing stays white in both themes. It is the product, and it reads cleanly on both backgrounds.

---

## 10. Accessibility

- Every interactive element has a visible focus ring: 2px `--accent`, 3px offset.
- Touch targets ≥ 44px on phones.
- Pills and switches expose `aria-pressed` / `aria-checked`.
- Dial and telemetry update through `aria-live="polite"` regions.
- Colour is never the only signal: active pills also get a weight change and a border.
- The 3D view has a text description, and camera changes are announced.

---

## 11. Verification checklist

Run for both `dark` and `light`:

1. Desktop 1280×800, 1440×900, 1920×1080: no horizontal scroll. The control panel fits fully at 1080px height; on shorter screens (≤900px) it scrolls inside the panel only, and the stage stays fixed.
2. Tablet 1024×1366 and 1100×800.
3. Phones 390×844 and 360×800: dock visible, no overlap with the last control group.
4. Axe WCAG 2.1 AA: 0 violations on dashboard, lock screen and settings sheet.
5. Interactions: temperature, power, mode, fan, louver, 4-Way, capacity, all four features, camera views, sound toggle, lock/unlock, theme toggle.
6. Swing: auto sweep visibly dwells at the ends; fixed steps settle without overshoot; 4-Way eases in and out.
7. Theme persists after reload; no flash of the wrong theme.
8. Reduced motion: no swing oscillation, no shake.

---

## 12. Out of scope

- Changing MQTT topics, PIN hashing, or the ESP32 contract.
- Replacing the 3D model geometry (only materials, lighting and the louver/vane motion change).
- Adding new device features.
