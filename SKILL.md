---
name: skill-rack-device-3d-model-assets
description: Research, create, repair, and validate exact-model simplified GLB/GLTF assets for website display from verified dimensions and six evidence-based orthographic face textures. Use for rack servers, storage, switches, routers, firewalls, and similar equipment; do not use for engineering-grade CAD, generic concept art, or unverified look-alike models.
---

# Rack Device 3D Model Assets

Build a new, visually faithful, lightweight website model whose identity, proportions, six faces, orientation, opacity, and rack hardware can be traced to exact-model evidence. A polished approximation is still a failure.

## Route the work

- For source research, optional official-model discovery, six-face evidence, variants, and dimension interpretation, read [references/research-and-sources.md](references/research-and-sources.md).
- For image generation/editing, coordinate conventions, rack ears, mesh construction, UVs, materials, and optimization, read [references/textures-and-modeling.md](references/textures-and-modeling.md).
- For inspection, repair, viewer diagnosis, and final acceptance, read [references/quality-assurance.md](references/quality-assurance.md).
- When the user needs a reusable or one-round repair instruction, read [references/prompt-templates.md](references/prompt-templates.md).
- For front/rear elevation-specific source handling, also apply the exact-model invariants from the installed `rack-device-elevation-assets` skill when available. This skill extends that workflow to all six faces and the final GLB.

For an end-to-end build or batch, read all four references before producing final assets.

## Non-negotiable invariants

1. Resolve the exact manufacturer, full product identifier, generation suffix, U height, and physical variant before searching. Family photos and nearby model numbers are not interchangeable.
2. The primary deliverable is a newly constructed simplified model. Search for a public official 3D download or viewer during research, but report it only as an optional backup/source reference unless the user explicitly asks to use it. Finding an official GLB does not replace or complete the requested build.
3. Build from official dimensions and exact-model evidence for **front, rear, left, right, top, and bottom**. The other four faces may be reconstructed from multiple official three-quarter photos, manuals, exploded diagrams, videos, or technical drawings, but never invented from a generic metal box.
4. Record what is directly verified, what is reconstructed from multiple views, and what remains unknown. If a materially visible face cannot be verified, stop or obtain explicit approval for a labeled approximation.
5. Record body width, overall width, height, depth, and protrusions separately. State whether published dimensions include rack ears, handles, bezel, cable-management parts, power supplies, or rear handles. Never scale the chassis from a maximum-installation dimension without checking its scope.
6. Treat rack ears as separate mechanical parts. Front ears exist only when exact-model evidence confirms them. A rear photograph that sees the front ears in perspective does not prove rear ears. Do not add rear ears unless the real product has rear mounting brackets at that location.
7. Prefer geometric cutouts for rack-ear holes. If alpha is used, isolate it to the ear material and keep anti-aliased hole edges high resolution. Never remove pixels globally by color in a way that damages the chassis or turns screw heads, vents, logos, or labels transparent.
8. The exterior chassis and all six visible equipment surfaces are opaque. Dark vents and ports are dark pixels or geometry, not transparency. Use transparency only for real open holes or an external image background before texturing.
9. Preserve factory logos, readable labels, port order, bay count, grille pattern, colors, and left/right placement. Do not mirror a face. Text and logos must read normally in the final GLB, not merely in the source PNG.
10. Preserve the physical aspect ratio of every face: front/rear use width:height, left/right use depth:height, and top/bottom use width:depth. Do not force all six images to one canvas ratio or stretch compressed previews into textures.
11. Use a closed, outward-facing mesh with consistent normals. Do not expose an empty interior through a face, backface, alpha material, or detached panel. Simplification may omit removable component depth, but may not change silhouette or major face layout.
12. Use sRGB base-color textures with neutral color factors. For photo-derived faces, prefer `KHR_materials_unlit` when faithful website color is more important than relighting. Avoid metallic/lighting settings that make the GLB uniformly gray compared with its source textures.
13. Embed or deliberately package all required resources. A delivered `.glb` must not depend on accidental local file paths.
14. Validate the actual standard and web GLBs, not only `views/`, screenshots, or a pipeline report. A correct PNG does not prove correct UV orientation, material alpha, geometry, or embedded texture color.
15. Do not mark a model complete because one viewer looks acceptable. Inspect structure and render it in at least two independent glTF-capable viewers or renderers using front, rear, both sides, top, bottom, and three-quarter views.

## Required workflow

1. Build a target/evidence matrix and a separate list of any official 3D files found as optional alternatives.
2. Preserve downloads and source images. Record URLs, access dates, exact model/variant, source authority, and what each item proves.
3. Establish a dimension ledger before image or mesh work. Separate chassis dimensions from rack-ear and handle extents.
4. Produce and approve six canonical face assets. Use reference-preserving image editing/generation only when direct extraction is not possible.
5. Build the simplified mesh under the canonical coordinate convention. Keep ears, handles, body, and any alpha-requiring part separable.
6. Run structural audits on the six images and GLB, then visually compare rendered GLB faces against the approved sources.
7. Repair the causal layer. Do not edit a good `views/` PNG to compensate for a mirrored UV, or change viewer lighting to hide a bad material.
8. Deliver only after the completion gate passes, with an evidence and QA report plus optional official-file links found during research.

## Working layout

```text
<MODEL_KEY>/
├── source/
│   ├── originals/          official photos and documents, unchanged
│   ├── optional-3d/        official 3D files/links found; not the main build
│   └── evidence.md         URLs, dimensions, variants, inclusion rules
├── views/
│   ├── front.png
│   ├── rear.png
│   ├── left.png
│   ├── right.png
│   ├── top.png
│   └── bottom.png
├── model/
│   ├── <MODEL_KEY>.glb
│   └── <MODEL_KEY>-web.glb
└── qa/
    ├── audit.json
    └── renders/
```

Keep failed generations and intermediate crops outside `views/` and `model/`. Never overwrite an official source file.

## Completion gate

Finish only when the exact model/variant is proven; all six faces have traceable evidence; dimensions and rack-ear scope are resolved; source images retain physical aspect ratio; text is not mirrored; body surfaces are opaque; only true holes are transparent; front/rear hardware is physically correct; the newly built actual GLB passes structural inspection and multi-angle visual comparison; and all missing or approximate facts are explicitly reported. An official GLB may be listed as a backup but cannot substitute for these checks unless the user changes the task.
