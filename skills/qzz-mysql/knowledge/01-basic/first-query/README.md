# 第一次查询

> 连上 MySQL 之后第一件该做的事：建一个自己的数据库，建一张表，写第一条 SELECT。

## 为什么需要它

前面装好了 MySQL，但打开之后只有系统自带的四个库——不是你该碰的东西。你需要一个**自己的地方**放自己的数据。

这一节你会在 MySQL 里圈一块地盘，建第一张表，跑第一条查询。后面的 SQL 练习都在这个环境里做。

## 怎么用

### 第一步：确认环境

连上 MySQL，跑三条命令确认一切正常：

```sql
SELECT VERSION();      -- 确认版本，应该看到 8.x
SHOW DATABASES;        -- 看看有哪些数据库
SELECT DATABASE();     -- 确认当前在哪个库（显示 NULL 说明还没选）
```bash

你会看到 `information_schema`、`mysql`、`performance_schema`、`sys` 这四个数据库——这些是 MySQL 自己的，**不要改也不要删**。

### 第二步：创建自己的数据库

```sql
CREATE DATABASE IF NOT EXISTS mysql_practice
  CHARACTER SET utf8mb4;

USE mysql_practice;

SELECT DATABASE();     -- 这次应该返回 mysql_practice
```sql

- `CREATE DATABASE`：建一个数据库
- `IF NOT EXISTS`：如果已经有了就不会重复创建，不会报错
- `CHARACTER SET utf8mb4`：用 UTF-8 编码，能存中文、emoji
- `USE`：告诉 MySQL "后面的操作都在这个库里"

### 第三步：建第一张表

```sql
CREATE TABLE IF NOT EXISTS user (
    id        INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name      VARCHAR(32)  NOT NULL DEFAULT '' COMMENT '姓名',
    city      VARCHAR(20)  NOT NULL DEFAULT '' COMMENT '城市',
    age       TINYINT UNSIGNED NOT NULL DEFAULT 0  COMMENT '年龄',
    mobile    VARCHAR(20)  NOT NULL DEFAULT '' COMMENT '手机号',
    created_at DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
```sql

现在还不需要理解每一行——[02-ddl](../../02-ddl/) 会逐个拆解。现在你只需要知道：你建了一张叫 `user` 的表，有 6 个列。

看看表结构：

```sql
DESC user;
```sql

输出会告诉你每个列叫什么、什么类型、能不能为空。

### 第四步：插入几条数据

```sql
INSERT INTO user (name, city, age, mobile) VALUES
  ('张三', '北京', 22, '13800001111'),
  ('李四', '上海', 25, '13900002222'),
  ('王五', '深圳', 21, '13700003333');
```sql

### 第五步：写第一条查询

```sql
SELECT * FROM user;
```sql

这就是你的第一条查询。`SELECT *` = 查所有列，`FROM user` = 从 user 表里查。

再试试加条件：

```sql
SELECT name, city FROM user WHERE age > 22;
```sql

这条的意思是：只查 name 和 city 两列，只返回 age 大于 22 的行。

## 注意事项

- **系统数据库不要碰。** `mysql`、`information_schema`、`performance_schema`、`sys` 是 MySQL 自己的。你的东西放在自己建的库里。
- **SQL 关键字不区分大小写。** `SELECT` 和 `select` 效果一样。但表名和列名在有些系统上区分大小写——统一用小写最省事。
- **字符串用单引号。** `'北京'` 可以，`"北京"` 在 MySQL 里也能用，但在其他数据库不一定。统一用单引号是好习惯。

## 和什么有关

- [02-ddl/create-database/](../../02-ddl/create-database/) — CREATE DATABASE 的详细用法
- [02-ddl/create-table/](../../02-ddl/create-table/) — CREATE TABLE 每个细节
- [03-dml/insert/](../../03-dml/insert/) — INSERT 的各种写法
- [04-query/select-basic/](../../04-query/select-basic/) — SELECT 的完整用法
