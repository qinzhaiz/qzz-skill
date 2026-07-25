# 常见错误

## 错误 1：Buffer Pool 太小——忘了调

**症状**：数据库内存 32GB，但 Buffer Pool 还是默认 128MB。查询一直读磁盘，磁盘 IO 居高不下。

**原因**：新装的 MySQL 默认 `innodb_buffer_pool_size = 128MB`，很多人都忘了调。这个默认值适用于几十年前的硬件。

**怎么修**：立即调大到物理内存的 50-70%。MySQL 8.0 支持动态调整：`SET GLOBAL innodb_buffer_pool_size = 20G;`。但最好在 my.cnf 中持久化设置。

## 错误 2：Buffer Pool 太大——导致 swap

**症状**：数据库刚开始很快，运行一段时间后整体变慢，操作系统也开始卡。

**原因**：Buffer Pool 设到了物理内存的 90%，OS 和别的进程没有足够内存。OS 开始用 swap——swap 在磁盘上，比正常磁盘操作还慢。一旦 swap，整个系统性能断崖式下跌。

**怎么修**：留至少 20-30% 物理内存给 OS、文件系统缓存、其他进程。观察 `free -h`，确保 available memory 始终有足够的余量。

## 错误 3：不知道 Buffer Pool 支撑预读也会浪费

**症状**：`SHOW GLOBAL STATUS` 看到大量 `Innodb_buffer_pool_read_ahead_evicted`（预读后被淘汰的页）。

**原因**：InnoDB 默认开启了线性预读——如果连续访问了几个页，InnoDB 猜测你接下来也会按顺序读，提前加载后续页。但如果实际访问模式不是顺序的（比如随机跳跃），预读的页根本没用上，白白消耗 IO 和 Buffer Pool 空间。

**怎么修**：SSD 下随机读性能已经不差，预读的收益变小。如果 `_evicted` 占比高（> 50%），考虑调低 `innodb_read_ahead_threshold`（默认 56，改小更保守）或直接关掉（不推荐，对少数顺序扫描场景有帮助）。
