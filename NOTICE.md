# NOTICE

## 上游

| 本项目文件 | 上游 | 版本 | 上游文件 |
| --- | --- | --- | --- |
| `fonts/LilyPatchWenYuanSC-Regular.ttf` | [WenYuan Sans](https://github.com/takushun-wu/WenYuanFonts) | 1.110 | `WenYuanSansSC-Regular.ttf` 11,071,676 B，SHA-256 `1135b02c88da983cb828d8b206e3fa732c794b22e0916ef7cc7e985c783ec341` |
| `fonts/LilyPatchSansSC-Regular.ttf` | [Source Han Sans](https://github.com/adobe-fonts/source-han-sans) | 2.005 | `SourceHanSansSC-Regular.ttf` 19,931,428 B，SHA-256 `354a0ee20d673141700e1dadf1895bfbd16da0fd89d26a42a2608b370a1b225f` |
| `fonts/LilyPatchGlowSansSC-Regular.otf` | [Glow Sans](https://github.com/welai/glow-sans) | 0.93 | `GlowSansSC-Normal-Regular.otf` 9,119,372 B，SHA-256 `ca7d34947401b2fa6dd4fd46676d970a8cc47a40ee60c022eb7dd5068bee67ff` |

思源黑体的 TrueType 版本由 [unix755/SourceHan-font-ttf](https://github.com/unix755/SourceHan-font-ttf) 从官方 OTF 转换而来；转换只改容器格式，字形轮廓未变。未来荧黑的上游仓库已归档。

## 修改内容

三款字体都只修改头部与名称，**没有修改任何字形轮廓、横向坐标或 advance**：

1. `hhea.ascent/descent`、`OS/2.sTypoAscender/Descender`、`OS/2.usWinAscent/Descent` 归一为 `880/-120`，`lineGap=0`，使 32px GDI 单元格得到约 28px ascent、32px 全角 advance。
2. 在 `OS/2.ulCodePageRange1` 设置 GB2312 与 GBK 位，使 `lfCharSet=134` 可以选中字体。
3. family/full/PostScript/unique name 改为 `LilyPatch ...`，不使用上游的 Reserved Font Name（`Source`、`WenYuan Sans`、`Glow Sans` 等）。
4. `OS/2.achVendID` 设为 `LPAT`；固定 `head.modified` 保证构建可复现。

具体步骤见 `tools/build_fonts.py`；生成文件哈希见 `fonts/manifest.json`。

## 下载与安装

启动器把选中的一个字体文件放到：

```text
%LOCALAPPDATA%\LilyPatch\fonts\
```

游戏进程通过 `AddFontResourceExW(..., FR_PRIVATE)` 私有加载；系统不安装该字体。启动器只读取本地 catalog/下载 manifest，未选择、文件缺失或加载失败时回落 SimHei，不枚举系统 CJK 字体。

## 许可

- 文源黑体：`LICENSE-WenYuan-OFL-1.1.txt`（SIL OFL 1.1，含 Reserved Font Name 条款；本项目已改名）。
- 思源黑体：`LICENSE-OFL-1.1.txt`（SIL OFL 1.1，含 Reserved Font Name `Source` 条款；本项目已改名）。
- 未来荧黑：`LICENSE-Glow-OFL-1.1.txt`（SIL OFL 1.1，含 Reserved Font Name 条款；本项目已改名）。
- 构建/校验脚本：`LICENSE-CODE`（MIT）。

再分发字体时必须同时附带对应许可文件与本 NOTICE。本项目与 Adobe、Google、文源/未来荧黑作者没有隶属或背书关系；上游名称仅用于注明来源。
