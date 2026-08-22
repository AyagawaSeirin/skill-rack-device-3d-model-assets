# GLB inspection, diagnosis, repair, and acceptance

The actual exported model is the product. Preview PNGs and pipeline reports are supporting evidence only.

## 1. Pre-build exactness gate

Do not start mesh work until all of these exist and are `VERIFIED`:

- `identity-manifest.md` identifies the exact delivery subject, host/module relationship, installed module count, backplane/drive option, rear option, bezel/blanking state, and power/fan configuration;
- every major row in `feature-inventory.csv` has an exact count, layout, depth/relief, material, and source;
- each of the six faces has exact-configuration color and geometry evidence;
- body and fully installed assembly dimensions are distinguished.

If any item is unknown, report `BLOCKED`. Do not generate a visually plausible draft to “fill in later”; those drafts are likely to become false sources.

## 2. Run structural audits

Check six views before building:

```bash
python scripts/audit_views.py /path/to/views \
  --width-mm 445 --height-mm 43.6 --depth-mm 600 \
  --json-out /path/to/qa/views-audit.json
```

If rack ears are included in the front image, pass `--front-width-mm`; if a real rear silhouette has a different width, pass `--rear-width-mm`. Use the tightly cropped product content, not the original canvas, to judge physical aspect ratio.

Inspect a GLB:

```bash
python scripts/audit_glb.py /path/to/model.glb \
  --expected-width-mm 482.6 --expected-height-mm 43.6 --expected-depth-mm 600 \
  --json-out /path/to/qa/glb-audit.json
```

The helpers flag structural risks such as non-opaque face materials, embedded texture alpha, low texture resolution, missing UVs, external resources, negative/mirrored transforms, and dimension-ratio mismatch. They cannot establish exact-model fidelity, distinguish an intended perforated part from a damaged face, or prove that a texture reads correctly after UV mapping.

## 3. Inspect GLB internals

For the standard and web GLBs, record:

- glTF version, generator, extensions used/required;
- file size, scene/node/mesh/primitive/material/texture/image counts;
- root and mesh transforms, especially negative determinants;
- computed world-space bounds and proportions;
- base-color texture resolution and color-space handling;
- material `alphaMode`, cutoff, base-color alpha, double-sided setting, metallic/roughness, and `KHR_materials_unlit`;
- whether every textured primitive has UV coordinates;
- whether image/buffer URIs are embedded or deliberately packaged;
- whether standard and web variants have the intended same silhouette and orientation.

Do not infer that identical `views/` images mean identical embedded images. Extract or inspect the GLB's own resources when diagnosing.

## 4. Render the actual GLB

Use at least two independent glTF render paths, such as a local `<model-viewer>` gallery plus Blender, Gestaltor, or another glTF-aware desktop viewer. Use neutral light/background and disable optional post-processing for the comparison pass.

Capture at minimum:

- front, rear, left, right, top, bottom;
- front-left/front-right and rear-left/rear-right three-quarter views;
- light and dark checkerboard backgrounds for alpha inspection;
- a close-up of each rack ear and any fine logo/text area.

Compare renders directly with the approved six source views and the identity checklist. Inspect text at 100% zoom.

Match the reference camera, crop, canvas size, and neutral background. Generate a comparison sheet for each orthographic view and every authoritative three-quarter source:

```bash
python scripts/create_comparison_sheet.py \
  /path/to/qa/reference/front.png \
  /path/to/qa/renders/front.png \
  /path/to/qa/comparisons/front.png
```

The script creates reference/render/overlay/difference panels. It deliberately refuses mismatched pixel dimensions instead of silently stretching one image. A numeric pixel difference is diagnostic only; final acceptance is feature-by-feature.

## 5. Exact-appearance acceptance checklist

### Identity and geometry

- exact PID/generation/variant, U height, drive layout, port order, PSU/riser arrangement, logo, and model badge;
- exact delivery subject and installed assembly: enclosure, module/sled count and positions, backplane/drive option, rear option, blanking panels, bezel, power and fan configuration;
- every feature-inventory row has an exact counterpart in the GLB render with the same count, row/column structure, order, relative size, position, and relief;
- world-space aspect ratio matches the dimension ledger within documented tolerance;
- front ears only where verified, correct width and hole pattern;
- no false rear ears caused by copying a perspective rear photograph;
- no top duplicated as bottom, left duplicated as right, or generic side panels;
- no single-box construction where source three-quarter views show distinct modules, bays, handles, steps, recesses, or panel thickness;
- closed body, correct outward normals, no gaps, doubled planes, z-fighting, or visible interior.

### UV and texture

- all six approved views are present in the GLB;
- physical face ratios are preserved without squeezing or padding artifacts;
- text and logo are readable and located on the correct side;
- no mirror, rotation, face swap, repeat, seam discontinuity, or atlas bleed;
- sufficient resolution remains in the embedded web asset, not only in `views/`.
- no pseudo-text, invented displays/LEDs, decorative ports, repeated AI patterns, vectorized surfaces, toon outlines, posterization, or flat illustration shading;
- front/rear and three-quarter overlays show no unmatched large panel, missing module, wrong relief, or shifted feature group.

### Alpha and rack-ear holes

- main front/rear/side/top/bottom materials are opaque;
- black ports, vents, grilles, screw heads, logos, and labels are not transparent;
- no partial-alpha haze or accidental window into the empty model;
- external background has not been baked as a white/gray rectangle;
- rack-ear through-holes are true openings with clean high-resolution edges;
- alpha used for an ear is isolated from the chassis face.

### Color and viewing

- GLB colors are close to approved sRGB source assets under a neutral render;
- no uniform gray veil from metallic factors, wrong color space, excessive roughness, transparency, or double tonemapping;
- both viewers agree on orientation and opacity even if their lighting differs.
- standard and web GLBs retain the same externally visible geometry and identifying texture detail.

### Immediate rejection symptoms

Return `REWORK`, not a warning, when the result:

- resembles a generic rack server more than the exact official product;
- has the wrong number of sleds, drives, nodes, PSUs, fans, modules, or blanking panels;
- represents a module as a nonexistent standalone chassis or combines incompatible front and rear configurations;
- replaces real mechanical structure with large blank rectangles, flat icon-like ports, fake screens, or decorative labels;
- looks illustrated, cartoon-like, cel-shaded, or heavily vectorized compared with official product photography;
- cannot be mapped one-to-one to the visible-feature inventory.

## 6. Decide whether the viewer or model is at fault

Use this sequence:

1. compare `views/` PNGs with textures extracted from the GLB;
2. inspect material alpha, base-color factor, unlit/PBR settings, and texture color space;
3. render the same GLB in a second viewer with neutral settings;
4. compare UV landmarks and node transforms;
5. inspect geometry from rear and side angles.

Interpretation:

- If only one viewer looks gray while extracted textures and neutral second-viewer render are correct, document a viewer lighting/color-management issue.
- If multiple viewers show the same gray veil, mirror, missing face, false rear ear, or transparency, the model/export is defective.
- If `views/` is correct but GLB text is mirrored, repair UV order or transforms; do not regenerate the source image.
- If texture resolution or alpha is already damaged inside the GLB, repair/re-embed the approved source texture and re-export.

## 7. Repair rules

Repair at the earliest defective layer:

- evidence wrong → research exact model again;
- assembly identity wrong → discard the generic enclosure and rebuild from the verified host/module/backplane configuration;
- model looks illustrated or generic → return to exact photos; rectify/composite or bake source-derived textures and rebuild visible relief instead of polishing the approximation;
- visible component counts/layout wrong → rebuild from the feature inventory; do not clone or mirror repeated patterns to fill space;
- dimensions ambiguous → resolve body/overall inclusion rules;
- face image invented or compressed → regenerate from exact references at the correct ratio;
- cutout damaged → edit from the original source with reference-preserving image generation;
- GLB mirrored with correct PNG → repair UVs/transforms only;
- rear ears copied from perspective → remove rear-ear geometry and rebuild the rear plane from the approved rear source;
- transparent chassis → set body/face materials opaque and restore alpha `255` for product pixels;
- gray appearance in all viewers → correct sRGB, base-color factor, unlit/PBR material, and tone-mapping assumptions;
- optional official model available → continue the new build, but report the official file as a backup choice.

Do not overwrite the prior version. Create a new repair directory and retain before/after QA renders.

## 8. Batch completion gate

For a batch, publish a row for every requested model with `PASS`, `REWORK`, `BLOCKED`, or `OPTIONAL-OFFICIAL`, plus exact reasons. A missing model is a failure, not an omitted row. `OPTIONAL-OFFICIAL` supplements rather than replaces the build status. Finish only when:

- the inventory count matches the request;
- every model and physical variant has all six evidence-backed faces;
- every modular model has a verified installed-assembly manifest;
- every feature-inventory row is matched in actual-GLB renders;
- standard/web GLBs have both been checked when both are delivered;
- structural audit has no unresolved error;
- every newly built GLB has multi-angle render evidence;
- matched-camera comparison sheets show no unresolved exterior mismatch;
- an approximate result, even if separately authorized, is never labeled exact-replica `PASS`.
