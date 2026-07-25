# Naming Conventions

## 技能命名

- 格式：`qzz-<domain>`，如 `qzz-explain`、`qzz-mysql`
- 全小写字母 + 数字 + 连字符，最长 64 字符
- 目录名 = SKILL.md frontmatter 中的 `name` 字段
- `qzz`（不带后缀）保留给编排入口

## 章节目录命名

- 格式：`NN-topic`，NN = 两位数字编号
- `topic` 使用英文小写，单词间用连字符
- 编号固定，不可插入新编号

## 概念目录命名

- 格式：`<concept-name>`
- 全小写英文 + 连字符
- 尽量控制在 2-4 个单词
- 示例：`create-table`、`inner-join`、`transaction-isolation`

## 文件名

- `SKILL.md`、`README.md`、`LICENSE` — 大写
- `metadata.yaml`、`roadmap.md`、`glossary.md` — 小写
- `examples.md`、`exercises.md`、`mistakes.md`、`interview.md`、`references.md` — 小写

## 资源目录

- `assets/` — 所有资源目录统一用此名称
- `images/`、`diagrams/`、`sql/`、`datasets/` — 小写复数
