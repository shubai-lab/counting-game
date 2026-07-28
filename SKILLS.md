# 技能分类清单

> 📋 本项目的技能按使用场景分为「全局通用」和「项目专用」两类。
> 🔄 项目专用技能通过 git 同步，团队成员自动获得。

---

## 🌍 全局通用技能

存放路径：`~/.agents/skills/`

| 技能 | 说明 | 安装命令 |
|------|------|---------|
| memory-merger | 记忆合并，将成熟记忆合并到 instruction 文件 | `npx skills add github/awesome-copilot@memory-merger -g -y` |
| remembering-conversations | 对话历史搜索，dispatch search-conversations agent | `npx skills add obra/episodic-memory@remembering-conversations -g -y` |
| simplify | 代码优化，Review changed code for reuse | 已安装 |
| skill-creator | 创建/修改技能，通用开发工具 | 已安装 |
| find-skills | 技能查找，`npx skills find` 命令入口 | 已安装 |

---

## 📁 项目专用技能

存放路径：`.claude/skills/`（已配置 git 同步）

### 设计系统（Figma + UI）

| 技能 | 说明 | Agent角色 |
|------|------|----------|
| figma | Figma MCP 集成，fetch design context | 小美（UE设计师） |
| figma-use | Figma 使用前置技能，**MANDATORY prerequisite** | 小美 |
| figma-implement-design | 将 Figma 设计转为代码，1:1 视觉还原 | 小码（程序员） |
| figma-generate-design | 将应用页面转为 Figma 设计 | 小美 |
| figma-create-design-system-rules | 生成设计系统规则 | 小美 |
| figma-create-new-file | 创建新 Figma 文件 | 小美 |
| ue-design-spec | 十周年游戏 UI 设计规范（弹窗/按钮/字色/动效） | 小美 |
| bencium-impact-designer | 高质量前端界面设计 | 小美 |

### 数据分析（Metabase + SQL）

| 技能 | 说明 | Agent角色 |
|------|------|----------|
| data-analysis | Excel/CSV 数据分析，生成洞察和可视化 | 小数（数据分析师） |
| exploratory-data-analysis | 科学数据探索分析，200+ 文件格式 | 小数 |
| data-analysis-methodology | 数据分析方法论（《谁说菜鸟不会数据分析》等） | 小数 |
| chart-visualization | 数据可视化，26 种图表智能选择 | 小数 |
| infographic-creator | 创建信息图，报告可视化 | 小数 |
| ppt-visual | PPT 可视化设计，生成分析报告 | 小数 |

### 游戏系统设计

| 技能 | 说明 | Agent角色 |
|------|------|----------|
| huashu-nuwa | 女娲造人，输入人名生成人物 Skill | 小系（系统策划） |
| shang-xirui-perspective | 商细蕊思维框架（100条台词深度调研） | 角色扮演 |
| yinzheng-perspective | 尹正思维框架（180条微博深度调研） | 角色扮演 |

### OpenSpec 工作流

| 技能 | 说明 | 用途 |
|------|------|------|
| openspec-propose | 提出新变更，生成所有 artifacts | `/openspec-propose` |
| openspec-explore | 需求探索，thinking partner | `/openspec-explore` |
| openspec-apply | 任务执行，实现变更 | `/openspec-apply` |
| openspec-archive | 归档完成变更 | `/openspec-archive` |

### 需求原型工作流

| 技能 | 说明 | 来源 |
|------|------|------|
| pm-agile-workflow | 游戏策划工作流：PRD + HTML 原型 + Mermaid 流程图，九步引导式产出 | arcsin1/pm-agile-workflow |

### 浏览器自动化

| 技能 | 说明 | Agent角色 |
|------|------|----------|
| steel-browser | 浏览器自动化（JS渲染/表单/复杂抓取） | 通用工具 |
| chrome-cdp-skill | Chrome CDP 交互，本地浏览器调试 | 小码 |

---

## 📝 技能管理命令

### 安装项目技能

```bash
# 不加 -g flag，安装到项目级
npx skills add owner/repo@skill-name -y
```

### 查看已安装技能

```bash
npx skills list
```

### 更新技能

```bash
# 更新项目技能
npx skills update

# 更新全局技能
npx skills update -g
```

---

## 🔄 技能迁移记录

**迁移时间**：2026-04-22

从全局迁移到项目级的技能（15个）：
- ✅ bencium-impact-designer
- ✅ chart-visualization
- ✅ data-analysis
- ✅ exploratory-data-analysis
- ✅ figma
- ✅ figma-create-design-system-rules
- ✅ figma-create-new-file
- ✅ figma-generate-design
- ✅ figma-implement-design
- ✅ figma-use
- ✅ huashu-nuwa
- ✅ infographic-creator
- ✅ ppt-visual
- ✅ steel-browser
- ✅ ue-design-spec

---

## 🎯 常见场景

### 数据分析任务
调用：小数（data_analyst_role.md）
技能：data-analysis + chart-visualization + data-analysis-methodology

### UI 设计任务
调用：小美（ue_designer_role.md）
技能：figma-use → figma-implement-design + ue-design-spec

### 系统设计任务
调用：小系（system_planner_role.md）
技能：huashu-nuwa（生成人物 Skill）

### OpenSpec 工作流
命令：`/openspec-propose` → `/openspec-explore` → `/openspec-apply` → `/openspec-archive`

---

**最后更新**：2026-05-07