# 代码示例

## 示例 1：违反 1NF

**场景**：一个字段存多个值。

```sql
-- ❌ 违反 1NF：hobbies 字段里存了逗号分隔列表
CREATE TABLE student_bad (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    hobbies VARCHAR(200)  -- "篮球,编程,音乐"
);

-- 查询"喜欢编程的学生"有多痛苦：
SELECT * FROM student_bad WHERE hobbies LIKE '%编程%';
-- 慢、不能走索引、可能有假匹配（"编程马拉松"也被匹配）

-- ✅ 符合 1NF：拆成两张表
CREATE TABLE student (
    id INT PRIMARY KEY,
    name VARCHAR(50)
);
CREATE TABLE student_hobby (
    student_id INT,
    hobby VARCHAR(50),
    PRIMARY KEY (student_id, hobby)
);
-- 查起来清楚多了：SELECT * FROM student_hobby WHERE hobby = '编程';
```

## 示例 2：违反 2NF → 修正

**场景**：联合主键，但有的列只依赖其中一部分。

```sql
-- ❌ 违反 2NF：student_name 只依赖 student_id，不依赖 course_id
CREATE TABLE score_bad (
    student_id INT,
    course_id INT,
    student_name VARCHAR(50),  -- 问题
    course_name VARCHAR(100),  -- 问题
    score INT,
    PRIMARY KEY (student_id, course_id)
);

-- ✅ 修正：拆表
-- student 表（主键是 student_id 就够了）
-- course 表（主键是 course_id 就够了）
-- score 表（只有 score 同时依赖两个主键）
CREATE TABLE score (
    student_id INT,
    course_id INT,
    score INT,
    PRIMARY KEY (student_id, course_id)
);
```

## 示例 3：违反 3NF → 修正

**场景**：非主键列依赖另一个非主键列。

```sql
-- ❌ 违反 3NF：city_name 依赖 city_id（非主键），不是直接依赖主键
CREATE TABLE employee_bad (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    city_id INT,
    city_name VARCHAR(50)  -- 通过 city_id 就能查到，冗余了
);

-- ✅ 符合 3NF：
CREATE TABLE city (
    id INT PRIMARY KEY,
    name VARCHAR(50)
);
CREATE TABLE employee (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    city_id INT,
    FOREIGN KEY (city_id) REFERENCES city(id)
);
```

## 示例 4：反范式化的权衡

```sql
-- 场景：订单列表页每秒查询 1000 次，每次都 JOIN 用户表查用户名

-- 3NF（纯规范）：JOIN 查询
SELECT o.id, o.amount, u.username
FROM orders o JOIN user u ON o.user_id = u.id
ORDER BY o.created_at DESC LIMIT 20;

-- 反范式化（以空间换时间）：
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    username VARCHAR(50) NOT NULL,  -- 冗余！但省了一次 JOIN
    amount DECIMAL(10,2),
    created_at DATETIME
);
-- 代价：用户改名时，需要 UPDATE orders SET username = 新名字 WHERE user_id = ?
-- 判断：查询频率 >> 改名频率 → 值得
```
