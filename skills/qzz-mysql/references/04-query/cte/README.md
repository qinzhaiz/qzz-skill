# CTE 公用表表达式

> CTE（Common Table Expression）用 WITH 子句给子查询起个名字，让复杂 SQL 分成一步一步写。MySQL 8.0 开始支持。

## 为什么需要它

写一个复杂查询——三层嵌套子查询、两个 JOIN、一个聚合——写完了自己都看不懂。

CTE 让你把复杂查询拆成几个有名字的"临时视图"，每一步都看得清。**逻辑上 = 定义变量，实际上是内联展开。**

## 基本语法

```sql
WITH cte_name AS (
    SELECT ...
)
SELECT ... FROM cte_name;
```

### 单个 CTE

```sql
WITH beijing_users AS (
    SELECT * FROM user WHERE city = '北京'
)
SELECT name, age FROM beijing_users WHERE age > 20;
```

先定义 `beijing_users`（所有北京用户），然后在它上面再查。

### 多个 CTE

```sql
WITH
    beijing_users AS (
        SELECT * FROM user WHERE city = '北京'
    ),
    young_users AS (
        SELECT * FROM beijing_users WHERE age < 25
    )
SELECT name FROM young_users ORDER BY age;
```

一个 CTE 可以引用前面定义的 CTE——像搭积木一样一层一层来。

### 递归 CTE

CTE 可以引用自己——处理树形结构（组织架构、评论嵌套、菜单层级）：

```sql
WITH RECURSIVE cte AS (
    -- 基础：顶层节点
    SELECT id, name, parent_id, 1 AS level
    FROM category WHERE parent_id IS NULL

    UNION ALL

    -- 递归：子节点 = 父节点的下一层
    SELECT c.id, c.name, c.parent_id, cte.level + 1
    FROM category c
    JOIN cte ON c.parent_id = cte.id
)
SELECT * FROM cte ORDER BY level, id;
```

逐层展开——先查出所有顶层分类（parent_id IS NULL），再把每个分类的子分类找出来，一直递归到没有子分类为止。

## CTE vs 子查询 vs VIEW

| | CTE | 子查询 | VIEW |
|---|---|---|---|
| 生命周期 | 单个查询结束就没了 | 同 CTE | 持久存在 |
| 可读性 | ✅ 好 | ⚠️ 嵌套深了很难读 | ✅ |
| 可引用次数 | 多次 | 写一次用一次 | 多次 |
| 递归支持 | ✅ | ❌ | ❌ |

**子查询嵌套超过两层 → 改成 CTE。** 这是最实用的改写原则。

## 注意事项

- **CTE 是 MySQL 8.0 才有的。** 5.7 不支持。
- **CTE 不存数据——它只是查询的别名。** 每次引用 CTE 都会重新执行里面的查询。
- **递归 CTE 必须写 `RECURSIVE` 关键字。**

## 和什么有关

- [子查询](../subquery/) — CTE 是子查询的高级替代
- [JOIN](../join/) — CTE 经常配合 JOIN 使用
