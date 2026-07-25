# 面试题

## Q1：MySQL 源码的主要目录结构是怎样的？

**考点**：是否真的看过源码。

**回答**：两大核心——`sql/`（Server 层：解析→优化→执行）和 `storage/innobase/`（InnoDB 引擎：存储、索引、事务、锁）。其他重要目录：`client/`（客户端工具）、`mysys/`（底层工具库）、`include/`（头文件）、`mysql-test/`（测试用例）。Server 层与引擎层通过 `handler.cc` 的抽象接口交互。

**加分点**：能说出 `sql/` 目录下的关键文件——`sql_parse.cc`（入口）、`sql_optimizer.cc`（优化器）、`sql_executor.cc`（执行器）。能说出 InnoDB 的关键子目录——`buf/`（Buffer Pool）、`btr/`（B+Tree）、`lock/`（锁）、`trx/`（事务）。

## Q2：怎样高效地阅读 MySQL 源码？

**考点**：学习方法论。

**回答**：(1) 带着具体问题读，不要从头到尾读。(2) 先理解架构和设计文档，再看实现细节。(3) 用 IDE 的代码跳转功能（CLion 或 VSCode）追踪函数调用链。(4) 从简单问题开始——如"SELECT * FROM table 怎么执行"→ 从 `dispatch_command` 开始追踪。

**加分点**：能说出具体的学习路径——先看 Server 层入口（sql_parse.cc），再看 InnoDB 核心（Buffer Pool → B+Tree → 事务 → 锁）。用 grep 或 IDE 搜索关键函数名快速定位。
