# 面试题

## Q1：InnoDB 的内存结构包括哪些？

**考点**：不只是背名字，要理解各自的作用。

**回答**：四大组件——(1) Buffer Pool：缓存数据页和索引页，InnoDB 最重要的内存结构，命中率直接影响性能。(2) Change Buffer：对二级索引的非唯一修改暂时缓存在内存，延迟写入，减少随机 IO。(3) Adaptive Hash Index：对 Buffer Pool 中热点数据页自动建立哈希索引，加速等值查询。(4) Log Buffer：redo log 的写缓冲，日志先写到这里再刷新到磁盘。

**加分点**：能说出 Change Buffer 只适用于非唯一的二级索引（因为唯一索引需要读盘检查唯一性）。能解释为什么 Adaptive Hash Index 对范围查询没用（哈希表只能等值查）。

## Q2：doublewrite buffer 是什么？为什么需要它？

**考点**：看是否理解"部分写"这个底层问题。

**回答**：InnoDB 的数据页是 16KB，但操作系统写磁盘通常是 4KB 为单位。如果写一个 16KB 页时机器断电，这个页可能只有前 4KB 被写入（后半截是旧数据）——这就是"部分写"。这种情况 redo log 无法恢复（redo log 恢复需要数据页是完整的）。doublewrite buffer 的解决方案：先把脏页顺序写入 doublewrite buffer（2 份连续 16KB），再随机写到数据文件的对应位置。启动恢复时如果发现某个页坏了，从 doublewrite buffer 恢复完整页。

**加分点**：能说出 doublewrite 的性能代价（每个页写两次），以及什么条件下可以关（支持原子写的 SSD，如 `innodb_doublewrite = DETECT_AND_RECOVER`）。
