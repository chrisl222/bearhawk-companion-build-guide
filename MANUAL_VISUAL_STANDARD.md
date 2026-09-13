# Companion visual standard · v2

Reference: CTRL001, six steps. Reuse this standard; do not redesign each subassembly.

**Authority.** Geometry and part relationships: official Companion plans → current factory documentation → applicable legacy manuals → builder references. Explicit QB hardware IDs/counts: current Companion count sheet → current factory documentation → plans → legacy → builder references. Keep the QB hardware when another source differs; display **SOURCE CONFLICT — VERIFY** and record the difference for human review. Never invent missing hardware or a critical assembly relationship.

**Palette.** White paper; page ink `#172C3C`; labels blue `#087DB0`; warning labels `#C74A13`; secondary text `#596976`; rules `#D4DDE3`. Blender RGBA: new part `(0.02,0.48,0.72,1)`; installed `(0.55,0.60,0.65,1)`; existing structure `(0.96,0.97,0.98,1)`; hardware `(0.09,0.13,0.17,1)`; arrows `(1,0.28,0.035,1)`. Use spatial separation and outlines as well as color. Existing structure must remain subordinate. No textures or reflective finishes.

**Page.** Landscape 22:15. Logical canvas 2200×1500; export 4400×3000 PNG. Outer margins 65; title band ends at y=215; main view `(35,245,1320,1110)`; divider x=1370; hardware begins `(1410,260)`; detail panel `(1385,690,750,583)`; footer rule y=1400. The detail image is about 28% wider than v1. Do not crop the active joint or its exploded hardware; surrounding tube ends may leave a detail frame.

**Typography.** Arial regular/bold. Logical sizes: step number 82; action title 49; assembly label 25; hardware ID 34 and quantity 35; detail title 28; verify flag 28–40; orientation 28; footer 23. Multiply by two at export. Rule weight 2; orientation shaft 5. Keep labels within their columns. Shared values and drawing helpers live in `scripts/visual_standard.py`.

**Arrows and orientation.** Orange straight cylinder/cone arrows; typical shaft radius 0.10–0.15 illustration units. Point from the exploded part toward its installed position; keep the head visible. Dashed gray lines mark alignment. Opposing arrows mean a conceptual movement check, never verified travel limits. A dark FWD arrow follows the camera's projected aircraft-forward direction; use BENCH ASSEMBLY for an isolated off-aircraft step.

**Hardware.** Put a large Blender-rendered hardware symbol beside every exact designation and total quantity. Show bolts, washers, nuts, castle nuts, cotter symbols, rod ends and applicable bushings as separate geometry. The nearby detail shows the joint and exploded stack. Counts come from the QB sheet: do not add a washer merely to match a generic example. Hardware identity graphics are symbolic, not a dimensional reference. Unresolved nuts stay in a separate tray, never an invented installed stack.

**Uncertainty.** Use an orange question mark with VERIFY HARDWARE / ORIENTATION / POSITION / ROUTING, and SEE PLAN XX when useful. Use SOURCE CONFLICT — VERIFY for unresolved cross-source callout differences. Keep an actionable record in `HUMAN_REVIEW_REQUIRED.md`, with sources, depicted choice and open question. Continue past isolated uncertainty without making the rest of the illustration more certain than its sources.

**Camera/render.** Blender 5.2 LTS, deterministic bpy, orthographic isometric plus joint details, white composite background, Workbench studio light, shadows/specular off, smooth simple tubes and object outlines. Coordinates: X right, Y aft, Z up. Named component collections remain editable. Approximate shape and connection relationships matter; welds, threads and manufacturing detail do not. Inspect every release page; limit meaningful visual correction cycles to two.

**Text and PDF.** One action title, exact hardware labels, short joint/orientation labels and necessary flags; no prose blocks on step pages. Footer: ILLUSTRATIVE — NOT TO SCALE / BOB BARROWS COMPANION PLANS CONTROL. One PDF per logical subassembly, 11×7.5 inches (792×540 points), one step per page, lossless 400-ppi page images and step bookmarks. Website and PDF consume the same PNGs. Validate page count/order, dimensions, nonblank content, clipping, and readable hardware before release.
