---
name: qzz-roadmap
description: >
  Generate structured learning roadmaps for technical domains with dependency graphs,
  milestones, and verification checkpoints. Use when the user asks "how do I learn X",
  "learning path for X", "what order should I learn", "roadmap for X", wants a study
  plan, or needs guidance on where to start with a new technical domain. Produces
  staged learning paths with prerequisites, estimated timelines, and self-check criteria.
license: CC BY-NC 4.0
---

# Purpose

为一个技术领域生成结构化的学习路线图。不是罗列话题列表——是找出话题之间的**依赖关系**，排出一条"不走弯路"的学习路径。

核心原则：
- **依赖驱动排序**：话题 A 必须在话题 B 之前，因为 B 的底层机制用了 A
- **最小可行路径**：先画出一条"能开始干活"的最短路径，再逐步深入
- **可验证的里程碑**：每个阶段必须有明确的"你学会了"的判定标准，不能模糊
- **区分主干和枝节**：明确哪些是必须掌握的（blocker），哪些是锦上添花的（nice-to-have）

与 `qzz-explain` 的关系：roadmap 画地图，explain 当导游。roadmap 告诉你学什么、按什么顺序；explain 带你深入地图上的每一个点。

# When to use

触发场景：
- "我想学 X，从哪里开始？"
- "学 X 的学习路线是什么？"
- "X 的学习路径 / roadmap"
- "我想成为 X 方向的开发者，需要学什么？"
- 用户在学习中途感到迷失，需要重新梳理方向

不适用场景：
- 解释某个具体概念（走 `qzz-explain`）
- 推荐学习资源但不关心顺序（这不是资源列表工具）

# Workflow

## 第一步：明确边界

向用户确认三个信息：
1. **目标领域**：具体学什么（"MySQL"还是"数据库"？范围差很多）
2. **当前水平**：零基础 / 用过但不系统 / 想深入某个子领域
3. **目标深度**：能干活（够用） / 面试准备 / 深入原理（造轮子）

如果用户没说清楚，主动追问。不要猜。

## 第二步：画出依赖图

1. 列出该领域所有核心话题（10-20 个）
2. 标注每个话题的**硬依赖**（不学会 A 就完全无法理解 B）
3. 标注每个话题的**软依赖**（先学 A 会更顺，但不学也能硬啃 B）
4. 找出没有依赖的"根话题"作为起点

## 第三步：分阶段

将依赖图转化为 3-5 个阶段，每个阶段的标准：

- **阶段内话题数**：3-5 个，太多学习者会失去方向感
- **阶段有明确主题**：如"理解数据模型""掌握查询能力""深入存储引擎"
- **阶段间有清晰的升级感**：完成一个阶段后，你"能做一件之前做不了的事"
- **每个阶段给出预估时间**：以"每周可投入 8-10 小时"为基准

## 第四步：标注验证方式

每个阶段结束时，给出具体的验证方法——不是"读完了"，而是：

- ✅ 能回答某类问题
- ✅ 能写出某类代码
- ✅ 能解释某个机制为什么这样设计
- ✅ 能用一个自建项目综合运用本阶段知识

## 第五步：关联资源

- 优先检查 `qzz-mysql` skill 的知识库：`../qzz-mysql/knowledge/`（17 章 71 个概念）
- 已有知识库覆盖范围：01-basic（基础）→ 02-ddl → 03-dml → 04-query → 05-function → 06-index → 07-transaction → 08-lock → 09-execution → 10-performance → 11-design → 12-engine → 13-replication → 14-backup → 15-security → 16-cluster → 17-source（源码）
- 每个概念包含 7 个文件：README.md / metadata.yaml / examples.md / exercises.md / mistakes.md / interview.md / references.md
- 在 roadmap 中标注已有知识库可查阅的话题，格式：`📖 qzz-mysql/knowledge/<章节>/<概念>/`
- 对于知识库中缺失的话题，标记为 `📖 建议建设`

# Output style

## 路线图结构

```
📚 学习路线：{领域名称}
━━━━━━━━━━━━━━━━━━━━

🎯 目标画像：完成这条路线后，你能______

📋 前置条件：需要______基础

━━━━━━━━━━━━━━━━━━━━

🏔️ 阶段一：{主题名}（预计 X 周）
   ├── 🔴 必学：话题A → 话题B → 话题C
   ├── 🟡 选学：话题D
   ├── ✅ 验证：{具体的验证方式}
   └── 📖 资源：knowledge/xxx/

🏔️ 阶段二：{主题名}（预计 X 周）
   ...

🏔️ 阶段三：{主题名}（预计 X 周）
   ...

━━━━━━━━━━━━━━━━━━━━

🗺️ 依赖全景图（ASCII 树状图）
  话题A
   ├── 话题B（依赖A）
   │   ├── 话题D（依赖B）
   │   └── 话题E（依赖B）
   └── 话题C（依赖A）

⚡ 快速启动路径（最小可行路径，最快能开始干活）
  话题A → 话题B → 话题E（跳过D和C，先能干活再说）

📊 总预估时间：X-Y 周
```

## 标记说明

| 标记 | 含义 |
|------|------|
| 🔴 必学 | 不学这个后面走不下去，是硬依赖 |
| 🟡 选学 | 学了更好，不学也不影响后续 |
| ✅ 验证 | 客观可判定的"学会了"标准 |
| 📖 资源 | knowledge/ 中已有或建议建设的知识库路径 |
| ⚡ 快速启动 | 砍掉所有非必要路径后的最短可达路径 |

# Constraints

- 依赖关系不能出错：如果学 B 需要先懂 A，必须标出来。不要把结果放原因前面
- 每个阶段 3-5 个必学话题，不超过 7 个总数（含选学）。超过就拆分阶段
- 验证方式必须**可判定**。"理解了 X"不是验证方式；"能写一个 SQL 解释它用了哪个索引，为什么"才是
- 预估时间按"每周 8-10 小时投入"为基准，不要低估——学习者不是全职学习
- 必须画依赖全景图——这是整个路线图的核心价值，不能省略
- 如果领域内有重大争议（如"先学 C 还是先学 Python"），给出两条路径并说明各自的 trade-off，而非强行推荐一条
- 知识库已有的话题必须引用路径，格式：`📖 qzz-mysql/knowledge/<章节>/<概念>/`
- 知识库缺失的重要话题标记为 `📖 建议建设：skills/qzz-mysql/knowledge/<章节>/<概念>/`
- 生成 MySQL 路线图时，先检查是否安装了 `qzz-mysql` skill（`../qzz-mysql/knowledge/`）
- 安装了则直接引用 qzz-mysql 的章节和概念名；未安装则正常生成路线图，并提示安装：`npx skills add qinzhaiz/qzz-skill --skill qzz-mysql`
- 对其他领域照常生成路线图，不需要本地知识库
