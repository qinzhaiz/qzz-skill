# 练习

## 基础练习

1. 在 InnoDB 源码中找到 `buf_page_get_gen()` 函数（`buf/buf0buf.cc`），理解它的参数含义——它是怎么判断页是否在 Buffer Pool 中的。

2. 找到 `ReadView` 结构的定义（`read/read0types.h` 或类似文件），对照 MVCC 章节的理论，理解每个字段的含义。

## 进阶练习

1. 从 `row_insert_for_mysql()` 开始，追踪一条 INSERT 的完整路径：从 Server 层调用 → InnoDB 插入记录 → 写 undo log → 写 redo log。

2. 阅读 `btr_cur_optimistic_insert()` 和 `btr_cur_pessimistic_insert()` 的区别。乐观插入和悲观插入分别对应什么场景？

## 答案

1. `buf_page_get_gen()` 先在 Buffer Pool 的 hash 表中查找 `page_id`，如果找到返回缓存页；如果未找到，从 free list 或 LRU 尾部获取一个空闲块，调用 `fil_io()` 从磁盘读取。

2. `ReadView` 包含 `m_ids`（活跃事务 ID 列表）、`m_low_limit_id`（下一个待分配 ID）、`m_up_limit_id`（最小活跃事务 ID）、`m_creator_trx_id`（创建者 ID）。可见性判断：如果 `trx_id < m_up_limit_id` → 可见（已提交）；如果 `trx_id >= m_low_limit_id` → 不可见（还没开始）。

3. INSERT 路径：`handler::ha_write_row()` → `row_insert_for_mysql()` → `row_ins_step()`（插入 B+Tree）→ `trx_undo_report_row_operation()`（写 undo log）→ `log_write_up_to()`（写 redo log）。

4. 乐观插入：页有足够空间，直接在目标页插入。悲观插入：页空间不足，需要先分裂页再插入。乐观插入是常见路径（快），悲观插入需要额外 IO 和加锁（慢）。
