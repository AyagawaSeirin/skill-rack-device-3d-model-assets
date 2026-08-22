# Prompt templates

Replace every bracketed field with verified facts. Attach source images and documents; a prompt containing only a model name is insufficient.

## End-to-end exact-model build

```text
Use the skill-rack-device-3d-model-assets workflow to create a new simplified website
GLB for the exact [MANUFACTURER] [FULL PID] [VARIANT].

Search official dimensions and exact-model visual sources for front, rear, left,
right, top, and bottom. Also search for any public official GLB/glTF/CAD asset,
but list it only as a backup option; do not substitute it for the newly built
model unless I explicitly choose that option. Do not invent an undocumented face
or substitute a family model.

Record source URLs and what each proves. Resolve whether width/depth include rack
ears, bezel, handles, PSUs, or other protrusions. Treat the chassis body and ears
as separate dimensions and geometry.

Create six high-resolution orthographic face assets at their physical aspect
ratios. Preserve real branding, text orientation, port/bay/fan/PSU order, vents,
seams, and left/right placement. Keep all chassis pixels opaque; black vents and
ports are not transparency. Use transparency only outside the product and in
verified through-holes. Prefer actual geometry for rack-ear holes. Never infer
rear ears from front ears visible in an angled rear photo.

Build a closed, outward-normal simplified mesh. Use explicit non-mirrored UVs,
sRGB base-color textures, OPAQUE main-face materials, and KHR_materials_unlit for
photo-derived faces unless verified PBR is required. Embed resources in the GLB.

Validate the actual standard and web GLBs, not just views or preview renders.
Render six orthographic and four three-quarter views in two independent viewers,
test on light/dark checkerboards, verify readable non-mirrored text, correct ears
and hole transparency, no visible interior, correct world-space proportions, and
close color agreement with the approved source images. Deliver source/evidence,
views, newly built GLBs, QA renders, PASS/REWORK/BLOCKED report, and separate
backup links for any exact official 3D files found.
```

## Six-face reference-preserving image edit

```text
Create the exact [FACE] orthographic texture for [MANUFACTURER] [FULL PID]
[VARIANT], using the attached exact-device official photos, technical drawings,
and three-quarter views as binding references. This is not a generic server or
family-model generation.

Verified facts for this face: [ENUMERATE FEATURES FROM LEFT TO RIGHT OR FRONT TO
BACK]. Output one perfectly straight face with no adjacent face, perspective,
floor, shadow, cables, rails, callouts, watermark, or detached fragments. Preserve
factory logo and readable text in the real location and orientation. Do not
mirror, repeat, or fabricate ports, vents, seams, labels, handles, feet, or holes.

Use the verified physical ratio [A:B] and at least [RESOLUTION] on the long edge.
The external background must be transparent. Every visible product pixel must be
fully opaque, including black ports and vents. Only the explicitly verified true
through-holes [LIST, OR NONE] may be transparent. If the evidence does not prove
a visible feature, leave the task unresolved instead of inventing it.
```

## GLB-only repair when source views are already correct

```text
Repair the actual newly built GLB for [MODEL KEY] without regenerating already
approved view PNGs. The source views are binding.

Observed defects: [MIRRORED UV / FALSE REAR EARS / TRANSPARENT BODY / GRAY MATERIAL
/ COMPRESSED EMBEDDED TEXTURE / WRONG DIMENSIONS / OTHER]. Diagnose the earliest
defective layer by inspecting embedded textures, UVs, node transforms, geometry,
materials, color space, and world bounds.

Keep the approved six PNGs unchanged unless the extracted GLB texture proves that
the source itself is damaged. Fix UV orientation rather than flipping source
images. Remove rear-ear geometry unless exact evidence proves rear hardware.
Make main face/body materials OPAQUE with product alpha 255; preserve real ear
holes as geometry or an isolated high-resolution mask. Use sRGB and neutral
base-color factors; prefer KHR_materials_unlit for photo-derived surfaces.

Export into a new version directory. Validate the repaired standard and web GLBs
in two viewers from six orthographic and four three-quarter angles. Provide before
and after findings and do not mark PASS from preview images alone. If an exact
official 3D file is found, report it separately as a backup rather than replacing
the repair.
```

## One-round batch repair

```text
Audit every requested model and every delivered GLB. Inventory the request first;
missing models must appear as REWORK, never disappear from the report. Preserve
the prior version and write repairs to [NEW VERSION DIRECTORY].

For each model, classify the root cause separately: source identity, dimensions,
six-face texture, UV orientation, geometry, rack ears, material/alpha, color, or
missing evidence. Reuse the previous approved front/rear originals rather than
angled images. Generate or repair left/right/top/bottom only from exact-model
official evidence. Record any public official 3D source as a separate optional
backup; continue repairing the newly built model.

Global gates: no mirrored logo/text; no rear ears inferred from perspective; no
generic ears on devices without them; body/front/rear/side/top/bottom opaque; only
real holes transparent; no visible empty interior; no face stretching; correct
body-versus-overall dimensions; correct sRGB/unlit-or-verified-PBR materials; and
actual GLB render QA in two viewers. Output a per-file PASS/REWORK/BLOCKED table
and continue until every repair either passes or has a documented evidence block.
```
