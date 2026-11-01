# aigc-suite-skills 安装方案

本套件由三件组成，任何平台都必须完整安装：

| 组件 | 是什么 | 缺了会怎样 |
|------|--------|-----------|
| `skills/` | 14 个 SKILL.md（8 个主链工作流 + 6 个风格段） | agent 不知道怎么干 |
| `shared/` | 规则、数据契约、词典（硬闸/品牌词/运镜词/风格库） | skill 引用落空，检查无依据 |
| `tools/` | 机器闸门脚本（lint/花钱门/品牌扫/提示词自检/五道硬闸 pre_gen_gate/OCR） | 质检靠人肉，花钱门失守 |

通用第一步：克隆到**固定路径**（skill 内部按仓库根相对路径引用 `shared/` 与 `tools/`）：

```bash
git clone git@github.com:nan1010082085/aigc-suite-skills.git ~/aigc-suite-skills
```

---

## 一、Claude Code（推荐）

skills 通过符号链接安装，仓更新即生效，不用重拷：

```bash
for s in ~/aigc-suite-skills/skills/*; do
  ln -s "$s" ~/.claude/skills/$(basename "$s")
done
ln -s ~/aigc-suite-skills/shared ~/.claude/skills/aigc-suite-shared
```

验证：新开会话输入「帮我把小说改编成分集剧本」，应触发 `novel-to-drama` skill。

- 卸载：删除 `~/.claude/skills/` 下各同名 symlink 与 `aigc-suite-shared`
- 升级：`cd ~/aigc-suite-skills && git pull`，无需重装
- 说明：skill 文档内 `shared/…`、`tools/…` 均以仓库根为基准；克隆路径固定后 agent 可直接解析

## 二、Cursor

Cursor 以项目规则方式接入：

```bash
mkdir -p .cursor/rules vendor
cp -r ~/aigc-suite-skills/skills .cursor/rules/aigc-suite
cp -r ~/aigc-suite-skills/{shared,tools} vendor/aigc-suite-skills-refs/
```

在项目 `AGENTS.md`（或 `.cursor/rules/aigc-suite.mdc`）追加：

```markdown
## AIGC 漫剧创作套件
创作流程按 vendor/aigc-suite-skills-refs/skills/<name>/SKILL.md 执行；
规则与词典在 vendor/aigc-suite-skills-refs/shared/，机器闸门在 vendor/aigc-suite-skills-refs/tools/。
涉及出图/出片必须过花钱门与品牌扫描。
```

## 三、Codex

Codex 读 `AGENTS.md` 约定，采用 vendor 目录 + 链式引用：

```bash
mkdir -p vendor
cp -r ~/aigc-suite-skills vendor/aigc-suite-skills
```

`AGENTS.md` 中按任务类型链式引用（Codex 会跟随读取）：

```markdown
## 任务路由
- 小说改编 → 读并执行 vendor/aigc-suite-skills/skills/novel-to-drama/SKILL.md
- 想法创作 → 读并执行 vendor/aigc-suite-skills/skills/idea-to-drama/SKILL.md
- 分镜创作 → 读并执行 vendor/aigc-suite-skills/skills/storyboard-director/SKILL.md
- 人物素材 → 读并执行 vendor/aigc-suite-skills/skills/character-studio/SKILL.md
- 场景素材 → 读并执行 vendor/aigc-suite-skills/skills/scene-studio/SKILL.md
- 道具素材 → 读并执行 vendor/aigc-suite-skills/skills/prop-studio/SKILL.md
- 出视频执行 → 读并执行 vendor/aigc-suite-skills/skills/video-producer/SKILL.md
- 风格段 → 按剧目风格锁读 vendor/aigc-suite-skills/skills/style-*/SKILL.md（默认 style-cg-refined）
- 出片检查 → 读并执行 vendor/aigc-suite-skills/skills/shot-qa/SKILL.md
```

## 四、DSH Plugin

封装为 DSH 插件（npm 分发），按 DSH 插件规范打包：

```
packages/dsh-plugin-aigc-suite/
├── lib/
│   ├── index.js        # 服务端：导出 { name, inject, Config, apply }
│   └── client.js       # 客户端：window.__ModuleLoader__.load() 注册 { apply, inject }
├── skills/             # 全部 skill 目录原样打入（含风格 skill）
├── shared/             # 规则词典原样打入
├── tools/              # 闸门脚本原样打入
├── cordis.patch.yml
└── package.json        # name: dsh-plugin-aigc-suite
```

- `lib/index.js` 的 `apply(ctx)` 内用 `ctx.slots.inject("settings.section", …)` 注册一个「AIGC 套件」文档/状态面板（展示全部 skill 入口与三道闸状态），skill 文档通过插件包内路径读取
- 配置项走 API 获取保存，禁止 localStorage；中英文 `ctx.locale.register`
- 发布与安装：

```bash
cd packages/dsh-plugin-aigc-suite && npm publish
dsh plugin --profile web add dsh-plugin-aigc-suite
dsh web   # 验证无报错
```

修改插件须走 DSH 发布流程：改代码 →  bump `package.json` version（semver）→ `npm publish` → `dsh plugin --profile web add` 重装 → 验证。禁止 link 依赖/手动改 node_modules。

---

## 安装后自检清单

```bash
cd ~/aigc-suite-skills
python3 -m pytest tests/ -q                    # 25 passed
for s in skills/*/; do python3 tools/skill_lint.py "$s"; done   # 14/14 OK
python3 tools/brand_scan.py --help             # 品牌扫描可用
```

三项全过即安装成功。
