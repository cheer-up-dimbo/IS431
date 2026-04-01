# Adding 3D Models to the FYP Web Report

This guide explains how to add new interactive 3D models to any page in the IS431 web report using the `<explode-viewer>` component.

---

## Supported Formats

| Format | Extension | Notes |
|:---|:---|:---|
| **glTF** | `.gltf` + `.bin` + textures | Text-based JSON with external binary data and texture files. Must keep all referenced files in the same folder. |
| **glTF Binary** | `.glb` | Single self-contained file (binary + textures embedded). Easiest to manage. |

> **Recommendation:** Use `.glb` when possible — it's a single file with no external dependencies. Use `.gltf` when you need to inspect/edit the JSON manually or when exported from SolidWorks/Blender in that format.

---

## Step-by-Step Guide

### 1. Export from CAD

**SolidWorks (direct glTF export):**
- Install the [SolidWorks glTF exporter plugin](https://github.com/pjdietz/SolidWorks-glTF-Exporter) or use **File → Save As → .STL** per-part, then assemble in Blender.

**Blender (recommended workflow):**
1. Import your model (`.step`, `.stl`, `.obj`, etc.)
2. Verify each component is a **separate named object** in the Outliner (this enables the explode slider)
3. **File → Export → glTF 2.0 (.glb/.gltf)**
   - Format: `glTF Binary (.glb)` for single file, or `glTF Separate (.gltf + .bin + textures)` if multi-file
   - Check **"Include → Selected Objects"** or **"All"** with hierarchy preserved
   - Enable **"Geometry → Apply Modifiers"**

**Naming parts for explode view:**
Name each object/mesh after its mechanical function:
```
motor_1, motor_2, helical_gear_L, helical_gear_R,
bevel_gear, housing_outer, d_shaft_6mm, delrin_pin, arm_tube
```
The explode-viewer traverses the scene graph and separates each named mesh outward.

### 2. Place Files in Assets

Create a subfolder under:
```
documents/IS431/assets/3d_models/<model_name>/
```

**For `.glb` (single file):**
```
assets/3d_models/my_assembly/
└── my_assembly.glb
```

**For `.gltf` (multi-file):**
```
assets/3d_models/my_assembly/
├── my_assembly.gltf    ← JSON scene description
├── data.bin            ← binary geometry data
└── texture.dds         ← texture file (if any)
```

> ⚠️ **All files referenced in the `.gltf` must be in the same folder** — the glTF format uses relative paths.

### 3. Add the Import Map (once per page)

If the page does **not** already have a Three.js importmap in `<head>`, add it **before** the explode-viewer script tag:

```html
<!-- Three.js import map (required for explode-viewer) -->
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.164.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.164.0/examples/jsm/"
  }
}
</script>
<!-- 3D Explode Viewer -->
<script type="module" src="../../components/explode-viewer/explode-viewer.js"></script>
```

> Pages that already include the explode-viewer (e.g., `mechanical-design.html`) do not need this again.

### 4. Insert the Component

Add the `<explode-viewer>` element wherever you want the 3D model to appear:

```html
<explode-viewer
  src="../../assets/3d_models/my_assembly/my_assembly.glb"
  alt="Description of the model for the caption"
  height="500"
  explode-scale="2.0">
</explode-viewer>
```

**Attributes:**

| Attribute | Default | Description |
|:---|:---|:---|
| `src` | (required) | Relative path to the `.glb` or `.gltf` file |
| `alt` | `"3D Model"` | Caption text displayed below the viewer |
| `height` | `500` | Canvas height in pixels |
| `explode-scale` | `2.0` | How far parts spread when slider is at 100%. Increase for large assemblies, decrease for small ones. |

### 5. Test Locally

Open the page via Live Server (e.g., `http://127.0.0.1:5501/...`).

**Checklist:**
- [ ] Model loads and renders (no console errors)
- [ ] Orbit controls work (click-drag to rotate, scroll to zoom)
- [ ] Explode slider separates parts outward
- [ ] Part count displayed matches expected component count
- [ ] If part count shows `1 component` — the model is a single mesh. Re-export from Blender with separate objects.

---

## Troubleshooting

| Issue | Cause | Fix |
|:---|:---|:---|
| Model doesn't load | Wrong path or missing files | Check browser console; verify all `.gltf`-referenced files are in the same folder |
| Black/missing textures | `.dds` format not supported by Three.js | Re-export textures as `.png` or `.jpg` from Blender |
| Explode slider does nothing | Model is a single mesh | Re-export with each part as a separate Blender object |
| Parts explode incorrectly | All parts centred at origin | In Blender, apply transforms (`Ctrl+A → All Transforms`) before export |
| CORS errors | Opening via `file://` protocol | Use a local server (VS Code Live Server, `python -m http.server`) |

---

## Quick Reference — Copy-Paste Template

```html
<!-- In <head> — only if not already present -->
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.164.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.164.0/examples/jsm/"
  }
}
</script>
<script type="module" src="../../components/explode-viewer/explode-viewer.js"></script>

<!-- In <body> — where you want the viewer -->
<explode-viewer
  src="../../assets/3d_models/MODEL_FOLDER/MODEL_FILE.glb"
  alt="Caption describing the model"
  height="500"
  explode-scale="2.0">
</explode-viewer>
```
