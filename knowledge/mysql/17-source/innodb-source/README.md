# InnoDB 源码导读

> 理解了前面的 Buffer Pool、B+Tree、事务、锁——现在看看源码里它们是怎么实现的。

## 为什么需要它

前面章节讲的都是 InnoDB 的"设计原理"。但有些问题只有看源码才能回答：B+Tree 页分裂时到底做了什么？MVCC 的 ReadView 创建时机是在哪个函数里？死锁检测的 O(N²) 循环在哪里？这篇导读帮你快速定位这些关键代码。

## 它是什么

InnoDB 源码在 `storage/innobase/` 目录下，约 100 万行 C 代码。按功能分为几个子系统：

| 子系统 | 目录 | 关键概念 |
|--------|------|---------|
| **Buffer Pool** | `buf/` | LRU 淘汰、脏页刷新、预读 |
| **B+Tree 索引** | `btr/` | 页分裂/合并、游标遍历 |
| **行存储** | `row/` | 行格式、MVCC 读取 |
| **事务** | `trx/` | 事务生命周期、undo log、purge |
| **锁** | `lock/` | Record/Gap/Next-Key Lock、死锁检测 |
| **日志** | `log/` | redo log 写入和恢复 |
| **文件 IO** | `fil/` | 表空间文件管理 |
| **数据字典** | `dict/` | 表、索引元数据 |

## 怎么工作

### 关键数据结构和函数

**Buffer Pool（`buf/buf0buf.cc`）**
- `buf_pool_t`：Buffer Pool 实例（多个实例减少锁竞争）
- `buf_block_t`：缓存页控制块
- `buf_page_get_gen()`：获取数据页的核心函数
- `buf_LRU_get_free_block()`：LRU 淘汰找空闲页

**B+Tree（`btr/btr0cur.cc`）**
- `btr_cur_search_to_nth_level()`：从根到叶搜索
- `btr_page_split_and_insert()`：页分裂
- `btr_cur_optimistic_insert()`：乐观插入（页有空间直接插）

**事务（`trx/trx0trx.cc`）**
- `trx_t`：事务对象（状态、锁、undo log）
- `trx_commit_for_mysql()`：事务提交流程
- `ReadView`（在 `read/read0read.cc`）：可见性判断

**锁（`lock/lock0lock.cc`）**
- `lock_rec_lock()`：加行锁
- `lock_deadlock_check()`：死锁检测（O(N²) 循环在这里）
- `lock_rec_lock_slow()`：锁冲突处理

### 阅读建议

从 Buffer Pool 开始（最基础），再到 B+Tree（索引实现），最后看事务和锁（最复杂）。

## 怎么用

```bash
# 进入 InnoDB 源码目录
cd storage/innobase

# 找 Buffer Pool 初始化代码
grep -rn "buf_pool_init" buf/

# 找 B+Tree 页分裂代码
grep -rn "btr_page_split" btr/

# 找死锁检测代码
grep -rn "Deadlock" lock/

# 用 Doxygen 生成源码文档（更易读）
# 在源码根目录执行：
doxygen Doxyfile
```

### 阅读流程

1. 从 `handler/ha_innodb.cc` 看 InnoDB 如何实现 MySQL 引擎接口
2. `handler::index_read()` → `row_search_mvcc()`：追踪索引查询
3. `handler::write_row()` → `row_insert_for_mysql()`：追踪插入
4. 看 `buf/buf0buf.cc` 中 Buffer Pool 的 `buf_page_get_gen()` 理解缓存命中/未命中

## 注意事项

1. **源码是 C 风格的 C++**——主要是 C 语法，用了一些 C++ 特性（类、模板）。不需要精通 C++ 就能读懂主要逻辑。
2. **不要从头到尾读**——每个功能模块独立阅读。从"为什么页分裂"这个具体问题出发，只看相关代码路径。
3. **配合 Doxygen 文档**——MySQL 官方有 Doxygen 生成的源码文档，可以快速浏览函数和数据结构。

## 和什么有关

- [MySQL 源码结构](../source-structure/) —— 先了解整体结构
- [编译与调试](../compile-debug/) —— 把 InnoDB 跑起来
- [InnoDB 架构](../../12-engine/innodb-architecture/) —— 先理解架构再看代码
