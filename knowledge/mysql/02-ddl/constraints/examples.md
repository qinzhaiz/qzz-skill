# 代码示例

## 示例 1：NOT NULL + DEFAULT 组合

```sql
CREATE TABLE post (
    id      INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title   VARCHAR(100) NOT NULL,
    views   INT UNSIGNED NOT NULL DEFAULT 0,
    status  TINYINT NOT NULL DEFAULT 1
);

-- 不指定 views 和 status
INSERT INTO post (title) VALUES ('Hello World');
-- 实际插入：title='Hello World', views=0, status=1
```

## 示例 2：UNIQUE 约束

```sql
CREATE TABLE account (
    id    INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20)  NOT NULL UNIQUE
);

INSERT INTO account (email, phone) VALUES ('a@test.com', '13800001111');
-- ✅ 成功

INSERT INTO account (email, phone) VALUES ('a@test.com', '13900002222');
-- ❌ Duplicate entry 'a@test.com' for key 'email'
```

## 示例 3：外键保护

```sql
CREATE TABLE user (
    id   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(32) NOT NULL
);

CREATE TABLE orders (
    id      INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    amount  DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- user 表里没有 id=999 的用户
INSERT INTO orders (user_id, amount) VALUES (999, 100.00);
-- ❌ Cannot add or update a child row: a foreign key constraint fails
```

外键拦住了脏数据——这是数据库层面的最后一道防线。
