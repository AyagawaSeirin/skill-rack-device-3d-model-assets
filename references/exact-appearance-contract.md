# Exact-appearance fidelity contract

Read this before generating images or creating geometry. The deliverable is an exact exterior replica for website viewing, not a recognizable interpretation.

## 1. Meaning of “exact”

The model must match the requested real installed device configuration in every externally visible fact supported by the source set:

- silhouette and body proportions;
- enclosure, sled, node, controller, line-card, bay, blanking-panel, PSU, fan, and handle counts;
- row/column structure, spacing, recess/protrusion, and left/right order;
- port families, grilles, vents, seams, fasteners, latches, rack ears, and through-holes;
- factory colors, surface finish, logo, model badge, and readable markings;
- appearance from all verified orthographic and authoritative three-quarter views, with only the documented generic-bottom fallback exception.

The result must look like the same photographed device, not merely the same equipment category or product family. “Web-ready” describes format and performance only.

## 2. Assembly identity gate

Create `source/identity-manifest.md` before source generation or modeling:

```text
manufacturer:
requested_product_id:
delivery_subject: complete-appliance | enclosure-with-modules | standalone-module
host_enclosure_model:
installed_module_model:
installed_module_count:
installed_module_positions:
front_backplane_or_drive_configuration:
rear_io_or_controller_configuration:
bezel_and_blanking_panel_state:
power_and_fan_configuration:
u_height:
evidence_urls:
status: VERIFIED | BLOCKED
```

Do not infer an enclosure from a module name. Do not invent an installed node count or combine incompatible front and rear options.

## 3. Visible-feature inventory gate

Create one row per visible component group before building:

```text
face,component,count,rows,columns,left_to_right_order,relative_size,
position,depth_or_relief,color_material,source_url,confidence
```

Enumerate rather than summarize. “Front has drives and vents” is insufficient; record exact counts, carrier style, row/column layout, status-panel side, handle shape, and blanking panels. For a modular enclosure, enumerate every installed and empty slot.

Do not start modeling while any major identity-bearing visible row has `confidence` below verified. The only exception is a bottom row explicitly marked `GENERIC_BOTTOM_FALLBACK` after the required search escalation.

## 4. Source-lock rule

The approved exact-device web images, inspected PDF-page renders, and third-party sources are binding references. Prepare them with operations that change the fewest factual pixels:

1. crop, rectify, and isolate an exact photo;
2. composite unobstructed regions from multiple exact photos of the same configuration;
3. bake or project exact-source color onto verified geometry;
4. render relevant PDF pages and isolate the applicable figure or equipment view;
5. reject prompt-only or family-reference generation.

Reference preparation is not the final face-asset workflow. For each canonical face, invoke the `imagegen` skill and built-in image-generation tool using the inspected sources as labeled inputs. Generate one orthographic transparent-background PNG per call. A direct crop or locally removed background alone is insufficient.

Lock every face to one production mode:

- `SOURCE_LOCKED_GENERATION`: an exact real photograph of that face exists. Imagegen creates a new orthographic transparent asset, while that photograph remains the binding identity, geometry, material, color, texture, and photographic-style reference.
- `MULTI_REFERENCE_RECONSTRUCTION`: no usable direct face photo exists; use multiple exact-model real photographs and technical views as binding references.
- `GENERIC_BOTTOM_FALLBACK`: bottom-only exception after search exhaustion.

Earlier AI generations, GLB renders, preview images, and stylized derivatives cannot outrank real photographs and cannot be the primary identity/style source. Keep a source lock record with paths/URLs and SHA-256 values.

Image generation must reconstruct the same real device in the same photographic character rather than redesign or restyle it. Preserve the identity/feature inventory as invariants. Discard and regenerate an output if it introduces pseudo-text, new ports, decorative indicators, repeated patterns, changed component counts, mirrored branding, invented panel seams, opaque background, transparent chassis pixels, or a different visual style. Keep the final prompt, input-role list, and selected output path in the evidence/QA record.

## 5. Photographic-style lock

Style is factual source data, not a creative choice. Match the primary real photograph's:

- genuine metal, plastic, paint, grille, connector, label, and fastener appearance;
- color balance, saturation, contrast, highlight softness, and shadow depth within ports/recesses;
- surface grain, small scratches, wear, stamping, machining, and imperfect real-world texture;
- camera/product-photography character without converting it to a clean CGI render.

The generated face may become orthographic and transparent, but must not become a different representation style. Reject 3D-render polish, game-asset shading, vectorized edges, painted texture, toon/flat shading, aggressive denoising, artificial symmetry, relighting, beautification, material smoothing, or a “cleaner modern product shot.” `Photorealistic` alone is too weak; prompts must say `same photographic style and real material character as the primary binding photograph` and enumerate the locked traits.

## 6. Controlled generic-bottom fallback

Use this exception only when all of the following are true:

- exact-model official documents, media, videos, 3D viewers, and service material were searched;
- interactive/dynamic pages were inspected with the available Browser skill where useful;
- exact-model reseller, marketplace, auction, used-equipment, review, teardown, and local-language searches were attempted;
- no usable exact underside view remains;
- front, rear, left, right, top, installed configuration, dimensions, and all silhouette-affecting bottom features are otherwise verified.

Select fallback reference material in this order: same model family, same vendor and chassis generation, same U height/form factor, then a neutral generic rack-device underside. Inspect the fallback images, label their role, and use them with built-in image generation to create the final transparent `bottom.png`. Match verified width:depth ratio, sheet-metal color, finish, and edge treatment. Do not mirror the top or invent labels, logos, vents, holes, feet, rails, seams, fasteners, or protrusions. Preserve any bottom-edge or rail feature already proven by side/three-quarter references.

Record the source and search log as `GENERIC_BOTTOM_FALLBACK`, keep `bottom.png` for pipeline compatibility, and set final status to `PASS_WITH_BOTTOM_FALLBACK`. This exception applies only to the bottom face and does not relax exactness for geometry, silhouette, or any other face.

## 7. Geometry fidelity rule

Use geometry wherever a feature creates visible silhouette, parallax, occlusion, seam depth, recess, protrusion, or cast shadow in the target website cameras. This normally includes separate sleds/modules, drive carriers or bay recesses, handles, bezels, rack ears, large ports, fan/PSU blocks, raised covers, and stepped chassis panels.

Fine flush printing may remain in a texture. Dense perforation may use geometry, a normal/height treatment, or a high-resolution opaque texture only when matched renders remain indistinguishable at the target camera distance.

A single beveled cuboid with six decorative planes is forbidden when source views show multi-part construction or relief.

## 8. Allowed and forbidden web optimization

Allowed when reference renders remain unchanged:

- remove completely hidden internal components;
- reduce subdivisions on visually flat surfaces;
- merge coplanar parts with identical material and no visible seam;
- compress meshes and textures without losing readable or identifying detail;
- remove unused data and generate mipmaps.

Forbidden:

- removing visible removable parts;
- replacing real bays, sleds, ports, fans, or PSUs with generic rectangles;
- merging separate modules so seams or depth disappear;
- flattening handles, recesses, or stepped panels that are visible in three-quarter views;
- replacing photo-real color with vector, toon, cel-shaded, or flat-color art;
- reducing texture resolution until labels, hole edges, grilles, or port structure become synthetic.

## 9. Immediate rejection conditions

Reject before delivery if any view shows:

- a generic server shape unrelated to the exact source;
- a correct real face photo existed but an AI-generated/stylized derivative was selected instead of a source-locked result;
- an earlier AI output or GLB render was treated as the primary style reference over a real photograph;
- wrong module/sled/drive count or nonexistent assembly;
- invented controls, displays, ports, labels, LEDs, or branding;
- copied/mirrored left-right layouts or a bottom copied from the top; a documented conservative generic-bottom fallback is allowed, but never a mirrored top;
- cartoon outlines, flat illustration shading, exaggerated bevels, or artificial color blocks;
- CGI cleanup, relighting, beautification, smoothing, denoising, color restyling, or any other departure from the primary real photograph's visual character;
- large blank panels where the real device has distinct mechanical structure;
- texture-only details that should create visible depth in a three-quarter view;
- a result that cannot be paired feature-for-feature with the identity inventory.

Do not downgrade these to warnings. The status is `REWORK` or `BLOCKED`.
