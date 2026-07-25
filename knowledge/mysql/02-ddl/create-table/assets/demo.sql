-- demo.sql：建表 + 查看结构
-- 需要先 CREATE DATABASE test_ddl; USE test_ddl;

CREATE TABLE IF NOT EXISTS student (
    id      INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name    VARCHAR(32)  NOT NULL DEFAULT '' COMMENT '姓名',
    gender  TINYINT      NOT NULL DEFAULT 0  COMMENT '0未知 1男 2女',
    age     TINYINT UNSIGNED NOT NULL DEFAULT 0,
    city    VARCHAR(20)  NOT NULL DEFAULT '',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DESC student;

SHOW CREATE TABLE student\G
