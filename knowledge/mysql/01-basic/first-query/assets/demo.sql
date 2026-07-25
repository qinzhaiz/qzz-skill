-- demo.sql：第一次查询的完整流程
-- 在 mysql> 下执行：SOURCE demo.sql

CREATE DATABASE IF NOT EXISTS mysql_practice CHARACTER SET utf8mb4;
USE mysql_practice;

CREATE TABLE IF NOT EXISTS user (
    id         INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name       VARCHAR(32)  NOT NULL DEFAULT '' COMMENT '姓名',
    city       VARCHAR(20)  NOT NULL DEFAULT '' COMMENT '城市',
    age        TINYINT UNSIGNED NOT NULL DEFAULT 0  COMMENT '年龄',
    mobile     VARCHAR(20)  NOT NULL DEFAULT '' COMMENT '手机号',
    created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

INSERT INTO user (name, city, age, mobile) VALUES
('张三', '北京', 22, '13800001111'),
('李四', '上海', 25, '13900002222'),
('王五', '深圳', 21, '13700003333');

SELECT * FROM user;

SELECT name, city FROM user WHERE age > 22;
