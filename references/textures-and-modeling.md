# Six-face textures and simplified GLB modeling

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

Choose the least generative path:

1. isolate and perspective-correct an exact orthographic photograph;
2. use reference-preserving image editing with several exact-model views and a mechanical checklist;
3. use official drawings or optional official 3D renders to constrain geometry and feature placement while still producing a new simplified model;
4. stop if only family-level or contradictory evidence exists.

When raster generation/editing is required, use the available image-generation skill/tool with the original exact-device images attached. Do not ask for a face from only a model name. For a hidden surface, attach the official three-quarter views or diagrams that jointly prove its features. If local background removal damages edges or holes, regenerate/edit from the original source instead of repeatedly eroding the derivative.

For each view, require:

- one straight orthographic face, no visible adjacent face or perspective;
- exact verified feature layout and silhouette;
- neutral lighting, no cast shadow or floor;
- readable factory logo/model text in the source orientation;
- transparent external background where needed;
- alpha `255` over all visible chassis pixels, including black vents and ports;
- alpha `0` only outside the product and within verified through-holes;
- no annotation, watermark, reseller sticker, cable, rail, or detached fragment.

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

The `scripts/audit_views.py` helper checks filenames, resolution, aspect ratios, and suspicious alpha in the opaque core. It does not prove model identity or correct orientation.

## 4. Rack-ear geometry and holes

Model the chassis body and rack ears separately.

- Derive body width from the chassis dimension, not the ear-to-ear rack span.
- Derive each ear's lateral extension, height, thickness, front/rear offset, hole count, and hole shape from exact evidence.
- Attach front ears at the verified front plane. Do not extrude them down the full chassis depth.
- A rear photograph may show the front ears because the camera sees along the side. Do not copy those visible ears onto the rear plane.
- Devices with integrated bezel tabs, release handles, or status panels are not automatically devices with generic stamped rack ears.
- Use real mesh cutouts for circular, square, keyhole, or slotted openings when practical. Preserve anti-aliased alpha only as a fallback on a separate ear plane/material.

Never use an alpha-masked full front or rear plane to make ear holes; it can also open vents, logos, labels, and chassis pixels and reveal the model interior.

## 5. Simplified geometry

Website simplification may use a beveled closed body plus shallow relief for major panels. Preserve:

- verified overall body proportions and silhouette;
- front and rear planes at their true offsets;
- front-only or real rear mounting hardware;
- large handles, bezels, air ducts, raised covers, and other silhouette-changing parts;
- major side/top/bottom seams or vents visible in official views.

It may omit independently removable drives, fans, and PSUs when the user only needs an overall display, but their visible face layout must remain correct in the texture or shallow geometry.

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

For photo-derived face textures intended to look like the approved PNGs:

- mark base-color textures as sRGB;
- use `baseColorFactor: [1, 1, 1, 1]`;
- keep face materials `alphaMode: OPAQUE`;
- prefer `KHR_materials_unlit` for a consistent product-photo appearance across website viewers;
- if PBR is required, normally use `metallicFactor: 0` for painted chassis/photo cards, a plausible roughness, neutral lighting, and no double application of baked lighting or color correction;
- do not compensate for a dark/gray export by brightening textures blindly.

Use `MASK` only on a separate verified perforated part when geometry is impractical; choose a cutoff that preserves anti-aliased edges. Avoid `BLEND` for main equipment faces because sorting and partial alpha can expose the interior.

## 8. Optional official model usage

The main deliverable remains newly modeled. Keep any exact official GLB/CAD file under `source/optional-3d/` or record its link. It may be inspected as authoritative evidence for dimensions, silhouette, feature placement, and canonical renders when usage terms allow.

Do not copy its mesh or substitute it for the new build unless the user explicitly requests that path. If the user later chooses the official option, preserve the original unchanged and create a separate derivative.

## 9. Web export

Optimization is target-driven:

- remove unused nodes/materials/images;
- merge only parts that do not require distinct transforms or materials;
- use quantization, mesh compression, or KTX2 only when target viewers support them;
- retain readable branding and sufficient texture resolution;
- compare web and standard renders from the same cameras;
- keep the editable/source model and prior GLB version unchanged.

Deliver a self-contained GLB unless the website pipeline explicitly expects external resources.
