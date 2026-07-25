# 代码示例

## 示例 1：五个聚合函数

```sql
SELECT
  COUNT(*)    AS total,
  SUM(amount) AS total_amount,
  AVG(amount) AS avg_amount,
  MAX(amount) AS max_amount,
  MIN(amount) AS min_amount
FROM orders;
```

## 示例 2：配合 GROUP BY

```sql
SELECT city, COUNT(*) AS cnt, AVG(age) AS avg_age
FROM user GROUP BY city;
```

## 示例 3：COUNT(*) vs COUNT(col)

```sql
SELECT COUNT(*) FROM user;        -- 100 行（所有）
SELECT COUNT(phone) FROM user;    -- 95 行（有 5 行 phone 为 NULL）
```
