# 修改表

> 表建完了想改？ALTER TABLE 就是干这个的。

## 为什么需要它

没有人能一次就把表设计对。上线后发现少了个列、类型选小了、默认值设错了——ALTER TABLE 让你改已经存在的表结构。

CREATE 是"从零建"，ALTER 是"对已有的修修补补"。

## 常用操作

### 加列

```sql
ALTER TABLE user ADD COLUMN email VARCHAR(100) NOT NULL DEFAULT '' COMMENT '邮箱' AFTER name;
```sql

`AFTER name` 把新列插在 name 之后。不加的话默认放在最后。

### 删列

```sql
ALTER TABLE user DROP COLUMN temp_field;
```sql

**数据一起丢了。** 删之前确认这列真的没人用了。

### 改列的类型

```sql
ALTER TABLE user MODIFY COLUMN name VARCHAR(64) NOT NULL DEFAULT '';
```sql

只能把列往宽了改（VARCHAR(32) → VARCHAR(64) OK），不能往窄了改——已有数据可能放不下。

### 改列名 + 类型

```sql
ALTER TABLE user CHANGE COLUMN name username VARCHAR(64) NOT NULL DEFAULT '';
```sql

`CHANGE` 同时改名字和类型。`MODIFY` 只改类型不改名。

### 加索引 / 删索引

```sql
ALTER TABLE user ADD INDEX idx_city (city);
ALTER TABLE user DROP INDEX idx_city;
```sql

### 改表名

```sql
RENAME TABLE user TO users;
```sql

## 一次改多个

```sql
ALTER TABLE user
  ADD COLUMN email VARCHAR(100) NOT NULL DEFAULT '' AFTER name,
  MODIFY COLUMN city VARCHAR(50) NOT NULL DEFAULT '',
  ADD INDEX idx_city (city);
```sql

一次 ALTER 做完所有变更——比分三次跑快，因为只需要一次表结构重建。

## 危险警告

**ALTER TABLE 在大表上可能锁表很久。**

- 几万行的表：秒级，随便改
- 几十万行的表：可能几秒到几十秒，需要评估
- 几百万行以上的表：**线上别直接跑**——用 pt-online-schema-change 或 gh-ost 这类在线改表工具

学习阶段怎么改都行。但记住：生产环境改表 = 高风险操作。

## 注意事项

- **先 `DESC 表名` 看现状，再 ALTER。** 知己知彼。
- **改之前备份。** 至少 `SHOW CREATE TABLE` 存一下建表语句，万一改坏了还能回。
- **MODIFY vs CHANGE 的区别：** MODIFY 只改列定义，CHANGE 可以顺便改列名。如果不需要改列名，用 MODIFY 更简洁。

## 和什么有关

- [创建表](../create-table/) — 建表和改表是一对
- [06-index/](../../06-index/) — 索引的创建和删除
