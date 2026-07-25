# 面试题

## Q1：ALTER TABLE 在大表上为什么慢？怎么安全地改？

**考点**：考察有没有生产环境经验。

**回答**：MySQL 8.0 之前多数 ALTER 需要全表拷贝——新建一张临时表，把数据从旧表复制过去，切换，删旧表。数据量越大，复制时间越长。期间还可能有锁等待。安全做法是用 pt-online-schema-change（Percona Toolkit）或 gh-ost（GitHub）——它们创建一张新表、慢慢同步、最后切换，几乎不影响线上读写。

**加分**：能说出 MySQL 8.0 的原子 DDL 改进了什么，以及哪些 ALTER 操作是 INPLACE 的（只改元数据不拷贝数据，如改名、加索引）。

## Q2：ADD COLUMN 和 AFTER 有什么用？

**考点**：考细节——很多开发只会 ADD COLUMN，不知道可以指定位置。

**回答**：`ALTER TABLE t ADD COLUMN c INT AFTER name` 把新列 c 加在 name 列之后。不加 AFTER 默认在最后。生产环境加列通常放最后——省得折腾顺序。但建表脚本里为了可读性，会按逻辑顺序排列列，这是人看得舒服。
