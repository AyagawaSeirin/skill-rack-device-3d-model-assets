# skill-rack-device-3d-model-assets

用于研究、制作、修复和验收机架式设备简化 3D 模型的 Codex Skill。适用于服务器、存储、交换机、路由器、防火墙等设备，主要输出可放在网站中展示的 GLB/GLTF 模型。

技能会根据官方尺寸、官方文档及不同角度的真实设备资料制作新的简化模型。搜索到的官方 GLB、CAD 或其他 3D 文件只作为备用选项提供，不会自动替代自制模型。

## 主要能力

- 核对完整品牌、型号、代次、机箱和硬盘规格变体。
- 查找并记录机身宽度、含挂耳总宽、高度、深度及突出部件尺寸。
- 根据官方正面、背面、左右侧面、顶部、底部及多角度资料制作六面素材。
- 防止 Logo、文字、端口布局或整张贴图被水平镜像。
- 正确区分机身、前挂耳和真实后部安装结构。
- 优先使用实体几何制作挂耳孔洞，避免低分辨率透明抠图。
- 防止端口、散热孔和机箱表面被错误处理为透明。
- 检查 sRGB、`KHR_materials_unlit`、PBR、透明模式和灰蒙问题。
- 直接解析和验收最终 GLB，而不是只检查 `views/` 或预览图。
- 支持逐型号批量验收和一轮返工提示词。

正面和背面素材规范参考了 [skill-rack-device-assets](https://github.com/AyagawaSeirin/skill-rack-device-assets)，本技能在其基础上增加另外四面素材、几何建模、UV、材质和真实 GLB 验收流程。

## 安装

### 方法一：使用 Codex 安装

在 Codex 中输入：

```text
请从 https://github.com/AyagawaSeirin/skill-rack-device-3d-model-assets 安装这个 Skill。
```

也可以明确调用技能安装器：

```text
使用 $skill-installer 安装 https://github.com/AyagawaSeirin/skill-rack-device-3d-model-assets
```

### 方法二：Git 克隆

macOS 或 Linux：

```bash
git clone https://github.com/AyagawaSeirin/skill-rack-device-3d-model-assets.git \
  ~/.codex/skills/skill-rack-device-3d-model-assets
```

Windows PowerShell：

```powershell
git clone https://github.com/AyagawaSeirin/skill-rack-device-3d-model-assets.git `
  "$HOME\.codex\skills\skill-rack-device-3d-model-assets"
```

如果 Codex 已经打开，安装后刷新技能列表或重新开启一个会话。

## 使用方式

技能名称：

```text
$skill-rack-device-3d-model-assets
```

### 制作单个型号

```text
使用 $skill-rack-device-3d-model-assets，为 Cisco N9K-C9336C-FX2 制作一个
用于网站展示的简化 GLB。搜索官方尺寸和六面视觉资料，自行建立模型；
如果找到官方 3D 文件，只作为备用选项列出。
```

### 检查并修复现有模型

```text
使用 $skill-rack-device-3d-model-assets，检查这个目录中的所有真实 GLB，
重点检查贴图镜像、后部错误挂耳、挂耳孔洞、机箱穿透、灰蒙材质、六面贴图
分辨率和尺寸比例。逐文件给出 PASS、REWORK 或 BLOCKED，并完成可修复项。
```

### 批量制作

```text
使用 $skill-rack-device-3d-model-assets，为清单中的所有服务器和网络设备
制作网站 GLB。逐型号核对官方尺寸和六面资料，缺少依据的面不得随意生成；
输出来源记录、六面素材、标准 GLB、Web GLB 和真实模型验收报告。
```

详细提示词模板位于 [`references/prompt-templates.md`](references/prompt-templates.md)。

## 自动检查工具

脚本依赖 Python 3 和 [Pillow](https://pypi.org/project/pillow/)：

```bash
python3 -m pip install Pillow
```

### 检查六面 PNG

六面文件默认命名为 `front.png`、`rear.png`、`left.png`、`right.png`、`top.png`、`bottom.png`。

```bash
python3 scripts/audit_views.py /path/to/views \
  --width-mm 445 \
  --height-mm 43.6 \
  --depth-mm 600 \
  --json-out /path/to/qa/views-audit.json
```

如果正面图片包含挂耳，可增加 `--front-width-mm`；只有设备真实存在后部安装结构时才使用 `--rear-width-mm`。

### 检查 GLB

```bash
python3 scripts/audit_glb.py /path/to/device.glb \
  --expected-width-mm 482.6 \
  --expected-height-mm 43.6 \
  --expected-depth-mm 600 \
  --min-basecolor-images 6 \
  --json-out /path/to/qa/glb-audit.json
```

自动检查能够发现材质透明、嵌入纹理分辨率、外部资源、UV 缺失、负行列式镜像变换和尺寸比例问题，但不能替代 exact-model 资料对照和多角度视觉验收。

## 推荐输出结构

```text
<MODEL_KEY>/
├── source/
│   ├── originals/
│   ├── optional-3d/
│   └── evidence.md
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

## 重要原则

- 官方 3D 文件是备用选项，不是本技能默认的优先成品。
- 正面和背面不能代替完整六面资料。
- 不能用通用机箱或相似型号填补缺失资料。
- 后视图中看到前挂耳，不代表设备后面存在挂耳。
- 黑色端口和散热孔不是透明区域。
- `views/` 正确不代表 GLB 的 UV、材质、透明和嵌入纹理正确。
- 最终必须检查实际导出的标准 GLB 和 Web GLB。
