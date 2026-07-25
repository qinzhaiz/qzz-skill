# MySQL 源码结构

> MySQL 是用 C/C++ 写的开源数据库——下载源码，看它是怎么实现的。

## 为什么需要它

前面的章节都在"用" MySQL。如果你想深入理解——为什么 InnoDB 的索引是 B+Tree、查询优化器怎么决策、redo log 怎么实现——最终都要看源码。理解源码结构是深入 MySQL 的第一步。

## 它是什么

MySQL 8.0 源码是一个巨大的 C/C++ 项目（约 300 万行代码），用 CMake 构建。从 [GitHub](https://github.com/mysql/mysql-server) 获取源码。

### 核心目录

| 目录 | 内容 | 对应学习内容 |
|------|------|-------------|
| `sql/` | **Server 层**：SQL 解析、优化器、执行器 | 09-execution |
| `storage/innobase/` | **InnoDB 引擎**：存储、索引、事务、锁 | 06-index, 07-transaction, 08-lock |
| `storage/myisam/` | MyISAM 引擎 | 12-engine |
| `storage/perfschema/` | Performance Schema | 10-performance |
| `client/` | 客户端工具（mysql 命令行） | 01-basic |
| `mysys/` | 底层工具库（内存、文件、线程） | - |
| `include/` | 头文件 | - |
| `scripts/` | 安装脚本 | - |
| `mysql-test/` | 测试用例 | - |

### Server 层关键文件（`sql/` 目录）

| 文件 | 作用 |
|------|------|
| `sql_parse.cc` | SQL 入口，语句分发 |
| `sql_lex.cc` | 词法分析 |
| `sql_yacc.yy` | 语法分析（Bison 语法文件） |
| `sql_optimizer.cc` | 查询优化器 |
| `sql_executor.cc` | 查询执行器 |
| `handler.cc` | 存储引擎抽象接口 |

### InnoDB 关键文件（`storage/innobase/`）

| 文件 | 作用 |
|------|------|
| `buf/buf0buf.cc` | Buffer Pool 实现 |
| `btr/btr0cur.cc` | B+Tree 游标操作 |
| `lock/lock0lock.cc` | 锁系统实现 |
| `trx/trx0trx.cc` | 事务管理 |
| `log/log0log.cc` | redo log |

## 怎么工作

阅读源码的推荐路径（由浅入深）：

1. **先看 Server 层入口**：`sql/sql_parse.cc` → 理解一条 SQL 怎么被分发
2. **再看 InnoDB 的核心**：`buf/buf0buf.cc`（Buffer Pool）→ `btr/btr0cur.cc`（B+Tree）
3. **最后看高级特性**：`lock/lock0lock.cc`（锁）→ `trx/trx0trx.cc`（事务）

## 怎么用

```bash
# 克隆源码
git clone https://github.com/mysql/mysql-server.git
cd mysql-server
git checkout mysql-8.0.37  # 特定版本

# 查看源码统计
cloc sql/ storage/innobase/

# 搜索关键函数
grep -r "ha_rnd_next" sql/           # 全表扫描接口
grep -r "trx_commit" storage/innobase/ # 事务提交

# 用 IDE 打开（推荐 CLion 或 VSCode）
# 关键是代码跳转——从函数调用链理解执行流程
```

## 注意事项

1. **不需要全部读懂**——300 万行代码没人能全看懂。聚焦你要理解的那部分。
2. **以问题驱动阅读**——带着具体问题看源码（比如"B+Tree 分裂怎么实现"），而不是线性的从头读。
3. **先看文档再看源码**——InnoDB 有官方文档 + 大量博客分析，先理解设计思想再看实现细节。

## 和什么有关

- [InnoDB 源码导读](../innodb-source/) —— 深入 InnoDB 实现
- [编译与调试](../compile-debug/) —— 把源码跑起来
- [InnoDB 架构](../../12-engine/innodb-architecture/) —— 先理解架构再看源码
