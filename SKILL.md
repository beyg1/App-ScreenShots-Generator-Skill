---
name: app-screenshot-generator
description: Generates high-converting App Store & Google Play screenshots with a focus on storytelling, aesthetics, and consistency. Use this skill when the user wants to create marketing screenshots for their mobile app, needs app store optimization (ASO) assets, wants "Premium", "Prismatic Glass", "Liquid Platinum", or "Vivid Pop" style screenshots, or struggles to get consistent UI across multiple AI-generated images.
---

# App Screenshot Generator

Generate professional App Store and Play Store screenshots using a deterministic prompt engine and sequential image generation.

## Workflow

### Phase 1: Discovery & Strategy

**FIRST RESPONSE RULE**: In your **very first message** to the user, you MUST:
1.  Ask for input assets (or confirm "from scratch" generation).
2.  Ask for app basics (name, category, USP).
3.  Based on the app concept, recommend **2-3 specific visual styles** from the list below that fit best. (Do not dump all available styles at once).
4.  Ask for device selection.

Gather context conversationally. Cover these topics (ideally in ONE prompt):

1.  **Input Assets (CRITICAL)**: Ask the user to upload their *actual* app screenshots (raw UI).
    *   **Image Discovery (NON-NEGOTIABLE)**: The system metadata (`ADDITIONAL_METADATA`) will list uploaded image paths, but these paths may point to a temporary staging location (`tempmediaStorage/`) that is **cleared before you can access it**. You MUST verify by running `list_dir` on the **conversation artifact directory** (`<appDataDir>/brain/<conversation-id>/`) and filtering for image files (`.jpg`, `.png`, `.webp`). The uploaded images will be stored there as `media__*.jpg` or similar.
    *   Count and acknowledge ALL discovered images: "I found N images in the artifact directory."
    *   **Handling Large Batches**: The system can handle ANY number of images (5, 10, 20+). Do not artificially limit the user.
    *   If the count doesn't match what the user described or uploaded, ask them to re-upload any missing images before proceeding.
    *   If images arrive across **multiple user messages**, re-scan the artifact directory after each message to update your image list.
    *   **Do NOT copy uploaded images** into the project directory. Reference them by their absolute paths in the artifact directory. Only *generated* assets belong in the project directory.
    *   **"From Scratch" Mode**: If the user has NO screenshots (no app built yet, concept-only, or wants AI-generated screens), skip step 1.5 and proceed to step 1.6.
1.5 **Image Analysis & Feature Mapping (NON-NEGOTIABLE)**:
    *   View each uploaded image (one at a time) and identify what feature/screen it shows.
    *   Build a mapping table and show it to the user for approval BEFORE generating prompts:
        | # | Filename | Screen Description | Suggested Headline |
        |---|----------|--------------------|--------------------|  
        | 1 | media__001.jpg | Home screen, dark mode | "Your Daily Azkaar" |
        | 2 | media__002.jpg | Collections list | "Your Duas, Organized" |
    *   The number of rows MUST equal the number of uploaded images. **No image may be skipped.**
    *   Headlines must be action-oriented and highlight a specific benefit visible in the screen.
        - **BAD**: "Dashboard", "Settings", "Collections"
        - **GOOD**: "Track Every Prayer", "Customize Your Experience", "Your Duas, Beautifully Organized"
1.6 **"From Scratch" Screen Planning** — *Only when user has NO screenshots*:
    *   Ask the user: How many screens? (default: 5). Which screens to show? The script has auto-suggestions per category if the user isn't sure.
    *   Build a planning table and show it for approval BEFORE generating:
        | # | Screen Description | Suggested Headline |
        |---|--------------------|--------------------|  
        | 1 | Home dashboard with progress, streaks | "Track Your Progress" |
        | 2 | Workout tracking with timer, sets | "Crush Every Workout" |
    *   **IMPORTANT**: This is a TWO-STEP process:
        1. **Step 1 — Mockup Generation**: Use `--mode mockup` to generate raw portrait UI screens (no device frame, no marketing chrome).
        2. **Step 2 — Marketing Generation**: Use the generated mockup images as `--screenshots` inputs to `--mode marketing`.
2.  **App Basics**: Name, Category (e.g., Fitness, Finance, Prayer), and Core Value Prop (USP).
3.  **App Color Palette**:
    *   **When screenshots exist (AUTO-EXTRACTED — DO NOT ASK THE USER)**: Select 1-2 representative screenshots and **view them** using the `view_file` tool to visually identify dominant UI colors. Describe the extracted palette in the feature-mapping table and include it for user confirmation.
    *   **From Scratch (ASK THE USER)**: Ask the user for their preferred color palette / brand colors directly (e.g., "Electric Purple, White, Fresh Green").
    *   This palette is passed via `--app-colors` to ensure screenshots complement the app's brand.
4.  **Device Selection**: Ask the user which device frame to display.
    *   Available presets: `iphone_16_pro`, `iphone_16_pro_max`, `iphone_15_pro`, `iphone_15_pro_max`, `samsung_s24_ultra`, `samsung_s24`, `pixel_9_pro`, `pixel_9`, `oneplus_12`, `generic_android`, `ipad_pro`, `no_device`.
    *   If the user's device is not listed, use `--device custom --custom-device-name "Device Name"`.
    *   **Note for "No Device"**: This mode removes the phone frame entirely. The UI screenshot becomes a floating plane or integrated surface within the scene. Ideal for abstract or highly stylized marketing assets.
5.  **Visual Style**:
    *   Read `references/design_trends_2025.md` to understand all available styles:
        1.  **Prismatic Glassmorphism** (`glassmorphism`) — Frosted glass panels, premium depth. Best for: fintech, productivity, health.
        2.  **Satin Minimalist** (`minimalist`) — Clean matte surfaces, Apple-style. Best for: tools, utilities, developer apps.
        3.  **Cyber-Gloss** (`dark_futuristic`) — Neon on black, wet-floor reflections. Best for: gaming, crypto, tech.
        4.  **Vinyl Toy 3D** (`3d_playful`) — Colorful pastel, Pixar-style. Best for: kids, casual games, social.
        5.  **Obsidian & Accent** (`dark_luxury`) — Piano black, metallic highlights. Best for: fashion, fintech, premium.
        6.  **Ethereal Bokeh** (`ethereal_bokeh`) — Floating particles, dreamy glow. Best for: meditation, prayer, art.
        7.  **Aurora Gradient** (`aurora_gradient`) — Flowing mesh gradients. Best for: any modern app.
        8.  **Neumorphism** (`neumorphism`) — Soft embossed UI. Best for: productivity, dashboards.
        9.  **Matte Clay 3D** (`clay_3d`) — Clay mockup finish. Best for: design portfolios, SaaS.
        10. **Duotone** (`duotone`) — Bold two-color split. Best for: music, fashion, bold brands.
        11. **Immersive Scene** (`immersive_scene`) — Frameless UI floating in a rich 3D environment. Best for: high-concept marketing, storytelling, abstract visuals.
    *   Based on the app's category and UI, **recommend 2-3 styles** with a brief rationale (e.g., "I recommend **Ethereal Bokeh** or **Aurora Gradient** — they match the spiritual, meditative nature of your app").
    *   **Show the remaining options efficiently**: Present the full list of remaining available styles (from `references/design_trends_2025.md`) to the user using a **Markdown Carousel** so they know all their options without overwhelming the chat window.
    *   **Wait for the user to confirm** their style choice before proceeding to Phase 2.
6.  **Narrative**: Consult `references/story_arcs.md` to pick a structure.
    *   Options: `feature_dive`, `lifestyle_flow`, `game_hype`, `ai_magic`.
7.  **Headlines**: If the user provides custom headlines, use them. Otherwise, generate feature-focused marketing copy per screen based on the Image Analysis table (step 1.5). Headlines MUST highlight a specific benefit or feature — never use generic labels.
8.  **Aspect Ratio**: `9:16` (phone, default) or `16:9` (tablet/landscape).

### Phase 2: Prompt Generation

#### Standard Mode (user provided screenshots)

Run the bundled Python script. Pass all collected inputs. **Do NOT hardcode `--count`** — it defaults to the number of uploaded images.

```bash
python3 scripts/prompt_generator.py \
  --name "MyApp" \
  --category "Finance" \
  --usp "AI-powered budgeting" \
  --style "aurora_gradient" \
  --device "samsung_s24_ultra" \
  --screenshots "home.png" "details.png" "profile.png" \
  --headlines "Master Your Money" "Track Every Dollar" "Smart Insights" \
  --aspect-ratio "9:16" \
  --story-arc "feature_dive" \
  --app-colors "Deep Blue, White, Emerald Green" \
  --output-dir ".screenshot-gen-tmp"
```

#### From-Scratch Mode (no user screenshots — TWO STEPS)

**Step 1 — Generate Mockup Screens** (raw portrait app UI):
```bash
python3 scripts/prompt_generator.py \
  --mode mockup \
  --name "FitLife" \
  --category "Health" \
  --usp "AI-powered workout plans" \
  --count 3 \
  --app-colors "Electric Purple, White, Fresh Green" \
  --platform play_store \
  --output-dir ".screenshot-gen-tmp"
```
This generates `mockup_prompts.json`. Use each prompt with `generate_image` (**NO input image**) to produce raw app UI screens. Save the generated images.

**Step 2 — Generate Marketing Screenshots** (use mockups as inputs):
```bash
python3 scripts/prompt_generator.py \
  --mode marketing \
  --name "FitLife" \
  --category "Health" \
  --usp "AI-powered workout plans" \
  --style "aurora_gradient" \
  --device "pixel_9_pro" \
  --screenshots "/path/to/mockup_1.png" "/path/to/mockup_2.png" "/path/to/mockup_3.png" \
  --headlines "Crush Every Workout" "Track Your Progress" "Download Now" \
  --app-colors "Electric Purple, White, Fresh Green" \
  --output-dir ".screenshot-gen-tmp"
```

**Output location**: Set `--output-dir` to `.screenshot-gen-tmp` in the user's project directory. This dedicated temp folder prevents cluttering the root project workspace or the brain artifact directory.

**Post-Script Verification (NON-NEGOTIABLE)**:
*   After running the script, read the **Verification Table** from stdout.
*   Confirm: (a) total count matches the number of uploaded images, (b) each filename maps to the correct headline.
*   If ANY mismatch, fix `--screenshots` / `--headlines` order and re-run.

### Phase 3: Execution Loop

**RATE LIMIT WARNING (CRITICAL)**: Image generation APIs have strict rate limits. You MUST execute generation **one image at a time SEQUENTIALLY**. Do NOT attempt to generate multiple images in parallel. You must wait for the previous `generate_image` call to complete before initiating the next one.

#### Composition Guardrails (NON-NEGOTIABLE)

Every generated image MUST satisfy these rules:

1.  **Device/Content ≥65%**: The device frame (or the UI content in "No Device" mode) fills at least 65% of the total image height. The app interface is the hero — large and prominent.
2.  **Text outside device**: Headline text is ABOVE or BELOW the device frame. It NEVER overlaps, covers, or obstructs the device screen.
3.  **Clean background**: No random floating objects unless the chosen style explicitly includes them (e.g., `3d_playful`).
4.  **Materiality**: Every surface must have a defined texture (glass, metal, plastic, liquid). NOTHING should look flat or unrendered.
5.  **Aspect Ratio & Resolution**: The script automatically injects aspect ratio framing at the START and END of every prompt. The agent does NOT need to manually append an `OUTPUT FORMAT` suffix — it's baked in. If the output is still square, see Troubleshooting.


#### Execution Steps

1.  Use the `prompt` field from the script's JSON output as the prompt.
2.  If `input_file` is not null, pass it as the `ImagePaths` argument to `generate_image`.
3.  Save the generated image using a descriptive `ImageName` (e.g., `appname_screenshot_1_hero`).
4.  **CRITICAL — SAVE TO PROJECT DIRECTORY (NON-NEGOTIABLE)**: The `generate_image` tool saves images to the agent's internal artifact directory (`<appDataDir>/brain/<conversation-id>/`). You MUST move each generated image to the **user's project workspace directory** immediately after generation.
    *   Determine the project directory from the user's workspace URI (visible in `<user_information>`). If multiple workspaces exist, ask the user which one to use.
    *   Create a subfolder called `screenshots/` inside the project directory if it doesn't already exist.
    *   Command: `mkdir -p /path/to/project/screenshots/ && mv /path/to/brain/image.png /path/to/project/screenshots/image.png`
    *   Use clean, numbered filenames: `01_Headline_Name.png`, `02_Headline_Name.png`, etc.
    *   The `.screenshot-gen-tmp` directory and its contents should be deleted after the task is complete to clean up the workspace.
5.  **After generating**: Visually verify the 3 guardrails. If violated, regenerate with explicit corrections appended to the prompt.
6.  Show the first image to the user for style approval before generating the rest.
7.  Generate remaining images, maintaining the SAME style keywords throughout.

### Phase 4: Final Assembly & Export

*   Verify all **final** generated images are saved in the user's **project directory** under `screenshots/`. Run `list_dir` on the `screenshots/` folder to confirm all expected images are present.
*   Verify that `prompts.json` and intermediate files were **NOT** left in the project root or the agent's artifact directory.
*   Verify that the agent's brain/artifact directory does **NOT** contain any final screenshot PNGs — they should all have been moved.
*   Offer to regenerate any specific screen that breaks the visual flow.

## References

*   [Design Trends 2025](references/design_trends_2025.md): Visual styles with concrete prompt templates.
*   [Story Arcs](references/story_arcs.md): Narrative templates for different app categories.

## Troubleshooting

*   **Text overlapping UI**: Append to prompt: "Place the headline text in the TOP 15% of the image, above the device. Do not put any text on the phone screen."
*   **Device too small**: Append to prompt: "Make the phone MUCH LARGER. It should fill 70% of the image height. Zoom in on the device."
*   **Wrong device**: Verify the `--device` flag matches user's request. Use `--custom-device-name` for unlisted devices.
*   **Panoramic mismatch**: Append: "The left edge of this image must seamlessly continue from the right edge of Image N-1."
*   **Can't find uploaded images**: The system metadata paths (e.g., `tempmediaStorage/`) may be stale or cleared. Always run `list_dir` on `<appDataDir>/brain/<conversation-id>/` and look for `media__*.jpg` / `media__*.png` files. These are the user's uploads.
*   **Image count mismatch**: Users may upload images across multiple messages. After each new message with uploads, re-scan the artifact directory to update your image list. Do NOT rely solely on the system metadata count.
