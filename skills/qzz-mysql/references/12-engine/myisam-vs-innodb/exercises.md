# 练习

## 基础练习

1. 在你的 MySQL 上创建一个 MyISAM 表和一个 InnoDB 表，分别模拟并发写入，观察锁的差异。

2. 用 `SHOW TABLE STATUS` 查看 MyISAM 和 InnoDB 表的信息差异。

## 进阶练习

1. 如果你们公司有一个遗留系统还在用 MyISAM，请列出迁移到 InnoDB 需要关注的风险点和迁移步骤。

2. MySQL 8.0 中还有哪些场景（如果有）MyISAM 比 InnoDB 更适合？请论证。

## 答案

1. 在 MyISAM 表上两个终端同时 UPDATE 不同行 → 一个阻塞。InnoDB 上同样操作 → 不阻塞。这是表锁 vs 行锁最直观的对比。

2. `SHOW TABLE STATUS` 的差异：InnoDB 的 Rows 列是估算值，MyISAM 是精确值。Data_length 和 Index_length 也不同——MyISAM 的数据和索引分开存储。

3. 迁移步骤：(a) 备份，(b) 评估——检查是否有 MyISAM 特有的特性依赖（如 MERGE 表），(c) 在测试环境 `ALTER TABLE ... ENGINE=InnoDB`，(d) 验证——确认数据完整、性能可接受，(e) 分批上线。风险：锁升级（大表 ALTER 可能锁很久）、空间增加（InnoDB 比 MyISAM 占更多磁盘）、主从延迟。

4. MySQL 8.0 中几乎没有 MyISAM 仍有优势的场景。全文索引曾经是 MyISAM 的优势（现在 InnoDB 也支持），GIS 曾经是 MyISAM 的优势（现在 InnoDB 也支持），COUNT(*) 快但为此牺牲事务和崩溃恢复完全不值。唯一的"优势"是磁盘空间占用略小——但差异已经可以忽略。
