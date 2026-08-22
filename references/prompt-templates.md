# Prompt templates

Replace every bracketed field with verified facts. Attach exact-configuration source images and documents; a prompt containing only a model name is insufficient.

## End-to-end exact-appearance build

```text
Use the skill-rack-device-3d-model-assets workflow to create a new website-ready
exact exterior replica GLB for [MANUFACTURER] [FULL PID] [INSTALLED CONFIGURATION].

“Website-ready” means optimized format and performance only. It does not permit
visual simplification, stylization, generic replacement, missing visible parts,
or a beveled box with decorative textures. The final model must look like the
same real photographed device from all supported camera angles.

Before generating anything, resolve the delivery subject: complete appliance,
host enclosure with modules, or standalone module. For modular systems record the
host chassis, module/sled model, installed count and positions, front backplane or
drive option, rear I/O option, bezel/blanking state, power and fan configuration.
If the installed configuration is ambiguous, stop as BLOCKED.

Search official dimensions and exact-configuration visual sources for front,
rear, left, right, top, bottom and available three-quarter views. Read official
datasheets, whitepapers and manuals with the PDF skill: extract configuration and
dimension text, render relevant pages to PNG, and visually inspect those pages.
When official pages are dynamic or hide galleries, use the Browser skill to open
and inspect them. If official imagery is insufficient, search and cross-check
authorized resellers, shopping sites, marketplaces, auctions, used-equipment
dealers, reviews, teardowns and videos. Search for any public official 3D asset
but list it only as a backup; do not substitute it unless I explicitly choose it.

Record source URLs and what each proves. Resolve whether width/depth include rack
ears, bezel, handles, PSUs, or other protrusions. Treat the chassis body, ears,
standalone module and fully installed enclosure as separate dimension subjects.

Create a feature inventory before modeling. Enumerate exact counts, row/column
layout, left-to-right order, position, relative size, depth/relief, color/material
and source for every drive bay, sled, module, blanking panel, PSU, fan, port group,
grille, handle, latch, rack ear, hole, seam, label and visible fastener.

Download the selected web images and PDF-page renders. Inspect every image at
high/original detail with the image-viewing capability, confirming exact PID,
configuration, face/angle, orientation, seller changes, crop and resolution.
Record the source URL, PDF page/figure when applicable, visual findings and the
role each image will have in GPT image generation.

Use the imagegen skill and built-in image_gen tool to generate six separate
high-resolution photoreal orthographic transparent-background assets, one call
per face. Use the inspected online images and PDF-page views as explicitly labeled
binding references. Do not stop after cropping, perspective correction or local
background removal. Preserve real branding, text, counts, order, materials and
relief. Reject and regenerate pseudo-text, invented screens/LEDs/ports, repeated
AI patterns, vector art, toon outlines, flat illustration, opaque background,
transparent chassis pixels or any redesign. Only real through-holes may be transparent.

If exact bottom imagery remains unavailable after official, Browser-assisted and
third-party searches, choose the closest conservative generic-bottom references,
inspect them, and feed them to imagegen to generate a non-identifying transparent
bottom matching verified dimensions/material. Do not mirror the top or invent
labels, vents, holes, rails, feet or protrusions. Mark the result
GENERIC_BOTTOM_FALLBACK and use final status PASS_WITH_BOTTOM_FALLBACK.

Build the complete visible exterior as a closed outward-normal mesh. Every feature
that produces silhouette, seam depth, parallax, recess, protrusion, occlusion or
shadow in an official three-quarter view must have correctly placed geometry or
faithful relief. Do not omit visible removable parts. Use explicit non-mirrored
UVs and sRGB OPAQUE face materials. Choose unlit or PBR only after matching the
source appearance. Embed resources in the GLB.

Validate the actual standard and web GLBs, not previews. Render six orthographic
and all authoritative three-quarter views in two independent viewers. Create
matched-camera side-by-side, overlay and difference sheets. Verify every feature
inventory row, readable text, correct ears/holes, exact world proportions,
photo-real materials, and no missing or invented visible part. Deliver identity
manifest, evidence, feature inventory, six views, GLBs, QA renders/comparisons,
imagegen prompts/input roles, PASS/PASS_WITH_BOTTOM_FALLBACK/REWORK/BLOCKED report,
and separate backup links for official 3D files found.
```

## Six-face source-preserving image edit

```text
Use the imagegen skill and built-in image_gen tool. Generate this face in one
dedicated call; do not use a local crop/cutout as the final deliverable.

Create the exact [FACE] orthographic texture for [MANUFACTURER] [FULL PID]
[INSTALLED CONFIGURATION], using the attached exact-device official photos,
technical drawings and three-quarter views as binding references. This is not a
generic, same-family or freely redesigned equipment image.

Input images: [IMAGE 1: BINDING FACE REFERENCE; IMAGE 2: BINDING THREE-QUARTER
GEOMETRY REFERENCE; IMAGE 3: MATERIAL/COLOR REFERENCE; IMAGE 4: RENDERED PDF
TECHNICAL VIEW]. Every input was visually inspected before use.

Verified feature inventory for this face: [ENUMERATE EVERY COMPONENT GROUP,
COUNT, ROW/COLUMN LAYOUT, LEFT-TO-RIGHT ORDER, SIZE, POSITION, DEPTH AND MATERIAL].

Preserve the real face rather than beautifying or redesigning it. Prefer source
rectification and compositing. Do not convert it into vector art, illustration,
toon shading, a cleaner generic product render or a symmetrical repeated layout.
Do not invent pseudo-text, screens, indicators, LEDs, labels, ports, vents, seams,
handles, feet, holes, blanking panels or modules.

Output one perfectly straight photoreal face with no adjacent face, perspective,
floor, shadow, cables, rails, callouts, watermark or detached fragments. Preserve
factory logo and readable text in the real location and orientation. Use physical
ratio [A:B] and at least [RESOLUTION] on the long edge.

The external background must be transparent. Every visible product pixel must be
fully opaque, including black ports and vents. Only the verified true through-holes
[LIST, OR NONE] may be transparent. If evidence does not prove any visible fact,
stop instead of inventing it.

Before accepting, compare exact counts and left-to-right order against the feature
inventory. Reject changed seams, simplified relief, missing modules, repeated AI
patterns or any output that is merely recognizable rather than the same device.
```

## Bottom fallback image generation

```text
Use the imagegen skill and built-in image_gen tool to generate a new transparent
bottom-face PNG. Exact-model underside imagery was not found after documented
official, PDF, Browser-assisted, reseller, shopping, marketplace, used-equipment,
video and local-language searches.

Input images: [LABEL INSPECTED SAME-FAMILY / SAME-VENDOR / SAME-U / GENERIC
UNDERSIDE REFERENCES] plus [LABEL VERIFIED SIDE/TOP MATERIAL AND EDGE REFERENCES].

Generate a conservative non-identifying rack-device underside at physical ratio
[WIDTH:DEPTH]. Match only the verified sheet-metal color, finish and edge treatment.
Preserve bottom-edge or rail features proven by side views. Do not copy/mirror the
top. Do not invent or include logos, model labels, vents, holes, feet, rails, seams,
fasteners, protrusions, ports or service labels. Transparent external background;
all product pixels opaque. Save as bottom.png, record GENERIC_BOTTOM_FALLBACK and
use final status PASS_WITH_BOTTOM_FALLBACK.
```

## GLB repair when views are already exact

```text
Repair the actual GLB for [MODEL KEY] without regenerating already approved exact
view PNGs. The approved views, identity manifest and feature inventory are binding.

Observed defects: [MIRRORED UV / FALSE REAR EARS / TRANSPARENT BODY / GRAY MATERIAL
/ GENERIC OR ILLUSTRATED APPEARANCE / WRONG ASSEMBLY OR COMPONENT COUNT /
COMPRESSED EMBEDDED TEXTURE / WRONG DIMENSIONS / OTHER]. Diagnose the earliest
defective layer: assembly identity, source, texture, UV, transform, visible
geometry, material, color space or bounds.

If the existing result is generic, illustrated or based on the wrong assembly, do
not polish or retain its box mesh. Lock the correct host/module/backplane identity,
return to original exact-device photos and rebuild the complete visible exterior.

If the source views are correct, fix UV orientation instead of flipping them.
Remove rear-ear geometry unless exact evidence proves it. Make face/body materials
OPAQUE with product alpha 255; preserve real ear holes as geometry or an isolated
high-resolution mask. Use sRGB and choose unlit/PBR only through source comparison.

Export to a new version directory. Validate standard and web GLBs in two viewers
from six orthographic and all authoritative three-quarter angles. Create matched
reference/render overlays and verify every feature-inventory row. Do not mark PASS
from preview images. Report any official 3D file separately as a backup.
```

## One-round batch repair

```text
Audit every requested model and every delivered GLB. Inventory the request first;
missing models must appear as REWORK. Preserve the prior version and write repairs
to [NEW VERSION DIRECTORY].

For each model classify root cause separately: product identity, installed
assembly, dimensions, feature inventory, six-face sources, UV orientation, visible
geometry, rack ears, material/alpha, color or missing evidence. Reuse only exact,
approved source assets. Generate or repair every face solely from exact-configuration
evidence. Use PDF reading/rendering, visual image inspection and one built-in
imagegen call per face; local crop/cutout alone is not accepted. Escalate from
official sources to Browser-assisted galleries and cross-checked third-party
commerce sources. Allow only the documented generic-bottom fallback. Record
official 3D files as optional backups.

Global gates: no mirrored logo/text; no rear ears inferred from perspective; no
generic ears; all main surfaces opaque; only real holes transparent; no visible
interior; no generic-box, stylized, illustrated, vectorized or AI-invented
appearance; exact module/bay/port/PSU/fan counts and relief; no stretching; correct
assembly dimensions; matched-camera source comparisons; and actual GLB QA in two
viewers. Output a per-file PASS/PASS_WITH_BOTTOM_FALLBACK/REWORK/BLOCKED table and
continue until every repair passes exact feature comparison, uses the documented
bottom-only fallback, or has a genuine non-bottom evidence block.
```
