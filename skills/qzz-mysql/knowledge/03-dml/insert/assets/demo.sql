-- demo.sql：INSERT 各种写法
-- 需要先建表：参考 02-ddl/create-table/assets/demo.sql

-- 单行插入（推荐写法：列出列名）
INSERT INTO student (name, gender, age, city) VALUES ('张三', 1, 22, '北京');

-- 多行插入
INSERT INTO student (name, gender, age, city) VALUES
('李四', 1, 25, '上海'),
('王五', 0, 21, '深圳'),
('赵六', 1, 23, '广州');

-- 查看结果
SELECT * FROM student;
