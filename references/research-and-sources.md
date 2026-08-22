# Research, official sources, and dimensions

Read this guide before downloading, generating, or modeling an exact device.

## 1. Define one row per physical variant

Record at least:

| Field | Required decision |
|---|---|
| Manufacturer and exact PID | Preserve suffixes such as Gen10, V3, V5, EI, FX2, Plus |
| Equipment type and U height | Server, storage, switch, router, firewall, chassis, module |
| Front variant | SFF/LFF, bay count, bezel state, line-card configuration |
| Rear variant | PSU, riser, controller, node, fan, or port configuration |
| Optional official 3D | URL, format, exact PID match, and usage terms; not the main deliverable |
| Six required faces | Evidence status for front, rear, left, right, top, bottom |
| Dimensions | Body and overall W/H/D, units, tolerance, and inclusion notes |
| Delivery target | GLB name, web budget, viewer support, coordinate convention |

Do not merge variants because their family name is similar. A shared rear may be reused only after documentation proves it is physically identical.

## 2. Search official 3D assets as a backup

The requested workflow constructs a new simplified model. During research, still search current official product pages, media libraries, support downloads, AR/3D viewers, CAD/BIM portals, Visio pages, and installation tools. Useful queries include:

- `site:<vendor-domain> "<exact PID>" 3D`, `AR`, `GLB`, `glTF`, `CAD`, `STEP`, `OBJ`, `FBX`
- `site:<vendor-domain> "<exact PID>" dimensions`
- `site:<vendor-domain> "<exact PID>" hardware installation guide PDF`
- `"<exact PID>" front rear side top`

An official interactive viewer can load a GLB or glTF that is not exposed as a visible download button. Inspect its public network resources when permitted, but do not bypass authentication, access controls, licensing checks, or private APIs. Record the viewer page and direct public asset URL. If downloaded, preserve the original file, byte size, and SHA-256 checksum.

Report an exact official model as an optional alternative and potentially authoritative visual reference. Do not automatically substitute it for the newly built model, copy its mesh into the main deliverable, or call the task complete. Use or derive from it only when the user explicitly changes that scope.

Do not call an AI reconstruction “official.”

## 3. Evidence hierarchy for the new build

Prefer evidence in this order:

1. exact-model official color photos, manuals, 3D viewers, CAD screenshots, product videos, exploded diagrams, and mechanical drawings;
2. exact-PID official distributor or authorized-reseller photography;
3. exact-model regulatory filings or reputable used-equipment photos for hidden faces;
4. family diagrams only as leads, never as conclusive identity evidence.

Use image search only for discovery; open and record the underlying page. Search in English and the vendor's local language when useful.

For every source record:

```text
URL:
accessed_at:
claimed_model:
variant:
view_or_dimension:
authority: official | authorized | secondary
proves:
limitations:
```

## 4. Six-face evidence rules

Front and rear straight-on images are not enough for a six-sided model.

- **Front/rear:** use exact-model elevations or near-orthogonal photographs. Confirm logo side, port/bay order, rack ears, handles, PSU/riser layout, and model badge.
- **Left/right:** use exact-model side photos, installation diagrams, rail/cover removal instructions, regulatory label views, or multiple three-quarter images. The two sides may have different vents, labels, latches, or rail slots.
- **Top:** use top/cover photos, service-manual cover diagrams, or multiple elevated three-quarter views. Confirm seams, cover latches, vents, and raised regions.
- **Bottom:** use official mechanical drawings, rail/feet diagrams, regulatory photos, or exact-model underside photography. Do not mirror the top or invent vents. For a website simplification, a plain bottom is acceptable only when evidence shows it is plain or the user explicitly accepts a labeled approximation.

Three-quarter photos are supporting evidence, not textures to stretch flat. Use multiple angles to resolve silhouette and feature placement, then generate or reconstruct the canonical orthographic face. A face built from insufficient evidence must remain `blocked`, not silently completed.

## 5. Dimension ledger and inclusion rules

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

Resolve these common ambiguities:

- rack ears or mounting flanges included in width;
- front bezel, drive handles, release levers, and air filters included in depth;
- rear PSU handles, fan modules, power connectors, and cable-management parts included in depth;
- shipping dimensions confused with product dimensions;
- nominal rack height such as `1U` confused with the chassis's actual clearance height;
- inches rounded differently from millimeters;
- body width confused with the 19-inch rack mounting span.

Use official numeric dimensions for the body. Use image measurement only for the relative size and placement of ears or small protrusions, anchored to a verified known dimension. Record the assumption and tolerance.

## 6. Front/rear elevation guidance

The reference project [skill-rack-device-assets](https://github.com/AyagawaSeirin/skill-rack-device-assets) supplies the baseline exact-model rules for front/rear transparent PNG assets: preserve variants and branding, use straight orthographic views, retain only real complete rack ears, avoid generic hybrids, and validate transparency/cropping. Apply those principles to this workflow, then add the four other verified faces and final-GLB checks.

When the local `rack-device-elevation-assets` skill is available, read its research and QA references for front/rear-specific work rather than duplicating ad hoc rules.

## 7. Stop conditions

Stop and report the strongest available evidence when:

- the exact PID cannot be distinguished from a family member;
- official dimensions conflict and the inclusion scope cannot be resolved;
- a materially visible face lacks exact-model evidence;
- the requested drive, controller, line-card, or rear configuration is not documented;
- an official source is access-controlled and cannot be obtained without new authority.

Do not fill any of these gaps with a visually plausible guess.
