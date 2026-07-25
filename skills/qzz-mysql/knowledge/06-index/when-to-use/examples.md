# 代码示例

## 示例 1：判断哪个索引该建

```sql
-- 先看慢查询
-- 确认查询的 WHERE 条件、JOIN 列、ORDER BY 列

EXPLAIN SELECT * FROM orders WHERE user_id = 5 ORDER BY created_at;
-- key: NULL, rows: 500000 → 该建索引了

CREATE INDEX idx_user_created ON orders(user_id, created_at);

EXPLAIN SELECT * FROM orders WHERE user_id = 5 ORDER BY created_at;
-- key: idx_user_created, rows: 12 ✅
```sql

## 示例 2：查未使用索引

```sql
SELECT * FROM sys.schema_unused_indexes;
-- 列出从未被用过的索引 → 候选删除
```sql

## 示例 3：查冗余索引

```sql
SELECT * FROM sys.schema_redundant_indexes;
-- idx_a 被 idx_a_b 覆盖 → idx_a 可以删了
```
