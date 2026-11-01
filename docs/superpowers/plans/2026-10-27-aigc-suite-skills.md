# aigc-suite-skills 五 Skill 套件 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建成漫剧创作五 skill 套件（novel-to-drama / idea-to-drama / storyboard-director / asset-studio / shot-qa）+ shared 规则词典 + 可测工具脚本，替代 manju-pipeline。

**Architecture:** 内容为主的 skill 仓：`shared/` 放全部硬闸、方法论、创作词典与跨 skill 数据契约；`skills/` 五个独立 SKILL.md（统一结构，skill_lint 校验）；`tools/` 放可测的 Python 工具（品牌扫描、提示词自检、花钱门、lint）与迁移脚本（OCR/Notion/pre_gen_gate）。skill 之间只通过 `shared/output-formats.md` 的字段契约耦合。

**Tech Stack:** Markdown（skill 文档）；Python 3 stdlib-only 工具 + pytest；git/GitHub 私有仓。

**Spec:** `docs/superpowers/specs/2026-10-27-aigc-suite-skills-design.md`

## Global Constraints

- 出片自动为主：skill 经共享花钱门（报价→用户批→跑）直调 dreamina-canvas；手动贴即梦仅备选
- 单集时长自动决定，30–120 秒区间，由剧情与分镜自然成型，不硬凑不牵强；分集按故事单元，禁止「一章=一集」机械映射
- 中文提示词 ≤500 字；单次生成 ≤15s，超出自动分段；每时间片一个动作一个运镜
- 情绪必须可视化（「泪水滑落、嘴唇微颤」而非「她很伤心」）；禁废话词（4K/8K/杰作/超清晰等），用物理材质词替代
- 广告植入三层禁（画面/语音/字幕）：真实品牌名、品牌感商品包装、品牌 Logo
- 转场必交代时间+地点（旁白或屏幕 UI 层字幕卡）+转场过渡句（空间延续、不硬切）
- Notion 唯一控制面：生成状态=生成中才出片；Notion 指令零压缩逐字搬运（SHA-256 校验）
- 验真只认提交后新 resource（`submission.resources`，createdAt 比对）
- 写实真人面部转 3D/cel-shaded；出图前置调研（先检索资料再出指令）
- 留存三主轴既是产出标准也是自检项：场景转场连贯、剧情分镜、人物建模质量
- 工具脚本 stdlib-only（pytest 仅开发态）；每个任务结束 git commit

## Review Focus

1. **skill 触发失灵**——SKILL.md description 不含领域触发词，用户提到「漫剧/分镜/出图」时不启动 → Task 1 的 lint 测试断言 description 含 ≥3 个领域词
2. **跨 skill 字段契约漂移**——剧本/分镜/素材/检查四类产出字段名不一致，流水线断链 → Task 2 锁定 `output-formats.md` 字段名，Task 5–9 各任务测试断言引用同一组字段名
3. **品牌词漏扫语音/字幕层**——扫描只查画面描述，台词旁白弹幕漏网 → Task 3 brand_scan 测试覆盖三层文本各一正一反样例
4. **花钱门可绕过**——无批准能跑扣积分命令 → Task 3 credit_gate 测试：缺 `--approved-by` 必须拒绝执行
5. **运镜词典不足量、自检漏废话词**——词典<50 词、banned 词缺失 → Task 4 计数断言 ≥50；Task 5 prompt_selfcheck 对废话词正反样例测试

---

### Task 1: 仓库骨架 + skill_lint 工具

**Files:**
- Create: `tools/skill_lint.py`, `tests/test_skill_lint.py`, `tests/fixtures/skill_ok/SKILL.md`, `tests/fixtures/skill_bad/SKILL.md`

**Interfaces:**
- Produces: `skill_lint.lint(skill_dir: Path) -> list[str]`（返回问题清单，空=通过）；CLI `python3 tools/skill_lint.py <skill_dir>` 问题非空则 exit 1。SKILL.md 统一结构契约：frontmatter 必含 `name`、`description`（≥40 字符且含领域触发词表中任意 3 词：漫剧/短剧/剧本/分镜/出图/出片/小说/人物/场景/即梦/Seedance）；正文必含标题 `## 何时使用`、`## 流程`、`## 硬闸与自检`、`## 产出与格式`

- [ ] **Step 1: 写失败测试** `tests/test_skill_lint.py::test_ok_fixture_passes`（`lint(fixture_ok)==[]`）、`test_bad_fixture_reports_sections`（结果含「缺标题」项）、`test_description_needs_trigger_words`（description 缺触发词时报问题）
- [ ] **Step 2: 跑测试确认失败** `python3 -m pytest tests/test_skill_lint.py -v` → FAIL（模块不存在）
- [ ] **Step 3: 实现 `tools/skill_lint.py`**：frontmatter 用 `---` 分隔手解析（stdlib），按上述契约逐项检查；两个 fixture 一正一反
- [ ] **Step 4: 跑测试确认通过** → PASS
- [ ] **Step 5: Commit** `feat: skill_lint 工具与 SKILL.md 结构契约`

### Task 2: shared/ 规则文档五件

**Files:**
- Create: `shared/hard-gates.md`, `shared/split-methodology.md`, `shared/output-formats.md`, `shared/brand-wordlist.txt`, `shared/lessons.md`

**Interfaces:**
- Consumes: 设计稿 §三（硬闸）、§skill1-4（拆分方法论）、§七（拍板）
- Produces（后续任务依赖的字段契约，锁在 `output-formats.md`）：
  - 剧本条目：`{集数, 时长秒(30–120, 自动), 场景节拍[], 人物[], 本集看点, 结尾钩子}`；节拍 = `{目标/冲突, 起承转合, 钩子}`
  - 分镜块：`{镜号, 时间片[], 六要素{主体外貌,动作,场景,光影,焦段运镜,音效}, 转场交代?, 素材映射[], 提示词}`（提示词=代码块交付物）
  - 素材注册表 assets.json：`{characters:[{name, visual_id, three_view, face_card, expressions[], outfits:[{名, three_view, 配饰}]}], scenes:[{名, image, 光影锁定}]}`
  - 检查报告：`{价格闸{报价, 批准}, 剧情校验{逐字, 转场, 品牌, 违禁}, 素材校验{挂载, 格式, 验真}}`
- `brand-wordlist.txt`：种子词表 ≥30 条（高德地图/谷歌地图/淘宝/京东/美团/星巴克/麦当劳/肯德基/卫龙/可口可乐… + 包装词组「品牌字样」「商标样式」等）
- `hard-gates.md`：设计稿 §三全部硬闸逐条落文，含花钱门操作程序（报价→用户批→跑、超账单重新批）
- `split-methodology.md`：收录用户 2026-10-27 拆解方法论全文要点（换算锚 200–400 字/分钟、故事单元拆分、连贯改编技法、每集结构模板）

- [ ] **Step 1: 写五份文档**（内容按上面 Interfaces 锁定；lessons.md 收 manju-pipeline 已验教训：i2i 锚构图、显老词、服装漂移、表情抄外貌、video ref 塌缩、quote≠run 报价、submission 验真、转场裸切打回、广告植入打回）
- [ ] **Step 2: 校验** `grep -cve '^\s*$' shared/brand-wordlist.txt` ≥30 且 `grep -q '时长秒' shared/output-formats.md` && `grep -q 'submission.resources' shared/hard-gates.md`
- [ ] **Step 3: Commit** `docs: shared 规则/方法论/数据契约/品牌词表/教训`

### Task 3: tools 基建（花钱门 + 品牌扫描）

**Files:**
- Create: `tools/credit_gate.py`, `tools/brand_scan.py`, `tests/test_credit_gate.py`, `tests/test_brand_scan.py`

**Interfaces:**
- Consumes: `shared/brand-wordlist.txt`
- Produces:
  - `credit_gate.quote(cmd: list[str]) -> dict{total_max_credits, items}`（调 dreamina-canvas node quote，dry 模式可注入假 runner）；`credit_gate.run(cmd: list[str], approved_by: str|None, max_credits: int) -> int`——`approved_by` 为 None 一律拒绝（exit 前抛 `PermissionError`）
  - `brand_scan.scan_text(text: str) -> list[dict{word, layer_guess}]`；`brand_scan.scan_shot(画面, 台词旁白弹幕) -> list[dict]`——三层都扫

- [ ] **Step 1: 写失败测试**：`test_run_without_approval_raises`（`approved_by=None` 抛 PermissionError 且不调用执行器）、`test_run_with_approval_passes_ceiling`（批准后传递 ceiling 给执行器）、`test_brand_hit_in_dialogue`（台词含「高德地图」必报）、`test_brand_hit_in_visual`（画面含「星巴克」必报）、`test_clean_text_empty`（干净文本返回 []）
- [ ] **Step 2: 跑测试确认失败** → FAIL
- [ ] **Step 3: 实现两脚本**（stdlib + 可注入 runner 便于测试；词表按行读 `shared/brand-wordlist.txt`）
- [ ] **Step 4: 跑测试通过** → PASS
- [ ] **Step 5: Commit** `feat: 共享花钱门与品牌三层扫描`

### Task 4: shared/ 创作词典三件

**Files:**
- Create: `shared/camera-dictionary.md`, `shared/director-styles.md`, `shared/lighting-system.md`

**Interfaces:**
- Produces: `camera-dictionary.md` 收 **≥50 条安全运镜词**（中文名+英文对照+一句适用语境，如 推近/拉远/摇移/跟拍/甩切/升降/环绕/手持感/变焦…）；`director-styles.md` ≥6 种风格（维伦纽瓦/韦斯·安德森/新海诚/武侠/皮克斯/赛博朋克，每种：视觉特征+光影+运镜偏好+色彩）；`lighting-system.md` 三层光影（环境层/主光层/情绪层）+ 各情绪的光影配方

- [ ] **Step 1: 写三份词典**（运镜词按条目 `- **中文**（English）：语境` 格式，便于计数）
- [ ] **Step 2: 校验** `grep -c '^- \*\*' shared/camera-dictionary.md` ≥50
- [ ] **Step 3: Commit** `docs: 运镜词典/导演风格库/三层光影`

### Task 5: storyboard-director skill（含 prompt_selfcheck）

**Files:**
- Create: `skills/storyboard-director/SKILL.md`, `skills/storyboard-director/references/prompt-format.md`, `skills/storyboard-director/references/selfcheck-7.md`, `tools/prompt_selfcheck.py`, `tests/test_prompt_selfcheck.py`

**Interfaces:**
- Consumes: Task 2 字段契约（分镜块）、Task 3 词典、Task 1 lint 契约
- Produces: `prompt_selfcheck.check(prompt: str, refs: list[str]) -> list[str]`——检查：①≤500 中文字符 ②时间片格式 `\d+[–-]\d+ ?秒` ③违禁词（4K/8K/杰作/超清晰/大师作/wallpaper）④裸英文运镜词（pan/zoom/dolly/tilt 未中译）⑤refs 数 ≤9。SKILL.md 流程 = 需求五问→视觉构思→六要素组装→7 项自检→交付（主题/素材映射/导演阐述/代码块提示词）

- [ ] **Step 1: 写失败测试**：`test_over_500_chars`、`test_banned_word`、`test_bare_english_camera`、`test_too_many_refs`、`test_good_prompt_passes`（合格样例返回 []）
- [ ] **Step 2: 跑测试失败** → FAIL
- [ ] **Step 3: 实现 `prompt_selfcheck.py`**
- [ ] **Step 4: 写 SKILL.md 与两份 references**（分镜块字段引用 output-formats.md 原名；转场交代为强制项；>15s 自动分段；写实转 3D/cel-shaded；镜头细切可拼接）
- [ ] **Step 5: 跑测试 + lint** `pytest tests/test_prompt_selfcheck.py -v && python3 tools/skill_lint.py skills/storyboard-director` → PASS
- [ ] **Step 6: Commit** `feat: storyboard-director skill 与提示词自检`

### Task 6: novel-to-drama skill（含 OCR 工具迁移）

**Files:**
- Create: `skills/novel-to-drama/SKILL.md`, `skills/novel-to-drama/references/adaptation-workflow.md`
- Modify（迁移）: `tools/fanqie_ocr.py`（从 `~/.claude/skills/manju-pipeline/scripts/` 原样拷入，路径常量改相对仓内）

**Interfaces:**
- Consumes: `shared/split-methodology.md`（分集规则）、`shared/output-formats.md`（剧本条目）、lint 契约
- Produces: SKILL.md 流程 = 抽正文（OCR/直取）→ 拆解（人物/伏笔/名场面/爽点）→ 分集（30–120s 自动、故事单元、禁一章一集）→ 分集剧本（灵活叙事+剧本理解两核心）

- [ ] **Step 1: 拷贝并改路径** `fanqie_ocr.py`，`python3 -c "import ast; ast.parse(open('tools/fanqie_ocr.py').read())"` 语法通过
- [ ] **Step 2: 写 SKILL.md 与 adaptation-workflow.md**（含用户拆解方法论的操作化步骤：标转折点→分组场景→逐集撰写→连贯检查→时长自然成型；开头 5 秒抓人；钩子设计；人物靠对话不用旁白）
- [ ] **Step 3: lint 通过 + 契约引用断言** `python3 tools/skill_lint.py skills/novel-to-drama && grep -q 'output-formats' skills/novel-to-drama/SKILL.md && grep -q 'split-methodology' skills/novel-to-drama/SKILL.md`
- [ ] **Step 4: Commit** `feat: novel-to-drama skill 与 OCR 工具迁移`

### Task 7: idea-to-drama skill

**Files:**
- Create: `skills/idea-to-drama/SKILL.md`, `skills/idea-to-drama/references/idea-workflow.md`

**Interfaces:**
- Consumes: `shared/split-methodology.md`、`shared/output-formats.md`
- Produces: SKILL.md 流程 = 需求澄清（≤2 问）→ 搜索同类题材/爆款冲突结构 → 戏剧结构（logline→多集结构→人物小传）→ 分集剧本（同两核心）；集数规划按故事单元自然成型

- [ ] **Step 1: 写 SKILL.md 与 idea-workflow.md**
- [ ] **Step 2: lint 通过 + 契约引用断言** `python3 tools/skill_lint.py skills/idea-to-drama && grep -q 'output-formats' skills/idea-to-drama/SKILL.md && grep -q 'split-methodology' skills/idea-to-drama/SKILL.md`
- [ ] **Step 3: Commit** `feat: idea-to-drama skill`

### Task 8: asset-studio skill（含风格库调研）

**Files:**
- Create: `skills/asset-studio/SKILL.md`, `skills/asset-studio/references/asset-system.md`, `skills/asset-studio/references/research-before-gen.md`, `shared/style-library.md`

**Interfaces:**
- Consumes: Task 2 素材注册表契约、Task 4 光影/风格、lint 契约
- Produces: 三视图锚点制（主体三视图=身份锚；每套服装三视图=模块；表情表；场景空镜；i2i 挂主体保机位）；**出图前置调研**流程（出图前检索该风格出图经验/提示词写法/翻车点→对齐核心要素→出指令→沉淀回 style-library）；`style-library.md` 初版=WebSearch 调研 3 种风格（3D 卡通渲染、日漫、皮克斯质感）的出图经验+提示词模板+负面词表

- [ ] **Step 1: WebSearch 调研三种风格**（关键词：AI 角色三视图 提示词 / character turnaround prompt cel-shading / consistency tips image gen），结论写入 `shared/style-library.md`（每风格：出图要点/提示词模板/负面词/翻车点）
- [ ] **Step 2: 写 SKILL.md、asset-system.md、research-before-gen.md**（资产字段引用 output-formats.md；多套服装逐件写死；禁包装特写等广告闸并入）
- [ ] **Step 3: lint 通过 + `grep -q '出图前置调研' shared/style-library.md`**
- [ ] **Step 4: Commit** `feat: asset-studio skill 与风格库初版`

### Task 9: shot-qa skill（含 pre_gen_gate 与 Notion 客户端迁移）

**Files:**
- Create: `skills/shot-qa/SKILL.md`, `skills/shot-qa/references/three-gates.md`
- Modify（迁移）: `tools/pre_gen_gate.py`, `tools/notion_mcp_client.py`（从 manju-pipeline 拷入改路径）

**Interfaces:**
- Consumes: `tools/brand_scan.py`（Task 3）、`tools/credit_gate.py`、`shared/output-formats.md` 检查报告契约
- Produces: 三道闸流程=价格闸（credit_gate.quote→用户批→run）→ 分镜剧情校验（逐字 SHA-256/转场交代/brand_scan 三层/违禁词/≥250 字/钩子句号）→ 素材校验（挂载齐/ref 格式 `node_[a-z0-9]{10}`/节点 success/验真 submission.resources）；输出检查报告，全过才出片

- [ ] **Step 1: 迁移两脚本**，`ast.parse` 语法通过
- [ ] **Step 2: 写 SKILL.md 与 three-gates.md**（检查报告字段名引用 output-formats.md）
- [ ] **Step 3: lint 通过 + 契约引用断言** `python3 tools/skill_lint.py skills/shot-qa && grep -q 'output-formats' skills/shot-qa/SKILL.md && grep -q 'brand_scan' skills/shot-qa/SKILL.md`
- [ ] **Step 4: Commit** `feat: shot-qa skill 与 pre_gen_gate/notion 客户端迁移`

### Task 10: 收尾（README + 全量测试 + 推仓）

**Files:**
- Create: `README.md`
- Modify: 无

- [ ] **Step 1: 写 README**（套件定位、五 skill 一览表、shared/tools 目录导览、与 manju-pipeline 关系：试产后再摘）
- [ ] **Step 2: 全量验证** `python3 -m pytest tests/ -v` 全 PASS；`for s in skills/*/; do python3 tools/skill_lint.py "$s"; done` 全过
- [ ] **Step 3: Commit + push** `chore: README 与全量验证`；`git push`
