# 代码示例

## 示例 1：邻接表 + CTE 递归查询

**场景**：查询某个部门及其所有子部门。

```sql
CREATE TABLE department (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id INT,
    FOREIGN KEY (parent_id) REFERENCES department(id)
);

INSERT INTO department VALUES
(1, '总公司', NULL),
(2, '技术部', 1),
(3, '前端组', 2),
(4, '后端组', 2),
(5, '市场部', 1);

-- MySQL 8.0 CTE 递归：查"技术部"及所有子部门
WITH RECURSIVE dept_tree AS (
    -- 起点：技术部
    SELECT id, name, parent_id, 0 AS level
    FROM department WHERE id = 2
    UNION ALL
    -- 递归：找子部门
    SELECT d.id, d.name, d.parent_id, dt.level + 1
    FROM department d
    JOIN dept_tree dt ON d.parent_id = dt.id
)
SELECT * FROM dept_tree;
```

```text
+----+--------+-----------+-------+
| id | name   | parent_id | level |
+----+--------+-----------+-------+
|  2 | 技术部 |         1 |     0 |
|  3 | 前端组 |         2 |     1 |
|  4 | 后端组 |         2 |     1 |
+----+--------+-----------+-------+
```

## 示例 2：软删除的完整用法

```sql
-- 建表
CREATE TABLE article (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    is_deleted TINYINT NOT NULL DEFAULT 0,
    deleted_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_is_deleted (is_deleted)
);

-- 创建视图：（封装 is_deleted 过滤条件）
CREATE VIEW article_active AS
SELECT id, title, content, created_at
FROM article WHERE is_deleted = 0;

-- 业务代码里：用视图查活跃文章
SELECT * FROM article_active WHERE id = 1;

-- "删除"操作：实际上是软删除
UPDATE article SET is_deleted = 1, deleted_at = NOW() WHERE id = 1;

-- 恢复操作：
UPDATE article SET is_deleted = 0, deleted_at = NULL WHERE id = 1;
```

## 示例 3：JSON 列替代传统 EAV

**场景**：商品属性各不相同。

```sql
-- ✅ MySQL 8.0 推荐：JSON 列
CREATE TABLE product (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    attrs JSON,  -- {"author": "张三", "pages": 300} 或 {"brand": "Apple", "memory": "256GB"}
    INDEX idx_category (category)
);

-- 查询所有"256GB 内存"的手机
SELECT * FROM product
WHERE category = 'phone' AND attrs->>'$.memory' = '256GB';
-- 可以用虚拟列 + 索引优化这种查询

-- 添加虚拟列并建索引：
ALTER TABLE product
ADD COLUMN memory VARCHAR(50)
GENERATED ALWAYS AS (attrs->>'$.memory') STORED;
CREATE INDEX idx_memory ON product(memory);
```

## 示例 4：审计日志的触发器实现

```sql
CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100)
);

CREATE TABLE audit_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    table_name VARCHAR(50) NOT NULL,
    record_id BIGINT NOT NULL,
    action VARCHAR(10) NOT NULL,
    changed_by VARCHAR(50),
    old_data JSON,
    new_data JSON,
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 用触发器自动记录 UPDATE 变更
DELIMITER $$
CREATE TRIGGER user_audit_update
AFTER UPDATE ON user FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_id, action, old_data, new_data)
    VALUES ('user', NEW.id, 'UPDATE',
            JSON_OBJECT('username', OLD.username, 'email', OLD.email),
            JSON_OBJECT('username', NEW.username, 'email', NEW.email));
END$$
DELIMITER ;
```
