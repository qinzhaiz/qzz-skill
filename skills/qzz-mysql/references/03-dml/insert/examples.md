# 代码示例

## 示例 1：插一条完整数据

```sql
INSERT INTO user (name, city, age, mobile, created_at) VALUES
  ('张三', '北京', 22, '13800001111', NOW());
```

`NOW()` 返回当前日期时间——等于你手写 `'2025-07-25 14:30:00'`，但不用每次都敲。

## 示例 2：省略非必填列

```sql
-- mobile 有 DEFAULT ''，不写就默认空字符串
INSERT INTO user (name, city, age) VALUES ('李四', '上海', 25);
```

## 示例 3：批量插入

```sql
INSERT INTO user (name, city, age) VALUES
  ('张三', '北京', 22),
  ('李四', '上海', 25),
  ('王五', '深圳', 21),
  ('赵六', '广州', 23);
```

## 示例 4：从查询结果插入

```sql
-- 把北京的用户归档到备份表
INSERT INTO user_backup (id, name, city, age, created_at)
SELECT id, name, city, age, created_at
FROM user
WHERE city = '北京';
```
