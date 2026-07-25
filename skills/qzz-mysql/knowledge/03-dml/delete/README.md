# 删除数据

> DELETE 删行。这是最危险的一条 SQL——删错了没法回退。

## 为什么需要它

用户注销账号、商品下架、订单取消——都需要删数据。但删的数据比改的数据更不可逆，所以 DELETE 是三个 DML 操作里最需要谨慎的。

## 怎么用

### 删指定行

```sql
DELETE FROM user WHERE id = 1;
```sql

只删 id=1 这一行。**必须有 WHERE。**

### 删一批行

```sql
DELETE FROM user WHERE city = '北京' AND status = 0;
```sql

删除所有符合 WHERE 条件的行。

### 删所有行——两个方法

```sql
-- 方法 1：逐行删除，触发 ON DELETE 行为
DELETE FROM user;

-- 方法 2：直接清空，重建表结构（更快，不触发行级触发器）
TRUNCATE TABLE user;
```sql

| | DELETE | TRUNCATE |
|---|---|---|
| 逐行删除 | ✅ | ❌ |
| 触发 ON DELETE | ✅ | ❌ |
| 重置 AUTO_INCREMENT | ❌ | ✅ |
| 速度 | 慢（大表） | 快 |
| 能回滚吗 | ✅（事务中） | ❌（隐式提交） |

清测试数据用 TRUNCATE——快。清部分数据用 DELETE + WHERE。

## 危险警告

```sql
DELETE FROM user;  -- 没有 WHERE！
```sql

**整张 user 表变空。** 生产环境跑这一行 = 严重事故。

写 DELETE 之前，先 SELECT：

```sql
-- 1. 确认要删哪些
SELECT * FROM user WHERE id = 1;

-- 2. 确认无误后换成 DELETE
DELETE FROM user WHERE id = 1;
```sql

## 注意事项

- **DELETE 必须带 WHERE。** 不带的只有一种情形——你确定要清整张表，且用 TRUNCATE 更快。
- **DELETE + WHERE = 也要小心。** WHERE 条件写错了（`id > 0` 等于所有行）和没写一样危险。
- **用 LIMIT 控制最大删除行数。** `DELETE FROM user WHERE city = '北京' LIMIT 100;`——分批执行，避免大数据量删除锁表太久。

## 和什么有关

- [插入数据](../insert/) — 插进去，也可能要删
- [更新数据](../update/) — UPDATE 和 DELETE 是最危险的两条 SQL
- [04-query/where/](../../04-query/where/) — WHERE 的正确写法
