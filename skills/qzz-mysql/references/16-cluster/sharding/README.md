# 分库分表

> 当单表数据量超过千万级、单库 QPS 过万——一台机器扛不住了。分库分表把数据拆到多台机器上，水平扩展存储和计算能力。

## 为什么需要它

读写分离解决了"读"的扩展，但主库的"写"和"存储"仍然在单机上。当单表数据量太大时：
- 查询变慢（B+Tree 层级增加）
- DDL 操作执行不了（改个字段要锁表几小时）
- 备份和恢复太慢
- 单机磁盘容量不够

这时就需要分库分表——把一张大表的数据按规则拆分到多个数据库实例上。

## 它是什么

两种拆分方式：

| 方式 | 怎么拆 | 例子 |
|------|--------|------|
| **垂直拆分** | 按业务模块拆库 | 用户库、订单库、商品库 |
| **水平拆分** | 按数据行拆分同一张表 | order_0, order_1, ..., order_15 |

### 水平拆分（最常用）

```
订单表（5 亿行）
    ↓ 按 user_id % 16 分片
    ├── order_0（user_id % 16 = 0）
    ├── order_1（user_id % 16 = 1）
    ├── ...
    └── order_15（user_id % 16 = 15）
```

**分片键**（Sharding Key）的选择是核心——选得好数据均匀分布，选不好热点集中在某几个分片。

### 中间件

| 方案 | 特点 |
|------|------|
| **ShardingSphere-Proxy** | Apache 开源，支持分库分表 + 读写分离 |
| **Vitess** | YouTube 开源，云原生，Kubernetes 友好 |
| **MyCat / DBLE** | 国内使用较多 |

## 怎么工作

```
应用 → ShardingSphere-Proxy → 数据库（分片1）
                             → 数据库（分片2）
                             → 数据库（分片3）
```

中间件拦截 SQL：`SELECT * FROM user WHERE id = 123` → 计算 `123 % 3 = 0` → 路由到分片 0。

### 分片键选择原则

1. **查询都带分片键**——不带分片键的查询需要广播到所有分片（性能很差）
2. **数据均匀分布**——选基数大、分布均匀的字段（如 user_id，不选 gender）
3. **避免跨分片 JOIN**——关联查询尽量在同一个分片内完成

## 怎么用

```yaml
# ShardingSphere-Proxy 配置示例
rules:
  - !SHARDING
    tables:
      user:
        actualDataNodes: ds0.user_${0..1}, ds1.user_${0..1}
        tableStrategy:
          standard:
            shardingColumn: id
            shardingAlgorithmName: user_inline
      orders:
        actualDataNodes: ds0.orders_${0..3}, ds1.orders_${0..3}
        databaseStrategy:
          standard:
            shardingColumn: user_id
            shardingAlgorithmName: orders_db_inline
        tableStrategy:
          standard:
            shardingColumn: user_id
            shardingAlgorithmName: orders_tbl_inline

    shardingAlgorithms:
      user_inline:
        type: INLINE
        props:
          algorithm-expression: user_${id % 2}
      orders_db_inline:
        type: INLINE
        props:
          algorithm-expression: ds${user_id % 2}
      orders_tbl_inline:
        type: INLINE
        props:
          algorithm-expression: orders_${user_id % 4}
```

## 注意事项

1. **分库分表是最后手段**——在尝试了索引优化、缓存、读写分离、硬件升级之后再考虑。复杂度极高。
2. **不带分片键的查询是灾难**——需要广播到所有分片，然后合并结果。尽量避免。
3. **扩容很痛苦**——从 4 个分片扩到 8 个，数据需要重新分布。提前规划好分片数量和扩容方案。
4. **事务跨分片**——分布式事务（XA/Seata）复杂且性能差。尽量保证事务在单个分片内完成。

## 和什么有关

- [主从复制](../../13-replication/master-slave/) —— 分库分表 + 主从复制 + 读写分离 = 完整架构
- [数据库代理](../proxy/) —— 中间件屏蔽分片细节
- [高可用架构](../high-availability/) —— 每个分片还需要做高可用
