# <Skill 名称>

## 概述

一句话说明这个技能。

## 知识库结构

```
knowledge/
├── roadmap.md          # 学习路线
├── glossary.md         # 术语速查表
├── 01-topic/           # 章节
│   └── <concept>/      # 概念
│       ├── README.md   # 正文
│       ├── examples.md # 示例
│       ├── exercises.md# 练习
│       ├── mistakes.md # 常见错误
│       ├── interview.md# 面试题
│       └── references.md
└── ...
```

## 使用方式

1. 用户提问 → 在知识库中搜索
2. 已有内容 → 提炼回答 + 引导阅读原文
3. 没有覆盖 → 通用讲解 + 可选保存

## 面向人群

大学生和初级开发工程师。

## 维护

- 新概念从 `shared/templates/knowledge/` 复制模板
- 完成后跑 `python tools/lint.py` 校验
- 跑 `python tools/metadata.py` 检查元数据
