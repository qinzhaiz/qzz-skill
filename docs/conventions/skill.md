# Skill Development Conventions

## SKILL.md 格式

```yaml
---
name: <skill-name>            # 小写字母 + 数字 + 连字符，最长 64 字符，与目录名一致
description: >                # 最长 1024 字符，必须包含触发关键词
  What the skill does AND when to use it.
  Include trigger keywords to help agents identify relevant tasks.
license: CC BY-NC 4.0          # 可选但建议
---
```

## 标准章节

每个 SKILL.md 应包含以下章节：

1. `# Purpose` — 这个技能解决什么问题
2. `# When to use` — 触发场景和关键词
3. `# Workflow` — 具体执行流程
4. `# Output style` — 输出格式和风格要求
5. `# Constraints` — 硬性约束（不做什么）

## 两种技能类型

### 知识型（Knowledge-type）

特征：维护结构化知识库，包含章节和概念。
目录结构见 `shared/templates/skill/knowledge/`。
实例：`qzz-mysql`

### 流程型（Flow-type）

特征：纯编排/工作流，不维护知识库。
目录结构见 `shared/templates/skill/flow/`。
实例：`qzz`、`qzz-explain`、`qzz-roadmap`、`qzz-practice`

## description 写作要求

- 必须包含 3-5 个触发关键词（用户会怎么问就用什么词）
- 中文描述用中文关键词，英文描述用英文关键词
- 不要只写功能，要写"用户什么时候会用这个"
- 技能名称本身不算触发关键词（Claude 不会因为用户说了 skill 名字就触发）

## 发布

通过 skills.sh 自动索引（公开 GitHub 仓库有 SKILL.md 即自动发现）。用户安装：

```bash
npx skills add qinzhaiz/qzz-skill --all
```
