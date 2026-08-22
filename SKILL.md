---
name: skill-rack-device-3d-model-assets
description: Research, create, repair, and validate exact-appearance web-ready GLB/GLTF replicas of specific rack-device models and installed configurations from authoritative dimensions and multi-angle visual evidence. Use for servers, storage, switches, routers, firewalls, and modular chassis; do not use for generic concept art, stylized approximations, or engineering/internal CAD.
---

# Rack Device 3D Model Assets

Build a new website-ready **exact exterior replica** whose visible geometry, installed configuration, proportions, six faces, orientation, materials, branding, and rack hardware match the real device. “Web-ready” permits performance optimization; it never permits visual simplification. A polished, plausible, or same-family approximation is a failure.

## Route the work

- For source research, optional official-model discovery, six-face evidence, variants, and dimension interpretation, read [references/research-and-sources.md](references/research-and-sources.md).
- Before modeling, read [references/exact-appearance-contract.md](references/exact-appearance-contract.md) and satisfy its assembly-identity and visible-feature gates.
- For image generation/editing, coordinate conventions, rack ears, mesh construction, UVs, materials, and optimization, read [references/textures-and-modeling.md](references/textures-and-modeling.md).
- For inspection, repair, viewer diagnosis, and final acceptance, read [references/quality-assurance.md](references/quality-assurance.md).
- When the user needs a reusable or one-round repair instruction, read [references/prompt-templates.md](references/prompt-templates.md).
- For front/rear elevation-specific source handling, also apply the exact-model invariants from the installed `rack-device-elevation-assets` skill when available. This skill extends that workflow to all six faces and the final GLB.

For an end-to-end build or batch, read all five references before producing final assets.

## Non-negotiable invariants

1. Resolve the exact manufacturer, full product identifier, generation suffix, U height, physical variant, and **delivery subject** before searching. Family photos and nearby model numbers are not interchangeable.
2. For modular systems, resolve the complete assembly: enclosure/host chassis, node or sled model, installed node count and positions, front backplane/drive option, rear module option, bezel state, blanking panels, and power/fan configuration. A module model name alone does not define a rack-level appearance.
3. The primary deliverable is a newly constructed exact-appearance model. Search for a public official 3D download or viewer, but report it only as an optional backup/source reference unless the user explicitly asks to use it.
4. Build from official dimensions and exact-model/configuration evidence for **front, rear, left, right, top, and bottom**. Reconstruct a face only when multiple exact-device sources jointly prove every visible feature; never fill gaps with a generic chassis, symmetry, repeated texture, or design convention.
5. Create a visible-feature inventory before modeling. Counts, rows/columns, sizes, positions, colors, recess/protrusion, and source evidence must be exact for drive bays, sleds, PSUs, fans, ports, grilles, handles, latches, screws, seams, labels, and blanking panels.
6. Record body width, overall width, height, depth, and protrusions separately. State whether published dimensions include rack ears, handles, bezel, cable-management parts, power supplies, or rear handles. Never scale from a maximum-installation or shipping dimension without checking its scope.
7. The six source assets must be photorealistic, reference-preserving reconstructions. Prefer rectification, compositing, or texture baking from exact photos. Do not generate a whole face from the model name, redraw it as vector art, or accept pseudo-text, invented displays, decorative LEDs, generic ports, or repeated AI patterns.
8. Every externally visible part that affects silhouette, depth, seam, shadow, or parallax in the approved three-quarter views must exist as correctly placed geometry or faithful relief. Do not deliver a beveled box with six decorative images when the real product has separate sleds, bays, handles, bezels, panels, or recesses.
9. Treat rack ears as separate mechanical parts. Front ears exist only when exact evidence confirms them. A rear photograph that sees the front ears in perspective does not prove rear ears.
10. Prefer geometric cutouts for rack-ear holes. If alpha is used, isolate it to the ear material and keep anti-aliased hole edges high resolution. Never globally delete colors that also occur on the chassis.
11. All six visible equipment surfaces are opaque. Dark vents and ports are dark pixels or geometry, not transparency. Use transparency only for real open holes or an external image background before texturing.
12. Preserve logos, readable labels, component order, counts, colors, and left/right placement. Do not mirror a face. Text must read normally in the final GLB, not merely in the source PNG.
13. Preserve every face's physical aspect ratio. Do not force six images to one canvas ratio, stretch compressed previews, or reduce texture resolution until identifying details disappear.
14. Use a closed outward-facing mesh with consistent normals. Do not expose an empty interior. Do not omit visible drives, fans, PSUs, sled fronts, handles, or bezels merely because they are removable.
15. Use photoreal materials without toon outlines, flat illustration shading, exaggerated bevels, or synthetic color blocks. Use sRGB base-color textures with neutral factors; choose unlit or PBR only after matching reference renders.
16. Optimize only invisible internals, redundant topology, compression, and file packaging. The standard and web GLBs must retain the same externally visible form and reference-level appearance.
17. Validate the actual GLBs in at least two independent viewers. Compare matched-camera renders against exact source views using side-by-side, overlay, and feature-count review; previews alone cannot pass.

## Required workflow

1. Freeze an assembly identity manifest. If the requested installed configuration is ambiguous, mark it `BLOCKED` before image generation or modeling.
2. Build a source matrix, dimension ledger, and visible-feature inventory; list official 3D files only as optional alternatives.
3. Preserve exact-device downloads and source images unchanged. Record URLs, access dates, exact configuration, authority, and the feature each source proves.
4. Produce six photoreal canonical face assets and reject any face whose counts, layout, branding, material, or text differs from the exact source.
5. Build the full visible exterior under the canonical coordinate convention. Keep independently shaped assemblies, ears, handles, body panels, and any alpha-requiring part separable.
6. Render a draft GLB from the same six orthographic cameras plus matched official three-quarter cameras. Create comparison sheets and repair every unmatched visible feature before export optimization.
7. Run structural audits on six images and both GLBs. Repair the causal layer rather than editing a good PNG to compensate for bad UVs or hiding a bad material with viewer lighting.
8. Deliver only after exact-appearance and structural gates pass, with identity, evidence, feature inventory, comparison sheets, QA report, and optional official-file links.

## Working layout

```text
<MODEL_KEY>/
├── source/
│   ├── originals/          official photos and documents, unchanged
│   ├── optional-3d/        official 3D files/links found; not the main build
│   ├── identity-manifest.md
│   ├── feature-inventory.csv
│   └── evidence.md         URLs, dimensions, configuration, inclusion rules
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
    ├── reference/
    ├── renders/
    └── comparisons/
```

Keep failed generations and intermediate crops outside `views/` and `model/`. Never overwrite an official source file.

## Completion gate

Finish only when the exact installed configuration is proven; every visible feature in all six faces and available three-quarter sources is present with correct count, shape, position, depth, material, and branding; dimensions and rack hardware are resolved; no stylization, invention, mirroring, transparency defect, or texture compression damage remains; and the actual standard and web GLBs pass matched-camera comparisons in two viewers. Unknown visible facts require `BLOCKED`, not an approximate `PASS`. An official GLB may be listed as a backup but cannot substitute unless the user changes the task.
