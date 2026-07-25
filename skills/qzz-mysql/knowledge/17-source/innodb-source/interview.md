# 面试题

## Q1：InnoDB 源码中，查询一条记录的完整路径是怎样的？

**考点**：是否理解 Server 层到 InnoDB 的调用链。

**回答**：Server 层 `JOIN::exec()` → `handler::ha_index_read()` → `ha_innobase::index_read()` → InnoDB 的 `row_search_mvcc()`。`row_search_mvcc` 做三件事——(1) B+Tree 搜索找到叶子页，(2) 逐行遍历匹配的记录，(3) 对每一行做 MVCC 可见性检查（对比记录的 `trx_id` 和当前 ReadView），不可见的行通过 undo log 版本链回溯。

**加分点**：能说出 `row_search_mvcc` 是 InnoDB 最长最复杂的函数之一（约 2000 行），处理了索引扫描、MVCC 判断、锁检查等多种逻辑。

## Q2：如果想理解 Buffer Pool 的 LRU 淘汰算法，应该看哪些代码？

**考点**：具体到文件级。

**回答**：`storage/innobase/buf/buf0buf.cc`——`buf_LRU_get_free_block()` 从 LRU 链表尾部找空闲页。`buf_page_make_young()` 把热页移到 LRU 头部。关键数据结构：`buf_pool->LRU`（双向链表）、`buf_pool->free`（空闲页链表）、`buf_pool->flush_list`（脏页链表）。配合 `buf/buf0flu.cc` 理解脏页刷盘逻辑。

**加分点**：能说出冷端/热端的实现——`BUF_LRU_OLD_PCT`（默认 3/8）控制链表冷端占比，`buf_page_peek_if_too_old()` 判断新页是否应该留在冷端。
