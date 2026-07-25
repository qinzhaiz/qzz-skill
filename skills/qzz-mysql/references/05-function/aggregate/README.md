# 聚合函数

> 聚合函数对一组行做计算，返回一个值。COUNT 数行、SUM 求和、AVG 求平均。

## 五个核心函数

```sql
SELECT COUNT(*) FROM orders;              -- 总订单数
SELECT SUM(amount) FROM orders;           -- 总金额
SELECT AVG(amount) FROM orders;           -- 平均金额
SELECT MAX(amount), MIN(amount) FROM orders; -- 最高和最低金额
```

## COUNT 的细节

```sql
COUNT(*)       -- 所有行（含 NULL 行）
COUNT(col)     -- col 非 NULL 的行数
COUNT(DISTINCT col)  -- col 非 NULL 且去重
```

| 写法 | 用途 |
|------|------|
| `COUNT(*)` | 统计表里有多少行 |
| `COUNT(col)` | 统计某列有多少非空值 |
| `COUNT(1)` | 和 `COUNT(*)` 一样，没有更快 |
| `COUNT(DISTINCT city)` | 有多少个不同的城市 |

**InnoDB 没有缓存总行数**——每次 `COUNT(*)` 都要扫描。这是 MVCC 的代价：不同事务看到的数据不一样，维护一个"正确的计数"成本太高。

## 配合 GROUP BY

```sql
SELECT city, COUNT(*), AVG(age)
FROM user
GROUP BY city;
```

每个城市一行，带上该城市用户数和平均年龄。

## NULL 和聚合

所有聚合函数**忽略 NULL 值**：

```sql
SELECT AVG(age) FROM user;  -- 只算 age 非 NULL 的行
```

如果所有行都是 NULL，除 COUNT 外都返回 NULL。COUNT 返回 0。

## 注意事项

- **聚合不能用在 WHERE 里。** `WHERE COUNT(*) > 5` 不行——WHERE 在分组之前执行。用 HAVING。
- **COUNT(*) 在大表上慢。** InnoDB 没有行数缓存。如果需要频繁精确计数，用计数器表 + 业务层维护。
- **SUM/AVG 在空结果上返回 NULL。** 程序里要处理 `NULL`，或者用 `IFNULL(SUM(amount), 0)`。

## 和什么有关

- [04-query/group-by/](../../04-query/group-by/) — 聚合函数和 GROUP BY 配合，含 HAVING 用法
