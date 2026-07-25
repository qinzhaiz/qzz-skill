# 代码示例

## 示例 1：基本过滤

```sql
-- 单条件
SELECT * FROM user WHERE city = '北京';

-- 多条件 AND
SELECT * FROM user WHERE city = '北京' AND age > 20;

-- 多条件 OR
SELECT * FROM user WHERE city = '北京' OR city = '上海';

-- IN 等价写法
SELECT * FROM user WHERE city IN ('北京', '上海', '深圳');
```

## 示例 2：NULL 的坑

```sql
SELECT * FROM user WHERE email = NULL;
-- Empty set —— 永远不会返回结果

SELECT * FROM user WHERE email IS NULL;
-- 正确返回 email 为空的行
```

## 示例 3：LIKE 匹配

```sql
WHERE name LIKE '张%'  -- 张三、张三丰 ✅
WHERE name LIKE '张_'  -- 张三 ✅，张三丰 ❌（名字太长）
WHERE name LIKE '%三'  -- 张三、王三 ✅（但前导通配符 = 不能走索引，大表慢）
```
