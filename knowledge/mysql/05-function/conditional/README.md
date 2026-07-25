# 条件函数

> 在 SQL 里做 if-else 判断——CASE WHEN、IF、IFNULL、COALESCE。

## CASE WHEN — SQL 里的 if-else

```sql
SELECT name, age,
  CASE
    WHEN age < 18 THEN '未成年'
    WHEN age < 30 THEN '青年'
    WHEN age < 60 THEN '中年'
    ELSE '老年'
  END AS age_group
FROM user;
```

每一行按年龄判断属于哪个年龄段。**CASE 按顺序判断——命中第一个 WHEN 后就跳过后面。**

### 简写形式

```sql
SELECT name,
  CASE city
    WHEN '北京' THEN '一线'
    WHEN '上海' THEN '一线'
    WHEN '深圳' THEN '一线'
    ELSE '其他'
  END AS city_level
FROM user;
```

等值比较的简写——`CASE col WHEN val1 THEN ... WHEN val2 THEN ...`。

## IF 函数 — 简单的三目运算

```sql
IF(条件, 真值, 假值)

-- 示例
SELECT name, IF(age >= 18, '成年', '未成年') FROM user;
```

## IFNULL — NULL 时的兜底值

```sql
SELECT name, IFNULL(phone, '未填写') AS phone FROM user;
```

phone 为 NULL 时显示"未填写"。**经常用在 LEFT JOIN 结果上——右表没有匹配的行填 NULL，用 IFNULL 兜底。**

## COALESCE — 取第一个非 NULL 值

```sql
SELECT name, COALESCE(phone, email, '无联系方式') AS contact FROM user;
```

先取 phone，phone 为 NULL 取 email，email 也为 NULL 就显示"无联系方式"。

## NULLIF — 两个值相等时返回 NULL

```sql
NULLIF(expr1, expr2)   -- 如果 expr1 = expr2，返回 NULL；否则返回 expr1

-- 实战：避免除零错误
SELECT amount / NULLIF(count, 0) FROM orders;
```

## 实战：行转列（CASE WHEN + GROUP BY）

```sql
SELECT
  DATE_FORMAT(created_at, '%Y-%m') AS month,
  SUM(CASE WHEN status = 1 THEN 1 ELSE 0 END) AS active,
  SUM(CASE WHEN status = 0 THEN 1 ELSE 0 END) AS inactive
FROM user
GROUP BY month;
```

每个月一行，两列分别统计激活和未激活用户数。比子查询简洁很多。

## 注意事项

- **CASE WHEN 按顺序判断。** 条件重叠时，先命中的生效。
- **IFNULL 只替换 NULL，不替换空串。** `IFNULL(col, '兜底')` 对 `''`（空字符串）不生效。
- **COALESCE 可以传多个参数——不像 IFNULL 只有两个。**

## 和什么有关

- [04-query/group-by/](../../04-query/group-by/) — CASE WHEN + GROUP BY 做行转列
- [04-query/join/](../../04-query/join/) — IFNULL 配合 LEFT JOIN 兜底 NULL
