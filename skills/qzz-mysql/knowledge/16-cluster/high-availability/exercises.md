# 练习

## 基础练习

1. 用 Docker 搭建 3 节点的 MySQL 主从复制。模拟主库宕机（`docker stop`），手动将一个从库提升为主库。

2. 解释脑裂是什么，为什么单纯的"VIP 漂移"方案容易产生脑裂。

## 进阶练习

1. 用 MySQL Shell 搭建 3 节点 InnoDB Cluster，测试故障切换：停止主库，观察 MySQL Router 是否自动将流量路由到新主库。

2. 对比 MHA 和 InnoDB Cluster 的选主策略差异。

## 答案

1. 手动切换：从库 `STOP SLAVE; RESET SLAVE ALL; SET GLOBAL read_only=OFF` → 应用改连 → 其他从库 `CHANGE MASTER TO` 指向新主库。

2. 脑裂 = 两个节点都认为自己是主库并接受写入。VIP 漂移依赖网络通信判断节点存活——网络分区时旧主库仍持有 VIP，新主库也绑定了 VIP → 两个主库。

3. InnoDB Cluster 用 Paxos 协议，要求 majority（> 50% 节点）达成一致才能选主。3 节点最多容忍 1 节点故障。

4. MHA 基于 binlog position/GTID 选数据最新的从库。InnoDB Cluster 基于 Paxos 协议，节点投票选举。
