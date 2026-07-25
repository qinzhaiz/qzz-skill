# 子查询

> 子查询是 SELECT 里面套 SELECT。把内层查询的结果交给外层查询使用。

## 三种子查询

### 标量子查询——返回一个值

```sql
SELECT name, age
FROM user
WHERE age > (SELECT AVG(age) FROM user);
```sql

内层算出平均年龄（一个数字），外层用这个数字做过滤条件。

### IN 子查询——返回一组值

```sql
SELECT * FROM user
WHERE city IN (SELECT city FROM city_list WHERE province = '广东');
```sql

查出所有广东的城市名，然后查在这些城市里的用户。等价于：先用一个查询拿到城市列表，再把这个列表塞进第二个查询的 IN 里。

### EXISTS 子查询——判断有没有

```sql
SELECT * FROM user
WHERE EXISTS (
    SELECT 1 FROM orders WHERE orders.user_id = user.id
);
```sql

查出所有有订单的用户。`EXISTS` 不关心子查询返回什么值——只关心有没有行。有 = TRUE，没有 = FALSE。

## IN vs EXISTS

| | IN | EXISTS |
|---|---|---|
| 适合场景 | 内层结果集小 | 外层表小、内层表大 |
| 怎么工作 | 先跑内层，拿结果跑外层 | 外层每行跑一次内层（但内层有索引就快） |
| NULL 问题 | 有坑——NOT IN + NULL = 全空 | 无 |

### NOT IN 的坑

```sql
-- 如果子查询结果里包含 NULL……
SELECT * FROM user WHERE id NOT IN (1, 2, NULL);
-- 永远返回空！因为 id != NULL 结果是 UNKNOWN，不是 TRUE。
```sql

不确定子查询有没有 NULL 时，用 `NOT EXISTS` 替代 `NOT IN`。

## 注意事项

- **子查询可读性比 JOIN 好，但性能不一定。** 简单的 IN 子查询 MySQL 8.0 优化得很好，复杂的可能需要改写为 JOIN。
- **标量子查询只能返回一行一列。** 多行多列用 IN、EXISTS 或 JOIN。

## 和什么有关

- [JOIN](../join/) — 很多子查询可以改写为 JOIN，反过来也行
- [05-function/aggregate/](../../05-function/aggregate/) — 子查询配合聚合函数
