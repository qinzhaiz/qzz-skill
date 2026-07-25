-- demo.sql：JOIN 三种类型对比
-- 需要先建 user 和 orders 表，插入测试数据

-- 建测试表
CREATE TABLE IF NOT EXISTS user (
    id   INT UNSIGNED PRIMARY KEY,
    name VARCHAR(32) NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id      INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    amount  DECIMAL(10,2) NOT NULL
);

INSERT IGNORE INTO user VALUES (1, '张三'), (2, '李四'), (3, '王五');
INSERT IGNORE INTO orders (user_id, amount) VALUES (1, 100), (1, 200), (3, 300);

-- INNER JOIN：只返回有订单的用户
SELECT u.name, o.amount FROM user u INNER JOIN orders o ON u.id = o.user_id;

-- LEFT JOIN：所有用户（李四无订单显示 NULL）
SELECT u.name, o.amount FROM user u LEFT JOIN orders o ON u.id = o.user_id;
