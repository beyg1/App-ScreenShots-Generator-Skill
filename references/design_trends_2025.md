# App Store & Play Store Design Trends (2025)
# PROMPT ENGINEERING REFERENCE — STYLE BIBLE

> **Usage**: Each style section below contains the EXACT prompt fragment injected into `prompt_generator.py`.
> These are not descriptions — they are **production-grade image generation prompts** designed to produce
> consistent, high-quality, commercially viable App Store screenshots.

---

## 📐 Universal Composition Rules

These rules apply to EVERY style. They are non-negotiable.

1.  **Device/Content Size**: The device frame (or floating UI plane) fills ≥65% of the total image height. The phone is the hero subject.
2.  **Text Placement**: Headline text is placed ABOVE or BELOW the device, never overlapping the screen.
3.  **Clean Focus**: Background + device + headline. Minimize distractions.
4.  **3D Perspective**: Every device has a dynamic tilt angle (6-12°) with appropriate shadows. No flat, static framing.
5.  **Brand Colors**: Background and accents always complement the app's UI color palette.

---

## 🎨 Style Prompt Templates

Each style has a concrete prompt fragment embedded in `prompt_generator.py`. Below are the design rationales and tuning guidance.

---

### 1. Premium Prismatic Glassmorphism (`glassmorphism`)

**When to use**: Premium apps, fintech, productivity, health/wellness.

**Prompt fragment** (injected verbatim):
```
STYLE: Premium Prismatic Glassmorphism — a flagship product launch aesthetic.
BACKGROUND: A deep, rich two-tone gradient (e.g., midnight indigo to deep violet, or obsidian to teal), rendered as a smooth, high-bit-depth gradient with zero banding. The gradient transitions from a dark saturated tone at the top to a slightly lighter complementary tone at the bottom.
GLASS PANELS: 1-2 large frosted glass panels BEHIND the device, each at a slight angle to create parallax depth. Glass material properties: 'dispersion' (rainbow edge splitting), 'chromatic aberration' at panel edges, 'caustics' (light bending through glass creating bright patterns on the background), 'frosted borosilicate glass' at 40% opacity. The glass edges catch the key light as sharp, bright edge highlights (like a real glass pane in sunlight).
DEVICE FRAME: Polished titanium or ceramic white frame. The frame has 'anisotropic brushed metal' texture on the sides, catching colored reflections from the glass panels behind it.
LIGHTING: Three-point studio lighting — (1) Key light: top-right at 45°, warm white, casting a defined highlight on the device frame's right edge. (2) Fill light: bottom-left, cool blue-tinted, at 30% intensity. (3) Rim light: directly behind the device, creating a bright halo outline separating it from the background. 'Subsurface scattering' through glass elements creates soft internal glow.
SHADOWS: Soft, multi-layered contact shadow beneath the device — a sharp inner shadow (5px) and a wide diffused outer shadow (40px) at 60% opacity. Ambient occlusion where glass panels meet the background.
CAMERA: 35mm lens at f/2.8, shallow depth of field focused on the device screen. Glass panels slightly out of focus.
VIBE: Crystal clear, expensive, breathable. Like a flagship Apple or Samsung product launch keynote slide.
```

---

### 2. Satin Minimalist Luxury (`minimalist`)

**When to use**: Tools, utilities, developer-focused apps, Apple-style brands.

**Prompt fragment** (injected verbatim):
```
STYLE: Satin Minimalist Luxury — Apple Store display table aesthetic.
BACKGROUND: A single solid 'satin finish' surface in a muted, sophisticated tone (warm off-white, cool light grey, or pale sage). The surface has a visible 'soft-touch matte' grain texture (like premium paper or anodized aluminum). A subtle radial vignette darkens the corners by 15%, drawing the eye to the center. No gradients — the color is flat but textured.
DEVICE FRAME: Matte ceramic or clay-rendered frame. The frame material has precise 'ambient occlusion' at every edge and corner — dark, tight shadows in crevices. The frame color is either pure white or deep space grey, contrasting cleanly with the background.
LIGHTING: Global Illumination (GI) soft box lighting from directly overhead — even, diffused, no harsh shadows. A subtle gradient of light falls off toward the bottom of the image (top is slightly brighter). The device screen is the only source of color in the scene.
SHADOWS: A single, precise, soft contact shadow directly beneath the device — 20px blur, 40% opacity. No other shadows exist in the scene. The shadow is perfectly centered.
TYPOGRAPHY ZONE: The headline text area (top or bottom 20%) uses a bold, Swiss-style grotesque typeface (Helvetica Neue, SF Pro, or Inter) in a high-contrast tone against the background. Large, confident, minimal.
CAMERA: 50mm prime lens at f/4, perfectly centered composition. Mathematical precision. No lens distortion.
VIBE: Apple Store display table. Museum exhibition. Unboxing experience. Restrained confidence.
```

---

### 3. Cyber-Gloss / High-Tech (`dark_futuristic`)

**When to use**: Gaming utilities, crypto, tech-heavy apps.

**Prompt fragment** (injected verbatim):
```
STYLE: Cyber-Gloss / High-Tech — Blade Runner 2049 product photography.
BACKGROUND: Deepest matte black (#050505) surface. A 'wet floor' mirror reflection extends beneath the device, showing a perfect, slightly blurred reflection of the device and neon accents. A subtle scan-line or hexagonal grid pattern at 4% opacity overlays the far background, suggesting a high-tech environment.
NEON ACCENTS: Two thin neon LED accent strips (one on each side of the device, running vertically), 2-3px wide, in a color complementing the app's palette (e.g., electric cyan, hot magenta, or acid green). These strips reflect on the wet floor surface as elongated colored smears.
DEVICE FRAME: Glossy black titanium with 'carbon fiber weave' texture visible on the back edges. The screen emits a soft 'screen space global illumination' — the UI colors bleed onto the immediately surrounding frame, creating a colored glow halo.
LIGHTING: (1) Single hard rim light from directly behind the device — creates a bright white outline on both device edges. (2) Two colored point lights (matching neon accent colors) positioned left and right, casting colored shadows. (3) Volumetric fog haze at 10% opacity in the lower third of the image. 'Ray-traced reflections' on the wet floor.
SHADOWS: Sharp, defined mirror reflection on the wet floor. No soft shadows — everything is hard-edged and precise. The reflection fades out at 60% distance from the device.
CAMERA: 24mm wide-angle lens at f/1.8. Slight barrel distortion. Cinematic anamorphic lens flare from the rim light, stretching horizontally across the image.
VIBE: Blade Runner 2049. High-performance gaming rig. Cyberpunk control room. Premium tech launch.
```

---

### 4. Vinyl Toy 3D / Pixar Render (`3d_playful`)

**When to use**: Kids apps, casual games, social apps.

**Prompt fragment** (injected verbatim):
```
STYLE: Vinyl Toy 3D / Pixar Render — premium designer collectible toy aesthetic.
BACKGROUND: Smooth, soft two-tone pastel gradient (e.g., baby blue to lavender, or peach to mint). The gradient is clean and uncluttered — no texture, no grain. It serves as a clean stage for the 3D elements.
3D ELEMENTS: 2-3 small 'blind box' style 3D icons floating near (but NOT overlapping) the device. These are premium designer collectible toys — think Kaws, Bearbrick, or Sonny Angel style. Material properties: 'Glossy ABS plastic' with sharp specular highlights (a bright white hotspot), 'subsurface scattering (SSS)' making the plastic glow slightly from within, 'soft matte rubber' finish on some elements. They cast soft, rounded contact shadows.
DEVICE FRAME: Soft, rounded, clay-like white frame. The frame has smooth beveled edges with 'ambient occlusion' in the corners. It looks like a premium toy itself.
LIGHTING: Octane Render / Blender Cycles HDRI studio lighting. Bright, evenly lit scene. Soft diffused shadows with a warm fill light from the front. A subtle rim light from behind separates the device from the background. Shot from slightly above at a 15-degree downward angle.
SHADOWS: Soft, rounded contact shadows beneath every floating element. Warm ambient occlusion. The shadows have a slight warm tint matching the background gradient.
CAMERA: 50mm lens at f/3.5, shot from 15° above. Slight downward tilt. Everything in focus.
VIBE: Fun, delightful, tactile, squishy. Like opening an expensive limited-edition toy box. Pixar's 'Toy Story' meets Apple's product photography.
```

---

### 5. Obsidian & Accent / Black Tie (`dark_luxury`)

**When to use**: Premium hardware, fashion, fintech, exclusive services.

**Prompt fragment** (injected verbatim):
```
STYLE: Obsidian & Accent / Black Tie — luxury watch advertisement aesthetic.
BACKGROUND: 'Piano black' high-gloss finish. The surface is so reflective it shows a faint, blurred reflection of the device. A single sweeping highlight curve (like a light streak on a lacquered surface) crosses the upper third of the image diagonally — bright white, 3-4px wide, with a 30px soft glow. This is the only bright element in the background.
ACCENT ELEMENTS: A single thin geometric accent line or shape (e.g., a thin gold or platinum horizontal rule, or a subtle circular arc) in the background, rendered in 'brushed metal' or 'polished brass'. It should be subtle — 20% opacity — suggesting exclusivity without being decorative.
DEVICE FRAME: 'Anisotropic brushed' dark titanium or ceramic black. The brushing direction is horizontal, creating fine parallel lines that catch the rim light as a bright streak. The frame edges are sharp and precise.
LIGHTING: Dramalit product photography. (1) Single hard key light from top-right at 60° — creates a dramatic chiaroscuro effect, illuminating the right side of the device brightly while the left side falls into deep shadow. (2) Sharp, defined rim lights outlining both device edges in bright white. (3) No fill light — the shadows are intentionally deep and dramatic.
SHADOWS: Sharp, dramatic. High contrast between light and shadow. The contact shadow beneath the device is sharp-edged (not soft), suggesting a hard surface.
CAMERA: 85mm portrait lens at f/2.0. Creamy, separated background. Slight upward tilt (shooting from slightly below) to convey power and authority.
VIBE: Credit card commercial. Luxury watch advertisement (Rolex, Patek Philippe). Exclusive invitation. Power and restraint.
```

---

### 6. Ethereal Bokeh / Dreamscape (`ethereal_bokeh`)

**When to use**: Meditation, sleep, prayer, art, creative tools.

**Prompt fragment** (injected verbatim):
```
STYLE: Ethereal Bokeh / Dreamscape — magical, spiritual, meditative aesthetic.
BACKGROUND: Abstract 'depth of field' particle field. Hundreds of tiny floating dust motes, sparkles, and soft orbs of light at varying distances from the camera. The particles are scattered across a smooth gradient void (e.g., deep indigo to soft rose, or midnight blue to warm amber). Near particles are sharp and bright; far particles are large, soft bokeh circles (30-80px diameter) at varying opacities.
PARTICLE DETAIL: Some particles are star-shaped (4-6 point stars with diffraction spikes). Others are perfect circles with a bright center and soft falloff. A few are elongated streaks suggesting motion. The overall density is high but not cluttered — like looking at a starfield through a telephoto lens.
LIGHTING: Extremely soft focus with heavy 'bloom' effect on all highlights. Overexposed light sources create 'halation' — a soft glow that bleeds into surrounding areas. Backlit particles glow with rim light. The entire scene feels like it's shot through gauze or a Tiffen Pro-Mist filter. The device screen is the brightest element in the scene.
DEVICE FRAME: Clean, semi-transparent frame edges that catch and refract the particle light. The frame appears to glow slightly, as if the particles are attracted to it. The frame color is neutral (white or very light grey) to not compete with the particle colors.
SHADOWS: Very soft, almost imperceptible. The device appears to float in the luminous void. A barely-visible soft shadow (5% opacity, 60px blur) suggests grounding.
CAMERA: 135mm telephoto lens at f/1.4 — maximum bokeh, minimum depth of field. Only the device screen is in sharp focus.
VIBE: Magical, spiritual, meditative, ASMR visual. Like a dream you don't want to wake from. Sacred geometry meets luxury product photography.
```

---

### 7. Aurora Mesh Gradient (`aurora_gradient`)

**When to use**: Any app wanting a modern, trendy look. Works universally.

**Prompt fragment** (injected verbatim):
```
STYLE: Aurora Mesh Gradient — macOS Sonoma / iOS 18 / Spotify Wrapped aesthetic.
BACKGROUND: Flowing, organic multi-color mesh gradient covering the entire background. The colors blend like the Northern Lights — smooth, continuous, and luminous. The gradient has at least 4 distinct color zones that blend seamlessly (e.g., deep purple → electric blue → emerald green → warm gold, or crimson → violet → cerulean → mint). The gradient has visible 'grain texture' at 3% opacity for analog warmth — like a high-quality film grain. No sharp edges between colors — everything flows and breathes.
GRADIENT MOVEMENT: The gradient appears to be in motion — the color zones are organic and irregular, not geometric. They suggest fluid dynamics, like ink dropped in water or the aurora borealis. The brightest zone is positioned to backlight the device from behind.
DEVICE FRAME: Polished neutral frame (silver or space grey) that picks up colorful reflections from the gradient background. The frame acts as a mirror, showing distorted reflections of the gradient colors. This makes the device feel integrated into the scene rather than placed on top of it.
LIGHTING: The gradient itself IS the light source. Brighter areas of the gradient illuminate the device from different angles, creating colorful reflected highlights on the device frame. No additional artificial lighting — the scene is lit entirely by the gradient's luminosity.
SHADOWS: Soft, colorful contact shadow beneath the device that picks up gradient hues — not a grey shadow, but a colored one (e.g., if the bottom of the gradient is green, the shadow has a green tint).
CAMERA: 50mm lens at f/2.8. Clean, modern composition. Slight rightward tilt (8°).
VIBE: macOS Sonoma wallpaper. iOS 18 lock screen. Spotify Wrapped. Modern, fresh, alive, premium. The gradient feels alive.
```

---

### 8. Neumorphism / Soft UI (`neumorphism`)

**When to use**: Productivity, utility, dashboard apps.

**Prompt fragment** (injected verbatim):
```
STYLE: Neumorphism / Soft UI — perfectly organized desk aesthetic.
BACKGROUND: A single matte surface in a medium-light neutral tone (e.g., #E0E5EC light grey-blue, or #F0EBE3 warm cream). The surface has BOTH a subtle 'outer shadow' (dark, bottom-right, 20px blur, 30% opacity) and a subtle 'inner highlight' (bright white, top-left, 20px blur, 80% opacity) creating the signature neumorphic embossed/debossed effect. The surface feels like soft silicone or foam — tactile and satisfying.
EMBOSSED SHAPE: A large soft rounded-rectangle shape is embossed into the background BEHIND the device. This shape is the same color as the background but with stronger dual shadows, making it appear raised from the surface. The device sits within or on top of this raised shape.
DEVICE FRAME: The device appears physically pressed into or raised from the soft material. It has a strong neumorphic dual-shadow: (1) Dark shadow bottom-right (15px blur, 40% opacity). (2) Bright highlight top-left (15px blur, 90% opacity). The frame color matches the background tone closely — it's part of the same material.
LIGHTING: Perfectly even, diffused top-left light source at 45°. This single light source creates the dual shadow/highlight effect consistently across all elements. No dramatic lighting — everything is soft, systematic, and calm.
SHADOWS: The signature neumorphic dual-shadow on every element. No colored shadows — everything is monochromatic with the background tone. Shadows are soft and wide, not sharp.
CAMERA: 50mm lens at f/5.6 for deep focus. Everything is sharp. Slight downward tilt (10°) from above.
VIBE: Calm, organized, systematic, satisfying. Like a perfectly organized minimalist desk. ASMR-inducing tidiness.
```

---

### 9. Matte Clay 3D Mockup (`clay_3d`)

**When to use**: Design portfolios, SaaS, sophisticated utility apps.

**Prompt fragment** (injected verbatim):
```
STYLE: Matte Clay 3D Mockup — Figma/Dribbble showcase aesthetic.
BACKGROUND: Smooth, matte single-color surface with minimal gradient — almost flat but with a subtle radial light falloff from center (center is 10% brighter than edges). The background color is a sophisticated muted tone (e.g., dusty rose, sage green, warm taupe, or slate blue) that complements the app's palette. Clean and distraction-free — the background is a stage, not a statement.
DEVICE FRAME: The device body is rendered in a 'matte clay' finish — smooth, rounded edges, zero metallic sheen. The clay material is the same color as the background (or a slightly darker/lighter variant), making the device feel sculpted from the environment. The clay has visible 'ambient occlusion' in every crevice — dark, tight shadows where surfaces meet. The screen content remains full-color and sharp — ONLY the device body is clay. This contrast between the colorful screen and the matte clay body is the key visual tension.
CLAY MATERIAL DETAIL: The clay surface shows subtle light-to-shadow gradations across curved surfaces — the top face of the device is lighter, the sides are mid-tone, the bottom is darkest. No specular highlights — the material is 100% matte.
LIGHTING: Soft, diffused dome light from above. Even illumination with gentle shadows. The clay material shows subtle light-to-shadow gradations. A secondary soft fill light from the front prevents the shadows from being too dark.
SHADOWS: Soft, matte contact shadow. No reflections — everything is matte and tactile. The shadow is wide (50px blur) and low opacity (30%), suggesting the device is floating slightly above the surface.
CAMERA: 35mm lens at f/4, shot from 10° above. Slight rightward tilt (8°). Clean, professional composition.
VIBE: Figma mockup. Dribbble showcase. Design portfolio. Professional, clean, sophisticated. The clay finish makes the device feel like a prototype.
```

---

### 10. Split Tone / Duotone (`duotone`)

**When to use**: Fashion, music, social, bold brand apps.

**Prompt fragment** (injected verbatim):
```
STYLE: Split Tone / Duotone — Spotify / Nike / Adobe editorial aesthetic.
BACKGROUND: The entire background is a bold two-color duotone treatment. One color dominates the top half (e.g., deep crimson, electric blue, or forest green), the other dominates the bottom half (e.g., warm gold, hot pink, or acid yellow). The two colors meet in a smooth gradient blend at the center — a 30% overlap zone where they mix. Both colors are HIGH SATURATION (90%+) and HIGH CONTRAST against each other. The split is not perfectly horizontal — it has a slight diagonal tilt (5-10°) for dynamism.
COLOR INTERACTION: Where the two colors meet, they create a third mixed color zone. This blending zone is the most visually interesting area and should be positioned behind the device.
DEVICE FRAME: Neutral frame (pure white or deep black) that serves as a canvas for the colored light reflections. The frame picks up the color of whichever half it's closest to — the top of the frame has a tint of the top color, the bottom has a tint of the bottom color.
LIGHTING: Colored lighting that matches the duotone split — (1) Top light source matches the top color, casting colored highlights on the top of the device. (2) Bottom fill light matches the bottom color, casting colored shadows upward. This creates dramatic colored shadows and highlights on the device frame. The device appears to be lit by the background itself.
SHADOWS: Colored shadow beneath the device — picking up the bottom half's dominant tone. Not a grey shadow — a fully colored one.
CAMERA: 35mm lens at f/2.8. Bold, graphic composition. The device is centered and large.
VIBE: Spotify campaign. Nike poster. Adobe Creative Cloud. Bold, graphic, editorial, brand-forward. Makes a statement from across the room.
```

---

### 11. Immersive Scene (`immersive_scene`)

**When to use**: High-concept marketing, storytelling, abstract visuals where the "phone" constraint limits creativity.

**Prompt fragment** (injected verbatim):
```
STYLE: Immersive Scene — high-concept marketing, the app as part of a world.
BACKGROUND: A rich, deep 3D environment that directly compliments the app's theme and features. The environment has genuine depth — foreground elements, midground subject, and background atmosphere. Examples: a dark abstract studio with volumetric light shafts for a productivity app; a lush forest floor with dappled light for a nature app; a futuristic lab with holographic displays for a tech app. The background is NOT a gradient — it's a PLACE.
ENVIRONMENT DETAIL: The environment has texture, atmosphere, and storytelling. Surfaces have material properties (wet concrete, polished marble, rough wood, brushed metal). Atmospheric effects are present (volumetric fog, dust particles, light rays, heat shimmer). The lighting in the environment is motivated — there are visible light sources (windows, screens, lamps, neon signs) that explain where the light is coming from.
FRAMELESS UI: NO PHONE FRAME. The app screenshot appears as a high-quality, glowing physical pane of glass or hologram floating in the environment. The pane has: (1) Thickness — visible edge depth of 4-6px. (2) Glass refraction — the edges of the pane slightly distort what's behind them. (3) A subtle glow — the screen content emits light that illuminates nearby surfaces. (4) NO BEZEL — the UI goes edge-to-edge.
3D PROPS: 3D objects relevant to the app's function float or rest near the UI pane, adding context and storytelling. These props are photorealistic and cast real shadows. They interact with the UI pane (e.g., a prop partially behind the pane, partially in front, creating depth).
LIGHTING: Dynamic, cinematic lighting. The glowing UI pane is a light source — it casts the UI's colors onto nearby props and the environment floor. Additional motivated lighting from the environment (e.g., a window casting a shaft of light, a neon sign reflecting on a wet floor). Volumetric fog/rays may be present, catching the light.
SHADOWS: Realistic contact shadows from props and the UI pane onto the environment. The UI pane casts a colored shadow (matching the dominant UI color) onto the floor beneath it.
CAMERA: 35mm lens at f/2.0. The environment background is slightly out of focus (bokeh), keeping the UI pane as the sharp focal point. Shot from eye level or slightly below for a dramatic, immersive perspective.
VIBE: Breaking the fourth wall. The app is not just on a phone — it's part of the world. High-concept marketing. The kind of screenshot that makes you stop scrolling.
```

---

## 📱 Device Framing

The script supports 12 device presets via `--device`:
*   iPhone 16 Pro / Pro Max
*   iPhone 15 Pro / Pro Max
*   Samsung Galaxy S24 Ultra / S24
*   Google Pixel 9 Pro / Pixel 9
*   OnePlus 12
*   Generic Android
*   iPad Pro
*   **No Device** (`no_device`) — Frameless floating UI plane

Use `--device custom --custom-device-name "Your Device"` for unlisted devices.

---

## 🎨 Brand Color Integration

Use `--app-colors "Color1, Color2, Color3"` to override the style's default colors with the app's brand palette. This ensures every screenshot complements the app's UI regardless of style choice.

**How it works**: The color override replaces ALL color references in the style prompt — background gradients, accent colors, rim lights, neon strips, and decorative elements — while preserving the style's lighting, materials, and composition.

---

## 📏 Platform Specifics

### Apple App Store
*   Higher strictness. Focus on UI accuracy.
*   Apple indexes text in screenshots (OCR) — use ASO keywords in headlines.
*   Preferred resolution: 1290x2796 (iPhone 16 Pro Max).

### Google Play Store
*   Moderate strictness. More informative text allowed.
*   "Feature-rich" and "data-heavy" vibes perform well.
*   Required resolution: 1080x1920.

---

## 🔑 Prompt Engineering Principles (for future style additions)

When adding a new style, follow these rules to ensure depth and consistency:

1.  **Name every material**: Don't say "glass" — say "frosted borosilicate glass at 40% opacity with chromatic aberration at edges."
2.  **Specify every light source**: Don't say "good lighting" — say "single hard key light from top-right at 60°, casting a defined shadow to the left."
3.  **Define the camera**: Always specify lens (mm), aperture (f/stop), and angle. This controls depth of field and perspective.
4.  **Describe the shadow**: Every style has a unique shadow character. Define blur radius, opacity, color, and sharpness.
5.  **Give it a cultural reference**: "Blade Runner 2049", "Apple Store", "Dribbble showcase" — these anchor the AI's aesthetic understanding.
6.  **Use material science terms**: SSS (subsurface scattering), ambient occlusion, anisotropic brushing, caustics, halation — these unlock photorealistic rendering.
