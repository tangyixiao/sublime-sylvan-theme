# Sublime Sylvan · 松雨

适用于 Sublime Text 4 的近黑松绿界面主题与代码配色方案，沿用 [DSH 外观 · Sylvan](https://github.com/tangyixiao/dsh-sylvan-appearance) 的界面色板与 [VS Code 现代深色](https://github.com/microsoft/vscode/blob/main/extensions/theme-defaults/themes/dark_modern.json) 语法高亮规则。

## 包含内容

- `Sylvan.sublime-theme`：基于 Sublime Text 4 内置 `Default Dark.sublime-theme` 扩展，覆盖标题栏、标签栏、侧边栏、命令面板、自动补全、底部面板、状态栏、按钮与提示框。
- `Sylvan.sublime-color-scheme`：近黑底 `#0f0f11` 编辑器画布、松绿光标与选区、以及 C/C++、Python、JavaScript/TypeScript、HTML/CSS、JSON/YAML、Markdown、Diff 等常见语法高亮规则。
- `Widget - Sylvan.sublime-settings` 与 `Widget - Sylvan.hidden-color-scheme`：统一查找替换框、命令面板与快速跳转输入框的深色背景、松绿光标和选区样式。

## 安装

需要 Sublime Text 4（已验证 Build 4215）。

1. 在 Sublime Text 中打开 **Preferences → Browse Packages**，进入 `Packages` 目录。
2. 将本仓库克隆或复制到 `Packages/Sylvan`：

```bash
git clone https://github.com/tangyixiao/sublime-sylvan-theme.git Sylvan
```

3. 通过命令面板（`Ctrl+Shift+P` / `Cmd+Shift+P`）分别运行 **UI: Select Theme** 选择 `Sylvan.sublime-theme`，运行 **UI: Select Color Scheme** 选择 `Sylvan`，或在 `Preferences.sublime-settings` 中写入：

```json
{
	"theme": "Sylvan.sublime-theme",
	"color_scheme": "Sylvan.sublime-color-scheme",
	"font_face": "JetBrainsMonoNL Nerd Font Mono",
	"themed_title_bar": true,
	"highlight_modified_tabs": true
}
```

## 字体配置

与 `dsh-sylvan-appearance` 的字体栈对应关系如下：

- **代码字体**：Sublime Text 的编辑器字体由用户配置 `Preferences.sublime-settings` 中的 `font_face` 控制，推荐设为 `JetBrainsMonoNL Nerd Font Mono`（若未安装 Nerd Font，可改为 `JetBrains Mono` 或 `Consolas`）。
- **界面字体**：`Sylvan.sublime-theme` 在 Windows 上默认使用 `Segoe UI Variable`，在 Linux / macOS 上沿用系统默认界面字体（`system`）。如需统一替换为其他界面字体，可在 **UI: Customize Theme** 中覆盖 `variables.font_face`。

## 配色概览

界面色板与 `dsh-sylvan-appearance` 的 [松雨预设](https://github.com/tangyixiao/dsh-sylvan-appearance/blob/main/src/sylvan.json) 保持一致：

| 用途 | 颜色 |
| --- | --- |
| 编辑器与输入框底色 | `#0f0f11` |
| 侧边栏与状态栏 | `#131416` |
| 标签栏、标题栏、底部面板与当前行 | `#18191b` |
| 命令面板与自动补全浮层 | `#202124` |
| 按钮与提示框表面 | `#26272b` |
| 边框与分割线 | `#27282c` / `#35373c` / `#46494f` |
| 主 / 次 / 弱文本 | `#e3e4e6` / `#a7aab1` / `#82858d` |
| 松绿强调 / 链接与匹配高亮 | `#4fa66b` / `#75bd8a` |
| 侧边栏选中 / 面板与编辑器选区 | `#1c3024` / `#21392a` / `#23372a` |
| 新增 / 错误状态 | `#69c967` / `#ff7e78` |

如需微调变量或单条规则，可在命令面板运行 **UI: Customize Theme** 或 **UI: Customize Color Scheme** 进行用户级覆盖。

## 本地校验

```bash
python3 scripts/validate.py
```

脚本会检查所有主题与配色 JSON 语法、变量引用完整性、Widget 关联配置以及松雨基础色板一致性。

## 许可证

软件采用 [MIT 许可证](LICENSE)。
