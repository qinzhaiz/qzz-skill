# Metadata Conventions

## 概念级 metadata.yaml

位于每个概念目录下（`knowledge/NN-topic/<concept>/metadata.yaml`）：

```yaml
name: <concept-name>           # 概念英文名（小写 + 连字符）
section: <NN-topic>            # 所属章节，如 01-basic
difficulty: beginner           # beginner | intermediate | advanced
prerequisites:                 # 前置概念列表（相对于 knowledge/ 根目录）
  - 01-basic/database-intro
topics:                        # 关键词标签
  - sql
  - ddl
  - create-table
updated: 2026-07-25            # 最后更新日期
```

## 技能级 metadata.yaml

位于技能根目录下（`skills/<skill-name>/metadata.yaml`），仅知识型技能需要：

```yaml
name: <skill-name>             # 与目录名一致
version: 1.0.0
chapters: 17                   # 章节总数
concepts: 0                    # 概念总数
updated: 2026-07-25
```

## 约束

- 所有日期使用 ISO 8601 格式：`YYYY-MM-DD`
- `name` 字段必须与所在目录名一致
- `difficulty` 只能是 `beginner`、`intermediate`、`advanced`
- `prerequisites` 为空时写 `[]`，不要省略
- `topics` 至少包含 2 个标签
