# 常见错误

## 错误 1：关闭 `innodb_file_per_table`

**症状**：`ibdata1` 不断变大，删表也不回收空间。磁盘快满了。

**原因**：`innodb_file_per_table = OFF` 时所有表数据存在共享表空间 `ibdata1` 中。即使删除表，`ibdata1` 不会自动缩小。长期运行后这个文件可能几百 GB。

**怎么修**：开启 `innodb_file_per_table = ON`。如果已经关了，需要导出所有数据 → 重建 InnoDB → 导入（非常痛苦的迁移）。

## 错误 2：不知道 doublewrite buffer 的写入开销

**症状**：写入性能不如预期，用 `SHOW GLOBAL STATUS` 发现 doublewrite 写入量巨大。

**原因**：doublewrite buffer 让每次写操作写入两次——先写到 doublewrite buffer，再写到实际位置。等于写入量翻倍。对于 SSD（写入寿命有限）和写入密集型场景，这是不可忽视的开销。

**怎么修**：如果确认硬盘支持原子写（如 Fusion-io 或某些 NVMe SSD），可以关闭 doublewrite buffer（`innodb_doublewrite = OFF`）。但绝大多数情况下不建议关——丢了数据得不偿失。
