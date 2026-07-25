# 练习

## 基础练习

1. 设计一个"无限层级评论"的数据库表（评论可以有回复，回复也可以有回复）。写出建表语句和查询某个评论所有子评论的 SQL。

2. 为 `user` 表实现软删除。要求：不能影响 username 的唯一约束。写出方案。

## 进阶练习

1. 设计一个审计日志系统：记录 user 表和 orders 表的所有变更。鼓励使用触发器实现自动记录。

2. 比较传统 EAV（product_attr 表）和 MySQL 8.0 JSON 列的优劣。给出各自的适用场景。

## 答案

1. 邻接表：`comment(id, content, parent_id)` + CTE 递归查询子评论。`WITH RECURSIVE ... SELECT ... UNION ALL ...`。

2. MySQL 不支持部分索引。方案：(a) 用 `UNIQUE KEY (username, is_deleted)` 但要注意已删除用户不能和活跃用户同名（已删除用户和活跃用户其实不冲突），(b) 删除时把 username 重命名为 `{id}_{原始username}`，释放唯一占位，(c) 用应用层检查唯一性。

3. 触发器中 INSERT INTO audit_log 记录 OLD 和 NEW 值。注意 JSON_OBJECT 用法。或者用 binlog 作为天然审计日志（但需要额外工具解析）。

4. JSON 列优于 EAV：(a) 一条 JSON 对应一个商品的所有属性，不需要多次 JOIN，(b) 可以用虚拟列 + 索引做查询优化，(c) JSON 有类型检查（JSON_VALID）。EAV 的唯一优势是跨表跨类型的数据分析（但这种情况应该考虑用列存储或 ES）。总体：优先 JSON，除非有非常特殊的需求。
