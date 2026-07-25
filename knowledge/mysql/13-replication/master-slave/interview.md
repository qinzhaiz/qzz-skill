# 面试题

## Q1：MySQL 主从复制的原理是什么？

**考点**：最高频的 MySQL 运维面试题。

**回答**：主从复制基于 binlog。三个线程协作：主库的 Binlog Dump 线程把 binlog 推送给从库，从库的 IO 线程接收并写入 relay log，从库的 SQL 线程从 relay log 重放 SQL。复制过程是异步的——主库写入事务提交后，从库可能稍后才同步完成。

**加分点**：能说出 GTID 替代传统位点的好处——自动定位、故障切换更简单。能说出三种 binlog 格式的区别——STATEMENT（记 SQL）、ROW（记行变更）、MIXED（混合）。能解释为什么推荐 ROW——保证主从数据一致，不受函数不确定性影响。

## Q2：MySQL 8.0 主从复制的新特性有哪些？

**考点**：关注版本演进。

**回答**：(1) **组复制（Group Replication）**：基于 Paxos 协议的多主复制，自动选主、故障检测。(2) **增强的半同步复制**：MySQL 5.7 开始支持，8.0 改进。主库等待至少一个从库确认收到 binlog 才返回客户端。(3) **并行复制**：从库的 SQL 线程可以并行回放多个事务（基于 group commit 或 writeset），大幅减少主从延迟。(4) **binlog 加密**：对 binlog 和 relay log 自动加密。

**加分点**：能解释并行复制的原理——同一 group commit 中的事务没有锁冲突，可以在从库并行回放。能提到 `slave_parallel_workers > 0` 开启并行复制。
