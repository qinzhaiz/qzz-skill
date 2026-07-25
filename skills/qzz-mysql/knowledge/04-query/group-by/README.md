# 分组统计

> GROUP BY 把行按某列的值分成组，然后对每组做统计。

## 聚合函数

| 函数 | 作用 |
|------|------|
| COUNT(*) | 行数 |
| COUNT(col) | 某列非 NULL 的行数 |
| SUM(col) | 求和 |
| AVG(col) | 平均值 |
| MAX(col) | 最大值 |
| MIN(col) | 最小值 |

```sql
SELECT COUNT(*) FROM user;               -- 一共多少用户
SELECT AVG(age) FROM user;               -- 平均年龄
SELECT MAX(age), MIN(age) FROM user;     -- 最大和最小年龄
```sql

## GROUP BY

```sql
SELECT city, COUNT(*) FROM user GROUP BY city;
```sql

每个城市一行，后面跟着该城市有多少用户。

```sql
SELECT city, COUNT(*) AS cnt
FROM user
GROUP BY city
ORDER BY cnt DESC;
```sql

按用户数从多到少排列。

## HAVING

```sql
SELECT city, COUNT(*) AS cnt
FROM user
GROUP BY city
HAVING cnt > 5;
```sql

HAVING 过滤分组后的结果——类似 WHERE 但作用在 GROUP BY 之后。**WHERE 过滤行，HAVING 过滤组。**

```sql
SELECT city, AVG(age) AS avg_age
FROM user
WHERE status = 1           -- 先过滤行（只要激活用户）
GROUP BY city              -- 再分组
HAVING avg_age > 25;       -- 再过滤组（只要平均年龄 >25 的城市）
```sql

## 执行顺序

```sql
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```sql

这个顺序解释了为什么：WHERE 不能用聚合函数（还没分组），HAVING 可以用（分完组了），ORDER BY 可以用 SELECT 别名（在 SELECT 之后）。

## 注意事项

- **SELECT 里的非聚合列必须在 GROUP BY 里。** `SELECT city, name, COUNT(*) FROM user GROUP BY city`——name 不在 GROUP BY 中，MySQL 可能挑一个随机的 name 返回（严格模式下直接报错）。
- **COUNT(*) vs COUNT(col)——前者包含 NULL 行，后者不。**
- **HAVING 不能替代 WHERE。** 先用 WHERE 做行过滤（能用索引），再用 HAVING 做组过滤。

## 和什么有关

- [WHERE 条件](../where/) — 先过滤再分组
- [05-function/aggregate/](../../05-function/aggregate/) — 更多聚合函数
