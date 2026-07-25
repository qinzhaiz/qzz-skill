# 练习

## 基础练习

1. 用 SQL 查看当前 MySQL 的 `innodb_buffer_pool_size` 和 Buffer Pool 命中率。判断是否需要调大。

2. 解释为什么 `innodb_buffer_pool_size` 设得太大反而有害。什么情况下会出现这种问题？

## 进阶练习

1. 用 `SHOW ENGINE INNODB STATUS` 查看 Buffer Pool 的详细信息（free buffers、database pages、modified db pages），解释每个指标的含义。

2. 在有数据的 MySQL 上执行一些查询，观察 Buffer Pool 命中率的变化。如果命中率低，尝试调大 Buffer Pool 后再次观察。

## 答案

1. Buffer Pool 命中率 = 1 - (`Innodb_buffer_pool_reads` / `Innodb_buffer_pool_read_requests`)。如果 < 99%，需要调大。

2. Buffer Pool 太大 → 占用 OS 内存 → OS 没有足够内存做文件系统缓存和系统操作 → 可能触发 swap → 内存变磁盘速度 → 比 Buffer Pool 小的时候还慢。如果 MySQL 不是服务器上唯一进程（还有 Web 服务等），需要留足够内存给其他进程。

3. `free buffers` = 可用的 Buffer Pool 页面数。`database pages` = 已缓存的数据页。`modified db pages` = 脏页（已修改但未写回磁盘）。如果 free buffers 长期为 0，可能需要调大 Buffer Pool（但也要看命中率，可能只是正常占满）。
