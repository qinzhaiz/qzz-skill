# 插入数据

> INSERT 往表里加新数据。建好的表是空壳，不加数据等于没用。

## 为什么需要它

你建了表，定义了列，设了约束——但表里一行数据都没有。INSERT 就是第一次真正"用"这张表——往里放数据。

## 怎么用

### 基本写法（推荐）

```sql
INSERT INTO user (name, city, age) VALUES ('张三', '北京', 22);
```sql

列出了列名，VALUES 按同样顺序给出值。**推荐这种写法**——表结构以后可能会变（加列、改列序），但明确列出列名的 INSERT 不会受影响。

### 不列列名（不推荐）

```sql
INSERT INTO user VALUES (NULL, '张三', '北京', 22, '13800001111', NOW());
```sql

必须按表定义列序给所有列填值——少了报错，顺序错了插错列。一个 ALTER TABLE 可能就让这条 SQL 报废。

### 一次插入多行

```sql
INSERT INTO user (name, city, age) VALUES
  ('张三', '北京', 22),
  ('李四', '上海', 25),
  ('王五', '深圳', 21);
```sql

一行一条 SQL 跑三次，不如一次跑三条——每条 SQL 都要走一次网络往返。

### 从别的表导数据

```sql
INSERT INTO user_archive (id, name, city, age)
SELECT id, name, city, age FROM user WHERE created_at < '2024-01-01';
```sql

INSERT 和 SELECT 组合——把查询结果直接插入目标表。数据迁移和归档常用。

### 插入或更新（存在就更新，不存在就插入）

```sql
INSERT INTO user (id, name, city) VALUES (1, '张三', '广州')
ON DUPLICATE KEY UPDATE city = '广州';
```sql

如果 id=1 的行已经存在，就更新 city；不存在就插入。`ON DUPLICATE KEY` 可以用来自增计数器、幂等写入。

## 注意事项

- **自增列不用填。** `AUTO_INCREMENT` 列 MySQL 自动处理——不给值即可，或者给 NULL。
- **列名和值一一对应。** 列了几列，VALUES 就得给几个值，类型还得对得上。
- **字符串和日期用单引号。** `'张三'`、`'2025-01-01'`。
- **省略列的条件：** 该列允许 NULL，或有 DEFAULT 值，或是自增列。否则报错。

## 和什么有关

- [更新数据](../update/) — 插完的数据，怎么改
- [删除数据](../delete/) — 插错了，怎么删
- [02-ddl/create-table/](../../02-ddl/create-table/) — 表必须先建好
