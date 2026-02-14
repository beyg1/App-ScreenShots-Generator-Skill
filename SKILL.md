---
name: app-screenshot-generator
description: Generates high-converting App Store & Google Play screenshots with a focus on storytelling, aesthetics, and consistency. Use this skill when the user wants to create marketing screenshots for their mobile app, needs app store optimization (ASO) assets, wants "Premium", "Prismatic Glass", "Liquid Platinum", or "Vivid Pop" style screenshots, or struggles to get consistent UI across multiple AI-generated images.
---

# App Screenshot Generator

Generate professional App Store and Play Store screenshots using a deterministic prompt engine and sequential image generation.

## Workflow

### Phase 1: Discovery & Strategy

Gather context conversationally. Ask these in order:

1.  **Input Assets (CRITICAL)**: Ask the user to upload their *actual* app screenshots (raw UI).
    *   **Image Discovery (NON-NEGOTIABLE)**: The system metadata (`ADDITIONAL_METADATA`) will list uploaded image paths, but these paths may point to a temporary staging location (`tempmediaStorage/`) that is **cleared before you can access it**. You MUST verify by running `list_dir` on the **conversation artifact directory** (`<appDataDir>/brain/<conversation-id>/`) and filtering for image files (`.jpg`, `.png`, `.webp`). The uploaded images will be stored there as `media__*.jpg` or similar.
    *   Count and acknowledge ALL discovered images: "I found N images in the artifact directory."
    *   **Handling Large Batches**: The system can handle ANY number of images (5, 10, 20+). Do not artificially limit the user.
    *   If the count doesn't match what the user described or uploaded, ask them to re-upload any missing images before proceeding.
    *   If images arrive across **multiple user messages**, re-scan the artifact directory after each message to update your image list.
    *   **Do NOT copy uploaded images** into the project directory. Reference them by their absolute paths in the artifact directory. Only *generated* assets belong in the project directory.
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
2.  **App Basics**: Name, Category (e.g., Fitness, Finance, Prayer), and Core Value Prop (USP).
3.  **App Color Palette**: Ask the user for their app's primary color palette (2-3 colors, e.g., "Navy Blue, Warm Cream, Gold").
    *   If not provided, **select 1-2 representative screenshots** (e.g., the Home screen) and examine ONLY those to extract the dominant UI colors. **DO NOT** attempt to analyze all uploaded images at once, as this may exceed tool limits.
    *   This palette is passed via `--app-colors` to ensure screenshots complement the app's brand.
4.  **Device Selection**: Ask the user which device frame to display.
    *   Available presets: `iphone_16_pro`, `iphone_16_pro_max`, `iphone_15_pro`, `iphone_15_pro_max`, `samsung_s24_ultra`, `samsung_s24`, `pixel_9_pro`, `pixel_9`, `oneplus_12`, `generic_android`, `ipad_pro`.
    *   If the user's device is not listed, use `--device custom --custom-device-name "Device Name"`.
5.  **Visual Style**: Consult `references/design_trends_2025.md` to suggest a style.
    *   Options: `glassmorphism`, `minimalist`, `dark_futuristic`, `3d_playful`, `dark_luxury`, `ethereal_bokeh`, `aurora_gradient`, `neumorphism`, `clay_3d`, `duotone`.
6.  **Narrative**: Consult `references/story_arcs.md` to pick a structure.
    *   Options: `feature_dive`, `lifestyle_flow`, `game_hype`, `ai_magic`.
7.  **Headlines**: If the user provides custom headlines, use them. Otherwise, generate feature-focused marketing copy per screen based on the Image Analysis table (step 1.5). Headlines MUST highlight a specific benefit or feature — never use generic labels.
8.  **Aspect Ratio**: `9:16` (phone, default) or `16:9` (tablet/landscape).

### Phase 2: Prompt Generation

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
  --output-dir "/tmp/screenshot_gen_task"
```

**Output location**: Set `--output-dir` to a **temporary directory** (e.g., `/tmp/` or the brain artifact directory). Do **NOT** clutter the user's project workspace with `prompts.json` or intermediate logs.

**Post-Script Verification (NON-NEGOTIABLE)**:
*   After running the script, read the **Verification Table** from stdout.
*   Confirm: (a) total count matches the number of uploaded images, (b) each filename maps to the correct headline.
*   If ANY mismatch, fix `--screenshots` / `--headlines` order and re-run.

### Phase 3: Execution Loop

Execute generation **one image at a time** using the agent's `generate_image` tool.

#### Composition Guardrails (NON-NEGOTIABLE)

Every generated image MUST satisfy these 3 rules:

1.  **Device ≥65%**: The device frame fills at least 65% of the total image height. The phone is the hero — large and prominent.
2.  **Text outside device**: Headline text is ABOVE or BELOW the device frame. It NEVER overlaps, covers, or obstructs the device screen.
3.  **Clean background**: No random floating objects unless the chosen style explicitly includes them (e.g., `3d_playful`).
4.  **Materiality**: Every surface must have a defined texture (glass, metal, plastic, liquid). NOTHING should look flat or unrendered.

#### Execution Steps

1.  Use the `prompt` field from the script's JSON output as the prompt.
2.  If `input_file` is not null, pass it as the `ImagePaths` argument to `generate_image`.
3.  Save the generated image using a descriptive `ImageName` (e.g., `appname_screenshot_1_hero`).
4.  **CRITICAL**: The `generate_image` tool saves to an internal directory. You MUST move it to the user's project directory immediately.
    *   Command: `mv /path/to/internal/brain/image.png /user/project/directory/image.png`
    *   The `prompts.json` file should remain in the temp directory and be deleted after the task is complete.
5.  **After generating**: Visually verify the 3 guardrails. If violated, regenerate with explicit corrections appended to the prompt.
6.  Show the first image to the user for style approval before generating the rest.
7.  Generate remaining images, maintaining the SAME style keywords throughout.

### Phase 4: Final Assembly & Export

*   Verify all **final** generated images are saved in the user's **project directory**.
*   Verify that `prompts.json` and source images were **NOT** left cluttering the project root.
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
