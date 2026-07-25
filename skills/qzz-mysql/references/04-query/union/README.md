# UNION 合并

> UNION 把两个 SELECT 的结果上下拼在一起。

## 为什么需要它

有时候你需要"查两张结构相似的表"或"同一个表按不同条件查两次，然后放一起看"。JOIN 是左右拼，UNION 是上下拼。

## 基本用法

```sql
SELECT name FROM user WHERE city = '北京'
UNION
SELECT name FROM user WHERE city = '上海';
```

两个查询的列数必须相同，列的类型要兼容。

## UNION vs UNION ALL

| | UNION | UNION ALL |
|---|---|---|
| 去重 | ✅ 自动去重 | ❌ 保留重复 |
| 速度 | 慢（要去重） | 快 |
| 什么时候用 | 需要去重 | 确定不会重复、或允许重复 |

**大多数场景用 UNION ALL——不去重更快。** 只有你真的需要去重时才用 UNION。

## 注意事项

- **列数和类型必须匹配。** 第一个 SELECT 查 3 列，第二个就得查 3 列。类型不匹配 MySQL 会尝试隐式转换，但别依赖这个。
- **ORDER BY 只能用在最后一个 SELECT 后面。** `UNION ALL ... ORDER BY name`——对整个合并结果排序。
- **别用 UNION 代替 JOIN。** 一个是上下拼，一个是左右拼，完全不同的操作。

## 和什么有关

- [JOIN](../join/) — 左右拼 vs 上下拼
- [ORDER BY](../order-limit/) — UNION 结果可以排序
