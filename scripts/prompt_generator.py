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
}

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

# --- COMPOSITION GUARDRAILS (injected into EVERY prompt) ---
COMPOSITION_RULES = (
    "1) DEVICE SIZING (CRITICAL): The device must fill approximately 55-60% of the total screenshot HEIGHT "
    "and approximately 90% of the total screenshot WIDTH. The device is the hero subject — it must be prominent and large, nearly edge-to-edge horizontally. "
    "Leave a 20-25% text zone at the top or bottom for the headline. "
    "The remaining space is clean breathing room around the device. "
    "2) TEXT PLACEMENT: The headline text MUST be placed ABOVE the device (in the top 20-25% of the image) "
    "or BELOW the device (in the bottom 20-25% of the image). "
    "The text must NEVER overlap, cover, or obstruct ANY part of the device screen or the app UI. "
    "The headline should be on the background area only. "
    "3) CLEAN BACKGROUND: The background should be clean and minimal. "
    "No random floating objects, no scattered icons, no emojis, no trophies unless the style explicitly calls for them. "
    "The focus is: background + device + headline text. Nothing else. "
    "4) MATERIALITY (CRITICAL): Every surface must have a defined texture (glass, metal, plastic, liquid). "
    "NOTHING should look flat or unrendered. All materials must react to light."
)

# --- STYLE PROMPTS (detailed, opinionated, bulletproof) ---
# Each style avoids hardcoded colors — uses relative color descriptions so --app-colors override works cleanly.
STYLES = {
    "glassmorphism": (
        "STYLE: Premium Prismatic Glassmorphism. "
        "BACKGROUND: A deep, rich two-tone gradient with 'multi-layered glass' depth, "
        "transitioning from a dark saturated tone to a lighter complementary tone via soft, high-bit-depth gradients. "
        "GLASS PANELS: 1-2 large frosted glass panels BEHIND the device creating parallax depth. "
        "Glass properties: 'dispersion', 'chromatic aberration at edges', 'caustics', "
        "'frosted borosilicate glass with 40% opacity'. The edges catch light as bright edge highlights. "
        "LIGHTING: Three-point studio lighting — key light at top-right, fill light at bottom-left, "
        "rim light behind device. Soft 'subsurface scattering' through glass elements. "
        "Shot from a 35mm lens at f/2.8, shallow depth of field on the glass panels. "
        "SHADOWS: Soft contact shadow beneath the device, ambient occlusion where glass meets background. "
        "VIBE: Crystal clear, expensive, high-tech, breathable. Like a flagship product launch."
    ),
    "minimalist": (
        "STYLE: Satin Minimalist Luxury. "
        "BACKGROUND: A single solid 'satin finish' surface with subtle tonal variation from center "
        "to edges (vignette). The surface has a visible 'soft-touch matte' grain texture. "
        "DEVICE FRAME: Matte ceramic or clay-rendered frame with precise 'ambient occlusion' at the edges. "
        "LIGHTING: Global illumination (GI) soft box lighting from overhead — even, diffused, no harsh shadows. "
        "A subtle gradient of light falling off toward the bottom of the image. "
        "Shot with a 50mm prime lens at f/4, centered composition with mathematical precision. "
        "SHADOWS: Precise, soft contact shadow directly beneath the device. No other shadows in the scene. "
        "TYPOGRAPHY: Bold, Swiss-style grotesque typography (like Helvetica Neue or SF Pro) in a contrasting tone. "
        "VIBE: Apple Store display table, unboxing experience, museum exhibition. Restrained and confident."
    ),
    "dark_futuristic": (
        "STYLE: Cyber-Gloss / High-Tech. "
        "BACKGROUND: Deepest matte black (#050505) surface with a 'wet floor' mirror reflection beneath "
        "the device. Subtle scan-line or grid pattern at 5% opacity in the far background. "
        "ACCENTS: Two thin neon LED accent strips (one on each side of the device) reflecting on the "
        "wet floor surface. The neon color should complement the app's palette. "
        "DEVICE FRAME: Glossy black titanium with 'carbon fiber weave' texture on the back. "
        "The screen emits a soft volumetric glow ('screen space global illumination') illuminating nearby surfaces. "
        "LIGHTING: Dramatic 'ray-traced reflections' and subtle 'volumetric fog' haze. "
        "A single hard rim light from behind creates a bright edge outline on the device. "
        "Shot with a 24mm wide-angle lens at f/1.8 with cinematic anamorphic lens flare. "
        "SHADOWS: Sharp, defined reflection on the wet floor. No soft shadows — everything is hard-edged. "
        "VIBE: Blade Runner 2049, high-performance, cyberpunk control room."
    ),
    "3d_playful": (
        "STYLE: Vinyl Toy 3D / Pixar Render. "
        "BACKGROUND: Smooth, soft two-tone pastel gradient. Clean and uncluttered. "
        "ELEMENTS: 2-3 small 'blind box' style 3D icons floating near (but NOT overlapping) the device. "
        "Material: 'Glossy ABS plastic' with visible specular highlights, 'subsurface scattering (SSS)', "
        "'soft matte rubber' finish on some elements. They look like premium designer collectible toys. "
        "DEVICE FRAME: Soft, rounded, clay-like white frame with smooth beveled edges. "
        "LIGHTING: Octane Render / Blender Cycles HDRI studio lighting, bright and evenly lit. "
        "Soft diffused shadows with warm fill. Shot from slightly above at a 15-degree downward angle. "
        "SHADOWS: Soft, rounded contact shadows beneath floating elements. Warm ambient occlusion. "
        "VIBE: Fun, delightful, tactile, squishy. Like opening an expensive toy box."
    ),
    "dark_luxury": (
        "STYLE: Obsidian & Accent / Black Tie. "
        "BACKGROUND: 'Piano black' high-gloss finish with a single sweeping highlight curve across "
        "the upper third. The surface is so reflective it mirrors the device faintly. "
        "ACCENTS: Metallic accent highlights — 'brushed metal' or 'polished brass' rim light. "
        "A thin accent-colored line or geometric shape as a subtle background element. "
        "DEVICE FRAME: 'Anisotropic brushed' dark titanium or ceramic black. Premium material render. "
        "LIGHTING: Dramalit product photography. Single hard key light from top-right creating a "
        "dramatic chiaroscuro effect. Sharp, defined rim lights outlining the device edges. "
        "Shot with an 85mm portrait lens at f/2.0 for creamy background separation. "
        "SHADOWS: Sharp, dramatic. High contrast between light and shadow areas. "
        "VIBE: Credit card commercial, luxury watch advertisement, exclusive invitation."
    ),
    "ethereal_bokeh": (
        "STYLE: Ethereal Bokeh / Dreamscape. "
        "BACKGROUND: Abstract 'depth of field' particle field. Hundreds of tiny floating dust motes, "
        "sparkles, and soft orbs of light at varying distances from the camera, creating natural bokeh circles. "
        "The particles are scattered across a smooth gradient void. "
        "LIGHTING: Extremely soft focus with heavy 'bloom' effect on highlights. Overexposed light sources "
        "create halation. Backlit particles glow with rim light. The entire scene feels like it's shot "
        "through gauze or a pro-mist filter. "
        "Shot with a 135mm telephoto lens at f/1.4 — maximum bokeh, minimum depth of field. "
        "DEVICE FRAME: Clean, semi-transparent frame edges that catch and refract the particle light. "
        "SHADOWS: Very soft, almost imperceptible. The device appears to float in the luminous void. "
        "VIBE: Magical, spiritual, meditative, ASMR visual. Like a dream you don't want to wake from."
    ),
    "aurora_gradient": (
        "STYLE: Aurora Mesh Gradient. "
        "BACKGROUND: Flowing, organic multi-color mesh gradient covering the entire background. "
        "The colors blend like the Northern Lights — smooth, continuous, and luminous. "
        "The gradient has visible 'grain texture' at 3% opacity for analog warmth. "
        "No sharp edges between colors — everything flows and breathes. "
        "LIGHTING: The gradient itself IS the light source. Brighter areas of the gradient "
        "illuminate the device from different angles, creating colorful reflected highlights on "
        "the device frame. Soft ambient lighting only. "
        "Shot with a 50mm lens at f/2.8. Clean, modern composition. "
        "DEVICE FRAME: Polished neutral frame (silver or space grey) that picks up colorful "
        "reflections from the gradient background. "
        "SHADOWS: Soft, colorful contact shadow beneath the device that picks up gradient hues. "
        "VIBE: macOS Sonoma, iOS 18 wallpaper, Spotify Wrapped. Modern, fresh, alive, premium."
    ),
    "neumorphism": (
        "STYLE: Neumorphism / Soft UI. "
        "BACKGROUND: A single matte surface in a medium-light neutral tone. The surface has "
        "BOTH a subtle 'outer shadow' (dark, bottom-right) and a subtle 'inner highlight' "
        "(bright, top-left) creating the signature embossed/debossed neumorphic effect. "
        "A large soft rounded-rectangle shape is embossed into the background BEHIND the device. "
        "LIGHTING: Perfectly even, diffused top-left light source creating the dual shadow/highlight "
        "effect. No dramatic lighting — everything is soft and systematic. "
        "Shot with a 50mm lens at f/5.6 for deep focus. Everything is sharp. "
        "DEVICE FRAME: Slightly raised from the background with a strong embossed shadow effect, "
        "as if the device is physically pressed into a soft material. "
        "SHADOWS: The signature neumorphic dual-shadow: dark shadow bottom-right, light highlight top-left. "
        "VIBE: Calm, organized, systematic, satisfying. Like a perfectly organized desk."
    ),
    "clay_3d": (
        "STYLE: Matte Clay 3D Mockup. "
        "BACKGROUND: Smooth, matte single-color surface with minimal gradient — almost flat but with "
        "a subtle radial light falloff from center. Clean and distraction-free. "
        "DEVICE FRAME: The device itself is rendered in a 'matte clay' finish — smooth, rounded edges, "
        "no metallic sheen. The clay material absorbs light softly and has visible 'ambient occlusion' "
        "in every crevice. The screen content remains full-color and sharp — ONLY the device body is clay. "
        "LIGHTING: Soft, diffused dome light from above. Even illumination with gentle shadows. "
        "The clay material shows subtle light-to-shadow gradations across curved surfaces. "
        "Shot from slightly above at a 10-degree downward angle with a 35mm lens at f/4. "
        "SHADOWS: Soft, matte contact shadow. No reflections — everything is matte and tactile. "
        "VIBE: Figma mockup, Dribbble showcase, design portfolio. Professional, clean, sophisticated."
    ),
    "duotone": (
        "STYLE: Split Tone / Duotone. "
        "BACKGROUND: The entire background is a bold two-color duotone treatment. One color dominates "
        "the top half, the other dominates the bottom half, meeting in a smooth gradient blend at the "
        "center. Both colors are high-saturation, high-contrast tones from the app's palette. "
        "LIGHTING: Colored lighting that matches the duotone split — the top light source matches the "
        "top color, the bottom fill matches the bottom color. This creates dramatic colored shadows "
        "and highlights on the device frame. "
        "Shot with a 35mm lens at f/2.8. Bold, graphic composition. "
        "DEVICE FRAME: Neutral frame (white or dark) that serves as a canvas for the colored light reflections. "
        "SHADOWS: Colored shadow beneath the device — picking up the bottom half's dominant tone. "
        "VIBE: Spotify, Nike, Adobe. Bold, graphic, editorial, brand-forward. Makes a statement."
    ),
}

QUALITY_BOOSTERS = (
    "Octane Render, Unreal Engine 5 render, global illumination, "
    "ray tracing, 8k resolution, highly detailed, photorealistic, "
    "masterpiece, professional color grading, depth of field, "
    "sharp focus, cinematic lighting, award-winning design"
)


def get_role_and_framing(index, total, arc_name=None):
    """Returns (role, framing_description) for a given screen position."""
    arc = STORY_ARCS.get(arc_name)
    if arc:
        arc_index = (index - 1) % len(arc)
        return arc[arc_index]

    if index == 1:
        return "HERO SHOT", _3D["dual_hero"]
    if index == total:
        return "CALL TO ACTION", _3D["cta"]
    framing_index = (index - 2) % len(DEFAULT_MIDDLE_ROLES)
    return DEFAULT_MIDDLE_ROLES[framing_index]


# --- Android Play Store resolution ---
_ANDROID_PLAYSTORE_RES = ("1080x1920", "1920x1080")

# Android device keys that should use Play Store resolution
_ANDROID_DEVICES = {
    "samsung_s24_ultra", "samsung_s24", "pixel_9_pro", "pixel_9",
    "oneplus_12", "generic_android",
}


def resolve_device(device_key, custom_device_name=None, platform="auto"):
    """Resolves a device key to (display_name, portrait_res, landscape_res).

    For Android devices, portrait resolution is hardcoded to 1080x1920 (Play Store standard).
    """
    if device_key == "custom" and custom_device_name:
        return (custom_device_name, "1080x1920", "1920x1080")

    preset = DEVICE_PRESETS.get(device_key, DEVICE_PRESETS["iphone_16_pro"])
    display_name, res_p, res_l = preset

    # Hardcode Android Play Store resolution
    if device_key in _ANDROID_DEVICES or platform == "play_store":
        res_p, res_l = _ANDROID_PLAYSTORE_RES

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
        if ss_file:
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

        # FULL PROMPT
        full_prompt = (
            f"Image {i} of {count} ({role}). "
            f"{selected_style} "
            f"{color_override}"
            f"{COMPOSITION_RULES} "
            f"QUALITY: {QUALITY_BOOSTERS}. "
            f"ASPECT RATIO: {aspect_ratio} ({resolution}). "
            f"SUBJECT: {visual_focus} "
            f"SEQUENCE: This is screenshot {i} in a {count}-image panoramic sequence. "
            f"Maintain consistent background gradient direction and color palette across all images."
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
    parser.add_argument("--name", required=True, help="App Name")
    parser.add_argument("--category", required=True, help="App Category")
    parser.add_argument("--count", type=int, default=None,
                        help="Number of screenshots (default: number of --screenshots provided)")
    parser.add_argument("--usp", required=True, help="Unique Selling Proposition")
    parser.add_argument("--style", default="glassmorphism",
                        choices=list(STYLES.keys()),
                        help="Visual Style (default: glassmorphism)")
    parser.add_argument("--screenshots", nargs="+",
                        help="User's actual app screenshot file paths")
    parser.add_argument("--headlines", nargs="+",
                        help="Custom headline text per screen")
    parser.add_argument("--aspect-ratio", default="9:16", choices=["9:16", "16:9"],
                        help="Aspect ratio (default: 9:16 portrait)")
    parser.add_argument("--story-arc", default=None,
                        choices=list(STORY_ARCS.keys()),
                        help="Story arc (default: auto)")
    parser.add_argument("--device", default="iphone_16_pro",
                        choices=list(DEVICE_PRESETS.keys()) + ["custom"],
                        help="Device frame to display (default: iphone_16_pro)")
    parser.add_argument("--custom-device-name", default=None,
                        help="Custom device name when --device=custom")
    parser.add_argument("--output-dir", default=".",
                        help="Directory to write prompts.json to (default: current directory)")
    parser.add_argument("--app-colors", default=None,
                        help="App's brand color palette (e.g., 'Navy Blue, Warm Cream, Gold'). "
                             "Overrides the style's default colors to match the app's theme.")
    parser.add_argument("--platform", default="auto",
                        choices=["auto", "play_store", "app_store"],
                        help="Target platform. 'play_store' forces 1080x1920 resolution. "
                             "'auto' detects from device (default: auto).")

    args = parser.parse_args()

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

    output_dir = getattr(args, 'output_dir', '.')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "prompts.json")

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    # --- VERIFICATION TABLE ---
    print(f"\nGenerated {len(result)} prompts → {output_path}")
    print()
    # Calculate column widths
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
