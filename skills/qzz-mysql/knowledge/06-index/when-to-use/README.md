# 什么时候该建索引

> 索引不是越多越好。建错了浪费空间拖慢写入，建对了查询起飞。

## 该建的

| 场景 | 原因 |
|------|------|
| WHERE 条件列 | 高频查询条件——没有索引就是全表扫 |
| JOIN 的关联列 | 被驱动表的关联列不建索引 = 每次都全表扫被驱动表 |
| ORDER BY 列 | 避免 filesort——直接按索引顺序返回 |
| 高频组合条件 | 建联合索引，最左列放最常查的 |

```sql
-- 经常按 city 过滤，按 age 排序 → 建联合索引
CREATE INDEX idx_city_age ON user(city, age);
```sql

## 不该建的

| 场景 | 原因 |
|------|------|
| 区分度低的列 | 性别、布尔值——只能筛掉一半，不如全表扫 |
| 很少查的列 | 建了没人用——白白拖慢写入 |
| 频繁更新的列 | 每次 UPDATE 都要维护索引——代价 > 收益 |
| 小表 | 几千行——全表扫可能比走索引还快 |

```sql
-- 不要这样：性别列区分度极低
CREATE INDEX idx_gender ON user(gender);  -- 不加这个索引
```sql

## 怎么判断该不该建

```sql
-- 1. 先看查询有没有用上索引
EXPLAIN SELECT * FROM user WHERE city = '北京';
-- key: NULL → 需要建索引
-- key: idx_city → 已经在用

-- 2. 看索引使用情况（MySQL 系统表）
SELECT * FROM sys.schema_unused_indexes;
-- 列出从未用过的索引 → 可以删了

-- 3. 看冗余索引
SELECT * FROM sys.schema_redundant_indexes;
-- 列出功能被其他索引覆盖的索引
```sql

## 黄金法则

1. **WHERE + JOIN + ORDER BY 的列优先建索引。**
2. **联合索引的列顺序 = 等值条件前，范围条件后。**
3. **建完后用 EXPLAIN 验证索引用上了。**
4. **定期清理没用的索引——sys.schema_unused_indexes。**

## 注意事项

- **不是查得慢就加索引——先看 EXPLAIN。** 慢的原因可能是数据量真的大、SQL 写法有问题、锁等待——盲目加索引治标不治本。
- **LIKE '%xxx' 用不到索引。** 前导通配符 = 全表扫。用全文索引（FULLTEXT）替代。
- **在列上做函数运算 = 索引失效。** `WHERE YEAR(created_at) = 2025`——函数让索引不能用。

## 和什么有关

- [EXPLAIN](../../10-performance/explain/) — 看索引用没用上
- [联合索引和最左前缀](../composite-index/) — 建了索引但没用到的情况
