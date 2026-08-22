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

## 2. Generate six canonical transparent assets with GPT image generation

Using online/PDF material as references is mandatory, but cropping and background removal alone are not the final production method. Use the `imagegen` skill and built-in `image_gen` tool by default to generate the six canonical face assets.

For every face:

1. collect multiple exact-configuration sources from official pages/PDFs and, when needed, Browser-assisted or cross-checked third-party/commerce pages;
2. download source images and render relevant PDF pages to PNG;
3. inspect every local input with `view_image` at high/original detail before generation;
4. classify references as `REAL_PHOTO`, `OFFICIAL_RENDER`, `TECHNICAL_DIAGRAM`, or `AI_DERIVATIVE`; AI derivatives cannot be the primary reference;
5. label each input role explicitly, for example `Image 1: PRIMARY BINDING REAL FACE PHOTO—identity, geometry, material and photographic style`, `Image 2: binding three-quarter geometry reference`, `Image 3: supporting material/color reference`, `Image 4: technical diagram`;
6. select `SOURCE_LOCKED_GENERATION` when a direct real face photo exists, otherwise `MULTI_REFERENCE_RECONSTRUCTION`, with `GENERIC_BOTTOM_FALLBACK` reserved for the documented bottom exception;
7. invoke built-in `image_gen` once for that face, requesting a new exact orthographic asset while locking both factual content and the real source's visual style;
8. request a genuinely transparent external background and preserve generated alpha;
9. inspect the output with `view_image`, compare it to the primary real photo, feature inventory and supporting sources, and reject factual or style drift;
10. iterate with one targeted correction while repeating identity and photographic-style invariants;
11. copy the selected project-bound output into `views/<face>.png` and record the final prompt, source-lock mode, input roles, generation method, and output path.

Use reference-guided `product-mockup` generation for a new orthographic face. When a direct real photograph exists, it is not merely a loose reference: make it Image 1 and explicitly state that its identity, layout, materials, color, surface texture, photographic character and style are binding and must not change. Do not prompt from only a model name. Do not use a single freely generated or earlier AI image to infer other faces.

Use one built-in call per face; do not collapse six different assets into one batch prompt or use `n` as a substitute. The built-in path is the default and supports transparent output. If it is unavailable, explain the explicit CLI fallback and its API-key requirement; use it only if the user confirms.

For third-party photos, exclude seller backgrounds, cables, rails, shipping damage, inventory labels, and non-factory stickers through the reference-guided generation prompt. Do not “clean up” the product itself, erase real surface character, or turn it into a cleaner CGI/product render. Do not transform a configuration difference into the requested model. For `GENERIC_BOTTOM_FALLBACK`, feed inspected fallback references to image generation and require a conservative non-identifying underside; never generate a detailed imaginary bottom from text alone.

For each view, require:

- one straight orthographic face, no visible adjacent face or perspective;
- exact verified feature layout and silhouette, except the documented bottom fallback which must preserve all silhouette-affecting evidence;
- exact component count, row/column arrangement, spacing, seams, recesses, and protrusions from the feature inventory; a bottom fallback stays intentionally non-identifying rather than inventing detail;
- neutral lighting, no cast shadow or floor;
- the same photographic style and real material character as the primary real photograph: matching color balance, contrast, surface grain, wear, highlight softness and recess shadows;
- readable factory logo/model text in the source orientation;
- transparent external background where needed;
- alpha `255` over all visible chassis pixels, including black vents and ports;
- alpha `0` only outside the product and within verified through-holes;
- no annotation, watermark, reseller sticker, cable, rail, detached fragment, pseudo-text, invented display, invented indicator, or decorative port.

Use this prompt scaffold for each face:

```text
Use case: product-mockup
Asset type: exact rack-device [FACE] texture for GLB
Input images: [LABEL EACH BINDING REFERENCE AND ROLE]
Primary request: generate a new exact [FACE] orthographic view of [EXACT PID AND INSTALLED CONFIGURATION] from the binding references
Scene/backdrop: genuinely transparent background
Style/medium: SOURCE-LOCKED real product photography; preserve the same photographic style, metal/plastic texture, wear, color balance, contrast, highlight softness and recess shadows as Image 1; not a cleaner CGI/product render, illustration or generic 3D concept art
Composition/framing: one complete face, perfectly straight-on, no adjacent face, physical ratio [A:B]
Constraints: Image 1 is the highest-authority binding identity-and-style reference; preserve [FEATURE INVENTORY]; keep factory logo/text location and orientation; product pixels fully opaque; only verified through-holes transparent; no seller labels, cables, rails, watermark, cast shadow, pseudo-text, invented parts, mirroring, repetition, redesign or style change
Avoid: generic server details, family substitution, CGI cleanup, relighting, beautification, material smoothing, aggressive denoising, color restyling, artificial symmetry, vectorized edges, toon/flat shading, fake displays/LEDs/ports, changed component counts
```

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
