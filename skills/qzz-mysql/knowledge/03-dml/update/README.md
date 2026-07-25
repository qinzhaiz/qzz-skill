# 更新数据

> UPDATE 改已经存在的数据。**永远加 WHERE，除非你确定要改所有行。**

## 为什么需要它

插进去的数据不是一成不变的。用户改名、商品调价、订单状态变更——都得靠 UPDATE。

## 怎么用

### 改单列

```sql
UPDATE user SET city = '广州' WHERE id = 1;
```sql

把 id=1 的用户城市改成广州。`WHERE id = 1` 只改这一行——没有 WHERE 就改整张表。

### 改多列

```sql
UPDATE user SET city = '广州', age = 23 WHERE id = 1;
```sql

一次改多列，用逗号隔开。

### 批量更新

```sql
UPDATE user SET status = 1 WHERE city = '北京';
```sql

所有北京用户的 status 变成 1——可能影响一行，也可能几千行。取决于 WHERE 条件。

### 用表达式更新

```sql
UPDATE product SET price = price * 1.1 WHERE category_id = 3;
```sql

所有 3 号分类的商品涨价 10%。不需要先查出来、程序里算、再写回去——SQL 直接搞定。

## 危险警告

```sql
UPDATE user SET city = '深圳';  -- 没有 WHERE！
```sql

**整张 user 表所有行的 city 全变成深圳。** 无法撤销（除非在事务里）。

写 UPDATE 之前，先写 WHERE 条件，确认一遍再执行：

```sql
-- 1. 先 SELECT 确认要修改哪些行
SELECT id, name, city FROM user WHERE id = 1;

-- 2. 确认无误后改成 UPDATE
UPDATE user SET city = '广州' WHERE id = 1;
```sql

## 注意事项

- **UPDATE 必须带 WHERE。** 唯一例外是你真的要改所有行（比如全量重置某个字段）。
- **改之前先 SELECT。** 用同样的 WHERE 条件查一遍，确认影响的正是你想改的那几行。
- **UPDATE 可以用 LIMIT 控制范围。** `UPDATE user SET status = 0 WHERE city = '北京' LIMIT 100;`——一次只改 100 行，分批来。

## 和什么有关

- [插入数据](../insert/) — 先有数据，才能改
- [删除数据](../delete/) — UPDATE 和 DELETE 是最危险的两条 SQL
- [04-query/where/](../../04-query/where/) — WHERE 条件的完整用法
