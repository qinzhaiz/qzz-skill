# 练习

## 基础练习

1. 克隆 MySQL 8.0 源码，统计 `sql/` 和 `storage/innobase/` 目录下的代码行数。

2. 在源码中找到 `sql_parse.cc` 文件，定位 `dispatch_command` 函数。理解它是如何分发不同 SQL 命令的。

## 进阶练习

1. 从 `sql_parse.cc` 开始，追踪一条 `SELECT * FROM t WHERE id = 1` 的完整执行路径——从 Server 层到 InnoDB 层。

2. 在 InnoDB 源码中，找到 Buffer Pool 的 LRU 链表实现（`buf/buf0buf.cc`），理解新页是如何加入 LRU 冷端头部的。

## 答案

1. `cloc sql/ storage/innobase/` 统计。Server 层 + InnoDB 引擎约 250-300 万行 C/C++ 代码。

2. `dispatch_command()` 在 `sql/sql_parse.cc`，根据 `command` 枚举值调用不同处理函数。`COM_QUERY` 调用 `mysql_execute_command()`。

3. 路径：`dispatch_command` → `mysql_parse`（词法+语法）→ `mysql_execute_command` → `execute_sqlcom_select` → `handle_query` → `JOIN::optimize`（优化）→ `JOIN::exec`（执行）→ `handler::ha_index_read`（InnoDB 索引读取）→ `row_search_mvcc`（B+Tree 查找 + MVCC）。

4. `buf_LRU_get_free_block()` → 从 LRU 链表尾部获取空闲块。新页加入冷端（old blocks）是通过 `buf_page_init_for_read()` → `buf_LRU_add_block()` 实现的，`BUF_LRU_OLD_PCT` 控制冷端占比。
