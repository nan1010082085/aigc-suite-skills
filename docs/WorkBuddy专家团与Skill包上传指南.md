# 把 aigc-suite-skills 做成 WorkBuddy 专家交付物（专家团 / 独立专家 / 整套 Skill 包）

> 2026-11-06 完成转化、注册、打包；同日追加「专家团拆成 3 个独立专家」；2026-11-07 剧本专家两次改名，并**冻结 18 个独立技能上架路径**，只保留 3 个独立专家 + 1 个专家团 + 1 个整套本地安装包。本文是唯一操作说明，涵盖「怎么做」「上传什么」「以后怎么维护」。

## 一、结论速览

**先分清边界（2026-11-06 用户口径）：WorkBuddy 专家团归专家团，GitHub 仓库归 GitHub 仓库，两者不能统一而论。**

| | GitHub 仓库 `nan1010082085/aigc-suite-skills` | WorkBuddy 专家团「漫剧制片厂」 |
|---|---|---|
| 是什么 | skill 源码仓：`skills/` + `shared/` + `tools/` + `tests/` | 平台侧独立交付物：`plugin.json` + 11 agents + 12 头像 + SOP + 版本 |
| 版本 | git commit（仓库自己的版本） | `plugin.json` 的 `version`（现 1.1.2） |
| 发布 | git push；Claude Code / Cursor symlink 安装 | 开放平台「专家」货架上传 → 审核 → 手动公开发布；本机 marketplace.json 注册 |
| 生命周期 | 独立演进 | 独立演进，不随仓库提交自动变化 |

专家团打包时**一次性取材**于仓库的 skill 内容（原样拷入），此后互不绑定：仓库改了不等于专家团要改，专家团改了也不回写仓库。第八节的 rsync 只是「决定更新专家团时」的手动取材动作，不是同步机制。

本次另建了 **Team 型专家团「漫剧制片厂」**，之后又按用户要求拆出 **3 个可单独上架的 Agent 型独立专家**；现有四种不同用途的上传物：

| 产物 | 路径 | 大小 | 用途 |
|------|------|------|------|
| **3 个独立专家 zip（当前主推）** | `dist/expert-packages/*.zip` | 625–664 KB / 个 | 逐个上架开放平台「专家」货架：剧本 / 素材 / 虚拟导演 |
| 专家团 zip | `dist/aigc-drama-studio.zip` | 5.7 MB | 整体交付 11 角色协作（保留作底稿，不再作上架首选） |
| 整套 skill 包 zip | `dist/aigc-suite-skills.zip` | 284 KB | 其他机器本地安装整套 18 个 skill（原版内容，非上架物） |
| ~~18 个独立技能 zip~~ | `dist/skill-packages/_retired/` | 已归档 18 个 | **已冻结，不再上架**（原因见路径 B）；顶层 0 个 zip |

4 个专家交付物（3 独立 + 1 团队）已于 2026-11-07 从最终 zip 内逐项验收通过：平台字段 / 双语 / 头像 / 声明资源 / 严格 YAML / 引用闭包 / 唯一性 / 本地注册，详见路径 B 后的自检清单。

专家包本体在 `~/.workbuddy/plugins/marketplaces/my-experts/plugins/`，**四个包都已注册进 marketplace.json**，本机专家中心现在就能看到 4 个漫剧相关条目（原团队包未删、未改动）。

## 二、两条发布路径（第三条已冻结）

| | 路径 A：专家团 | ~~路径 B：独立技能~~（已冻结） | **路径 C：三个独立专家（当前主推）** |
|---|---|---|---|
| 货架 | 开放平台 → 发布管理 → **专家** | ~~开放平台 → 发布管理 → 技能~~ | 开放平台 → 发布管理 → **专家** |
| 上传次数 | 1 次，11 角色 + 18 skill | 0（不再上架） | **3 次**，一个 zip = 一个单角色专家 |
| zip 上限 | 20 MB | ~~3 MB~~ | 20 MB（实际每个 <0.7 MB） |
| 用户得到什么 | 多角色协作团队 | 已归档；整套本地安装走 `aigc-suite-skills.zip` | 3 个对话即用的专家：剧本 / 素材 / 虚拟导演 |
| 适合 | 完整交付整套方法论 | 不适用（结构性原因见路径 B） | 货架上要多个独立专家、用户可只装一环 |

**当前交付 = 路径 A + 路径 C 共 4 个专家包，均已验收可用**：按需要选 A 或 C 上架；建议不要在同一次审核里既传团队又传拆分包（能力重复、名称易混）。路径 B 已于 2026-11-07 冻结，不再生成、不再提交。

## 三、转化是怎么做的（映射规则）

按 WorkBuddy 专家开发规范 v2.0（内置「专家包管理器」skill）执行：

| 源仓库内容 | 专家包里放哪 | 本次数量 |
|-----------|-------------|---------|
| `skills/*`（SKILL.md + references/） | `skills/`（原样，不压缩改写） | 18 个 / 55 文件 |
| `shared/` 规则词典 | `shared/` | 15 文件 |
| `tools/` 机器闸门 | `tools/` | 14 文件 |
| `tests/`、`docs/flow-map.md` | `tests/`、`docs/` | 回归用例与全链图 |
| 角色定义、能力、SOP、输出规范 | `agents/*.md` | 11 个角色 |
| 流水线与阶段门禁 | 主理人 MD 的 SOP / 预设 Workflow | 8 个 Phase + 8 个 Workflow |
| 多角色分工 | `plugin.json` 的 `teamInfo` / `members` | lead 1 + member 10 |
| 示例问法 | `quickPrompts`（3 条，第 1 条 = `defaultInitPrompt`） | 3 |
| 展示信息 | `displayName` / `profession` / `displayDescription` / `tags` / `categoryId` / `avatar` | 12 张头像 |

**关键判定（不能凭直觉填）**

- `expertType = "team"`：11 个角色协作，不是单专家。卡片显示「专家团」。
- `categoryId = "06-ContentCreative"`：主要输出物是剧本、分镜、视觉资产与成片，属内容创作；服务对象是创作者而非开发者/投资者。
- Team 型铁律：`profession` 必须与 `displayName` 完全一致（均为「漫剧制片厂」）；`members` 含主理人（role=lead），`teamInfo.memberAgents` 不含；主理人文件名带团队前缀（`aigc-drama-studio-team-lead.md`）。
- `tags` 固定 3 个、`quickPrompts` 固定 3 个、`displayDescription.zh` 40–50 字（本次 48 字）、Agent MD frontmatter 不得声明 `tools`。

**标准六步**：初始化目录 → 填内容 → 生成头像 → `validate_expert.py` → `register_expert.py` → `package_expert.py`。本次全部跑通，校验 0 error / 0 warning。

## 四、本次修掉的五个坑（旧版 10-27 骨架的问题）

1. **skill 残缺**：旧包只有 12 个 skill，且 SKILL.md 被压缩改写（如 character-studio 6351→3360 字节），36 份 `references/` 全部丢失 → 已从源仓库全量 rsync，18 个原样入库。
2. **未注册**：marketplace.json 里没有它，专家中心看不到 → 已注册（当前 v1.1.2）。
3. **无头像**：`avatars/` 只有 .gitkeep，但 plugin.json 声明了 12 个路径 → 已生成 12 张统一画风头像（暖光卡通插画、粉紫调对应内容创作分类，512×512、≤496KB）。
4. **SOP 顺序反了**：旧主理人写「剧本 → 分镜 → 资产」，源仓库 `shared/output-formats.md` 明确「2026-10-30 用户重排：剧本 → 素材 → 分镜」 → 已改为资产在分镜之前，`@引用` 才有落点。
5. **两个能力域没人管**：`prop-studio`（道具资产）与 `clip-review`（成片核验回流）没有对应角色 → 新增「伍备齐 · 道具资产设计师」和「顾复之 · 成片核验与规则回流师」，同时把风格库从 5 种扩到 9 种。

## 五、本地生效（已完成）

```
专家包：~/.workbuddy/plugins/marketplaces/my-experts/plugins/aigc-drama-studio/
注册表：~/.workbuddy/plugins/marketplaces/my-experts/.codebuddy-plugin/marketplace.json
```

以后任何字段改动都要重新注册，否则卡片信息不刷新：

```bash
EM="/Applications/WorkBuddy.app/Contents/Resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/expert-manager"
DST=~/.workbuddy/plugins/marketplaces/my-experts/plugins/aigc-drama-studio
python3 "$EM/scripts/register_expert.py" "$DST"
```

## 六、上传 / 发布（open.workbuddy.cn）

> **打包 ≠ 发布。** 本地注册只让你自己可见；要上公开市场必须走开放平台审核。

### 路径 A：发布专家团

1. 打开 `open.workbuddy.cn`，完成开发者入驻与认证（个人可发专家/技能，Buddy 应用需企业资质）。
2. 左侧「发布管理」→「专家」→ 右上角「+ 创建」。
3. **配置专家**：上传 `dist/aigc-drama-studio.zip`（5.59 MB，≤20 MB，仅 .zip，v1.1.2）。平台开包解析自动生成专家 ID。
4. **确认信息**：核对名称「漫剧制片厂」、描述、市场分类（内容创作）、服务类目（1–5 个）；上传团队头像 `avatars/team.png`（512×512、≤500KB、PNG）；确认版本号 `1.1.2`。右侧可实时预览卡片。
5. **提交审核**：官方口径 7 个工作日，列表可查状态、可撤回。
6. **过审后手动点「发布」并选「公开发布」** —— 这步最容易漏，不点就永远躺在后台。发布前先把开发者信息补全，否则会失败。

注意：名称提交后即被占用；若要收费，需先有 ≥1 个过审资产才能开通收款账户，且付费模式（买断/订阅）发布后不可改，内测期平台服务费 1%。

#### ⚠️ 已踩过的解析失败：`members[0].name` 的 en/zh 均为必填

首次上传 v1.1.0 时平台报这个错，包直接被拒。**根因是本地规范自相矛盾**：`expert-manager` 的 `plugin-json-spec.md` 表格写 `members[]` 含 `name:{en,zh}`，但同文件的模板示例用了 `displayName`；按模板写出来的包能被 `validate_expert.py` 判为合法（该脚本根本不检查 members 里的姓名字段），却过不了平台解析。官方市场里两个团队专家包（`ai-content-creator-team`、`software-company`）用的是 `name`，以平台为准。

修复：11 个成员的 `displayName` 全部改为 `name`（值不变），版本升 v1.1.1，重新注册 + 重新打包。上传前用这一条命令自检，输出应为空：

```bash
python3 -c "import json;d=json.load(open('$HOME/.workbuddy/plugins/marketplaces/my-experts/plugins/aigc-drama-studio/.codebuddy-plugin/plugin.json'));print([m['id'] for m in d['members'] if not (isinstance(m.get('name'),dict) and m['name'].get('en') and m['name'].get('zh'))])"
```

通用规则：**Team 型包 `members[]` 每项的 `id` / `name{en,zh}` / `profession{en,zh}` / `avatar` / `role` 一个都不能少**，且顶层所有双语字段（`displayName`、`profession`、`displayDescription`、`defaultInitPrompt`、`tags[]`、`quickPrompts[]`）en/zh 都要有值。本地校验通过 ≠ 平台解析通过，这两个是两套规则。

#### ⚠️ 已踩过的解析失败 2：`agents/xxx.md: yaml: line 2: mapping values are not allowed in this context`

第二次上传 v1.1.1 时平台报这个错，指向主理人 MD。**根因是 frontmatter 的 `description:` 写成了裸标量，值里含「冒号+空格」**——例如 `Owns the show-level plan and scheduling: routes novel or idea...`。YAML 里 `: ` 会被当成新映射的起始，go-yaml / psych 一律报错；`validate_expert.py` 用正则扫 frontmatter，只判断字段在不在，从不真正解析 YAML，所以照样判"合法"。

用标准解析器实测，11 个 agent 里有 3 个中招（`aigc-drama-studio-team-lead`、`drama-character-designer`、`drama-shot-inspector`）；为消除整类风险，把 **11 个 agent 的 `description` 全部改成带双引号的 YAML 标量**（只加引号，文字一字未改），版本升 v1.1.2。18 个上架技能包的 SKILL.md 也一起过了严格解析，无此问题，无需重生成。

上传前跑这条命令，**无输出即通过**（macOS 自带 Ruby，不必装 PyYAML）：

```bash
cd ~/.workbuddy/plugins/marketplaces/my-experts/plugins/aigc-drama-studio
ruby -ryaml -e 'Dir.glob("**/*.md").each{|f| l=File.readlines(f,chomp:true); next unless l[0]=="---"; s=l[1..].index("---"); next unless s; begin; YAML.load(l[1,s].join("\n")); rescue => e; puts "#{f}: #{e.message.lines.first}"; end }'
```

通用规则：frontmatter 里凡是值含 `: `、` #`、行首 `&`/`*`/`{`/`[`/`"`，都不要写裸标量，统一用双引号包起来（内部 `"` 和 `\` 要转义）。`validate_expert.py` 通过只说明结构合规，**不能替代 YAML 解析**。最稳的做法是打包后把 zip 解开、对包内所有 `.md` 跑一遍解析器，而不是只查源目录。

### 路径 C：逐个上架 3 个独立专家（当前主推）

2026-11-06 按用户要求，把 11 角色专家团拆成 3 个 **Agent 型**独立专家。每个包各走一遍
`init_expert.py → 填内容 → validate_expert.py → register_expert.py → package_expert.py`，
互不依赖、可分别审核、分别发布；原专家团 `aigc-drama-studio` 保留不动。

| 独立专家（目录 / zip） | 花名 / 职业（卡片标题） | 合并的原角色 | 挂载 skills | 主要输出 |
|---|---|---|---|---|
| `drama-episode-writer` | 漫剧分集编剧室 / 漫剧分集编剧 | 文择章（网文改编）、简灵犀（原创） | `novel-to-drama`、`idea-to-drama` | 分集方案表 + 剧本条目 + 交接卡 |
| `drama-asset-designer` | 漫剧素材设计室 / 视觉资产设计师 | 肖定妆、苏置景、伍备齐、林定调 | `character-studio`、`scene-studio`、`prop-studio` + 9 个 `style-*` | assets.json + 风格卡 + 生图指令 + 对账表 |
| `drama-virtual-director` | 漫剧虚拟导演 / 分镜与出片导演 | 柏景深、严过闸、毕成片、顾复之 | `storyboard-director`、`shot-qa`、`video-producer`、`clip-review` | 分镜块 + 检查报告 + 生成包 + 核验报告 |

**拆分口径**

- 18 个 skill **全量覆盖且零重叠**（2 + 12 + 4）；三域靠 `shared/output-formats.md` 的 LOCKED 数据契约衔接，Agent MD 写明上下游与《交接卡》，**不调度团队、不写 SendMessage / TeamCreate**——三个专家是独立会话，跨专家必须粘贴完整产出原文（零压缩铁律）。
- `expertType = "agent"`（单角色）、`categoryId = "06-ContentCreative"`（三者主要输出物均为剧本 / 视觉资产 / 分镜成片，服务对象是创作者）。
- 每个包**自包含**：本域 skills + 全量 `shared/`（15）与 `tools/`（14）+ `docs/flow-map.md` + 1 张头像；跨 skill 的 references 引用按闭包迭代补齐（只补被引用的 .md，不补 SKILL.md），包内带 SKILL.md 的目录与 `plugin.json` 声明完全一致。
- 头像沿用原团队同画风的 512×512 PNG（均 <500KB）：改编编剧 / 人物设计师 / 虚拟导演三张，统一重命名为 `avatars/expert.png`。
- 构建脚本 `tools/build_individual_experts.py`：构建时从仓库一次性取材，包发布后独立演进、不随仓库提交自动变化；脚本幂等（重跑覆盖重建三个包并重新校验 / 注册 / 打包），内置从最终 zip 反查的双语字段、严格 YAML、引用闭包与体积自检。

| 上架包 | 文件数 | 大小 | 自检 |
|---|---|---|---|
| `dist/expert-packages/drama-episode-writer.zip` | 47 | 638 KB | 0 error；30 篇 md 严格 YAML；引用闭包完整 |
| `dist/expert-packages/drama-asset-designer.zip` | 70 | 664 KB | 0 error；53 篇 md 严格 YAML；引用闭包完整 |
| `dist/expert-packages/drama-virtual-director.zip` | 57 | 625 KB | 0 error；40 篇 md 严格 YAML；引用闭包完整 |

上传步骤：发布管理 →「专家」→ + 创建 → 分别上传三个 zip → 核对花名 / 职业 / 描述 / 分类（内容创作）/ 头像 `avatars/expert.png` / 版本 `1.0.0` → 提交审核 → **过审后逐个手动点「发布」并选「公开发布」**。三个名称提交后即被占用，先想好再交。

#### ⚠️ 名称重复 / 已被占用（2026-11-07，剧本专家两次改名）

- **两次报错，判重字段不同，别只改 ID 和花名**：
  1. 上传 `drama-scriptwriter.zip` → 专家名重复（名称提交后即被占用）。
  2. 上传改名后的 `drama-episode-writer.zip` → `解析失败：该名称"剧本创作专家"已被使用，请修改 plugin.json 中的 profession.zh（需在同类型资产中保持唯一）后重新提交`。**`profession.zh` 也参与唯一性校验**，与 `name` / `displayName` 是各自独立的判重项；平台一次只报第一项失败，改完可能还有下一项。
- 先分辨两种情形：**同名条目是自己此前创建的** → 不要新建、也不用改名，直接在该条目里替换 zip 再提交审核；**平台上已存在同名 / 需要另开条目** → 走下面的改名流程。
- 最终口径（**ID + 中英花名 + 中英职业名一起改**，一次到位）：

  | 字段 | 原值 | 现值 |
  |---|---|---|
  | `name` / `agentName` / `plugin` | `drama-scriptwriter` | `drama-episode-writer` |
  | `displayName.zh` / `.en` | 漫剧剧本工坊 / Drama Script Atelier | 漫剧分集编剧室 / Drama Episode Writing Studio |
  | `profession.zh` / `.en` | 剧本创作专家 / Screenwriting Expert | 漫剧分集编剧 / Drama Episode Screenwriter |

  能力描述、技能分组、分类、prompts 一律不动。职业名换成本域细分词，避开「XX专家」这类通用头衔——最容易被占用。
- 改名必须全链路同步，否则另两个专家的交接文字会指向不存在的专家：`tools/build_individual_experts.py` 里的 `BASE_PLUGIN` key、`ORDER`、Agent MD frontmatter 的 `name` / `profession`、`UPSTREAM` / `DOWNSTREAM`、另两个专家正文里的上下游称呼，以及本文产物清单。重跑脚本会重建**三个**包（另两个只改交接称呼，能力与文件数不变）。
- 旧件一律归档、不删除：`dist/expert-packages/_retired/drama-scriptwriter.zip`（**勿再上传**）、`dist/_retired-plugins/drama-scriptwriter/`（旧插件目录，可拖回还原）；`marketplace.json` 中旧 ID 注册项已注销，本地专家中心不会再出现重复卡片。脚本的 `RETIRED_IDS` 负责幂等注销与归档，重跑不会复活旧名。
- 复核（从最终 zip 内）：`plugin.json` 的 `name` / `agentName` / `plugin`、zip 根目录、Agent MD 文件名五处一致；`displayName` 与 `profession` 的 en/zh 均为新值；三个包内旧 ID / 旧花名 / 旧职业名 0 残留；30 / 53 / 40 篇 md 严格 YAML、引用闭包、体积全过。

### 路径 B：18 个独立技能（已冻结，不再上架）

**2026-11-07 用户决定：不做单独的技能包，只保证 3 个独立专家 + 1 个专家团可用。**

- **结构性原因**：这 18 个 skill 本来就是一条流水线（剧本 → 人物 / 场景 / 道具 / 风格素材 → 分镜 → 三道闸 → 出片 → 成片核验），共用 `shared/` 15 份规则与 `tools/` 14 个脚本，SKILL.md 正文直接写协作关系（`走 prop-studio`、`交 shot-qa`、素材由 `character/scene/prop-studio` 供给、风格由 `style-*` 提供），还有 `skills/<其它 skill>/references/xxx.md` 文档互引。**「单独」只是打包形态，不是设计形态**；平台「一个 zip = 一个技能、按引用反查必需资源」的规则下无法原样成立。
- **三轮驳回递进**（评级均为「内置文件缺失」）：v1.0.0 缺跨 skill 文件路径 → 把目标文档扁平化补进 `references/` 并改写引用；v1.0.1 缺技能 ID → 把 18 个 ID 换成中文展示名；v1.0.2 平台又把中文展示名（「道具资产设计」「人物资产设计」「场景资产设计」「style-* 风格技能」）判成技能引用。换词是打地鼠，方向错了。
- **结论**：继续修词没有尽头。真要做独立技能，只能为每个 skill 重写一份不含任何跨技能引用的规则文本（等于维护 18 份与专家包分叉的规则），代价大且长期两套口径，不做。跨技能协作的完整交付走专家路径——专家包带全量 `skills/` + `shared/` + `tools/`，路径本来就有效。
- **处置**：`dist/skill-packages/` 顶层 18 个 zip 已移入 `_retired/`（移动不删除，可还原），顶层 0 个 zip，不会再误传；`tools/build_platform_skill_packages.py` 保留但不执行、不再生成上架包。平台上已驳回的条目不再重提。
- **源仓库零影响**：`git status --short skills/ shared/` 为空——源 skill 与共享规则一个字没改；所有脱敏只作用于打包时的 `dist/skill-packages/_build/` 副本。三个专家包、专家团、本机安装的 skill 全是原版内容，完全不受影响。
- **整套安装包保留**：`dist/aigc-suite-skills.zip` 是给本机 / 其他机器一次装齐 18 个 skill 的原版包，不是上架物，继续有效。

### 上传前自检清单

- [ ] zip 扩展名、大小未超限（专家 20MB）
- [ ] 专家包 `plugin.json` 的 `skills`/`agents`/`members`/`teamInfo` 四个数组与实际文件一致
- [ ] **`members[]` 每项都有 `name:{en,zh}`（不是 `displayName`）——平台会因这个字段直接拒包**
- [ ] **所有 `.md` 的 frontmatter 能被标准 YAML 解析器解析**（见上文 Ruby 命令）；含 `: ` 的值必须加引号
- [ ] 所有双语字段 en/zh 非空；`validate_expert.py` 0 error（本地通过不代表平台通过）
- [ ] 打包后从 zip 内再验一遍，别只查源目录
- [ ] **交付范围**：只验 4 个专家交付物（3 个独立 Agent + 1 个 Team）；`dist/skill-packages/` 顶层应为 0 个 zip（18 个已归档 `_retired/`，路径 B 已冻结）
- [ ] **三个独立专家包（路径 C）**：`python3 tools/build_individual_experts.py` 末尾自动从最终 zip 自检 `expertType=agent` / 双语字段 / 3 tags + 3 prompts / 首条 = `defaultInitPrompt` / 严格 YAML / 引用闭包 / ≤20MB / 头像 ≤500KB；三个 zip 各传各的，别合并
- [ ] Agent 型包 `skills` 数组 = 本域技能，包内带 SKILL.md 的目录与之完全一致；**无** `members` / `teamInfo` / `settings.json`；专家包内 `skills/` 引用保留有效路径（这条只适用于专家包，不适用于已冻结的独立技能包）
- [ ] 12 张头像齐全、512×512、≤500KB（专家团用）；三个独立专家各 1 张 `avatars/expert.png`
- [ ] 3 个 tags、3 个 quickPrompts、第 1 条 = defaultInitPrompt
- [ ] `description` 写清了用途与触发词，没有尖括号、没有「可能/也许」这类模糊词
- [ ] 名称想好再提交（提交后占用）；`plugin.json` 的 `name`（唯一标识）、`displayName.zh/en`、`profession.zh/en` 在同类型资产中**均需唯一**。被判重时 ID + 中英花名 + 中英职业名一起改，并重跑 `build_individual_experts.py` 同步三个包的交接称呼（见路径 C 的改名小节）
- [ ] 开发者信息已补全（否则发布失败）

**2026-11-07 收口验收（已完成，0 失败）**：4 个交付物均从最终 zip 内逐项通过——平台字段（`name` / `agentName` / `plugin` / 根目录一致）、双语字段、头像 512×512 且 ≤500KB、`agents[]` / `skills[]` 声明资源齐全、严格 YAML（30 / 53 / 40 / 92 篇 md）、引用闭包零断链、四包名称唯一性、本地 `marketplace.json` 4 项注册与源目录一致。专家团 README 里的 `shared/xxx.md`、`tools/xxx.py` 是说明性占位符，不参与断链判定。

## 七、产物清单

```
/Users/yangdongnan/work/aigc-suite-skills/
├── dist/
│   ├── expert-packages/                         3 个独立专家上架包（v1.0.0，各 <0.7 MB）
│   │   ├── drama-episode-writer.zip   638 KB / 47 文件
│   │   ├── drama-asset-designer.zip   664 KB / 70 文件
│   │   ├── drama-virtual-director.zip 625 KB / 57 文件
│   │   └── _retired/                           旧名包归档，勿上传
│   │       └── drama-scriptwriter.zip
│   ├── _retired-plugins/                        旧名插件目录归档（可还原）
│   ├── aigc-drama-studio.zip              5.59 MB 专家团上架包（126 文件，v1.1.2）
│   ├── aigc-suite-skills.zip             284 KB  整套 skill 本地安装包
│   └── skill-packages/                           路径 B 已冻结：顶层 0 个 zip
│       └── _retired/                            18 个旧上架包归档（可还原，勿上传）
├── tools/build_individual_experts.py            三个独立专家构建脚本（拆分 / 闭包 / 校验 / 注册 / 打包 / zip 内自检）
├── tools/build_platform_skill_packages.py       已冻结：独立技能上架包生成脚本（保留备查，不再执行）
└── docs/WorkBuddy专家团与Skill包上传指南.md      本文

~/.workbuddy/plugins/marketplaces/my-experts/plugins/
├── drama-episode-writer/      Agent：1 个 MD + 2 skills + 全量 shared/tools + 1 头像
├── drama-asset-designer/      Agent：1 个 MD + 12 skills + 全量 shared/tools + 1 头像
└── drama-virtual-director/    Agent：1 个 MD + 4 skills + 全量 shared/tools + 1 头像

~/.workbuddy/plugins/marketplaces/my-experts/plugins/aigc-drama-studio/
├── .codebuddy-plugin/plugin.json   ← 11 agents / 18 skills / 11 members
├── agents/      11 个角色 MD（含主理人 SOP + 8 个 Workflow + 协作铁律）
├── skills/      18 个 skill + 36 份 references
├── shared/      15 份共享规则
├── tools/       14 个机器闸门与脚本
├── avatars/     12 张头像
├── docs/ tests/ settings.json README.md
```

10-27 版旧骨架（v1.0.0、12 个压缩 skill、无头像）已按 2026-11-06 的指令清理，移入 macOS 废纸篓 `~/.Trash/aigc-drama-studio.bak-20261106-1335-20261106-135622/`，需要时可直接拖回还原；`.backups/` 目录已一并移除。现役专家包自带完整副本，无需依赖此备份。

## 八、两条线各自维护（互不绑定）

- **GitHub 仓库**：正常 git 提交、正常发版即可，不需要动专家团、不需要重打包。
- **WorkBuddy 专家团**：只有决定让专家团吸收仓库的新内容，或专家团自身的角色 / SOP / 展示信息要改时，才在专家包目录里单独操作一次，版本号与平台审核按专家团自己的流程重走。

下面是**「决定更新专家团内容」这一种情况**下的操作顺序；取材自仓库，但不属于仓库的提交流程，也不构成两边同步：

```bash
cd ~/work/aigc-suite-skills
DST=~/.workbuddy/plugins/marketplaces/my-experts/plugins/aigc-drama-studio
EM="/Applications/WorkBuddy.app/Contents/Resources/app.asar.unpacked/resources/plugins/workbuddy-builtin/skills/expert-manager"

# 1. 从仓库取一次内容（仅此次决定更新时）
for p in skills shared tools tests; do
  rsync -a --delete --exclude='.DS_Store' --exclude='__pycache__' --exclude='*.pyc' "$p/" "$DST/$p/"
done

# 2. 若增删了 skill 或角色，改专家包自己的 plugin.json 四个数组（否则校验会报路径不存在）

# 3. 校验 + 注册 + 重打包（版本号记得递增）
python3 "$EM/scripts/validate_expert.py" "$DST"
python3 "$EM/scripts/register_expert.py" "$DST"
python3 "$EM/scripts/package_expert.py" "$DST" dist

# 4. 独立技能上架路径已冻结（2026-11-07）：无需执行、不要重生成
#    tools/build_platform_skill_packages.py 保留备查；18 个包已归档到 dist/skill-packages/_retired/

# 5. 三个独立专家（路径 C）：改了 Agent 设定 / 展示字段 / 技能分组后重跑
#    脚本自行完成 init（首次）/ 覆盖内容 / 闭包补齐 / 校验 / 注册 / 打包 / zip 内自检
#    并幂等注销 RETIRED_IDS 里的旧名注册、归档旧插件目录与旧 zip（移动不删除）
python3 tools/build_individual_experts.py
```

版本号两处（都属专家团 / 上架产物这一侧，与仓库版本无关）：专家团 `plugin.json` 的 `version`（现 v1.1.2）、三个独立专家各自 `plugin.json` 的 `version`（由 `tools/build_individual_experts.py` 的 `VERSION` 统一写入，现 v1.0.0）。驳回改完重交时递增，方便追溯；两条发布线独立升版。已冻结的 `build_platform_skill_packages.py` 不再参与版本管理。

## 九、已知限制与兜底

- `novel-to-drama/references/browser-dump.md` 里的 `tools/playwright` 指 chrome-devtools / playwright **MCP**，不是本包内置脚本，按需在会话中挂载。
- `tools/ocr.swift` + `build_ocr.sh`、`fanqie_ocr.py` 仅在 macOS 本地抽取正文时使用；用途声明见源仓库 README，本包不含任何对抗/绕过手段。
- 平台若对 `shared/`、`tools/` 这类非标准子目录报解析失败：把生成脚本里这两个目录名改为 `assets/` 与 `scripts/`，同时对包内所有 md 做一次 `shared/xxx` → `assets/xxx`、`tools/xxx` → `scripts/xxx` 的路径替换即可；也可发邮件到 `openworkbuddy@tencent.com` 附报错原文。（此兜底仅针对独立技能包，该路径已冻结；专家包带完整 `skills/` 层，不需要这样改。）
- 技能市场按「一个 zip = 一个技能」解析，**不能**把 18 个 skill 塞一个 zip 当技能传；跨技能协作的完整交付走专家路径，独立技能上架已冻结（见路径 B）。
- 头像右下角带模型生成的来源水印，如需去除可自行替换 `avatars/*.png`（保持文件名、512×512、≤500KB）。
- **三个独立专家包内 `skills/` 下有少量仅含 references 的空壳目录**（跨 skill 引用闭包，不是技能，无 SKILL.md）；这是专家包结构，与已冻结的独立技能包口径不同，不要按技能包口径去删。若专家包上架时平台仍按目录扫描报「技能缺 SKILL.md」，兜底：把这些 .md 移到 `shared/`，并把包内 `skills/<x>/references/<f>` 与 `../<x>/references/<f>` 引用改写为 `shared/<f>`（同名冲突加 skill 名前缀），再重打包。
- 三个独立专家与专家团在本机同时注册（marketplace 6 项中的 4 项），同名 skill 出现在不同插件命名空间下，本机使用不受影响；**4 个专家包均已验收可用**，按路径 A 或 C 选择上架，别把独立技能包混进来。若不想本机重复，在专家中心停用 `aigc-drama-studio` 即可，无需删文件。
