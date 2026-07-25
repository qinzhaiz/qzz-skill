-- demo.sql：窗口函数示例
-- 需要先建 employee 表

CREATE TABLE IF NOT EXISTS employee (
    id         INT UNSIGNED PRIMARY KEY,
    name       VARCHAR(32),
    department VARCHAR(20),
    salary     DECIMAL(10,2)
);

INSERT IGNORE INTO employee VALUES
(1, '张三', '技术', 15000),
(2, '李四', '技术', 18000),
(3, '王五', '技术', 15000),
(4, '赵六', '销售', 12000),
(5, '孙七', '销售', 20000);

-- 全局排名
SELECT name, department, salary,
  ROW_NUMBER() OVER (ORDER BY salary DESC) AS rn,
  RANK()       OVER (ORDER BY salary DESC) AS rk,
  DENSE_RANK() OVER (ORDER BY salary DESC) AS dr
FROM employee;

-- 部门内排名
SELECT name, department, salary,
  RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employee;

-- 和 GROUP BY 的对比
SELECT department, SUM(salary) AS total FROM employee GROUP BY department;
