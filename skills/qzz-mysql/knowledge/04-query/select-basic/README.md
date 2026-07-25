# SELECT 基础

> SELECT 是你写得最多的 SQL。它从表里取数据，不修改任何东西。

## 为什么需要它

数据存进去了，你得能查出来。SELECT 就是查数据的命令——你能限制查哪些列、哪些行、怎么排。

## 怎么用

### 查所有列

```sql
SELECT * FROM user;
```sql

`*` = 所有列。开发调试快速扫一眼数据时有用。但写进代码里不要用 `*`——表结构变了会多出你不需要的列，浪费网络和内存。

### 查指定的列

```sql
SELECT name, city FROM user;
```sql

只取 name 和 city 两列。明确指定列名——这正是代码里该用的写法。

### 去重

```sql
SELECT DISTINCT city FROM user;
```sql

只返回不重复的城市名。如果 user 表里有 100 行但只有 5 个城市，`SELECT DISTINCT city` 只返回 5 行。

### 别名

```sql
SELECT name AS 姓名, city AS 城市 FROM user;
```sql

`AS` 给列起别名——输出时列名变成中文，给人看更友好。`AS` 还可以省略：`SELECT name 姓名 FROM user;` 等效。

### 限制行数

```sql
SELECT * FROM user LIMIT 5;
```sql

只返回前 5 行。数据量大时避免查出几十万行撑爆内存。配合 OFFSET 可以做分页——那一节专门讲。

## SQL 执行顺序

你看到的是 `SELECT ... FROM ... WHERE ... ORDER BY ... LIMIT ...`，但 MySQL 执行的时候不是按这个顺序：

```sql
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```sql

**实际顺序 vs 书写顺序不同**——这是新手最容易踩的坑。比如 WHERE 里不能用 SELECT 里定义的别名，因为 WHERE 先执行。

## 注意事项

- **代码里别用 `SELECT *`。** 明确列出你需要的列。多一行文档效果，少一堆 bug。
- **LIMIT 不是免费的。** `LIMIT 100000, 20` 仍然会扫描前面 100000 行再丢掉。大偏移量分页后面有一节专门讲怎么优化。

## 和什么有关

- [WHERE 条件](../where/) — SELECT 加过滤条件
- [排序和分页](../order-limit/) — ORDER BY + LIMIT 详解
- [分组统计](../group-by/) — COUNT、SUM、GROUP BY
