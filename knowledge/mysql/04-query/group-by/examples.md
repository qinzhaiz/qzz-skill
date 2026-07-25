# 代码示例

## 示例 1：简单分组

```sql
-- 每个城市有多少用户
SELECT city, COUNT(*) AS cnt FROM user GROUP BY city;
```

## 示例 2：多列分组

```sql
-- 每个城市 + 性别组合的用户数
SELECT city, sex, COUNT(*) FROM user GROUP BY city, sex;
```

## 示例 3：HAVING 过滤分组

```sql
-- 用户数超过 5 的城市
SELECT city, COUNT(*) AS cnt FROM user GROUP BY city HAVING cnt > 5;
```

## 示例 4：WHERE + GROUP BY + HAVING 完整链路

```sql
SELECT city, COUNT(*) AS cnt, AVG(age) AS avg_age
FROM user
WHERE status = 1        -- 1. 先过滤行
GROUP BY city           -- 2. 分组
HAVING cnt > 3          -- 3. 过滤组
ORDER BY avg_age DESC   -- 4. 排序
LIMIT 10;               -- 5. 限制行数
```
