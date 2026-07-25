# 常见错误

## 错误 1：新项目还在用 MyISAM

**症状**：新人建表时复制了网上的 SQL 代码，里面写着 `ENGINE=MyISAM`。上线后才发现没有事务、崩溃丢数据。

**原因**：很多老教程和博客（2010 年前）还在用 MyISAM。当时 InnoDB 还不成熟，MyISAM 是默认引擎。但现在（MySQL 8.0）InnoDB 是唯一推荐的引擎。

**怎么修**：设置默认引擎为 InnoDB：`SET GLOBAL default_storage_engine = InnoDB;`。建表时不写 ENGINE 子句，自动用默认的 InnoDB。Code Review 时检查建表语句。

## 错误 2：以为 InnoDB 的 COUNT(*) 和 MyISAM 一样快

**症状**：应用里到处用 `SELECT COUNT(*) FROM 大表`，切换到 InnoDB 后这些查询突然很慢。

**原因**：MyISAM 存了精确行数，COUNT(*) 是 O(1)。InnoDB 每次都要扫描（通常走最小的二级索引），大表可能要几秒。

**怎么修**：(1) 如果不需要精确值，用 `SHOW TABLE STATUS` 或 `EXPLAIN SELECT COUNT(*)` 的 rows 估算值，(2) 用 Redis 计数器或独立计数表维护精确值，(3) 如果必须精确计数，走最小索引而非主键（`SELECT COUNT(*) FROM large_table` 会自动选最小的索引）。
