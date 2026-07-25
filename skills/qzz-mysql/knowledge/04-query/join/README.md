# JOIN 联结

> JOIN 把两张（或更多）表的数据按某种关系连在一起查。

## 为什么需要它

一个订单属于某个用户——你不需要在订单表里存用户的所有信息，只需要存 user_id。查订单时用 JOIN 把用户信息带出来。

这就是关系型数据库的核心：数据拆成多张表，查询时 JOIN 把它们连起来。

## 三种 JOIN

假设两张表：

```sql
user:                      orders:
+----+------+              +----+---------+--------+
| id | name |              | id | user_id | amount |
+----+------+              +----+---------+--------+
| 1  | 张三 |              | 1  | 1       | 100    |
| 2  | 李四 |              | 2  | 1       | 200    |
+----+------+              | 3  | 3       | 300    |
                           +----+---------+--------+
```sql

### INNER JOIN — 两表都有的才返回

```sql
SELECT user.name, orders.amount
FROM user
INNER JOIN orders ON user.id = orders.user_id;
```sql

结果：

```sql
+------+--------+
| name | amount |
+------+--------+
| 张三 | 100    |
| 张三 | 200    |
+------+--------+
```sql

李四没有订单 → 不出现。order 里 user_id=3 没有对应用户 → 也不出现。**只返回匹配上的行。**

### LEFT JOIN — 左表全保留

```sql
SELECT user.name, orders.amount
FROM user
LEFT JOIN orders ON user.id = orders.user_id;
```sql

结果：

```sql
+------+--------+
| name | amount |
+------+--------+
| 张三 | 100    |
| 张三 | 200    |
| 李四 | NULL   |
+------+--------+
```sql

李四没有订单 → 保留，但 amount 填 NULL。**左表所有行都在，右表没有匹配的填 NULL。**

### RIGHT JOIN — 右表全保留

和 LEFT JOIN 方向相反。实际项目中几乎都用 LEFT JOIN——把主表放左边，可读性更好。

## 一张图记住 JOIN

```sql
INNER JOIN:     A ∩ B
LEFT JOIN:      A（B 没有的填 NULL）
RIGHT JOIN:     B（A 没有的填 NULL）
```sql

## ON vs WHERE

```sql
-- ON：定义"怎么连"
SELECT * FROM user LEFT JOIN orders ON user.id = orders.user_id

-- WHERE：在连接结果上再过滤
SELECT * FROM user LEFT JOIN orders ON user.id = orders.user_id
WHERE orders.amount > 100;
```sql

区别在 LEFT JOIN 上最明显：ON 条件影响"匹配什么"，不匹配的行保留填 NULL；WHERE 条件在连接完成后过滤——可能把 NULL 行也滤掉。

## 注意事项

- **被驱动表的 JOIN 字段必须建索引。** 否则每次关联都是全表扫，慢到怀疑人生。
- **LEFT JOIN 的 WHERE 条件别写在 ON 里。** ON 只管连接逻辑，WHERE 只管过滤逻辑。混在一起很难 debug。
- **JOIN 不要超过 3-5 张表。** 再多说明表设计可能有问题，或者该拆步骤了。

## 和什么有关

- [子查询](../subquery/) — 很多子查询可以改写为 JOIN
- [06-index/when-to-use/](../../06-index/when-to-use/) — JOIN 的字段建索引是刚需
- [11-design/normalization/](../../11-design/normalization/) — 为什么数据要拆成多张表
