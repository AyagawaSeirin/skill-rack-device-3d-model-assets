# Exact-appearance fidelity contract

Read this before generating images or creating geometry. The deliverable is an exact exterior replica for website viewing, not a recognizable interpretation.

## 1. Meaning of “exact”

The model must match the requested real installed device configuration in every externally visible fact supported by the source set:

- silhouette and body proportions;
- enclosure, sled, node, controller, line-card, bay, blanking-panel, PSU, fan, and handle counts;
- row/column structure, spacing, recess/protrusion, and left/right order;
- port families, grilles, vents, seams, fasteners, latches, rack ears, and through-holes;
- factory colors, surface finish, logo, model badge, and readable markings;
- appearance from all six orthographic views and every authoritative three-quarter view.

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

### C6420 failure-prevention example

Dell's official C6420 specification describes a 2U platform with up to four C6420 compute nodes. The host is the C6400 chassis, and the visible assembly changes with the backplane option. The same document lists, among other options:

- 24 × 2.5-inch Direct Backplane, up to 6 drives per C6420 sled;
- 24 × 2.5-inch Expander Backplane, up to 12 drives per sled and 2 C6420 sleds per C6400 chassis;
- 24 × 2.5-inch NVMe Backplane with a specified NVMe/SAS/SATA mix per sled;
- 12 × 3.5-inch Direct Backplane, up to 3 drives per sled;
- no-backplane configuration.

Therefore `C6420` alone is insufficient. Lock the C6400 enclosure, backplane, drive layout, sled count, and rear configuration before modeling. Source: [Dell EMC PowerEdge C6420 Spec Sheet](https://i.dell.com/sites/doccontent/shared-content/data-sheets/en/Documents/PowerEdge_C6420_Spec_Sheet.pdf).

## 3. Visible-feature inventory gate

Create one row per visible component group before building:

```text
face,component,count,rows,columns,left_to_right_order,relative_size,
position,depth_or_relief,color_material,source_url,confidence
```

Enumerate rather than summarize. “Front has drives and vents” is insufficient; record exact counts, carrier style, row/column layout, status-panel side, handle shape, and blanking panels. For a modular enclosure, enumerate every installed and empty slot.

Do not start modeling while any major visible row has `confidence` below verified. Missing evidence becomes `BLOCKED`.

## 4. Source-lock rule

The approved exact-device sources are binding. Prefer operations that change the fewest factual pixels:

1. crop, rectify, and isolate an exact photo;
2. composite unobstructed regions from multiple exact photos of the same configuration;
3. bake or project exact-source color onto verified geometry;
4. use reference-preserving image editing only for perspective correction, missing margins, background, or small occlusions;
5. reject prompt-only or family-reference generation.

Image generation must not redesign the device. Discard an output if it introduces pseudo-text, new ports, decorative indicators, repeated patterns, changed component counts, mirrored branding, invented panel seams, or illustration-like surfaces.

## 5. Geometry fidelity rule

Use geometry wherever a feature creates visible silhouette, parallax, occlusion, seam depth, recess, protrusion, or cast shadow in the target website cameras. This normally includes separate sleds/modules, drive carriers or bay recesses, handles, bezels, rack ears, large ports, fan/PSU blocks, raised covers, and stepped chassis panels.

Fine flush printing may remain in a texture. Dense perforation may use geometry, a normal/height treatment, or a high-resolution opaque texture only when matched renders remain indistinguishable at the target camera distance.

A single beveled cuboid with six decorative planes is forbidden when source views show multi-part construction or relief.

## 6. Allowed and forbidden web optimization

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

## 7. Immediate rejection conditions

Reject before delivery if any view shows:

- a generic server shape unrelated to the exact source;
- wrong module/sled/drive count or nonexistent assembly;
- invented controls, displays, ports, labels, LEDs, or branding;
- copied/mirrored left-right layouts or duplicated top/bottom faces;
- cartoon outlines, flat illustration shading, exaggerated bevels, or artificial color blocks;
- large blank panels where the real device has distinct mechanical structure;
- texture-only details that should create visible depth in a three-quarter view;
- a result that cannot be paired feature-for-feature with the identity inventory.

Do not downgrade these to warnings. The status is `REWORK` or `BLOCKED`.
