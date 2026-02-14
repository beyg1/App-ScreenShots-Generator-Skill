# App Store & Play Store Design Trends (2025)

## 📐 Universal Composition Rules

These rules apply to EVERY style. They are non-negotiable.

1.  **Device Size**: The device frame fills ≥65% of the total image height. The phone is the hero subject.
2.  **Text Placement**: Headline text is placed ABOVE or BELOW the device, never overlapping the screen.
3.  **Clean Focus**: Background + device + headline. Minimize distractions.
4.  **3D Perspective**: Every device has a dynamic tilt angle (6-12°) with appropriate shadows. No flat, static framing.
5.  **Brand Colors**: Background and accents always complement the app's UI color palette.

---

## 🎨 Style Prompt Templates

Each style has a concrete prompt fragment embedded in `prompt_generator.py`. Below are the design rationales and tuning guidance.

### 1. Premium Prismatic Glassmorphism (`glassmorphism`)

**When to use**: Premium apps, fintech, productivity, health/wellness.

**Key visual rules**:
*   Background: Deep two-tone gradient with frosted glass panels creating parallax depth.
*   Glass: Dispersion, chromatic aberration at edges, caustics, frosted borosilicate at 40% opacity.
*   Lighting: Three-point studio lighting with subsurface scattering through glass.
*   Camera: 35mm at f/2.8, shallow DOF on glass panels.
*   Vibe: Crystal clear, expensive, high-tech, flagship product launch.

### 2. Satin Minimalist Luxury (`minimalist`)

**When to use**: Tools, utilities, developer-focused apps, Apple-style brands.

**Key visual rules**:
*   Background: Single solid satin surface with soft vignette and matte grain texture.
*   Device: Matte ceramic with precise ambient occlusion.
*   Lighting: GI soft box from overhead. Even, diffused, no harsh shadows.
*   Camera: 50mm prime at f/4, mathematical precision.
*   Vibe: Apple Store display, unboxing experience, museum exhibition.

### 3. Cyber-Gloss / High-Tech (`dark_futuristic`)

**When to use**: Gaming utilities, crypto, tech-heavy apps.

**Key visual rules**:
*   Background: Deepest matte black with wet-floor mirror reflections, subtle grid overlay.
*   Accents: Neon LED strips reflecting on wet floor surface.
*   Device: Glossy black titanium with carbon fiber weave.
*   Lighting: Ray-traced reflections, volumetric fog, hard rim light from behind.
*   Camera: 24mm wide-angle at f/1.8 with anamorphic lens flare.
*   Vibe: Blade Runner 2049, cyberpunk control room.

### 4. Vinyl Toy 3D / Pixar Render (`3d_playful`)

**When to use**: Kids apps, casual games, social apps.

**Key visual rules**:
*   Background: Smooth two-tone pastel gradient, clean.
*   Elements: 2-3 premium blind box 3D icons near (not overlapping) device.
*   Materials: Glossy ABS plastic, SSS, soft matte rubber.
*   Lighting: Octane/Cycles HDRI, shot from 15° above.
*   Vibe: Fun, delightful, tactile. Like opening an expensive toy box.

### 5. Obsidian & Accent / Black Tie (`dark_luxury`)

**When to use**: Premium hardware, fashion, fintech, exclusive services.

**Key visual rules**:
*   Background: Piano black high-gloss with sweeping highlight curve.
*   Accents: Metallic brushed metal or polished brass rim light.
*   Device: Anisotropic brushed dark titanium or ceramic black.
*   Lighting: Dramalit product photography. Chiaroscuro. Sharp rim lights.
*   Camera: 85mm portrait lens at f/2.0.
*   Vibe: Credit card commercial, luxury watch, exclusive invitation.

### 6. Ethereal Bokeh / Dreamscape (`ethereal_bokeh`)

**When to use**: Meditation, sleep, prayer, art, creative tools.

**Key visual rules**:
*   Background: Hundreds of floating dust motes and bokeh circles at varying distances.
*   Lighting: Heavy bloom, halation, pro-mist filter effect. Backlit glowing particles.
*   Camera: 135mm telephoto at f/1.4 — maximum bokeh.
*   Device: Semi-transparent frame edges catching particle light.
*   Vibe: Magical, spiritual, meditative, ASMR. A dream you don't want to wake from.

### 7. Aurora Mesh Gradient (`aurora_gradient`) 🆕

**When to use**: Any app wanting a modern, trendy look. Works universally.

**Key visual rules**:
*   Background: Flowing, organic multi-color mesh gradient like Northern Lights. 3% grain texture.
*   Lighting: The gradient IS the light source — colored reflections on device frame.
*   Camera: 50mm at f/2.8, clean modern composition.
*   Device: Polished neutral frame picking up colorful gradient reflections.
*   Vibe: macOS Sonoma, iOS 18, Spotify Wrapped. Modern, fresh, alive.

### 8. Neumorphism / Soft UI (`neumorphism`) 🆕

**When to use**: Productivity, utility, dashboard apps.

**Key visual rules**:
*   Background: Matte neutral surface with dual shadow/highlight embossed effect.
*   Elements: Large embossed rounded-rectangle behind device.
*   Lighting: Even, diffused top-left light. Systematic dual shadows.
*   Camera: 50mm at f/5.6 for deep focus. Everything sharp.
*   Vibe: Calm, organized, systematic, satisfying.

### 9. Matte Clay 3D Mockup (`clay_3d`) 🆕

**When to use**: Design portfolios, SaaS, sophisticated utility apps.

**Key visual rules**:
*   Background: Smooth matte single-color with radial light falloff.
*   Device: Matte clay finish body (screen stays full-color). Ambient occlusion in crevices.
*   Lighting: Soft dome light from above. Even, gentle shadows.
*   Camera: 35mm at f/4, shot from 10° above.
*   Vibe: Figma mockup, Dribbble showcase, design portfolio.

### 10. Split Tone / Duotone (`duotone`) 🆕

**When to use**: Fashion, music, social, bold brand apps.

**Key visual rules**:
*   Background: Bold two-color split — top and bottom, blending at center.
*   Lighting: Colored lighting matching the duotone split for dramatic colored shadows.
*   Camera: 35mm at f/2.8, bold graphic composition.
*   Device: Neutral frame as canvas for colored reflections.
*   Vibe: Spotify, Nike, Adobe. Bold, editorial, brand-forward.

---

## 📱 Device Framing

The script supports 11 device presets via `--device`:
*   iPhone 16 Pro / Pro Max
*   iPhone 15 Pro / Pro Max
*   Samsung Galaxy S24 Ultra / S24
*   Google Pixel 9 Pro / Pixel 9
*   OnePlus 12
*   Generic Android
*   iPad Pro

Use `--device custom --custom-device-name "Your Device"` for unlisted devices.

## 🎨 Brand Color Integration

Use `--app-colors "Color1, Color2, Color3"` to override the style's default colors with the app's brand palette. This ensures every screenshot complements the app's UI regardless of style choice.

## 📏 Platform Specifics

### Apple App Store
*   Higher strictness. Focus on UI accuracy.
*   Apple indexes text in screenshots (OCR) — use ASO keywords in headlines.

### Google Play Store
*   Moderate strictness. More informative text allowed.
*   "Feature-rich" and "data-heavy" vibes perform well.
