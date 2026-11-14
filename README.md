# LilyPatch 字体

本仓库提供东方 Project 汉化补丁使用的三款无衬线中文字体，供启动器按 `catalog.txt` / CDN manifest 下载到本地字体目录。优先级由 `fonts/manifest.json` 的 `order` 声明：

1. **文源黑体（WenYuan Sans SC）** — 在思源基础上大范围调整汉字轮廓，观感最接近原版黑体；
2. **思源黑体（Source Han Sans SC）** — 基线字体，字形最中性；
3. **未来荧黑（Glow Sans SC）** — 更轻、更几何的独立风格。

更纱黑体（Sarasa Gothic）不进入发布仓库：其 CJK 部分与思源黑体几乎相同，差异主要在拉丁，而音乐室拉丁固定使用 SimHei。

## 字体

| 文件 | family | 格式 | 大小 |
| --- | --- | --- | --- |
| `fonts/LilyPatchWenYuanSC-Regular.ttf` | `LilyPatch WenYuan Sans SC` | TTF | 11.1 MB |
| `fonts/LilyPatchSansSC-Regular.ttf` | `LilyPatch Sans SC` | TTF | 19.9 MB |
| `fonts/LilyPatchGlowSansSC-Regular.otf` | `LilyPatch Glow Sans SC` | OTF | 9.1 MB |

三款字体**不修改任何字形轮廓、横向坐标或 advance**；构建期只归一 `hhea`/`OS/2` 的纵横度量、代码页位与字体名称，使 32px GDI 单元格下的中文宽度和基线与原版接近，同时让 `lfCharSet=134` 能选中字体。

项目文本覆盖 2,595 个唯一字符；三款字体均无缺字（控制字符 tab/newline/CR 不参与检查）。未来荧黑不包含 `U+2500 ─` 与 `U+266A ♪`；`♪` 由音乐室独立音符字体绘制，`─` 已在 TH07 译文中改为中文破折号。

## 目录

```
fonts/                  最终可分发字体与 manifest.json
tools/build_fonts.py    从上游字体重新生成（仅改头部/名称）
tools/verify_fonts.py   校验名称、度量、代码页、覆盖
upstream/               上游原始字体（不提交，见 .gitignore）
build/                  本地预览与实验产物（不提交）
upstream.json           上游版本、下载地址与源文件哈希
LICENSE-OFL-1.1.txt     思源黑体的 SIL OFL 1.1
LICENSE-WenYuan-OFL-1.1.txt  文源黑体的 SIL OFL 1.1
LICENSE-Glow-OFL-1.1.txt     未来荧黑的 SIL OFL 1.1
LICENSE-CODE            构建/校验脚本许可
NOTICE.md               上游、修改内容与下载/安装说明
```

## 重新生成

1. 按 `upstream.json` 把三个上游文件放入 `upstream/`；
2. 安装 fontTools；
3. 运行 `python tools/build_fonts.py`。

脚本会写入三款字体与 `fonts/manifest.json`。不要直接修改生成的字体；修改脚本后重新生成并更新哈希。

## 校验

```text
python tools/verify_fonts.py
python tools/verify_fonts.py --text path/to/project-chars.txt
```

## 许可与署名

三款字体均按 SIL Open Font License 1.1 分发，详见对应 `LICENSE-*.txt` 与 `NOTICE.md`。再分发字体文件时必须同时附带许可文件与本 NOTICE；启动器的一键下载包也应包含它们。
