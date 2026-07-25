-- demo.sql：主键、外键、UNIQUE、NOT NULL、DEFAULT
-- 需要先 CREATE DATABASE test_constraints; USE test_constraints;

-- 父表：用户
CREATE TABLE user (
    id   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(32) NOT NULL
);

-- 子表：订单（含外键约束）
CREATE TABLE orders (
    id      INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    amount  DECIMAL(10,2) NOT NULL,
    status  TINYINT NOT NULL DEFAULT 1 COMMENT '1待支付 2已支付',
    FOREIGN KEY (user_id) REFERENCES user(id)
);

DESC orders;

-- 插入正常数据
INSERT INTO user VALUES (1, '张三');
INSERT INTO orders (user_id, amount) VALUES (1, 100.00);

-- 尝试插入不存在的用户 → 外键约束拒绝
-- INSERT INTO orders (user_id, amount) VALUES (999, 100.00);
