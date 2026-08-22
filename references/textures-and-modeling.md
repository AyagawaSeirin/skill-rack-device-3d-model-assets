# Exact six-face textures and exterior GLB modeling

Use this guide after the target matrix, evidence records, and dimension ledger are complete.

## 1. Canonical coordinate and view convention

Use a right-handed glTF convention unless the project already defines one:

- `+X`: device right as seen from the front;
- `+Y`: up;
- `+Z`: front;
- body centered near the origin;
- front camera at `+Z` looking toward `-Z`;
- rear camera at `-Z` looking toward `+Z`;
- right/left cameras at `+X`/`-X`;
- top/bottom cameras at `+Y`/`-Y`.

Name views from the device's physical perspective. A rear view naturally reverses the screen position of left/right chassis features; do not horizontally flip it to resemble the front. Before UV assignment, annotate at least two asymmetric landmarks per face, such as logo, management port, PSU, status panel, latch, or label. After export, confirm every landmark and readable word in the rendered GLB.

Avoid negative node scales and mirrored parent transforms. Apply transforms before export and keep outward normals consistent.

## 2. Produce six canonical face assets

Choose the least generative and most source-preserving path:

1. isolate and perspective-correct an exact orthographic photograph;
2. composite unobstructed regions from exact photos of the same installed configuration;
3. bake/project exact photographic color from verified geometry;
4. use tightly constrained reference-preserving image editing for background, margins, perspective, or small occlusions only;
5. use official drawings or optional official 3D renders to constrain geometry and feature placement while still producing a new model;
6. stop if only family-level or contradictory evidence exists.

When raster editing is required, use the available image-generation skill/tool with original exact-device images attached. Do not ask it to redesign or freely regenerate an entire device face. Do not prompt from only a model name. For a hidden surface, attach all exact-configuration views and diagrams that jointly prove its features. If the edit changes counts, proportions, seams, logo, text, materials, ports, or relief, discard it. If local background removal damages edges or holes, edit again from the original source rather than eroding a derivative.

For each view, require:

- one straight orthographic face, no visible adjacent face or perspective;
- exact verified feature layout and silhouette;
- exact component count, row/column arrangement, spacing, seams, recesses, and protrusions from the feature inventory;
- neutral lighting, no cast shadow or floor;
- photoreal source-derived materials with no toon outline, illustration shading, or generic color blocks;
- readable factory logo/model text in the source orientation;
- transparent external background where needed;
- alpha `255` over all visible chassis pixels, including black vents and ports;
- alpha `0` only outside the product and within verified through-holes;
- no annotation, watermark, reseller sticker, cable, rail, detached fragment, pseudo-text, invented display, invented indicator, or decorative port.

## 3. Preserve physical aspect ratio and resolution

Use the verified dimensions to set each image's content ratio:

| Face | Physical ratio |
|---|---|
| front | front overall width : height, or body width : height when ears are separate geometry |
| rear | rear silhouette width : height; never add front ears merely to match front width |
| left/right | depth : height |
| top/bottom | body width : depth |

Do not resize width and height independently. Crop transparent margins before evaluating aspect ratio. If the face is wider than the chosen canvas, increase the canvas or resolution; never squeeze it.

Unless the project specifies another budget, use at least 2048 px on the long edge for front/rear and at least 1536 px on the long edge for the other faces. Increase resolution for dense port labels or small ear holes. Keep texel density reasonably consistent across adjacent faces and generate mipmaps during web optimization.

The `scripts/audit_views.py` helper checks filenames, resolution, aspect ratios, and suspicious alpha in the opaque core. It does not prove model identity, installed configuration, visual fidelity, or correct orientation.

## 4. Rack-ear geometry and holes

Model the chassis body and rack ears separately.

- Derive body width from the chassis dimension, not the ear-to-ear rack span.
- Derive each ear's lateral extension, height, thickness, front/rear offset, hole count, and hole shape from exact evidence.
- Attach front ears at the verified front plane. Do not extrude them down the full chassis depth.
- A rear photograph may show the front ears because the camera sees along the side. Do not copy those visible ears onto the rear plane.
- Devices with integrated bezel tabs, release handles, or status panels are not automatically devices with generic stamped rack ears.
- Use real mesh cutouts for circular, square, keyhole, or slotted openings when practical. Preserve anti-aliased alpha only as a fallback on a separate ear plane/material.

Never use an alpha-masked full front or rear plane to make ear holes; it can also open vents, logos, labels, and chassis pixels and reveal the model interior.

## 5. Exact visible geometry

Model the complete visible exterior represented by the feature inventory. Use separate geometry for any part that creates identifiable silhouette, parallax, occlusion, seam depth, recess, protrusion, or cast shadow in an approved orthographic or three-quarter view. Preserve:

- verified overall body proportions and silhouette;
- front and rear planes at their true offsets;
- front-only or real rear mounting hardware;
- large handles, bezels, air ducts, raised covers, and other silhouette-changing parts;
- major side/top/bottom seams or vents visible in official views.
- every installed sled/module boundary, blanking panel, drive bay or carrier recess, visible PSU/fan block, control area, and large port group;
- the real thickness, depth ordering, and gaps of handles, bezels, latches, rack ears, and stepped panels.

Do not omit a component because it is removable. If it is externally visible in the requested installed configuration, it must appear with the correct count, shape, position, and depth. A single beveled box with six decorative planes is forbidden when the real device is multi-part.

Fine flush labels may remain texture detail. Dense perforation may use real geometry, a normal/height treatment, or an opaque high-resolution texture only if the actual-GLB comparison at target viewing distance is indistinguishable from the source. Do not use flat black dots as a substitute when perforation depth or through-visibility is visibly important.

Use a watertight or visually closed body, outward normals, and `doubleSided: false` by default. Prevent z-fighting by avoiding coplanar duplicate face planes. Do not leave gaps behind front/rear texture cards.

## 6. UV orientation

Assign one explicit material/texture per canonical face or use a documented atlas. Avoid procedural projection whose sign differs between front and rear.

Before the final texture, use an orientation test image containing the face name, `L`/`R`, an upward arrow, and asymmetric numbered corners. Render all six views. Fix UV order or texture transforms until every marker is correct, then substitute approved textures without changing the UVs.

Reject:

- horizontally mirrored logo or text;
- front image on rear or left image on right;
- 90°/180° rotations;
- negative-scale fixes that reverse normals or tangent handedness;
- atlas bleeding at mip levels.

## 7. Materials and color

For photo-derived face textures intended to match the approved PNGs:

- mark base-color textures as sRGB;
- use `baseColorFactor: [1, 1, 1, 1]`;
- keep face materials `alphaMode: OPAQUE`;
- prefer `KHR_materials_unlit` for a consistent product-photo appearance across website viewers;
- if PBR is required, normally use `metallicFactor: 0` for painted chassis/photo cards, a plausible roughness, neutral lighting, and no double application of baked lighting or color correction;
- do not compensate for a dark/gray export by brightening textures blindly.
- do not use toon/cel shaders, outline passes, posterization, vectorized edges, or flat illustrative color regions.

Use `MASK` only on a separate verified perforated part when geometry is impractical; choose a cutoff that preserves anti-aliased edges. Avoid `BLEND` for main equipment faces because sorting and partial alpha can expose the interior.

## 8. Optional official model usage

The main deliverable remains newly modeled. Keep any exact official GLB/CAD file under `source/optional-3d/` or record its link. It may be inspected as authoritative evidence for dimensions, silhouette, feature placement, and canonical renders when usage terms allow.

Do not copy its mesh or substitute it for the new build unless the user explicitly requests that path. If the user later chooses the official option, preserve the original unchanged and create a separate derivative.

## 9. Web export

Optimization is target-driven and may not alter the exterior comparison:

- remove unused nodes/materials/images;
- merge only parts that do not require distinct transforms or materials;
- use quantization, mesh compression, or KTX2 only when target viewers support them;
- retain readable branding and sufficient texture resolution;
- compare web and standard renders from the same cameras;
- compare both against the exact reference views after every material or compression change;
- keep the editable/source model and prior GLB version unchanged.

Remove only invisible internals and redundant topology. Do not remove visible modules, bays, PSUs, fans, handles, seams, or relief, and do not merge distinct assemblies if their separation is visible.

Deliver a self-contained GLB unless the website pipeline explicitly expects external resources.
