# 代码示例

## 示例 1：经典注入攻击演示

**场景**：登录表单的 SQL 注入。

```python
# ❌ 危险：字符串拼接
def login_unsafe(username, password):
    sql = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(sql)
    return cursor.fetchone()

# 攻击输入：
# username: admin' --
# password: 随便填

# 拼接后的 SQL：
# SELECT * FROM user WHERE username = 'admin' --' AND password = 'xxx'
# -- 后面的部分被注释掉了！密码校验被绕过！

# 更狠的注入：
# username: '; DROP TABLE user; --
# SELECT * FROM user WHERE username = ''; DROP TABLE user; --' AND password = 'xxx'
```

```python
# ✅ 安全：参数化查询
def login_safe(username, password):
    sql = "SELECT * FROM user WHERE username = %s AND password = %s"
    cursor.execute(sql, (username, password))
    return cursor.fetchone()

# 不管攻击者输入什么，都只是数据，不会改变 SQL 结构
```sql

## 示例 2：动态排序的白名单防护

```python
# 场景：API 允许用户选择排序方式
# ❌ 危险：order_by 直接拼接到 SQL
def list_users(order_by):
    sql = f"SELECT * FROM user ORDER BY {order_by}"
    cursor.execute(sql)  # 如果 order_by = "id; DROP TABLE user;"

# ✅ 安全：白名单验证
ALLOWED_COLUMNS = {'id', 'username', 'email', 'created_at'}

def list_users_safe(order_by):
    if order_by not in ALLOWED_COLUMNS:
        raise ValueError(f"Invalid column: {order_by}")
    sql = "SELECT * FROM user ORDER BY " + order_by  # 此时 order_by 已经是安全的
    cursor.execute(sql)
```sql

## 示例 3：Go 语言的参数化查询

```go
// ✅ 安全
username := r.URL.Query().Get("username")
row := db.QueryRow(
    "SELECT id, email FROM user WHERE username = ?",
    username,  // 自动转义，安全
)

// ❌ 危险
sql := fmt.Sprintf("SELECT * FROM user WHERE username = '%s'", username)
// 不要这样写！
```bash

## 示例 4：MySQL 原生的参数化查询

```sql
-- 预处理语句
PREPARE stmt FROM 'SELECT * FROM user WHERE name = ? AND age > ?';

-- 设置参数
SET @name = 'test';
SET @age = 18;

-- 执行
EXECUTE stmt USING @name, @age;

-- 清理
DEALLOCATE PREPARE stmt;

-- 尝试注入（不会生效）
PREPARE stmt FROM 'SELECT * FROM user WHERE name = ?';
SET @name = "admin' OR '1'='1";  -- 被当作普通的字符串，不会产生注入
EXECUTE stmt USING @name;
-- 实际查找 name = "admin' OR '1'='1"（这个用户名不存在）
```
