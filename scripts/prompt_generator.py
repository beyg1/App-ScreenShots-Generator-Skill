import argparse
import json
import os

# --- DEVICE PRESETS ---
# Maps device keys to (display_name, default_resolution_portrait, default_resolution_landscape).
DEVICE_PRESETS = {
    "iphone_16_pro": ("iPhone 16 Pro", "1290x2796", "2796x1290"),
    "iphone_16_pro_max": ("iPhone 16 Pro Max", "1320x2868", "2868x1320"),
    "iphone_15_pro": ("iPhone 15 Pro", "1179x2556", "2556x1179"),
    "iphone_15_pro_max": ("iPhone 15 Pro Max", "1290x2796", "2796x1290"),
    "samsung_s24_ultra": ("Samsung Galaxy S24 Ultra", "1440x3120", "3120x1440"),
    "samsung_s24": ("Samsung Galaxy S24", "1080x2340", "2340x1080"),
    "pixel_9_pro": ("Google Pixel 9 Pro", "1280x2856", "2856x1280"),
    "pixel_9": ("Google Pixel 9", "1080x2424", "2424x1080"),
    "oneplus_12": ("OnePlus 12", "1440x3168", "3168x1440"),
    "generic_android": ("modern Android smartphone", "1080x2400", "2400x1080"),
    "ipad_pro": ("iPad Pro 12.9-inch", "2048x2732", "2732x2048"),
    "no_device": ("No Device", "1080x1920", "1920x1080"),
}

# --- PLATFORM DETECTION ---
# Maps device keys to their store platform for auto-detection.
_APPLE_DEVICES = {
    "iphone_16_pro", "iphone_16_pro_max",
    "iphone_15_pro", "iphone_15_pro_max",
    "ipad_pro",
}

_ANDROID_DEVICES = {
    "samsung_s24_ultra", "samsung_s24", "pixel_9_pro", "pixel_9",
    "oneplus_12", "generic_android",
}


def detect_platform(device_key, explicit_platform="auto"):
    """Auto-detect target platform from device key.

    Returns 'play_store' or 'app_store'. Defaults to 'play_store'
    when device is 'no_device', 'custom', or unknown.
    """
    if explicit_platform in ("play_store", "app_store"):
        return explicit_platform
    if device_key in _APPLE_DEVICES:
        return "app_store"
    # Default to play_store for Android devices, no_device, custom, and unknowns
    return "play_store"

# --- 3D FRAMING LIBRARY (no flat screens) ---
_3D = {
    "hero":       "floating at a dynamic 8-degree rightward tilt in 3D perspective, casting a soft diffused shadow beneath, as if suspended in mid-air",
    "dual_hero":  "TWO devices side by side: a LARGE foreground device tilted 15 degrees to the left in 3D perspective (occupying 55% of the frame width, positioned left-of-center), and a SMALLER background device upright and slightly behind it (occupying 35% of the frame width, positioned right-of-center, overlapping the foreground device by 15%). Both share a unified shadow beneath them. The foreground device is the primary focus",
    "feature_a":  "angled 12 degrees to the left with dramatic 3D perspective, a sharp contact shadow grounding it, slight reflection on the surface below",
    "feature_b":  "angled 12 degrees to the right with dramatic 3D perspective, a sharp contact shadow grounding it, slight reflection on the surface below",
    "supporting": "tilted 6 degrees to the left with gentle 3D depth, floating with a soft ambient shadow beneath",
    "cta":        "floating at a dynamic 8-degree leftward tilt in 3D perspective, casting a soft diffused shadow beneath, as if suspended in mid-air",
}

# --- STORY ARC DEFINITIONS ---
STORY_ARCS = {
    "feature_dive": [
        ("HERO SHOT", _3D["dual_hero"]),
        ("KEY FEATURE A", _3D["feature_a"]),
        ("KEY FEATURE B", _3D["feature_b"]),
        ("INTEGRATION", _3D["supporting"]),
        ("SOCIAL PROOF + CTA", _3D["cta"]),
    ],
    "lifestyle_flow": [
        ("THE DREAM", _3D["dual_hero"]),
        ("PROBLEM SOLVER", _3D["feature_a"]),
        ("DATA & PROGRESS", _3D["feature_b"]),
        ("COMMUNITY", _3D["supporting"]),
        ("START YOUR JOURNEY", _3D["cta"]),
    ],
    "game_hype": [
        ("KEY ART", _3D["hero"]),
        ("GAMEPLAY ACTION", _3D["feature_a"]),
        ("PROGRESSION & LOOT", _3D["feature_b"]),
        ("MULTIPLAYER", _3D["supporting"]),
        ("PLAY NOW", _3D["cta"]),
    ],
    "ai_magic": [
        ("INPUT → OUTPUT", _3D["hero"]),
        ("VARIETY", _3D["feature_a"]),
        ("ADVANCED CONTROL", _3D["feature_b"]),
        ("USE CASES", _3D["cta"]),
    ],
}

DEFAULT_MIDDLE_ROLES = [
    ("FEATURE HIGHLIGHT", _3D["feature_a"]),
    ("DATA & INSIGHTS", _3D["feature_b"]),
    ("SOCIAL PROOF", _3D["supporting"]),
    ("INTEGRATION", _3D["supporting"]),
    ("PERSONALIZATION", _3D["feature_a"]),
]

# --- ASPECT RATIO FRAMING (PLATFORM-AWARE) ---
#
# STRATEGY: Triple reinforcement — START, MIDDLE, and END of every prompt.
#   1. PREFIX (start)  = Primary control. Declarative, compositional, natural language.
#                        The model pays MOST attention to the first ~100 tokens.
#   2. COMPOSITION_RULES (middle) = Brief inline reminder embedded in guardrails.
#   3. SUFFIX (end)    = Short, punchy NEGATIVE constraints only.
#                        Models also attend to the end (recency effect).
#
# Two platform targets:
#   - Play Store:  9:16 portrait (1080×1920)  — standard Android
#   - App Store:   ~9:19.5 portrait (1320×2868) — bezel-less iPhone 16 Pro Max
#
PLATFORM_AR_FRAMES = {
    "play_store": {
        "portrait": {
            "prefix": "Create a 9:16 portrait image. ",
            "suffix": "",
            "ar_reminder": "",
        },
        "landscape": {
            "prefix": "Create a 16:9 landscape image. ",
            "suffix": "",
            "ar_reminder": "",
        },
    },
    "app_store": {
        "portrait": {
            "prefix": "Create a 9:19.5 portrait image. ",
            "suffix": "",
            "ar_reminder": "",
        },
        "landscape": {
            "prefix": "Create a 19.5:9 landscape image. ",
            "suffix": "",
            "ar_reminder": "",
        },
    },
}


def _get_ar_frame(platform, orientation):
    """Resolve the correct aspect ratio frame for platform + orientation."""
    platform_frames = PLATFORM_AR_FRAMES.get(platform, PLATFORM_AR_FRAMES["play_store"])
    return platform_frames.get(orientation, platform_frames["portrait"])


# --- COMPOSITION GUARDRAILS (injected into EVERY prompt) ---
# NOTE: Rule 5 (aspect ratio reminder) is injected dynamically per-platform.
COMPOSITION_RULES_BASE = (
    "COMPOSITION RULES: "
    "1) DEVICE/CONTENT SIZING (CRITICAL): The device (or floating UI plane) must fill approximately 55-60% of the total screenshot HEIGHT "
    "and approximately 90% of the total screenshot WIDTH. It is the hero subject — large and prominent. "
    "Leave a 20-25% text zone at the top or bottom for the headline. "
    "The remaining space is clean breathing room around the subject. "
    "2) TEXT PLACEMENT: The headline text MUST be placed ABOVE the subject (in the top 20-25% of the image) "
    "or BELOW the subject (in the bottom 20-25% of the image). "
    "The text must NEVER overlap, cover, or obstruct ANY part of the UI screen. "
    "The headline should be on the background area only. "
    "3) CLEAN BACKGROUND: The background should be clean and minimal. "
    "No random floating objects unless the style (e.g. 3d_playful, immersive_scene) explicitly calls for them. "
    "The focus is: background + subject + headline text. "
    "4) MATERIALITY (CRITICAL): Every surface must have a defined texture (glass, metal, plastic, liquid). "
    "NOTHING should look flat or unrendered. All materials must react to light. "
)

# --- STYLE PROMPTS (detailed, opinionated, bulletproof) ---
# Each style avoids hardcoded colors — uses relative color descriptions so --app-colors override works cleanly.
STYLES = {
    "glassmorphism": (
        "STYLE: Premium Prismatic Glassmorphism — a flagship product launch aesthetic. "
        "BACKGROUND: A deep, rich two-tone gradient (e.g., midnight indigo to deep violet, or obsidian to teal), "
        "rendered as a smooth, high-bit-depth gradient with zero banding. Transitions from a dark saturated tone "
        "at the top to a slightly lighter complementary tone at the bottom. "
        "GLASS PANELS: 1-2 large frosted glass panels BEHIND the device, each at a slight angle to create parallax depth. "
        "Glass material properties: 'dispersion' (rainbow edge splitting), 'chromatic aberration' at panel edges, "
        "'caustics' (light bending through glass creating bright patterns on the background), "
        "'frosted borosilicate glass' at 40% opacity. The glass edges catch the key light as sharp, bright edge highlights. "
        "DEVICE FRAME: Polished titanium or ceramic white frame with 'anisotropic brushed metal' texture on the sides, "
        "catching colored reflections from the glass panels behind it. "
        "LIGHTING: Three-point studio lighting — (1) Key light: top-right at 45 degrees, warm white, casting a defined "
        "highlight on the device frame's right edge. (2) Fill light: bottom-left, cool blue-tinted, at 30% intensity. "
        "(3) Rim light: directly behind the device, creating a bright halo outline. "
        "'Subsurface scattering' through glass elements creates soft internal glow. "
        "SHADOWS: Soft, multi-layered contact shadow beneath the device — a sharp inner shadow (5px) and a wide "
        "diffused outer shadow (40px) at 60% opacity. Ambient occlusion where glass panels meet the background. "
        "CAMERA: 35mm lens at f/2.8, shallow depth of field focused on the device screen. Glass panels slightly out of focus. "
        "VIBE: Crystal clear, expensive, breathable. Like a flagship Apple or Samsung product launch keynote slide."
    ),
    "minimalist": (
        "STYLE: Satin Minimalist Luxury — Apple Store display table aesthetic. "
        "BACKGROUND: A single solid 'satin finish' surface in a muted, sophisticated tone (warm off-white, cool light grey, "
        "or pale sage). The surface has a visible 'soft-touch matte' grain texture (like premium paper or anodized aluminum). "
        "A subtle radial vignette darkens the corners by 15%, drawing the eye to the center. No gradients — flat but textured. "
        "DEVICE FRAME: Matte ceramic or clay-rendered frame. The frame material has precise 'ambient occlusion' at every "
        "edge and corner — dark, tight shadows in crevices. Frame color is either pure white or deep space grey. "
        "LIGHTING: Global Illumination (GI) soft box lighting from directly overhead — even, diffused, no harsh shadows. "
        "A subtle gradient of light falls off toward the bottom of the image (top is slightly brighter). "
        "The device screen is the only source of color in the scene. "
        "SHADOWS: A single, precise, soft contact shadow directly beneath the device — 20px blur, 40% opacity. "
        "No other shadows exist in the scene. The shadow is perfectly centered. "
        "TYPOGRAPHY ZONE: The headline text area uses a bold, Swiss-style grotesque typeface (Helvetica Neue, SF Pro, or Inter) "
        "in a high-contrast tone against the background. Large, confident, minimal. "
        "CAMERA: 50mm prime lens at f/4, perfectly centered composition. Mathematical precision. No lens distortion. "
        "VIBE: Apple Store display table. Museum exhibition. Unboxing experience. Restrained confidence."
    ),
    "dark_futuristic": (
        "STYLE: Cyber-Gloss / High-Tech — Blade Runner 2049 product photography. "
        "BACKGROUND: Deepest matte black (#050505) surface. A 'wet floor' mirror reflection extends beneath the device, "
        "showing a perfect, slightly blurred reflection of the device and neon accents. "
        "A subtle hexagonal grid pattern at 4% opacity overlays the far background, suggesting a high-tech environment. "
        "NEON ACCENTS: Two thin neon LED accent strips (one on each side of the device, running vertically), 2-3px wide, "
        "in a color complementing the app's palette (e.g., electric cyan, hot magenta, or acid green). "
        "These strips reflect on the wet floor surface as elongated colored smears. "
        "DEVICE FRAME: Glossy black titanium with 'carbon fiber weave' texture visible on the back edges. "
        "The screen emits 'screen space global illumination' — the UI colors bleed onto the surrounding frame as a colored glow halo. "
        "LIGHTING: (1) Single hard rim light from directly behind the device — creates a bright white outline on both device edges. "
        "(2) Two colored point lights (matching neon accent colors) positioned left and right, casting colored shadows. "
        "(3) Volumetric fog haze at 10% opacity in the lower third. 'Ray-traced reflections' on the wet floor. "
        "SHADOWS: Sharp, defined mirror reflection on the wet floor. No soft shadows — everything is hard-edged and precise. "
        "The reflection fades out at 60% distance from the device. "
        "CAMERA: 24mm wide-angle lens at f/1.8. Slight barrel distortion. Cinematic anamorphic lens flare from the rim light, "
        "stretching horizontally across the image. "
        "VIBE: Blade Runner 2049. High-performance gaming rig. Cyberpunk control room. Premium tech launch."
    ),
    "3d_playful": (
        "STYLE: Vinyl Toy 3D / Pixar Render — premium designer collectible toy aesthetic. "
        "BACKGROUND: Smooth, soft two-tone pastel gradient (e.g., baby blue to lavender, or peach to mint). "
        "The gradient is clean and uncluttered — no texture, no grain. It serves as a clean stage for the 3D elements. "
        "3D ELEMENTS: 2-3 small 'blind box' style 3D icons floating near (but NOT overlapping) the device. "
        "These are premium designer collectible toys — think Kaws, Bearbrick, or Sonny Angel style. "
        "Material properties: 'Glossy ABS plastic' with sharp specular highlights (a bright white hotspot), "
        "'subsurface scattering (SSS)' making the plastic glow slightly from within, "
        "'soft matte rubber' finish on some elements. They cast soft, rounded contact shadows. "
        "DEVICE FRAME: Soft, rounded, clay-like white frame. Smooth beveled edges with 'ambient occlusion' in the corners. "
        "It looks like a premium toy itself. "
        "LIGHTING: Octane Render / Blender Cycles HDRI studio lighting. Bright, evenly lit scene. "
        "Soft diffused shadows with a warm fill light from the front. "
        "A subtle rim light from behind separates the device from the background. Shot from slightly above at a 15-degree downward angle. "
        "SHADOWS: Soft, rounded contact shadows beneath every floating element. Warm ambient occlusion. "
        "The shadows have a slight warm tint matching the background gradient. "
        "CAMERA: 50mm lens at f/3.5, shot from 15 degrees above. Slight downward tilt. Everything in focus. "
        "VIBE: Fun, delightful, tactile, squishy. Like opening an expensive limited-edition toy box. "
        "Pixar's Toy Story meets Apple's product photography."
    ),
    "dark_luxury": (
        "STYLE: Obsidian & Accent / Black Tie — luxury watch advertisement aesthetic. "
        "BACKGROUND: 'Piano black' high-gloss finish. The surface is so reflective it shows a faint, blurred reflection "
        "of the device. A single sweeping highlight curve (like a light streak on a lacquered surface) crosses the upper "
        "third of the image diagonally — bright white, 3-4px wide, with a 30px soft glow. "
        "This is the only bright element in the background. "
        "ACCENT ELEMENTS: A single thin geometric accent line or shape (e.g., a thin gold or platinum horizontal rule, "
        "or a subtle circular arc) in the background, rendered in 'brushed metal' or 'polished brass'. "
        "Subtle — 20% opacity — suggesting exclusivity without being decorative. "
        "DEVICE FRAME: 'Anisotropic brushed' dark titanium or ceramic black. The brushing direction is horizontal, "
        "creating fine parallel lines that catch the rim light as a bright streak. Frame edges are sharp and precise. "
        "LIGHTING: Dramalit product photography. (1) Single hard key light from top-right at 60 degrees — dramatic "
        "chiaroscuro effect, illuminating the right side brightly while the left falls into deep shadow. "
        "(2) Sharp, defined rim lights outlining both device edges in bright white. (3) No fill light — shadows are intentionally deep. "
        "SHADOWS: Sharp, dramatic. High contrast between light and shadow. The contact shadow beneath the device is "
        "sharp-edged (not soft), suggesting a hard surface. "
        "CAMERA: 85mm portrait lens at f/2.0. Slight upward tilt (shooting from slightly below) to convey power and authority. "
        "VIBE: Credit card commercial. Luxury watch advertisement (Rolex, Patek Philippe). Exclusive invitation. Power and restraint."
    ),
    "ethereal_bokeh": (
        "STYLE: Ethereal Bokeh / Dreamscape — magical, spiritual, meditative aesthetic. "
        "BACKGROUND: Abstract 'depth of field' particle field. Hundreds of tiny floating dust motes, sparkles, and soft "
        "orbs of light at varying distances from the camera. Particles scattered across a smooth gradient void "
        "(e.g., deep indigo to soft rose, or midnight blue to warm amber). "
        "Near particles are sharp and bright; far particles are large, soft bokeh circles (30-80px diameter) at varying opacities. "
        "PARTICLE DETAIL: Some particles are star-shaped (4-6 point stars with diffraction spikes). Others are perfect "
        "circles with a bright center and soft falloff. A few are elongated streaks suggesting motion. "
        "The overall density is high but not cluttered — like looking at a starfield through a telephoto lens. "
        "LIGHTING: Extremely soft focus with heavy 'bloom' effect on all highlights. Overexposed light sources create "
        "'halation' — a soft glow that bleeds into surrounding areas. Backlit particles glow with rim light. "
        "The entire scene feels like it's shot through gauze or a Tiffen Pro-Mist filter. "
        "The device screen is the brightest element in the scene. "
        "DEVICE FRAME: Clean, semi-transparent frame edges that catch and refract the particle light. "
        "The frame appears to glow slightly, as if particles are attracted to it. Frame color is neutral (white or very light grey). "
        "SHADOWS: Very soft, almost imperceptible. A barely-visible soft shadow (5% opacity, 60px blur) suggests grounding. "
        "CAMERA: 135mm telephoto lens at f/1.4 — maximum bokeh, minimum depth of field. Only the device screen is sharp. "
        "VIBE: Magical, spiritual, meditative, ASMR visual. Like a dream you don't want to wake from. "
        "Sacred geometry meets luxury product photography."
    ),
    "aurora_gradient": (
        "STYLE: Aurora Mesh Gradient — macOS Sonoma / iOS 18 / Spotify Wrapped aesthetic. "
        "BACKGROUND: Flowing, organic multi-color mesh gradient covering the entire background. "
        "The colors blend like the Northern Lights — smooth, continuous, and luminous. "
        "At least 4 distinct color zones blend seamlessly (e.g., deep purple to electric blue to emerald green to warm gold, "
        "or crimson to violet to cerulean to mint). "
        "The gradient has visible 'grain texture' at 3% opacity for analog warmth — like high-quality film grain. "
        "No sharp edges between colors — everything flows and breathes. "
        "GRADIENT MOVEMENT: The gradient appears to be in motion — color zones are organic and irregular, not geometric. "
        "They suggest fluid dynamics, like ink dropped in water or the aurora borealis. "
        "The brightest zone is positioned to backlight the device from behind. "
        "DEVICE FRAME: Polished neutral frame (silver or space grey) that picks up colorful reflections from the gradient. "
        "The frame acts as a mirror, showing distorted reflections of the gradient colors, making the device feel "
        "integrated into the scene rather than placed on top of it. "
        "LIGHTING: The gradient itself IS the light source. Brighter areas of the gradient illuminate the device from "
        "different angles, creating colorful reflected highlights on the device frame. No additional artificial lighting. "
        "SHADOWS: Soft, colorful contact shadow beneath the device that picks up gradient hues — not a grey shadow, "
        "but a colored one (e.g., if the bottom of the gradient is green, the shadow has a green tint). "
        "CAMERA: 50mm lens at f/2.8. Clean, modern composition. Slight rightward tilt (8 degrees). "
        "VIBE: macOS Sonoma wallpaper. iOS 18 lock screen. Spotify Wrapped. Modern, fresh, alive, premium. The gradient feels alive."
    ),
    "neumorphism": (
        "STYLE: Neumorphism / Soft UI — perfectly organized desk aesthetic. "
        "BACKGROUND: A single matte surface in a medium-light neutral tone (e.g., #E0E5EC light grey-blue, or #F0EBE3 warm cream). "
        "The surface has BOTH a subtle 'outer shadow' (dark, bottom-right, 20px blur, 30% opacity) AND a subtle "
        "'inner highlight' (bright white, top-left, 20px blur, 80% opacity) creating the signature neumorphic "
        "embossed/debossed effect. The surface feels like soft silicone or foam — tactile and satisfying. "
        "EMBOSSED SHAPE: A large soft rounded-rectangle shape is embossed into the background BEHIND the device. "
        "This shape is the same color as the background but with stronger dual shadows, making it appear raised from the surface. "
        "DEVICE FRAME: The device appears physically pressed into or raised from the soft material. "
        "Strong neumorphic dual-shadow: (1) Dark shadow bottom-right (15px blur, 40% opacity). "
        "(2) Bright highlight top-left (15px blur, 90% opacity). The frame color matches the background tone closely. "
        "LIGHTING: Perfectly even, diffused top-left light source at 45 degrees. This single light source creates the "
        "dual shadow/highlight effect consistently across all elements. No dramatic lighting — everything is soft and systematic. "
        "SHADOWS: The signature neumorphic dual-shadow on every element. No colored shadows — monochromatic with the background tone. "
        "Shadows are soft and wide, not sharp. "
        "CAMERA: 50mm lens at f/5.6 for deep focus. Everything is sharp. Slight downward tilt (10 degrees) from above. "
        "VIBE: Calm, organized, systematic, satisfying. Like a perfectly organized minimalist desk. ASMR-inducing tidiness."
    ),
    "clay_3d": (
        "STYLE: Matte Clay 3D Mockup — Figma/Dribbble showcase aesthetic. "
        "BACKGROUND: Smooth, matte single-color surface with minimal gradient — almost flat but with a subtle radial "
        "light falloff from center (center is 10% brighter than edges). The background color is a sophisticated muted tone "
        "(e.g., dusty rose, sage green, warm taupe, or slate blue) that complements the app's palette. "
        "Clean and distraction-free — the background is a stage, not a statement. "
        "DEVICE FRAME: The device body is rendered in a 'matte clay' finish — smooth, rounded edges, zero metallic sheen. "
        "The clay material is the same color as the background (or a slightly darker/lighter variant), making the device "
        "feel sculpted from the environment. The clay has visible 'ambient occlusion' in every crevice — dark, tight shadows "
        "where surfaces meet. The screen content remains full-color and sharp — ONLY the device body is clay. "
        "This contrast between the colorful screen and the matte clay body is the key visual tension. "
        "CLAY MATERIAL DETAIL: The clay surface shows subtle light-to-shadow gradations across curved surfaces — "
        "the top face of the device is lighter, the sides are mid-tone, the bottom is darkest. No specular highlights — 100% matte. "
        "LIGHTING: Soft, diffused dome light from above. Even illumination with gentle shadows. "
        "A secondary soft fill light from the front prevents shadows from being too dark. "
        "SHADOWS: Soft, matte contact shadow. No reflections — everything is matte and tactile. "
        "The shadow is wide (50px blur) and low opacity (30%), suggesting the device is floating slightly above the surface. "
        "CAMERA: 35mm lens at f/4, shot from 10 degrees above. Slight rightward tilt (8 degrees). Clean, professional composition. "
        "VIBE: Figma mockup. Dribbble showcase. Design portfolio. Professional, clean, sophisticated. "
        "The clay finish makes the device feel like a prototype."
    ),
    "duotone": (
        "STYLE: Split Tone / Duotone — Spotify / Nike / Adobe editorial aesthetic. "
        "BACKGROUND: The entire background is a bold two-color duotone treatment. One color dominates the top half "
        "(e.g., deep crimson, electric blue, or forest green), the other dominates the bottom half "
        "(e.g., warm gold, hot pink, or acid yellow). The two colors meet in a smooth gradient blend at the center — "
        "a 30% overlap zone where they mix. Both colors are HIGH SATURATION (90%+) and HIGH CONTRAST against each other. "
        "The split is not perfectly horizontal — it has a slight diagonal tilt (5-10 degrees) for dynamism. "
        "COLOR INTERACTION: Where the two colors meet, they create a third mixed color zone. "
        "This blending zone is the most visually interesting area and should be positioned behind the device. "
        "DEVICE FRAME: Neutral frame (pure white or deep black) that serves as a canvas for the colored light reflections. "
        "The frame picks up the color of whichever half it's closest to — the top of the frame has a tint of the top color, "
        "the bottom has a tint of the bottom color. "
        "LIGHTING: Colored lighting matching the duotone split — (1) Top light source matches the top color, casting colored "
        "highlights on the top of the device. (2) Bottom fill light matches the bottom color, casting colored shadows upward. "
        "The device appears to be lit by the background itself. "
        "SHADOWS: Colored shadow beneath the device — picking up the bottom half's dominant tone. Not a grey shadow — fully colored. "
        "CAMERA: 35mm lens at f/2.8. Bold, graphic composition. The device is centered and large. "
        "VIBE: Spotify campaign. Nike poster. Adobe Creative Cloud. Bold, graphic, editorial, brand-forward. "
        "Makes a statement from across the room."
    ),
    "immersive_scene": (
        "STYLE: Immersive Scene — high-concept marketing, the app as part of a world. "
        "BACKGROUND: A rich, deep 3D environment that directly compliments the app's theme and features. "
        "The environment has genuine depth — foreground elements, midground subject, and background atmosphere. "
        "Examples: a dark abstract studio with volumetric light shafts for a productivity app; "
        "a lush forest floor with dappled light for a nature app; a futuristic lab with holographic displays for a tech app. "
        "The background is NOT a gradient — it's a PLACE. "
        "ENVIRONMENT DETAIL: The environment has texture, atmosphere, and storytelling. "
        "Surfaces have material properties (wet concrete, polished marble, rough wood, brushed metal). "
        "Atmospheric effects are present (volumetric fog, dust particles, light rays, heat shimmer). "
        "The lighting in the environment is motivated — there are visible light sources (windows, screens, lamps, neon signs) "
        "that explain where the light is coming from. "
        "FRAMELESS UI: NO PHONE FRAME. The app screenshot appears as a high-quality, glowing physical pane of glass or "
        "hologram floating in the environment. The pane has: (1) Thickness — visible edge depth of 4-6px. "
        "(2) Glass refraction — the edges of the pane slightly distort what's behind them. "
        "(3) A subtle glow — the screen content emits light that illuminates nearby surfaces. (4) NO BEZEL — the UI goes edge-to-edge. "
        "3D PROPS: 3D objects relevant to the app's function float or rest near the UI pane, adding context and storytelling. "
        "These props are photorealistic and cast real shadows. They interact with the UI pane "
        "(e.g., a prop partially behind the pane, partially in front, creating depth). "
        "LIGHTING: Dynamic, cinematic lighting. The glowing UI pane is a light source — it casts the UI's colors onto nearby "
        "props and the environment floor. Additional motivated lighting from the environment. "
        "Volumetric fog/rays may be present, catching the light. "
        "SHADOWS: Realistic contact shadows from props and the UI pane onto the environment. "
        "The UI pane casts a colored shadow (matching the dominant UI color) onto the floor beneath it. "
        "CAMERA: 35mm lens at f/2.0. The environment background is slightly out of focus (bokeh), keeping the UI pane as "
        "the sharp focal point. Shot from eye level or slightly below for a dramatic, immersive perspective. "
        "VIBE: Breaking the fourth wall. The app is not just on a phone — it's part of the world. "
        "High-concept marketing. The kind of screenshot that makes you stop scrolling."
    ),
}


QUALITY_BOOSTERS = (
    "Octane Render, Unreal Engine 5 render, global illumination, "
    "ray tracing, 8k resolution, highly detailed, photorealistic, "
    "masterpiece, professional color grading, depth of field, "
    "sharp focus, cinematic lighting, award-winning design"
)


# --- SCREEN MOCKUP GENERATION ("from scratch") ---
# When the user has NO screenshots, we first generate realistic app UI mockups.
# These prompts produce raw UI screens (no marketing chrome, no device frames,
# no headlines) that look like real app screenshots. The generated mockups are
# then used as input_file for the marketing screenshot prompts.
#
# Category-to-screen-type mapping provides realistic screen suggestions.
SCREEN_SUGGESTIONS = {
    "Education": [
        "Home dashboard showing learning progress, streaks, and recommended courses",
        "Course content view with lesson cards, video previews, and progress bars",
        "Quiz/Practice screen with interactive coding challenges or quiz questions",
        "Achievement/Leaderboard screen showing badges, rankings, and milestones",
        "Profile screen with learning statistics, completed courses, and certificates",
    ],
    "Finance": [
        "Dashboard with account balance, spending chart, and recent transactions",
        "Transaction list with categories, amounts, and date/time grouping",
        "Budget tracker with category breakdown pie chart and spending limits",
        "Investment portfolio view with stock/crypto charts and gains/losses",
        "Profile with savings goals, credit score, and account settings",
    ],
    "Health": [
        "Dashboard with daily steps, heart rate, calories burned, and sleep score",
        "Workout tracking screen with exercise list, sets, reps, and timer",
        "Nutrition log with meal cards, calorie counter, and macro breakdown",
        "Progress charts showing weight, body measurements over time",
        "Profile screen with health goals, achievements, and connected devices",
    ],
    "Social": [
        "Feed/Timeline showing posts with images, likes, comments, shares",
        "Chat/Messaging view with conversation bubbles and media attachments",
        "Stories/Reels grid with user-generated content thumbnails",
        "Profile page with bio, follower count, photo grid, and highlights",
        "Discover/Explore screen with trending topics and suggested accounts",
    ],
    "Productivity": [
        "Dashboard with today's tasks, calendar events, and quick actions",
        "Task list view with categories, due dates, priorities, and checkboxes",
        "Project board (Kanban style) with columns and draggable cards",
        "Note editor with rich text formatting, checklists, and attachments",
        "Settings screen with theme options, notifications, and integrations",
    ],
    "default": [
        "Home screen / main dashboard showing the app's primary feature",
        "Detail view or content screen with the app's core functionality",
        "List or collection view with items, cards, or entries",
        "User profile or settings screen with account information",
        "Action screen showing a key workflow (e.g., creation, search, or interaction)",
    ],
}


def generate_screen_mockup_prompts(app_name, category, count, usp,
                                    screen_descriptions=None,
                                    app_colors=None, platform="auto",
                                    device="no_device"):
    """Generate prompts for raw app UI screen mockups (no marketing chrome).

    These produce realistic-looking app screenshots that can then be fed
    as input images to generate_prompts() for the marketing treatment.

    Args:
        app_name: Name of the app.
        category: App category.
        count: Number of screens to generate.
        usp: Unique Selling Proposition.
        screen_descriptions: Optional list of screen descriptions.
            If None, auto-generated from SCREEN_SUGGESTIONS by category.
        app_colors: App brand colors.
        platform: Target platform (affects aspect ratio).
        device: Device key (used for platform detection only).

    Returns:
        List of prompt dicts with keys: index, screen_description, prompt.
    """
    # Use provided descriptions or auto-suggest from category
    suggestions = SCREEN_SUGGESTIONS.get(category, SCREEN_SUGGESTIONS["default"])
    if screen_descriptions is None:
        screen_descriptions = []
    # Pad with auto-suggestions if fewer descriptions than count
    while len(screen_descriptions) < count:
        idx = len(screen_descriptions) % len(suggestions)
        screen_descriptions.append(suggestions[idx])

    # Resolve platform for aspect ratio framing
    resolved_platform = detect_platform(device, platform)
    ar_frame = _get_ar_frame(resolved_platform, "portrait")

    # Color directive
    color_directive = ""
    if app_colors:
        color_directive = (
            f"COLOR SCHEME: Use these brand colors throughout the UI: {app_colors}. "
            f"The primary color should be used for buttons, headers, and active elements. "
            f"The secondary color for accents and highlights. White or near-white for backgrounds "
            f"unless the app explicitly uses a dark theme. "
        )

    prompts = []
    for i in range(1, count + 1):
        screen_desc = screen_descriptions[i - 1]

        prompt = (
            f"{ar_frame['prefix']}"
            f"Generate a realistic, production-quality mobile app UI screenshot for '{app_name}' — a {category} app. "
            f"SCREEN: {screen_desc}. "
            f"UI REQUIREMENTS: "
            f"This must look like an ACTUAL app screenshot — NOT a wireframe, NOT a mockup, NOT a design concept. "
            f"Use real-looking UI components: proper navigation bars, tab bars, cards, buttons, text, icons, "
            f"avatars, charts, and spacing that follow modern mobile design guidelines (Material Design or iOS HIG). "
            f"All text must be legible and realistic (not lorem ipsum). Use plausible data, names, and numbers. "
            f"The UI should be polished, pixel-perfect, and look like it belongs in a top-100 {category} app. "
            f"{color_directive}"
            f"CRITICAL COMPOSITION: This is a FULL-SCREEN mobile UI. "
            f"The UI must fill the ENTIRE image from edge to edge — no bezels, no device frame, no background visible. "
            f"Include a status bar at the top (time, battery, signal icons) and a bottom navigation bar. "
            f"The layout must be vertically composed — content flows top to bottom. "
            f"QUALITY: Clean vector rendering, crisp text, sharp icons, anti-aliased edges, "
            f"consistent spacing, professional typography (Inter, SF Pro, or Roboto). "
            f"The overall app USP is: {usp}. "
            f"{ar_frame['suffix']}"
        )

        prompts.append({
            "index": i,
            "screen_description": screen_desc,
            "prompt": prompt,
        })

    return prompts


def get_role_and_framing(index, total, arc_name=None):
    """Returns (role, framing_description) for a given screen position.

    When total <= 3, the hero shot uses single-device 'hero' framing
    instead of 'dual_hero' to avoid rendering two identical planes.
    """
    arc = STORY_ARCS.get(arc_name)
    if arc:
        arc_index = (index - 1) % len(arc)
        role, framing = arc[arc_index]
        # Override dual_hero for small sets even within arcs
        if total <= 3 and framing == _3D["dual_hero"]:
            framing = _3D["hero"]
        return role, framing

    if index == 1:
        # Use single hero for small sets, dual_hero for 4+ screenshots
        if total <= 3:
            return "HERO SHOT", _3D["hero"]
        return "HERO SHOT", _3D["dual_hero"]
    if index == total:
        return "CALL TO ACTION", _3D["cta"]
    framing_index = (index - 2) % len(DEFAULT_MIDDLE_ROLES)
    return DEFAULT_MIDDLE_ROLES[framing_index]


# --- PLATFORM-AWARE RESOLUTIONS ---
_PLAY_STORE_RES = ("1080x1920", "1920x1080")
_APP_STORE_RES = ("1320x2868", "2868x1320")


def resolve_device(device_key, custom_device_name=None, platform="auto"):
    """Resolves a device key to (display_name, portrait_res, landscape_res).

    Resolution is determined by the target platform:
      - play_store: 1080×1920 (9:16)
      - app_store:  1320×2868 (~9:19.5, bezel-less)
    """
    resolved_platform = detect_platform(device_key, platform)

    if device_key == "custom" and custom_device_name:
        display_name = custom_device_name
    else:
        preset = DEVICE_PRESETS.get(device_key, DEVICE_PRESETS["iphone_16_pro"])
        display_name = preset[0]

    # Set resolution based on platform, not device
    if resolved_platform == "app_store":
        res_p, res_l = _APP_STORE_RES
    else:
        res_p, res_l = _PLAY_STORE_RES

    return (display_name, res_p, res_l)


def generate_prompts(app_name, category, count, usp, style_mode="glassmorphism",
                     screenshots=None, headlines=None, aspect_ratio="9:16",
                     story_arc=None, device="iphone_16_pro", custom_device_name=None,
                     app_colors=None, platform="auto"):
    """
    Generates a sequence of prompts for app store screenshots.

    Args:
        app_name: Name of the app.
        category: App category (e.g., "Fitness", "Finance").
        count: Number of screenshots to generate. If None, defaults to len(screenshots).
        usp: Unique Selling Proposition.
        style_mode: Visual style preset key.
        screenshots: List of user-provided screenshot file paths.
        headlines: List of custom headline texts per screen.
        aspect_ratio: "9:16" (portrait) or "16:9" (landscape).
        story_arc: Story arc name.
        device: Device preset key.
        custom_device_name: Custom device name when device="custom".
        app_colors: App's brand color palette (e.g., "Navy Blue, Warm Cream, Gold").
        platform: Target platform — "play_store", "app_store", or "auto" (auto-detect from device).
    """
    if screenshots is None:
        screenshots = []
    if headlines is None:
        headlines = []

    # Auto-set count from screenshots if not explicitly provided
    if count is None:
        count = len(screenshots) if screenshots else 5

    # --- MISMATCH WARNING ---
    if screenshots and count != len(screenshots):
        print(f"\n⚠️  WARNING: count={count} but {len(screenshots)} screenshots provided. "
              f"Some images will NOT be used!\n")
        # Force count to match screenshots so no image is dropped
        count = len(screenshots)

    # --- DEVICE RESOLUTION ---
    device_name, res_portrait, res_landscape = resolve_device(device, custom_device_name, platform)

    if aspect_ratio == "16:9":
        resolution = res_landscape
        orientation = "landscape"
    else:
        resolution = res_portrait
        orientation = "portrait"

    # --- STYLE ---
    selected_style = STYLES.get(style_mode, STYLES["glassmorphism"])

    # --- COLOR OVERRIDE ---
    color_override = ""
    if app_colors:
        color_override = (
            f"COLOR PALETTE OVERRIDE (CRITICAL): Ignore the default colors mentioned in the style above. "
            f"Instead, adapt ALL background gradients, accent colors, rim lights, and decorative elements "
            f"to harmonize with the app's brand colors: {app_colors}. "
            f"The style's lighting, materials, and composition remain the same — only the colors change. "
        )

    # --- HEADLINE DEFAULTS ---
    default_headlines = {
        "HERO SHOT": f"Discover {app_name}",
        "THE DREAM": f"Discover {app_name}",
        "KEY ART": f"Discover {app_name}",
        "INPUT → OUTPUT": f"Discover {app_name}",
        "CALL TO ACTION": "Download Now",
        "SOCIAL PROOF + CTA": "Download Now",
        "START YOUR JOURNEY": "Start Your Journey",
        "PLAY NOW": "Play Now",
    }

    # --- PROMPT GENERATION ---
    prompts = []

    for i in range(1, count + 1):
        role, framing = get_role_and_framing(i, count, story_arc)

        # Determine headline: user-provided > default > generic
        headline = ""
        if headlines and (i - 1) < len(headlines):
            headline = headlines[i - 1]
        else:
            headline = default_headlines.get(role, f"{app_name} — {usp}")

        # Determine screenshot file (1:1 mapping, no cycling)
        ss_file = None
        if screenshots and (i - 1) < len(screenshots):
            ss_file = screenshots[i - 1]

        # BUILD VISUAL FOCUS
        # FULL PROMPT
        if device == "no_device":
             # NO DEVICE / FRAMELESS LOGIC
            visual_focus = (
                f"A frameless, floating UI plane in {orientation} orientation, "
                f"displaying the provided screen content. "
                f"The screen content must EXACTLY match the input reference image. "
                f"Do NOT generate, hallucinate, or invent new UI elements. "
                f"The UI plane is {framing.replace('device', 'UI plane')}. "
                f"The headline text '{headline}' is placed ABOVE or BELOW the UI plane, "
                f"integrated into the scene composition — NOT overlapping the UI content."
            )
        elif ss_file:
            visual_focus = (
                f"A {device_name} device in {orientation} orientation "
                f"displaying the provided input image. "
                f"The screen content must EXACTLY match the input reference image. "
                f"Do NOT generate, hallucinate, or invent new UI elements. "
                f"The device is {framing}. "
                f"The headline text '{headline}' is placed ABOVE or BELOW the device, "
                f"on the background — NOT on the device screen."
            )
        else:
            visual_focus = (
                f"A {device_name} device in {orientation} orientation "
                f"running the {app_name} app. "
                f"The device is {framing}. "
                f"The screen displays content relevant to {category}, showcasing: {usp}. "
                f"The headline text '{headline}' is placed ABOVE or BELOW the device, "
                f"on the background — NOT on the device screen."
            )

        # --- ASPECT RATIO FRAMING (PLATFORM-AWARE) ---
        resolved_platform = detect_platform(device, platform)
        ar_frame = _get_ar_frame(resolved_platform, orientation)
        ar_prefix = ar_frame["prefix"]
        ar_suffix = ar_frame["suffix"]
        ar_reminder = ar_frame["ar_reminder"]
        composition_rules = COMPOSITION_RULES_BASE + ar_reminder

        # FULL PROMPT — Triple reinforcement:
        #   START: ar_prefix (primary control, natural language)
        #   MIDDLE: ar_reminder embedded in composition_rules
        #   END: ar_suffix (short, punchy negatives)
        full_prompt = (
            f"{ar_prefix}"
            f"Image {i} of {count} ({role}). "
            f"{selected_style} "
            f"{color_override}"
            f"{composition_rules} "
            f"QUALITY: {QUALITY_BOOSTERS}. "
            f"SUBJECT: {visual_focus} "
            f"SEQUENCE: This is screenshot {i} in a {count}-image panoramic sequence. "
            f"Maintain consistent background gradient direction and color palette across all images. "
            f"{ar_suffix}"
        )

        prompts.append({
            "index": i,
            "role": role,
            "headline": headline,
            "prompt": full_prompt,
            "input_file": ss_file,
            "device": device_name,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
        })

    return prompts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate App Store Screenshot Prompts")
    parser.add_argument("--mode", default="marketing",
                        choices=["mockup", "marketing"],
                        help="Generation mode: 'mockup' generates raw app UI screens "
                             "(from scratch), 'marketing' generates final store screenshots "
                             "(default: marketing).")
    parser.add_argument("--name", required=True, help="App Name")
    parser.add_argument("--category", required=True, help="App Category")
    parser.add_argument("--count", type=int, default=None,
                        help="Number of screenshots (default: number of --screenshots provided, or 5)")
    parser.add_argument("--usp", required=True, help="Unique Selling Proposition")
    parser.add_argument("--style", default="glassmorphism",
                        choices=list(STYLES.keys()),
                        help="Visual Style — only used in 'marketing' mode (default: glassmorphism)")
    parser.add_argument("--screenshots", nargs="+",
                        help="User's actual app screenshot file paths (marketing mode only)")
    parser.add_argument("--screen-descriptions", nargs="+",
                        help="Screen descriptions for mockup mode (e.g., 'Home dashboard with...'). "
                             "If not provided, auto-generated from --category.")
    parser.add_argument("--headlines", nargs="+",
                        help="Custom headline text per screen (marketing mode only)")
    parser.add_argument("--aspect-ratio", default="9:16", choices=["9:16", "16:9"],
                        help="Aspect ratio (default: 9:16 portrait)")
    parser.add_argument("--story-arc", default=None,
                        choices=list(STORY_ARCS.keys()),
                        help="Story arc — marketing mode only (default: auto)")
    parser.add_argument("--device", default="iphone_16_pro",
                        choices=list(DEVICE_PRESETS.keys()) + ["custom"],
                        help="Device frame to display (default: iphone_16_pro)")
    parser.add_argument("--custom-device-name", default=None,
                        help="Custom device name when --device=custom")
    parser.add_argument("--output-dir", default=".screenshot-gen-tmp",
                        help="Directory to write prompts.json to (default: .screenshot-gen-tmp)")
    parser.add_argument("--app-colors", default=None,
                        help="App's brand color palette (e.g., 'Navy Blue, Warm Cream, Gold').")
    parser.add_argument("--platform", default="auto",
                        choices=["auto", "play_store", "app_store"],
                        help="Target platform. 'play_store' forces 9:16/1080x1920. "
                             "'app_store' forces 9:19.5/1320x2868. "
                             "'auto' detects from device (default: auto).")

    args = parser.parse_args()

    # --- ROUTE TO CORRECT GENERATOR ---
    if args.mode == "mockup":
        result = generate_screen_mockup_prompts(
            app_name=args.name,
            category=args.category,
            count=args.count or 5,
            usp=args.usp,
            screen_descriptions=getattr(args, 'screen_descriptions'),
            app_colors=getattr(args, 'app_colors'),
            platform=args.platform,
            device=args.device,
        )
        output_filename = "mockup_prompts.json"
    else:
        result = generate_prompts(
            app_name=args.name,
            category=args.category,
            count=args.count,
            usp=args.usp,
            style_mode=args.style,
            screenshots=args.screenshots,
            headlines=args.headlines,
            aspect_ratio=getattr(args, 'aspect_ratio'),
            story_arc=getattr(args, 'story_arc'),
            device=args.device,
            custom_device_name=getattr(args, 'custom_device_name'),
            app_colors=getattr(args, 'app_colors'),
            platform=args.platform,
        )
        output_filename = "prompts.json"

    output_dir = getattr(args, 'output_dir', '.')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    # --- VERIFICATION TABLE ---
    print(f"\nGenerated {len(result)} {args.mode} prompts → {output_path}")
    print()

    if args.mode == "mockup":
        # Mockup verification table
        idx_w = max(5, max(len(str(p['index'])) for p in result) + 2)
        desc_w = max(40, max(len(str(p['screen_description'])[:60]) for p in result) + 2)

        header = f"{'Index':<{idx_w}} {'Screen Description':<{desc_w}}"
        sep = '-' * len(header)
        print(sep)
        print(header)
        print(sep)
        for p in result:
            desc = p['screen_description'][:58] + '...' if len(p['screen_description']) > 60 else p['screen_description']
            print(f"{p['index']:<{idx_w}} {desc:<{desc_w}}")
        print(sep)
    else:
        # Marketing verification table
        idx_w = max(5, max(len(str(p['index'])) for p in result) + 2)
        file_w = max(20, max(len(str(p.get('input_file') or 'NONE')) for p in result) + 2)
        head_w = max(28, max(len(str(p['headline'])) for p in result) + 2)
        role_w = max(15, max(len(str(p['role'])) for p in result) + 2)

        header = f"{'Index':<{idx_w}} {'Input File':<{file_w}} {'Headline':<{head_w}} {'Role':<{role_w}}"
        sep = '-' * len(header)
        print(sep)
        print(header)
        print(sep)
        for p in result:
            f_name = p.get('input_file') or 'NONE'
            print(f"{p['index']:<{idx_w}} {f_name:<{file_w}} {p['headline']:<{head_w}} {p['role']:<{role_w}}")
        print(sep)
    print()
