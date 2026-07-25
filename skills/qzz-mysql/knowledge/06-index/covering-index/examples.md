# 代码示例

## 示例 1：判断是否覆盖

```sql
CREATE INDEX idx_name_city ON user(name, city);

-- 覆盖索引——查询列全在索引里
EXPLAIN SELECT name, city FROM user WHERE name = '张三';
-- Extra: Using index ✅

-- 非覆盖——SELECT * 需要回表
EXPLAIN SELECT * FROM user WHERE name = '张三';
-- Extra: 无 Using index ❌
```sql

## 示例 2：实战覆盖索引设计

```sql
-- 高频查询：SELECT name, age FROM user WHERE city = '北京' ORDER BY created_at

-- 最优索引：
CREATE INDEX idx_city_created_name_age ON user(city, created_at, name, age);
-- city: 等值过滤
-- created_at: 排序（避免 filesort）
-- name, age: 覆盖列（不用回表）
```
