# Research, official sources, and dimensions

Read this guide before downloading, generating, or modeling an exact device.

## 1. Define one row per physical variant

Record at least:

| Field | Required decision |
|---|---|
| Manufacturer and exact PID | Preserve suffixes such as Gen10, V3, V5, EI, FX2, Plus |
| Equipment type and U height | Server, storage, switch, router, firewall, chassis, module |
| Delivery subject | Complete appliance, enclosure with installed modules, or standalone module |
| Host/module relationship | Host chassis, module/sled model, installed quantity and positions |
| Front variant | SFF/LFF, bay count, bezel state, line-card configuration |
| Rear variant | PSU, riser, controller, node, fan, or port configuration |
| Installed configuration | Backplane, drive count, blanking panels, power/fan state |
| Optional official 3D | URL, format, exact PID match, and usage terms; not the main deliverable |
| Six required faces | Evidence status for front, rear, left, right, top, bottom |
| Dimensions | Body and overall W/H/D, units, tolerance, and inclusion notes |
| Delivery target | GLB name, web budget, viewer support, coordinate convention |

Do not merge variants because their family name is similar. A shared rear may be reused only after documentation proves it is physically identical. For a modular product, do not continue until the host enclosure and installed module configuration are explicit.

## 2. Resolve appliance, enclosure, and module identity

Product marketing often names a compute sled, controller, blade, line card, or storage node even though the visible rack unit is a separate enclosure. Search the official installation/owner's manual for terms such as `enclosure`, `chassis`, `sled`, `node`, `module`, `appliance`, `backplane`, and `supported configuration`.

Record:

- whether the requested model has its own rack enclosure;
- the exact host enclosure if it does not;
- valid installed module counts and slot positions;
- which front backplane/drive option corresponds to which module count;
- which rear face belongs to that same front configuration;
- whether product dimensions refer to the module, host, or fully installed assembly.

If the request gives only a module model and multiple real rack assemblies are possible, stop as `BLOCKED` rather than selecting the most visually convenient option.

## 3. Search official 3D assets as a backup

The requested workflow constructs a new exact-appearance exterior model. During research, still search current official product pages, media libraries, support downloads, AR/3D viewers, CAD/BIM portals, Visio pages, and installation tools. Useful queries include:

- `site:<vendor-domain> "<exact PID>" 3D`, `AR`, `GLB`, `glTF`, `CAD`, `STEP`, `OBJ`, `FBX`
- `site:<vendor-domain> "<exact PID>" dimensions`
- `site:<vendor-domain> "<exact PID>" hardware installation guide PDF`
- `site:<vendor-domain> "<exact PID>" datasheet PDF`, `whitepaper PDF`, `owner manual PDF`, `installation PDF`
- `"<exact PID>" front rear side top`

An official interactive viewer can load a GLB or glTF that is not exposed as a visible download button. Inspect its public network resources when permitted, but do not bypass authentication, access controls, licensing checks, or private APIs. Record the viewer page and direct public asset URL. If downloaded, preserve the original file, byte size, and SHA-256 checksum.

Report an exact official model as an optional alternative and potentially authoritative visual reference. Do not automatically substitute it for the newly built model, copy its mesh into the main deliverable, or call the task complete. Use or derive from it only when the user explicitly changes that scope.

Do not call an AI reconstruction “official.”

## 4. Escalate with Browser and third-party sources

Do not conclude that imagery is unavailable merely because ordinary search results or official page text are sparse.

1. Use the available connector, search/API, or direct download path when it can retrieve the semantic content.
2. When an official or third-party page is JavaScript-rendered, interactive, gallery-driven, poorly indexed, or hides views behind tabs/carousels, use the available Browser skill. Follow its surface-selection rules, inspect the visible rendered page, open image galleries, switch product-view tabs, and capture the underlying high-resolution image or a faithful screenshot when direct download is unavailable.
3. If official sources still do not cover a face, search exact-model authorized distributors, refurbishers, used-equipment dealers, auction listings, shopping platforms, review sites, teardown posts, and product videos. Useful queries include the exact PID plus `used`, `for sale`, `listing`, `underside`, `bottom`, `left side`, `right side`, `top`, `rear`, `teardown`, and local-language equivalents.
4. Shopping and marketplace pages are evidence only when the listing can be tied to the exact model/configuration through a readable badge, PID, chassis layout, or corroborating documentation. Watch for stock family images, seller-combined galleries, replacement parts, damaged units, missing modules, custom stickers, and mismatched front/rear photos.
5. Cross-check a third-party view against a second independent exact-model source or against verified landmarks/dimensions from official documentation. Record disagreements instead of choosing the cleaner image.

Do not bypass authentication, access controls, anti-bot challenges, or private resources. If one page is blocked, continue with other public official or third-party sources.

## 5. Evidence hierarchy for the new build

Prefer evidence in this order:

1. exact-model official color photos, manuals, 3D viewers, CAD screenshots, product videos, exploded diagrams, and mechanical drawings;
2. exact-PID authorized distributor/reseller or vendor-certified refurbisher photography;
3. exact-model independent retailer, shopping-platform, auction, used-equipment, review, teardown, or video imagery that passes identity and configuration cross-checks;
4. exact-model regulatory filings and service/parts imagery for hidden faces;
5. family diagrams only as leads, except for the controlled bottom fallback after search exhaustion.

Use image search only for discovery; open and record the underlying page. Search in English and the vendor's local language when useful.

For every source record, include the installed configuration rather than only the family model:

```text
URL:
accessed_at:
claimed_model:
variant:
view_or_dimension:
authority: official | authorized | secondary
source_class: manual | product-page | browser-gallery | retailer | marketplace | auction | used-equipment | video | regulatory | generic-bottom-fallback
visual_origin: real-photograph | official-render | technical-diagram | AI-generated-derivative
primary_identity_style_reference: yes | no
pdf_page_or_figure:
image_inspection_notes:
proves:
limitations:
```

For each face, retain at least one exact-configuration color source. A straight photo is preferred; if the face is reconstructed from perspective, retain at least two exact-configuration angles that jointly prove both edges and every major feature. Diagrams may constrain geometry but cannot establish color or material alone.

## 6. Read PDFs and inspect images

Official product evidence is often embedded in datasheets, whitepapers, quick-specs, installation guides, owner's manuals, service manuals, and mechanical PDFs. When a relevant PDF is found:

1. use the available PDF skill;
2. extract searchable text with `pypdf`/`pdfplumber` for exact dimensions, configuration tables, captions, part numbers, and inclusion notes;
3. render every relevant page to PNG with the PDF workflow because text extraction does not preserve image/layout meaning;
4. inspect rendered pages at high/original detail with the image-viewing capability;
5. crop product views or diagrams only as reference inputs, never as the sole final face-production step;
6. record PDF URL, document title/version/date, page number, figure/caption, exact PID/configuration, and what the visual proves.

Inspect every downloaded web image, browser screenshot, PDF-page render, shopping image, and user-provided source with the image-viewing capability before accepting it. Check:

- exact model badge/PID and whether the photo is a family stock image;
- face or camera angle and which adjacent surfaces are visible;
- installed module/drive/PSU/fan configuration;
- left/right orientation and readable logo/text;
- seller stickers, cables, rails, damage, replacement parts, or missing modules;
- resolution, compression, crop, perspective, watermark, and whether detail survives use as an imagegen reference.

Do not treat filenames, alt text, search thumbnails, PDF text extraction, or seller titles as visual proof without image inspection.

## 7. Lock primary real sources before generation

Create `face-source-lock.csv` with:

```text
face,production_mode,primary_source_path,primary_source_url,sha256,
visual_origin,exact_pid_configuration,locked_visual_traits,
supporting_source_paths,final_output_path
```

Use `SOURCE_LOCKED_GENERATION` when a usable direct real photograph of that face exists. That photograph is the highest-authority reference for both device facts and photographic style. Use `MULTI_REFERENCE_RECONSTRUCTION` only when no direct face photograph exists, and use `GENERIC_BOTTOM_FALLBACK` only under its documented rules.

Do not promote an earlier AI-generated image, processed texture, GLB render, preview, reseller illustration, CAD-looking render, or search thumbnail over an exact real photograph. Preserve such assets only as rejected derivatives or supporting geometry leads, never as primary identity/style evidence.

## 8. Six-face evidence rules

Front and rear straight-on images are not enough for a six-sided model.

- **Front/rear:** use exact-model elevations or near-orthogonal photographs. Confirm logo side, port/bay order, rack ears, handles, PSU/riser layout, and model badge.
- **Left/right:** use exact-model side photos, installation diagrams, rail/cover removal instructions, regulatory label views, or multiple three-quarter images. The two sides may have different vents, labels, latches, or rail slots.
- **Top:** use top/cover photos, service-manual cover diagrams, or multiple elevated three-quarter views. Confirm seams, cover latches, vents, and raised regions.
- **Bottom:** search official mechanical drawings, rail/feet diagrams, regulatory photos, videos, service imagery, browser-only galleries, and exact-model third-party/marketplace underside photos. If these searches are documented and still yield no usable bottom evidence, a controlled generic bottom is allowed instead of blocking. Prefer a same-vendor/same-family/same-U underside reference; otherwise use a conservative generic sheet-metal bottom matching verified width, depth, color, and material. Do not copy the top, add branding, labels, vents, feet, holes, rails, or protrusions that are not supported. The fallback must not change any verified side silhouette or three-quarter view.

Three-quarter photos are supporting evidence, not textures to stretch flat. Use multiple exact-configuration angles to resolve silhouette, relief, and feature placement, then create the canonical orthographic face. A front, rear, left, right, or top face built from insufficient evidence remains `BLOCKED`; only the documented bottom fallback is exempt.

## 9. Dimension ledger and inclusion rules

Prefer official datasheets, hardware installation guides, mechanical drawings, and regulatory documents. Record the quoted wording and units, then normalize to millimeters without discarding the source value.

Maintain separate fields:

```text
body_width_mm:
overall_width_mm:
height_mm:
body_depth_mm:
overall_depth_mm:
front_projection_mm:
rear_projection_mm:
rack_ear_left_extension_mm:
rack_ear_right_extension_mm:
published_dimension_includes:
source_url:
```

For modular systems, maintain separate dimension rows for the host enclosure, standalone module, and fully installed assembly. The GLB bounds must be compared to the dimensions of the actual delivery subject.

Resolve these common ambiguities:

- rack ears or mounting flanges included in width;
- front bezel, drive handles, release levers, and air filters included in depth;
- rear PSU handles, fan modules, power connectors, and cable-management parts included in depth;
- shipping dimensions confused with product dimensions;
- nominal rack height such as `1U` confused with the chassis's actual clearance height;
- inches rounded differently from millimeters;
- body width confused with the 19-inch rack mounting span.

Use official numeric dimensions for the body. Use image measurement only for the relative size and placement of ears or small protrusions, anchored to a verified known dimension. Record the assumption and tolerance.

## 10. Feature-level source matrix

Before generation, create `feature-inventory.csv` with one row per component group. Include exact count, row/column arrangement, left-to-right order, relative size, position, depth/relief, material/color, source URL, and confidence. Cover at minimum:

- drive carriers, blanking panels, sleds/nodes, and bezels;
- PSUs, fans, risers, controllers, and rear modules;
- every port group, status/control panel, management module, and large grille;
- handles, latches, rack ears, mounting holes, cover seams, labels, and visible fasteners.

Do not summarize a dense face as “ports and vents.” The inventory is the build specification and later the QA checklist.

## 11. Front/rear elevation guidance

The reference project [skill-rack-device-assets](https://github.com/AyagawaSeirin/skill-rack-device-assets) supplies the baseline exact-model rules for front/rear transparent PNG assets: preserve variants and branding, use straight orthographic views, retain only real complete rack ears, avoid generic hybrids, and validate transparency/cropping. Apply those principles to this workflow, then add the four other verified faces and final-GLB checks.

When the local `rack-device-elevation-assets` skill is available, read its research and QA references for front/rear-specific work rather than duplicating ad hoc rules.

## 12. Stop conditions

Stop and report the strongest available evidence when:

- the exact PID cannot be distinguished from a family member;
- the requested module is not tied to a verified host enclosure and installed configuration;
- official dimensions conflict and the inclusion scope cannot be resolved;
- a materially visible front, rear, left, right, or top face lacks exact-model evidence after Browser and third-party escalation;
- the requested drive, controller, line-card, or rear configuration is not documented;
- an official source is access-controlled and cannot be obtained without new authority.

Do not fill identity-bearing gaps with a visually plausible guess. Missing bottom evidence alone does not block completion: record the searches, use `source_class: generic-bottom-fallback`, keep the bottom conservative and non-identifying, and report `PASS_WITH_BOTTOM_FALLBACK`. Any broader approximation must be a separately named deliverable and cannot receive an exact-replica `PASS`.
