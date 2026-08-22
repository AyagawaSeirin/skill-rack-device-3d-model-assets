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
10. Create `source/face-source-lock.csv` before image generation. For each face record its production mode, primary real photographic reference, URL/local path, SHA-256, exact configuration, supporting references, locked visual traits, and final output. Mark sources as real photo, official render, diagram, or AI derivative.
11. Never use an earlier AI-generated face, prior GLB texture, preview render, or processed stylized derivative as the primary source when a real exact-device photograph exists. Generated assets may be defect examples only, not identity or style evidence.
12. When an exact usable face photograph exists, production mode is `SOURCE_LOCKED_GENERATION`. Use that real photo as the primary binding reference for identity, layout, material, color, surface texture, photographic character, and style while imagegen creates the new orthographic transparent asset. Generation is required and allowed; style transformation is not.
13. `SOURCE_LOCKED_GENERATION` may change camera projection, external background, crop, and remove clearly non-factory surroundings, but it must preserve the real server's component counts/order, proportions, labels, logos, ports, metal/plastic texture, wear, color balance, highlight softness, shadows within recesses, and overall real product-photography appearance.
14. Only when no usable direct face photograph exists may production mode be `MULTI_REFERENCE_RECONSTRUCTION`, using multiple inspected exact-model real photos. The controlled bottom exception uses `GENERIC_BOTTOM_FALLBACK`. Make one built-in imagegen call per face and preserve genuine external transparency.
15. Generated face assets must remain in the same real photographic style as the primary reference, not merely satisfy a generic “photorealistic” adjective. Reject and regenerate CGI/product-render cleanup, illustration, toon/flat shading, relighting, beautification, symmetry correction, material smoothing, color restyling, denoising that erases texture, pseudo-text, invented displays/LEDs/ports, changed counts, or repeated AI patterns.
16. Every externally visible part that affects silhouette, depth, seam, shadow, or parallax in approved three-quarter views must exist as correctly placed geometry or faithful relief. Do not deliver a beveled box with six decorative images when the real product has separate sleds, bays, handles, bezels, panels, or recesses.
17. Treat rack ears as separate mechanical parts. Front ears exist only when exact evidence confirms them. A rear photograph that sees the front ears in perspective does not prove rear ears.
18. Prefer geometric cutouts for rack-ear holes. If alpha is used, isolate it to the ear material and keep anti-aliased hole edges high resolution. Never globally delete colors that also occur on the chassis.
19. All six visible equipment surfaces are opaque. Dark vents and ports are dark pixels or geometry, not transparency. Use transparency only for real open holes or the external transparent canvas around the face asset.
20. Preserve logos, readable labels, component order, counts, colors, and left/right placement. Do not mirror a face. Text must read normally in the final GLB, not merely in the generated PNG.
21. Preserve every face's physical aspect ratio. Do not force six images to one canvas ratio, stretch compressed previews, or reduce texture resolution until identifying details disappear.
22. Use a closed outward-facing mesh with consistent normals. Do not expose an empty interior. Do not omit visible drives, fans, PSUs, sled fronts, handles, or bezels merely because they are removable.
23. Use source-matched materials without toon outlines, flat illustration shading, exaggerated bevels, synthetic color blocks, or a generated visual style. Use sRGB base-color textures with neutral factors; choose unlit or PBR only after matching reference renders.
24. Optimize only invisible internals, redundant topology, compression, and file packaging. The standard and web GLBs must retain the same externally visible form and source-photograph appearance.
25. Validate the actual GLBs in at least two independent viewers. Compare matched-camera renders against the locked primary real sources using side-by-side, overlay, and feature-count review; previews alone cannot pass.

## Required workflow

1. Freeze an assembly identity manifest. If the requested installed configuration is ambiguous, mark it `BLOCKED` before image generation or modeling.
2. Build a source matrix, dimension ledger, and visible-feature inventory. Search official sources first, read/render official PDFs with the PDF skill, use Browser for interactive/dynamic pages, then search and cross-check third-party commerce/marketplace sources.
3. Preserve downloads unchanged. Render relevant PDF pages, inspect every raster reference, classify real versus AI-derived material, and record URL, page/figure, access date, exact configuration, authority, source class, face/angle, and the feature it proves.
4. Lock each face to `SOURCE_LOCKED_GENERATION`, `MULTI_REFERENCE_RECONSTRUCTION`, or `GENERIC_BOTTOM_FALLBACK`. If a usable real face photo exists, it must be the primary binding identity-and-style reference and takes precedence over every generated derivative.
5. Invoke built-in imagegen once per face under its locked mode. Generate a new orthographic transparent asset while explicitly locking the real source's structure, materials, photographic texture, color and style. Reject outputs with any factual or source-style drift.
6. Build the full visible exterior under the canonical coordinate convention. Keep independently shaped assemblies, ears, handles, body panels, and any alpha-requiring part separable.
7. Render a draft GLB from the same six orthographic cameras plus matched source-photo three-quarter cameras. Create comparison sheets and repair every unmatched feature or material before optimization.
8. Run structural audits on six images and both GLBs. Repair the causal layer rather than replacing correct source-locked assets or hiding a bad material with viewer lighting.
9. Deliver only after source-lineage, exact-appearance, and structural gates pass, with identity, evidence, `face-source-lock.csv`, PDF page references, imagegen edit/generation mode, input roles and final prompts, feature inventory, six transparent PNGs, comparison sheets, QA report, and optional official-file links.

## Working layout

```text
<MODEL_KEY>/
├── source/
│   ├── originals/          official photos and documents, unchanged
│   ├── optional-3d/        official 3D files/links found; not the main build
│   ├── pdf-pages/          rendered relevant PDF pages used as references
│   ├── third-party/        inspected reseller/marketplace/other images
│   ├── identity-manifest.md
│   ├── face-source-lock.csv
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

Finish when exact configuration is proven; each face's lineage and mode are recorded; every available exact face photograph remains the primary binding identity-and-style reference; the generated assets preserve the real device's photographic appearance and factual details; every identity-bearing feature is correct; and both GLBs pass source-photo comparisons in two viewers. If a correct real face photo was found but the final generated texture changes its visual style, materials, layout, or device identity, status is `REWORK` regardless of how polished it looks. Non-bottom evidence gaps remain `BLOCKED`; the documented bottom fallback remains the only built-in exception.
