---
name: skill-rack-device-3d-model-assets
description: Research, create, repair, and validate exact-appearance web-ready GLB/GLTF replicas of specific rack-device models and installed configurations from authoritative dimensions and multi-angle visual evidence. Use for servers, storage, switches, routers, firewalls, and modular chassis; do not use for generic concept art, stylized approximations, or engineering/internal CAD.
---

# Rack Device 3D Model Assets

Build a new website-ready **exact exterior replica** whose visible geometry, installed configuration, proportions, six faces, orientation, materials, branding, and rack hardware match the real device. “Web-ready” permits performance optimization; it never permits visual simplification. A polished, plausible, or same-family approximation is a failure.

## Route the work

- For source research, optional official-model discovery, six-face evidence, variants, and dimension interpretation, read [references/research-and-sources.md](references/research-and-sources.md).
- Before modeling, read [references/exact-appearance-contract.md](references/exact-appearance-contract.md) and satisfy its assembly-identity and visible-feature gates.
- For canonical transparent face generation, coordinate conventions, rack ears, mesh construction, UVs, materials, and optimization, read [references/textures-and-modeling.md](references/textures-and-modeling.md). Canonical face assets require the `imagegen` skill and built-in image generation path.
- When official whitepapers, datasheets, installation guides, manuals, or other PDFs are sources, use the `pdf` skill to extract text and render relevant pages, then inspect those page images with the available image-viewing capability.
- For inspection, repair, viewer diagnosis, and final acceptance, read [references/quality-assurance.md](references/quality-assurance.md).
- When the user needs a reusable or one-round repair instruction, read [references/prompt-templates.md](references/prompt-templates.md).
- For front/rear elevation-specific source handling, also apply the exact-model invariants from the installed `rack-device-elevation-assets` skill when available. This skill extends that workflow to all six faces and the final GLB.

For an end-to-end build or batch, read all five references before producing final assets.

## Non-negotiable invariants

1. Resolve the exact manufacturer, full product identifier, generation suffix, U height, physical variant, and **delivery subject** before searching. Family photos and nearby model numbers are not interchangeable.
2. For modular systems, resolve the complete assembly: enclosure/host chassis, node or sled model, installed node count and positions, front backplane/drive option, rear module option, bezel state, blanking panels, and power/fan configuration. A module model name alone does not define a rack-level appearance.
3. The primary deliverable is a newly constructed exact-appearance model. Search for a public official 3D download or viewer, but report it only as an optional backup/source reference unless the user explicitly asks to use it.
4. Escalate source research instead of stopping at ordinary official-domain search. When pages are interactive, script-rendered, gallery-driven, or poorly indexed, use the available Browser skill to inspect the rendered page and image galleries. When official imagery is insufficient, search exact-model authorized resellers, refurbishers, used-equipment sellers, auction sites, shopping platforms, and other third-party pages, then cross-check configuration and provenance.
5. Build from authoritative dimensions and exact-model/configuration evidence for **front, rear, left, right, top, and bottom**. Reconstruct a face only when multiple exact-device sources jointly prove visible features. The sole evidence exception is the controlled generic-bottom fallback defined in the references after official, interactive-browser, and third-party searches are exhausted.
6. Create a visible-feature inventory before modeling. Counts, rows/columns, sizes, positions, colors, recess/protrusion, and source evidence must be exact for drive bays, sleds, PSUs, fans, ports, grilles, handles, latches, screws, seams, labels, and blanking panels.
7. Record body width, overall width, height, depth, and protrusions separately. State whether published dimensions include rack ears, handles, bezel, cable-management parts, power supplies, or rear handles. Never scale from a maximum-installation or shipping dimension without checking its scope.
8. Treat PDFs as both textual and visual evidence. Use PDF text extraction for dimensions/configuration and render the relevant pages to images for diagrams and product views; inspect those images rather than relying on extracted text, filenames, captions, or thumbnails alone.
9. Inspect every downloaded photo, screenshot, PDF-page render, and user-provided image at high/original detail with the image-viewing capability. Classify exact PID, installed configuration, face/angle, visible adjacent faces, resolution, cropping, seller modifications, and what the image actually proves before using it.
10. Create the canonical `front.png`, `rear.png`, `left.png`, `right.png`, `top.png`, and `bottom.png` with the `imagegen` skill, using the collected online/PDF images as explicitly labeled binding references. Use the built-in image-generation tool by default and make one call per face. Cropping, rectification, compositing, screenshots, and local background removal may prepare references but do not replace reference-guided image generation. Request a genuinely transparent background and preserve alpha.
11. The generated face assets must be photorealistic and reference-preserving. Do not generate from only the model name, redraw as vector art, or accept pseudo-text, invented displays, decorative LEDs, generic ports, changed counts, or repeated AI patterns. Compare each output against its references and regenerate with a targeted correction when it drifts.
12. Every externally visible part that affects silhouette, depth, seam, shadow, or parallax in approved three-quarter views must exist as correctly placed geometry or faithful relief. Do not deliver a beveled box with six decorative images when the real product has separate sleds, bays, handles, bezels, panels, or recesses.
13. Treat rack ears as separate mechanical parts. Front ears exist only when exact evidence confirms them. A rear photograph that sees the front ears in perspective does not prove rear ears.
14. Prefer geometric cutouts for rack-ear holes. If alpha is used, isolate it to the ear material and keep anti-aliased hole edges high resolution. Never globally delete colors that also occur on the chassis.
15. All six visible equipment surfaces are opaque. Dark vents and ports are dark pixels or geometry, not transparency. Use transparency only for real open holes or the external transparent canvas around the generated face asset.
16. Preserve logos, readable labels, component order, counts, colors, and left/right placement. Do not mirror a face. Text must read normally in the final GLB, not merely in the generated PNG.
17. Preserve every face's physical aspect ratio. Do not force six images to one canvas ratio, stretch compressed previews, or reduce texture resolution until identifying details disappear.
18. Use a closed outward-facing mesh with consistent normals. Do not expose an empty interior. Do not omit visible drives, fans, PSUs, sled fronts, handles, or bezels merely because they are removable.
19. Use photoreal materials without toon outlines, flat illustration shading, exaggerated bevels, or synthetic color blocks. Use sRGB base-color textures with neutral factors; choose unlit or PBR only after matching reference renders.
20. Optimize only invisible internals, redundant topology, compression, and file packaging. The standard and web GLBs must retain the same externally visible form and reference-level appearance.
21. Validate the actual GLBs in at least two independent viewers. Compare matched-camera renders against exact source views using side-by-side, overlay, and feature-count review; previews alone cannot pass.

## Required workflow

1. Freeze an assembly identity manifest. If the requested installed configuration is ambiguous, mark it `BLOCKED` before image generation or modeling.
2. Build a source matrix, dimension ledger, and visible-feature inventory. Search official sources first, read/render official PDFs with the PDF skill, use Browser for interactive/dynamic pages, then search and cross-check third-party commerce/marketplace sources.
3. Preserve downloads unchanged. Render relevant PDF pages, inspect every raster reference with the image-viewing capability, and record URL, PDF page/figure when applicable, access date, exact configuration, authority, source class, view/angle, and the feature it proves.
4. For each face, label image inputs by role and invoke the built-in image-generation tool through the `imagegen` skill to generate a high-resolution transparent-background orthographic PNG. Reject and regenerate outputs whose counts, layout, branding, material, text, opacity, or orientation differs from the binding references. If only bottom evidence is unavailable after escalation, feed suitable generic-bottom references into image generation and mark the output explicitly.
5. Build the full visible exterior under the canonical coordinate convention. Keep independently shaped assemblies, ears, handles, body panels, and any alpha-requiring part separable.
6. Render a draft GLB from the same six orthographic cameras plus matched official three-quarter cameras. Create comparison sheets and repair every unmatched visible feature before export optimization.
7. Run structural audits on six images and both GLBs. Repair the causal layer rather than editing a good PNG to compensate for bad UVs or hiding a bad material with viewer lighting.
8. Deliver only after exact-appearance and structural gates pass, with identity, evidence, PDF page references, imagegen input roles and final prompts, feature inventory, six generated transparent PNGs, comparison sheets, QA report, and optional official-file links.

## Working layout

```text
<MODEL_KEY>/
├── source/
│   ├── originals/          official photos and documents, unchanged
│   ├── optional-3d/        official 3D files/links found; not the main build
│   ├── pdf-pages/          rendered relevant PDF pages used as references
│   ├── third-party/        inspected reseller/marketplace/other images
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
    ├── imagegen-prompts/
    ├── reference/
    ├── renders/
    └── comparisons/
```

Keep failed generations and intermediate crops outside `views/` and `model/`. Never overwrite an official source file.

## Completion gate

Finish when the exact installed configuration is proven; every identity-bearing visible feature is present with correct count, shape, position, depth, material, and branding; dimensions and rack hardware are resolved; no stylization, invention, mirroring, transparency defect, or texture compression damage remains; and the actual standard and web GLBs pass matched-camera comparisons in two viewers. An unresolved front, rear, side, top, silhouette, or installed configuration requires `BLOCKED`. An unresolved bottom may complete only as `PASS_WITH_BOTTOM_FALLBACK` after documented official, Browser-assisted, and third-party searches and a conservative fallback that does not alter the verified silhouette. An official GLB remains an optional backup unless the user changes the task.
