# MyISAM 与 InnoDB

> MySQL 有多个存储引擎，但今天（MySQL 8.0）你只需要知道：用 InnoDB，别用 MyISAM。

## 为什么需要它

MySQL 最独特的设计就是**可插拔存储引擎**——同一套 SQL 接口，底层可以用不同的引擎存储数据。早期 MySQL 默认引擎是 MyISAM，MySQL 5.5.5 起改为 InnoDB。理解两者的区别，才能理解为什么今天几乎所有场景都应该用 InnoDB。

## 它是什么

| 特性 | InnoDB | MyISAM |
|------|--------|--------|
| **事务** | ✅ ACID 事务 | ❌ 不支持 |
| **行锁** | ✅ 行级锁 | ❌ 只有表锁 |
| **外键** | ✅ 支持 | ❌ 不支持 |
| **崩溃恢复** | ✅ redo log 自动恢复 | ❌ 崩溃可能丢数据，需手动修复 |
| **MVCC** | ✅ 支持 | ❌ 不支持 |
| **全文索引** | ✅ 5.6+ 支持 | ✅ 支持（较早） |
| **GIS 空间索引** | ✅ 5.7+ 支持 | ✅ 支持 |
| **数据存储** | 表空间（.ibd） | 三个文件：.frm .MYD .MYI |
| **COUNT(*)** | 每次扫描（MVCC 原因） | O(1)（维护了行数变量） |
| **压缩** | ✅ 支持 | ✅ 支持（压缩后只读） |
| **适用场景** | 99% 场景 | 已废弃，仅遗留系统使用 |

## 怎么工作

### MyISAM 的文件结构

```sql
mydb/user.frm   → 表结构定义
mydb/user.MYD   → 数据文件（MYData）
mydb/user.MYI   → 索引文件（MYIndex）
```sql

数据和索引分开存储。索引的叶子节点存的是数据文件的磁盘地址（行指针），不是主键值——这和 InnoDB 完全不同。

### InnoDB 的表空间

```sql
mydb/user.ibd   → 表空间文件（数据 + 索引都在里面）
```sql

数据和索引都存 B+Tree，聚簇索引的叶子节点存完整行数据，二级索引的叶子节点存主键值。

### 为什么 MyISAM 的 COUNT(*) 是 O(1)

MyISAM 在表元数据中维护了一个精确的行数——因为 MyISAM 没有 MVCC，所有连接看到的数据是一样的，维护总数简单。InnoDB 的 MVCC 导致不同事务可能看到不同行数，维护"正确"的行数成本太高，所以每次 COUNT(*) 都要扫描。

## 怎么用

```sql
-- 查看所有引擎
SHOW ENGINES;

-- 查看某张表用的哪个引擎
SELECT TABLE_NAME, ENGINE
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'your_database';

-- 创建表时指定引擎（默认就是 InnoDB）
CREATE TABLE test_myisam (
    id INT,
    name VARCHAR(50)
) ENGINE=MyISAM;  -- 不推荐！仅用于演示

CREATE TABLE test_innodb (
    id INT,
    name VARCHAR(50)
) ENGINE=InnoDB;  -- 默认，推荐

-- 修改已有表的引擎
ALTER TABLE test_myisam ENGINE = InnoDB;
```bash

## 注意事项

1. **MySQL 8.0 中 MyISAM 已被标记为过时**——system tables 也改为 InnoDB 了。新项目不要用 MyISAM。
2. **MyISAM 的表锁是并发瓶颈**——一个写操作锁住整张表，所有其他读写都排队。InnoDB 的行锁允许多个写操作并行（只要不是同一行）。
3. **MyISAM 崩溃后需要手动修复**——`REPAIR TABLE` 可能需要几小时的修复时间和数据丢失风险。InnoDB 自动从 redo log 恢复，通常几秒到几分钟。
4. **例外情况**：极少数 MyISAM 仍有优势——比如极低频更新的"字典表"（但 InnoDB 也能胜任），或者历史遗留系统无法迁移。

## 和什么有关

- [InnoDB 架构](../innodb-architecture/) —— InnoDB 的内部结构
- [事务基础](../../07-transaction/what-is-transaction/) —— MyISAM 不支持事务的影响
- [行级锁](../../08-lock/row-lock/) —— MyISAM 只有表锁的后果
- [索引基础](../../06-index/what-is-index/) —— 两种引擎的索引差异
