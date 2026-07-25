# 创建表

> 表是数据库里真正存数据的地方。建表就是定义"每一行数据长什么样"。

## 为什么需要它

有了数据库，你还需要在里面建**表**。数据库是容器，表是容器里的抽屉——数据最终是存在表里的。

你可能觉得"我直接扔数据进去不行吗"。不行。MySQL 是强类型的——你必须先告诉它每列叫什么、存什么类型的数据，它才知道怎么存、怎么查。

## 它是什么

**表（Table）** 是二维的数据结构：行为单位（记录），列为字段（属性）。建表就是定义列——每列的名字、数据类型、约束。

一张典型的 `user` 表：

```sql
+----+--------+--------+-----+
| id | name   | city   | age |
+----+--------+--------+-----+
| 1  | 张三   | 北京   | 22  |
| 2  | 李四   | 上海   | 25  |
+----+--------+--------+-----+
```sql

建这张表的 SQL：

```sql
CREATE TABLE IF NOT EXISTS user (
    id   INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(32)  NOT NULL DEFAULT '' COMMENT '姓名',
    city VARCHAR(20)  NOT NULL DEFAULT '' COMMENT '城市',
    age  TINYINT UNSIGNED NOT NULL DEFAULT 0  COMMENT '年龄',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```sql

## 怎么用

### 基本结构

```sql
CREATE TABLE 表名 (
    列名 数据类型 约束,
    列名 数据类型 约束,
    ...
    PRIMARY KEY (某列)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```sql

### 每个部分的作用

| 部分 | 作用 |
|------|------|
| `IF NOT EXISTS` | 表已存在时不报错 |
| `列名 数据类型` | 每列必须指定类型（INT、VARCHAR……下一节讲） |
| `NOT NULL` | 这列不允许为空 |
| `DEFAULT` | 不指定值时的默认值 |
| `COMMENT` | 列的注释——给人看，不执行 |
| `PRIMARY KEY` | 主键——每行的唯一标识 |
| `AUTO_INCREMENT` | 自动递增——每次插入新行自增 1 |
| `ENGINE=InnoDB` | 存储引擎，99% 场景用 InnoDB |
| `DEFAULT CHARSET=utf8mb4` | 表的字符编码 |

### 查看表结构

```sql
DESC 表名;
```sql

输出每列的字段名、类型、是否可为空、默认值等信息。这是最常用的"这张表长什么样"命令。

### 删表

```sql
DROP TABLE IF EXISTS 表名;
```sql

不可逆。`IF EXISTS` 让不存在的表不报错。

## 注意事项

- **表名用小写。** 虽然 MySQL 支持大小写混合，但跨操作系统迁移时会踩坑——Linux 上大小写敏感，Windows 上不敏感。统一小写最省事。
- **必须设主键。** InnoDB 表必须有一个主键。你不指定的话 MySQL 会偷偷生成一个隐藏的——但对查询性能不利。主动设。
- **用 IF NOT EXISTS。** 建表脚本应该是可以反复跑的，不报错。养成习惯。

## 和什么有关

- [数据类型](../datatypes/) — 每列什么时候用什么类型
- [约束](../constraints/) — NOT NULL、DEFAULT、PRIMARY KEY 等详细用法
- [12-engine/innodb-architecture/](../../12-engine/innodb-architecture/) — InnoDB 是什么
