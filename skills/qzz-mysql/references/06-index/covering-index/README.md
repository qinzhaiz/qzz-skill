# 覆盖索引

> 覆盖索引让查询不回表——SQL 需要的所有数据都在索引里，直接用索引返回结果。

## 为什么需要它

上一节说了回表的代价——走二级索引找到主键后，要再去聚簇索引取整行数据，多一次磁盘 IO。

覆盖索引的解决方案：**把需要的列全放进索引里。**

```
普通查询：索引 → 回表 → 返回结果（2 次 IO）
覆盖索引：索引 → 返回结果（1 次 IO）
```

## 怎么实现

```sql
-- 查询只需要 name 和 city 两列
SELECT name, city FROM user WHERE name = '张三';

-- 联合索引包含查询需要的所有列 → 覆盖索引
CREATE INDEX idx_name_city ON user(name, city);
```

用 EXPLAIN 验证：

```sql
EXPLAIN SELECT name, city FROM user WHERE name = '张三';
-- Extra: Using index ← 这就是覆盖索引
```

`Using index` = 查询只读了索引，没回表。

## 实战

```sql
-- 查询：SELECT name, age FROM user WHERE city = '北京' ORDER BY age

-- 最优索引：
CREATE INDEX idx_city_age_name ON user(city, age, name);
-- city: 等值过滤（最左）
-- age: 排序（中间，避免 filesort）
-- name: 覆盖列（SELECT 需要，不用回表）
```

覆盖列放最后——不影响过滤和排序，只是顺便存着省一次回表。

## 覆盖索引 vs SELECT *

```sql
-- SELECT * 永远无法被覆盖——它要所有列，索引不可能存全表
SELECT * FROM user WHERE city = '北京';  -- 必须回表

-- 只查需要的列——可能被覆盖
SELECT name, age FROM user WHERE city = '北京';  -- 可能被 idx_city_age_name 覆盖
```

**这就是为什么代码里不要写 SELECT *——它让你永远无法享受覆盖索引的好处。**

## 注意事项

- **覆盖索引意味着索引变大。** 多存了几个列 = 写入时多维护这些列。权衡：读性能 vs 写性能和空间。
- **VARCHAR 列太长不建议放进覆盖索引。** `VARCHAR(500)` 会让索引页存不了几个 key → 索引变深 → 查询变慢。
- **覆盖索引 ≠ 索引本身没有开销。** 仍然需要更新维护，只是帮你少了一次回表的 IO。

## 和什么有关

- [聚簇索引和二级索引](../clustered-secondary/) — 理解回表才能理解覆盖
- [联合索引和最左前缀](../composite-index/) — 覆盖索引通常就是联合索引
- [SELECT 基础](../../04-query/select-basic/) — 为什么代码里不用 SELECT *
