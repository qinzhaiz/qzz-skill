# Knowledge Conventions

## 概念目录结构

每个知识概念是一个目录，必须包含以下 7 个文件，从 `shared/templates/knowledge/` 复制：

| 文件 | 内容 |
|------|------|
| `README.md` | 正文：为什么需要 → 是什么 → 怎么工作 → 怎么用 → 注意事项 → 和什么有关 |
| `metadata.yaml` | `name`, `section`, `difficulty`, `prerequisites`, `topics`, `updated` |
| `examples.md` | 场景 → 代码 → 输出 → 解释 |
| `exercises.md` | 基础练习 + 进阶练习 + 答案 |
| `mistakes.md` | 常见错误：症状 → 原因 → 修复 |
| `interview.md` | 面试题：考点 → 回答 → 加分点 |
| `references.md` | **仅放官方文档和公开文章**，不放版权书籍 |

外加一个 `assets/` 目录，存放配图、SQL 文件等资源。

## 写作约束

- 面向大学生和初级开发工程师，从零开始
- 每篇 README 控制在 200-500 字
- 代码示例必须可独立运行
- 中文正文，技术名词保留英文
- 不深入源码级实现细节（留给 17-source）
- 不引用版权书籍或付费内容
- 知识点之间用相对路径链接

## 章节组织

- 每章一个目录：`knowledge/NN-topic/`（NN = 两位数字编号）
- 每章下面挂多个概念子目录：`knowledge/NN-topic/<concept>/`
- 概念之间按依赖顺序排列，先基础后进阶
- 章节编号固定，不可插入新编号（新内容追加到末尾）

## 链接规范

- 跨概念引用：`../NN-topic/<concept>/README.md`
- 跨章节引用：`../../NN-topic/<concept>/README.md`
- 引用资源：`./assets/filename` 或 `../assets/filename`
