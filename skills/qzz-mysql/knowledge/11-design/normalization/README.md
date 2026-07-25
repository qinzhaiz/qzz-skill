# 数据库范式

> 范式是一套规则——用来检查你的表设计有没有冗余和不一致的风险。

## 为什么需要它

不合理的表设计会导致三个问题：
- **插入异常**：想加一个新员工，但还没分配到部门，部门信息没法存（因为员工表里嵌了部门信息）
- **删除异常**：把一个部门的所有员工都删了，这个部门的信息也丢了
- **更新异常**：改了 A 记录的部门电话，B 记录里同一个部门的电话没改——数据不一致

范式就是为了解决这些问题而设计的规则。

## 它是什么

范式从低到高依次是 1NF → 2NF → 3NF → BCNF → 4NF → 5NF。**实际开发中做到 3NF 就够了**。

| 范式 | 解决了什么问题 | 核心规则 |
|------|--------------|---------|
| **1NF** | 字段不可再分 | 每个字段都是原子的（不能存数组、JSON 子对象） |
| **2NF** | 非主键列对主键部分依赖 | 联合主键时，每个非主键列必须依赖**整个**主键（不能只依赖一部分） |
| **3NF** | 非主键列对非主键列依赖 | 非主键列只能依赖主键，**不能依赖其他非主键列** |

记忆口诀：**"每个字段不可分（1NF）、每个字段依赖完整主键（2NF）、每个字段只依赖主键（3NF）"**

## 怎么工作

以一张"学生选课成绩表"为例，逐步拆解：

```sql
-- 原始表：违反了三层范式
CREATE TABLE enrollment_bad (
    student_id INT,
    student_name VARCHAR(50),  -- 只依赖 student_id，不依赖 course_id（违反 2NF）
    course_id INT,
    course_name VARCHAR(100),  -- 只依赖 course_id，不依赖 student_id（违反 2NF）
    teacher_name VARCHAR(50),  -- 依赖 course_id，而 course_id 不是主键（违反 3NF）
    score INT,
    PRIMARY KEY (student_id, course_id)
);
```sql

### 修正到 3NF：

```sql
-- 1. 学生表（消除对主键的部分依赖）
CREATE TABLE student (
    id INT PRIMARY KEY,
    name VARCHAR(50)
);

-- 2. 课程表（消除传递依赖：teacher_name 依赖 course_id）
CREATE TABLE course (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    teacher_id INT  -- 老师也单独建表
);

-- 3. 选课表（只存关系的核心属性：score）
CREATE TABLE enrollment (
    student_id INT,
    course_id INT,
    score INT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (course_id) REFERENCES course(id)
);
```sql

## 怎么用

检查一张表是否符合 3NF：
1. 主键是什么？（复合主键？）
2. 每个非主键列——只改它自己需要改主键吗？（需要 → 可能违反 2NF）
3. 每个非主键列——能不能通过另一个非主键列推导出来？（能 → 违反 3NF）

### 反范式化：什么时候故意不遵守

范式减少冗余，但会导致查询时需要更多 JOIN。当 JOIN 代价大于冗余代价时，可以**故意反范式化**：

```sql
-- 3NF：订单表只存用户 ID，查用户名要 JOIN
SELECT o.*, u.name FROM orders o JOIN user u ON o.user_id = u.id;

-- 反范式化：订单表冗余存用户名（牺牲一致性换查询速度）
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT,
    username VARCHAR(50),  -- 冗余字段，不用 JOIN 就能拿到用户名
    ...
);
```sql

## 注意事项

1. **3NF 是底线，不是目标**——大部分业务表做到 3NF 就够了，不要追求更高范式（查询时 JOIN 灾难）。
2. **反范式化是有代价的**——冗余字段需要业务层保证一致性（改用户名时要同时更新用户表和订单表）。
3. **并不是所有冗余都不好**——当查询频率远高于更新频率时，适量冗余是合理的。

## 和什么有关

- [ER 模型](../er-model/) —— 画完 ER 图后用范式检查
- [常见设计模式](../design-patterns/) —— 具体场景的落地
- [索引策略](../../06-index/when-to-use/) —— 反范式化 + 索引是查询优化的双刃剑
