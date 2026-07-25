# 命名规范

> 名字起得好，代码读起来像文章；名字起得烂，三个月后自己都看不懂。

## 为什么需要它

没有统一的命名规范时：
- 有的表叫 `user`，有的叫 `users`，有的叫 `t_user`，有的叫 `UserInfo`
- 有的字段叫 `create_time`，有的叫 `created_at`，有的叫 `crt_tm`
- 同一个项目里看到十几种风格——新人不敢改、老人骂着改

命名规范不是为了"好看"，是为了**团队协作**和**长期维护**。数据库通常活得比任何应用代码都长。

## 它是什么

一套统一的命名规则，涵盖表名、字段名、索引名、约束名。下面是业界常用的一套规范：

### 表名

```
✅ user           -- 单数名词，小写
✅ user_order     -- 下划线分隔
✅ order_item     -- 多对多中间表

❌ users          -- 不要混用单复数
❌ UserInfo       -- 不要驼峰
❌ t_user         -- 不要加前缀
❌ _order         -- 不要下划线开头
```

### 字段名

```
✅ user_id        -- 外键：表名_主键
✅ created_at     -- 时间字段：动词_介词
✅ is_active      -- 布尔字段：is_xxx
✅ sort_order     -- 排序字段

❌ uid            -- 不要缩写（user_id 比 uid 清晰）
❌ time           -- 不要用保留字
❌ user_name_ID   -- 不要混用大小写
```

### 索引名

```
✅ idx_user_status (user_id, status)   -- idx_表名_字段1_字段2（联合索引按顺序连接字段名）
✅ idx_user_email (email)              -- idx_表名_字段名（单列索引）
✅ uk_email (email)                    -- uk_字段名（唯一索引）
✅ fk_order_user (user_id)             -- fk_表名_关联表（外键）
```

### 为什么要这些规则

- **小写 + 下划线**：MySQL 在 Windows 上表名不区分大小写，在 Linux 上区分。全小写避免跨平台坑。
- **不用前缀**：`t_` 或 `tbl_` 是 C 语言的遗产，现代 ORM 不需要。
- **外键命名**：`user_id` 一看就知道关联的是 `user` 表的 `id`。缩写 `uid` 还需要查文档。

## 怎么用

```sql
-- 建表时遵循规范
CREATE TABLE user_order (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
    user_id BIGINT UNSIGNED NOT NULL COMMENT '用户 ID',
    order_no CHAR(20) NOT NULL COMMENT '订单号',
    total_amount DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '总金额',
    status TINYINT NOT NULL DEFAULT 0 COMMENT '状态：0待支付 1已支付 2已取消',
    is_deleted TINYINT NOT NULL DEFAULT 0 COMMENT '软删除标记',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    UNIQUE KEY uk_order_no (order_no),
    INDEX idx_user_status (user_id, status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户订单表';
```

几个值得注意的细节：
- **主键用 BIGINT UNSIGNED**：不是每个表都要，但增长型主键用 BIGINT 避免溢出
- **NOT NULL + DEFAULT**：除非确实需要存 NULL，否则给默认值
- **COMMENT 写注释**：告诉后人每个字段的含义，特别是枚举值的含义
- **utf8mb4**：不要用 utf8（MySQL 的 utf8 是阉割版，不支持 emoji），utf8mb4 才是完整的 UTF-8

## 注意事项

1. **不用 MySQL 保留字做表名/字段名**：`order`、`group`、`key`、`status` 都是保留字。如果不确定，用反引号包一下。
2. **字段长度不要过度大方**：`VARCHAR(1000)` 影响索引效率，够用就行。实际上 `VARCHAR(255)` 是 InnoDB 的一个性能分界线。
3. **统一字符集和排序规则**：数据库、表、字段都用 `utf8mb4` + `utf8mb4_unicode_ci`，避免 JOIN 时字符集不匹配的坑。

## 和什么有关

- [表创建](../../02-ddl/create-table/) —— 命名规范最终体现在建表语句中
- [ER 模型](../er-model/) —— 实体名就是表名
- [范式设计](../normalization/) —— 好的命名 + 好的范式 = 好的设计
