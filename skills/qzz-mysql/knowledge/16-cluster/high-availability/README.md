# 高可用架构

> 主库挂了不是灾难——没有准备"挂了之后怎么办"才是。

## 为什么需要它

一台 MySQL 扛不住了可以主从+读写分离。但如果主库这台机器宕机了怎么办？硬件故障、机房断电、网络分区都会导致主库不可用。高可用就是为这种情况做预案：自动检测主库故障 → 选新主库 → 切换流量 → 尽可能减少停机时间。

## 它是什么

MySQL 高可用 = 数据冗余（复制）+ 故障检测 + 自动切换 + 流量路由。

| 方案 | 复杂度 | 特点 | 适用场景 |
|------|--------|------|---------|
| **MHA** | 中 | 成熟稳定，秒级切换，支持 GTID | 传统主从架构 |
| **Orchestrator** | 中 | 可视化拓扑管理，智能故障检测 | 需要拓扑管理的复杂架构 |
| **InnoDB Cluster** | 高 | MySQL 官方方案，Paxos 协议自动选主 | MySQL 8.0 新项目 |
| **Keepalived + VIP** | 低 | 简单，但容易脑裂 | 不推荐，仅测试环境 |

## 怎么工作

### InnoDB Cluster（推荐新项目使用）

```sql
应用 → MySQL Router → Group Replication
                        ├── 节点1（主，读写）
                        ├── 节点2（从，只读）
                        └── 节点3（从，只读）
```sql

- Group Replication 基于 Paxos 协议，节点间自动检测和选主
- MySQL Router 自动感知主节点变化，透明切换流量
- 有防脑裂机制：只有 majority（多数派）组才能写入

### MHA 切换流程

```sql
1. Manager 检测主库宕机（3 次心跳失败）
2. 选出数据最新的从库（基于 binlog position / GTID）
3. 从其他存活的从库拉取差异 binlog → 补到候选从库
4. 候选从库提升为主库
5. VIP 切换到新主库
6. 其他从库重新指向新主库
```bash

## 怎么用

```bash
# MySQL Shell 创建 InnoDB Cluster
mysqlsh --uri root@node1:3306
dba.createCluster('prod_cluster')
dba.getCluster().addInstance('root@node2:3306')
dba.getCluster().addInstance('root@node3:3306')
dba.getCluster().status()
```

```sql
-- 查看组复制成员状态
SELECT MEMBER_HOST, MEMBER_PORT, MEMBER_STATE, MEMBER_ROLE
FROM performance_schema.replication_group_members;
```sql

## 注意事项

1. **脑裂是最危险的**——两个节点同时认为自己是主库，数据彻底乱了。Group Replication 用 Paxos 防脑裂；VIP 方案无法防脑裂。
2. **异步复制会丢数据**——主库宕机时已提交但未同步的事务丢失。保证不丢数据用半同步复制或组复制。
3. **成本评估**——最小配置 3 台服务器（1 主 2 从），加上中间件（Router/Proxy）。

## 和什么有关

- [主从复制](../../13-replication/master-slave/) —— 高可用的数据基础
- [数据库代理](../proxy/) —— 应用层透明切换
- [分库分表](../sharding/) —— 规模更大时的扩展方案
