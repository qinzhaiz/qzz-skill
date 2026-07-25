# 代码示例

B+Tree 是数据结构，没有直接对应的 SQL。但可以通过表数据量估算树的高度：

## 示例：估算主键索引能存多大

一个 INT 主键占 4 字节。InnoDB 一页 16KB：

- 内部节点：每页约 1170 个 key（16KB ÷ (4B key + 10B 指针) ≈ 1170）
- 叶子节点：每页约 16 行（16KB ÷ 1KB 行数据 ≈ 16）

三层 B+Tree：1170 × 1170 × 16 ≈ **2190 万行**

四层就能存 256 亿行——但很少有 MySQL 表需要四层 B+Tree。

## 验证自己的表

```sql
-- 查看索引大小和深度
SELECT * FROM information_schema.INNODB_TABLESTATS WHERE name = '你的库/你的表';
```sql

B+Tree 本身不需要你管理——建了索引就自动构建。需要你管的是：选对列，把 EXPLAIN 里的 `rows` 控制住。
