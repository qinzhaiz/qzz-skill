# 联合索引和最左前缀

> 联合索引是多列一起建的索引。能不能用上——看最左前缀。

## 什么是联合索引

```sql
CREATE INDEX idx_city_age ON user(city, age);
```

B+Tree 里的 key 是 `(city, age)` 的组合。叶子节点先按 city 排序，city 相同的按 age 排序。**不是按 city 排再按 age 排——是完全按照 (city, age) 这个组合来排序。**

## 最左前缀原则

联合索引 `idx(a, b, c)` 相当于创建了三个索引：`a`、`a,b`、`a,b,c`。但**不能跳过前面的列去用后面的。**

| 查询条件 | 用上索引？ | 原因 |
|---------|-----------|------|
| `WHERE a=1` | ✅ | 匹配最左列 |
| `WHERE a=1 AND b=2` | ✅ | 匹配前两列 |
| `WHERE a=1 AND b=2 AND c=3` | ✅ | 全匹配 |
| `WHERE b=2` | ❌ | 跳过 a——索引失效 |
| `WHERE a=1 AND c=3` | ⚠️ 只用 a | 中间断了 b，c 失效 |
| `WHERE a=1 AND b>2 AND c=3` | ⚠️ 只用 a,b | b 用了范围→c 失效 |

**记一句话：从最左开始，连续匹配，中间不能断。**

## 联合索引的列顺序

谁放前面？三个原则：

1. **等值条件放前面，范围条件放后面。** 因为范围条件之后列的用不上索引。
2. **区分度高的列放前面。** 如 `school, gender`——school 区分度高，放前面能更快过滤数据。
3. **经常单独查询的列放最左。** 最左列等于一个单列索引——它自己就能独立工作。

## 为什么有最左前缀原则

B+Tree 按 `(a, b, c)` 的顺序排序。叶子节点看起来像：

```
(1,1,1) → (1,1,2) → (1,2,1) → (2,1,1) → (2,1,2) → ...
```

你要找 `b=2`——在 B+Tree 里 `b` 是全局乱序的（没有 a 的约束就无法定位），只能全表扫描。

## 实际验证

```sql
CREATE INDEX idx_city_age ON user(city, age);

EXPLAIN SELECT * FROM user WHERE city = '北京';                    -- key: idx_city_age ✅
EXPLAIN SELECT * FROM user WHERE city = '北京' AND age > 20;       -- key: idx_city_age ✅
EXPLAIN SELECT * FROM user WHERE age > 20;                         -- key: NULL ❌
EXPLAIN SELECT * FROM user WHERE city = '北京' AND age = 22;       -- key: idx_city_age ✅
```

## 注意事项

- **联合索引的列不是越多越好。** 超过 3-4 列的联合索引——列了，除非覆盖索引需求。
- **排序方向要一致。** `ORDER BY a ASC, b DESC` 需要索引也定义成降序（MySQL 8.0 支持降序索引）。

## 和什么有关

- [覆盖索引](../covering-index/) — 联合索引是覆盖索引最常用的实现方式
- [什么时候该建索引](../when-to-use/) — 建联合索引的决策
