# 练习

## 基础练习

1. 如果主键是 BIGINT（8 字节）而不是 INT（4 字节），三层 B+Tree 大约能存多少行？

2. 为什么 B+Tree 的范围查询比 Hash 索引快？用自己的话解释。

## 进阶练习

1. 查一下 MySQL 的页大小（`SHOW VARIABLES LIKE 'innodb_page_size'`）。如果页大小是 64KB，同样三层 B+Tree 能存多少行？

## 答案

1. BIGINT 主键让每个内部节点能存的 key 变少（8B vs 4B），三层大约能存 1600 万行——比 INT 少约 27%。

2. Hash 索引只适合等值查询——`WHERE id = 1`。对 `WHERE id BETWEEN 1 AND 100`，Hash 毫无作用——值被散列到随机位置，无法顺序扫描。B+Tree 的叶子节点是链表，直接从 1 往后扫到 100 即可。
