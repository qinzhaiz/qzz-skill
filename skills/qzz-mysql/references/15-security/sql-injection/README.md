# SQL 注入防护

> 把用户输入拼接到 SQL 字符串里——这是最常见、最危险的安全漏洞，也是最容易防御的（只要用参数化查询）。

## 为什么需要它

不防 SQL 注入会导致：攻击者绕过登录验证（不输入密码也能登录）、窃取全部用户数据、修改数据库内容、甚至删除整个数据库。OWASP 把注入攻击连续多年列为 Web 安全威胁第一名。

重要的是：SQL 注入不是 MySQL 特有的问题，但防御方法在 MySQL 上非常成熟。

## 它是什么

SQL 注入发生在应用代码把用户输入直接拼接到 SQL 字符串中时。攻击者可以通过精心构造的输入，改变 SQL 语句的语义。

```python
# ❌ 危险的写法
user_input = input("请输入用户名: ")
sql = f"SELECT * FROM user WHERE name = '{user_input}'"
# 用户输入: ' OR '1'='1' --
# 实际执行的 SQL: SELECT * FROM user WHERE name = '' OR '1'='1' --'
# 结果：返回所有用户！
```

## 怎么工作

### 攻击原理

1. 应用把用户输入拼进 SQL 字符串
2. 攻击者在输入中加入 SQL 关键字和特殊符号（`' " -- # ;`）
3. 拼接后的 SQL 被数据库当作合法语句执行
4. 攻击者的意图得以实现——读数据、改数据、删数据

### 防御核心：参数化查询

**永远不要拼接 SQL 字符串。用参数化查询（Prepared Statement）**——把 SQL 结构和数据分开：

```python
# ✅ 正确的写法
user_input = input("请输入用户名: ")
cursor.execute("SELECT * FROM user WHERE name = %s", (user_input,))
# 数据库知道 %s 是数据，不是 SQL 的一部分
# 用户输入 ' OR '1'='1' -- 会被当作普通字符串处理
```

不同的编程语言，语法不同，原理相同：
- Python: `cursor.execute("SELECT ... WHERE name = %s", (value,))`
- Java: `PreparedStatement ps = conn.prepareStatement("SELECT ... WHERE name = ?"); ps.setString(1, value);`
- Go: `db.Query("SELECT ... WHERE name = ?", value)`
- PHP: `$stmt = $pdo->prepare("SELECT ... WHERE name = ?"); $stmt->execute([$value]);`

## 怎么用

```sql
-- MySQL 原生的预处理语句（参数化查询在数据库层的实现）
PREPARE stmt FROM 'SELECT * FROM user WHERE name = ?';
SET @name = 'test';
EXECUTE stmt USING @name;
DEALLOCATE PREPARE stmt;
```

### 其他防护层

1. **输入验证**：对输入做白名单校验——如果是数字就验证是数字，是邮箱就验证格式
2. **最小权限**：应用账户不给 DROP、ALTER 等权限——即使被注入造成的影响也有限
3. **使用 ORM**：现代 ORM（SQLAlchemy、Hibernate）默认使用参数化查询
4. **WAF（Web Application Firewall）**：在应用前面加一层过滤，拦截常见的注入攻击

## 注意事项

1. **ORM 不是银弹**——ORM 的原生 SQL 方法（`raw()`、`execute()`）仍然可能拼接用户输入。
2. **LIKE 查询也需要参数化**：`cursor.execute("SELECT * FROM user WHERE name LIKE %s", (f"%{user_input}%",))`——注意 `%` 在参数值中不需要转义。
3. **ORDER BY / GROUP BY 不能参数化**——这些是 SQL 关键字，不是值。需要白名单验证（只允许传入预期的列名）。
4. **表名、列名不能参数化**：如果业务需要动态表名/列名，用白名单验证——只允许传入预定义的合法值。

## 和什么有关

- [用户与权限管理](../user-privileges/) —— 最小权限限制注入危害
- [SSL/TLS 加密连接](../ssl/) —— 传输层安全
