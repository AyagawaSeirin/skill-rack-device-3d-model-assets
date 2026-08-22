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
- `"<exact PID>" front rear side top`

An official interactive viewer can load a GLB or glTF that is not exposed as a visible download button. Inspect its public network resources when permitted, but do not bypass authentication, access controls, licensing checks, or private APIs. Record the viewer page and direct public asset URL. If downloaded, preserve the original file, byte size, and SHA-256 checksum.

Report an exact official model as an optional alternative and potentially authoritative visual reference. Do not automatically substitute it for the newly built model, copy its mesh into the main deliverable, or call the task complete. Use or derive from it only when the user explicitly changes that scope.

Do not call an AI reconstruction “official.”

## 4. Evidence hierarchy for the new build

Prefer evidence in this order:

1. exact-model official color photos, manuals, 3D viewers, CAD screenshots, product videos, exploded diagrams, and mechanical drawings;
2. exact-PID official distributor or authorized-reseller photography;
3. exact-model regulatory filings or reputable used-equipment photos for hidden faces;
4. family diagrams only as leads, never as conclusive identity evidence.

Use image search only for discovery; open and record the underlying page. Search in English and the vendor's local language when useful.

For every source record, include the installed configuration rather than only the family model:

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

For each face, retain at least one exact-configuration color source. A straight photo is preferred; if the face is reconstructed from perspective, retain at least two exact-configuration angles that jointly prove both edges and every major feature. Diagrams may constrain geometry but cannot establish color or material alone.

## 5. Six-face evidence rules

Front and rear straight-on images are not enough for a six-sided model.

- **Front/rear:** use exact-model elevations or near-orthogonal photographs. Confirm logo side, port/bay order, rack ears, handles, PSU/riser layout, and model badge.
- **Left/right:** use exact-model side photos, installation diagrams, rail/cover removal instructions, regulatory label views, or multiple three-quarter images. The two sides may have different vents, labels, latches, or rail slots.
- **Top:** use top/cover photos, service-manual cover diagrams, or multiple elevated three-quarter views. Confirm seams, cover latches, vents, and raised regions.
- **Bottom:** use official mechanical drawings, rail/feet diagrams, regulatory photos, or exact-model underside photography. Do not mirror the top, use a generic plain panel, or invent vents. If the underside cannot be verified, the exact-replica task is `BLOCKED`.

Three-quarter photos are supporting evidence, not textures to stretch flat. Use multiple exact-configuration angles to resolve silhouette, relief, and feature placement, then create the canonical orthographic face. A face built from insufficient evidence remains `BLOCKED`.

## 6. Dimension ledger and inclusion rules

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

## 7. Feature-level source matrix

Before generation, create `feature-inventory.csv` with one row per component group. Include exact count, row/column arrangement, left-to-right order, relative size, position, depth/relief, material/color, source URL, and confidence. Cover at minimum:

- drive carriers, blanking panels, sleds/nodes, and bezels;
- PSUs, fans, risers, controllers, and rear modules;
- every port group, status/control panel, management module, and large grille;
- handles, latches, rack ears, mounting holes, cover seams, labels, and visible fasteners.

Do not summarize a dense face as “ports and vents.” The inventory is the build specification and later the QA checklist.

## 8. Front/rear elevation guidance

The reference project [skill-rack-device-assets](https://github.com/AyagawaSeirin/skill-rack-device-assets) supplies the baseline exact-model rules for front/rear transparent PNG assets: preserve variants and branding, use straight orthographic views, retain only real complete rack ears, avoid generic hybrids, and validate transparency/cropping. Apply those principles to this workflow, then add the four other verified faces and final-GLB checks.

When the local `rack-device-elevation-assets` skill is available, read its research and QA references for front/rear-specific work rather than duplicating ad hoc rules.

## 9. Stop conditions

Stop and report the strongest available evidence when:

- the exact PID cannot be distinguished from a family member;
- the requested module is not tied to a verified host enclosure and installed configuration;
- official dimensions conflict and the inclusion scope cannot be resolved;
- a materially visible face lacks exact-model evidence;
- the requested drive, controller, line-card, or rear configuration is not documented;
- an official source is access-controlled and cannot be obtained without new authority.

Do not fill any gap with a visually plausible guess. An approximation requested later must be a separately named deliverable and cannot receive an exact-replica `PASS`.
