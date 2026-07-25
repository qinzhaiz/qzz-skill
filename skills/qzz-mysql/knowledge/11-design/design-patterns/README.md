# 常见设计模式

> 这些场景每个开发者都会遇到——已经有了成熟的建表方案，不用重复发明轮子。

## 为什么需要它

普通的用户表、订单表，按范式建就行了。但有些场景比较特殊——比如"无限层级的部门树"、"商品的不同属性（书的作者 vs 手机的内存）"、"删了但还要能恢复的数据"。这些场景有专门的设计模式，不必自己从头摸索。

## 五种常见模式

### 1. 邻接表（树形结构）

**场景**：部门层级、商品分类、评论嵌套。一条记录有一个父节点。

```sql
CREATE TABLE category (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    parent_id INT,  -- 指向父节点
    FOREIGN KEY (parent_id) REFERENCES category(id)
);
```bash

- ✅ 简单易懂，修改单个节点的父关系很容易
- ❌ 查所有子节点需要递归（MySQL 8.0 支持 CTE 递归查询）

### 2. 多态关联

**场景**：评论可以属于文章，也可以属于视频，也可以属于图片——同一个评论表关联多种不同类型的"被评论对象"。

```sql
CREATE TABLE comment (
    id INT PRIMARY KEY,
    content TEXT,
    target_type VARCHAR(20) NOT NULL,  -- 'article', 'video', 'photo'
    target_id INT NOT NULL,
    INDEX idx_target (target_type, target_id)
);
```sql

- ✅ 灵活——加新类型不需要改表
- ❌ 不能用外键约束（因为引用的表不固定），需要应用层保证数据完整性

### 3. 软删除

**场景**：用户"删除"了数据，但实际上需要保留记录（数据恢复、审计要求）。

```sql
CREATE TABLE user (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    is_deleted TINYINT NOT NULL DEFAULT 0,  -- 0正常 1已删除
    deleted_at DATETIME,                     -- 删除时间
    INDEX idx_is_deleted (is_deleted)
);

-- 所有查询都要加上 is_deleted = 0
SELECT * FROM user WHERE is_deleted = 0;
```bash

- ✅ 数据可恢复，删错了能找回
- ❌ 所有查询都要记得加 `is_deleted = 0`（建议用视图封装）
- ❌ 唯一索引要包含 `is_deleted` 或者用部分索引（MySQL 不支持，需要变通方案）

### 4. 审计日志

**场景**：需要追踪"谁在什么时候把什么字段从什么值改成了什么值"。

```sql
CREATE TABLE audit_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    table_name VARCHAR(50) NOT NULL,   -- 哪个表
    record_id BIGINT NOT NULL,          -- 哪条记录
    action VARCHAR(10) NOT NULL,        -- INSERT / UPDATE / DELETE
    changed_by VARCHAR(50),             -- 谁改的
    old_value JSON,                     -- 改之前的值
    new_value JSON,                     -- 改之后的值
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_table_record (table_name, record_id),
    INDEX idx_changed_at (changed_at)
);
```sql

- ✅ 完整的数据变更历史，可以查出任何时间点的数据
- ❌ 日志表增长很快，需要定期归档

### 5. EAV 模式（实体-属性-值）

**场景**：商品的不同类别有完全不同的属性——书的属性是"作者、ISBN、页数"，手机的属性是"品牌、内存、屏幕尺寸"。不可能每个类别建一张表。

```sql
-- 只有用在"属性种类极其多样且经常变化"时才用它
CREATE TABLE product_attr (
    product_id INT,
    attr_name VARCHAR(50),   -- 'color', 'memory', 'author'
    attr_value VARCHAR(200), -- 'red', '256GB', '张三'
    PRIMARY KEY (product_id, attr_name)
);
```sql

- ✅ 极其灵活，加新属性不需要改表
- ❌ 查询复杂（需要 PIVOT），无法做数据类型校验，性能差

**警告**：EAV 模式牺牲了太多数据库层面的约束（类型检查、非空检查、外键），大多数情况下**应该避免使用**。优先考虑：JSON 列 > 预留字段 > EAV。

## 怎么用

选择模式时问三个问题：
1. 查询模式是什么？（查子节点、查历史、查多态关联？）
2. 更新频率多高？（经常改 → 邻接表；很少改 → JSON 列）
3. 数据完整性要求多高？（财务 → 避免 EAV；社交评论 → 多态关联可以接受）

## 注意事项

1. **软删除的唯一索引问题**：MySQL 不支持部分索引。如果需要唯一约束 + 软删除，可以用唯一复合索引 `(original_unique_key, is_deleted)`。
2. **多态关联不能加外键**——数据完整性由应用层保证，做好测试。
3. **审计日志是资源大户**——定期归档（比如按月份分表或迁移到 ClickHouse/ES）。
4. **MySQL 8.0 的 JSON 列可以替代 EAV**——对不确定属性用 JSON 字段存，配合虚拟列 + 虚拟列索引做查询。

## 和什么有关

- [ER 模型](../er-model/) —— 这些模式是具体场景的 ER 设计
- [范式设计](../normalization/) —— 有些模式（EAV）是高范式，有些（JSON）是反范式
- [外键约束](../../02-ddl/constraints/) —— 多态关联不能用外键的权衡
- [JSON 数据类型](../../02-ddl/data-types/) —— JSON 列通常比 EAV 更好
