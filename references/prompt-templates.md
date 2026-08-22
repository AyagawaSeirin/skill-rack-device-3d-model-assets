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
rear, left, right, top, bottom and available three-quarter views. Search for any
public official GLB/glTF/CAD asset but list it only as a backup option. Do not
substitute it for the newly built model unless I explicitly choose that option.

Record source URLs and what each proves. Resolve whether width/depth include rack
ears, bezel, handles, PSUs, or other protrusions. Treat the chassis body, ears,
standalone module and fully installed enclosure as separate dimension subjects.

Create a feature inventory before modeling. Enumerate exact counts, row/column
layout, left-to-right order, position, relative size, depth/relief, color/material
and source for every drive bay, sled, module, blanking panel, PSU, fan, port group,
grille, handle, latch, rack ear, hole, seam, label and visible fastener.

Create six high-resolution photoreal orthographic assets at their physical aspect
ratios. Prefer rectification, compositing or texture baking from exact photos. Use
AI editing only for tightly constrained perspective, background, margin or small
occlusion repair; discard any output that redesigns the face. Preserve real
branding, text, counts, order, materials and relief. Reject pseudo-text, invented
screens/LEDs/ports, repeated AI patterns, vector art, toon outlines and flat
illustration. Keep chassis pixels opaque; only real through-holes may be transparent.

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
PASS/REWORK/BLOCKED report and separate backup links for official 3D files found.
```

## Six-face source-preserving image edit

```text
Create the exact [FACE] orthographic texture for [MANUFACTURER] [FULL PID]
[INSTALLED CONFIGURATION], using the attached exact-device official photos,
technical drawings and three-quarter views as binding references. This is not a
generic, same-family or freely redesigned equipment image.

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
evidence. Record official 3D files only as optional backups.

Global gates: no mirrored logo/text; no rear ears inferred from perspective; no
generic ears; all main surfaces opaque; only real holes transparent; no visible
interior; no generic-box, stylized, illustrated, vectorized or AI-invented
appearance; exact module/bay/port/PSU/fan counts and relief; no stretching; correct
assembly dimensions; matched-camera source comparisons; and actual GLB QA in two
viewers. Output a per-file PASS/REWORK/BLOCKED table and continue until every
repair passes exact feature comparison or has a documented evidence block.
```
