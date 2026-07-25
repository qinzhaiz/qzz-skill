# WHERE 条件

> WHERE 过滤行——只返回满足条件的那些，跳过不满足的。

## 为什么需要它

`SELECT * FROM user` 查出所有行——但你的需求几乎从来不是"所有行"。你要的是"年龄大于 20 的用户""城市是北京的用户""手机号不为空的用户"。WHERE 就是干这个的。

## 常用操作符

### 比较

```sql
WHERE age = 20          -- 等于
WHERE age != 20         -- 不等于（也可以用 <>）
WHERE age > 20          -- 大于
WHERE age >= 20         -- 大于等于
WHERE age < 20          -- 小于
WHERE age BETWEEN 20 AND 30  -- 在 20 到 30 之间（含边界）
```sql

### 逻辑组合

```sql
WHERE city = '北京' AND age > 20       -- 同时满足
WHERE city = '北京' OR city = '上海'   -- 满足其一
WHERE city IN ('北京', '上海', '深圳') -- 等价上面那条，更简洁
WHERE age NOT BETWEEN 20 AND 30       -- 不在这个范围
```sql

### 模糊匹配

```sql
WHERE name LIKE '张%'     -- % 匹配任意多个字符
WHERE name LIKE '张_'     -- _ 匹配单个字符
WHERE phone LIKE '%1234' -- 以 1234 结尾
```sql

### NULL 判断

```sql
WHERE email IS NULL       -- 为空
WHERE email IS NOT NULL   -- 不为空

-- 注意：WHERE email = NULL 永远不返回结果！
-- NULL 不等于任何东西，包括它自己。
```sql

## AND 和 OR 的优先级

```sql
-- 这条的真实含义是什么？
WHERE city = '北京' OR city = '上海' AND age > 20
```sql

AND 优先级高于 OR，所以实际是：`city='北京'` 或者 `(city='上海' AND age>20)`。

**不确定优先级时——加括号。** `WHERE (city='北京' OR city='上海') AND age>20` 一眼就能看明白。

## 注意事项

- **NULL 不能用 = 判断。** 用 `IS NULL` / `IS NOT NULL`。
- **LIKE 前导通配符（'%张'）无法用索引。** 数据量大时很慢。
- **BETWEEN 包含边界。** `BETWEEN 1 AND 10` 返回 1 到 10（含 1 和 10）。

## 和什么有关

- [SELECT 基础](../select-basic/) — SELECT + WHERE 是最常用的组合
- [排序和分页](../order-limit/) — 过滤完再排序
- [06-index/when-to-use/](../../06-index/when-to-use/) — WHERE 条件决定了该在哪些列建索引
