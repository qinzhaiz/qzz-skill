# 代码示例

## 示例 1：完整的建表语句（符合规范）

**场景**：一个规范的用户表。

```sql
CREATE TABLE user (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键 ID',
    username VARCHAR(50) NOT NULL COMMENT '用户名',
    email VARCHAR(100) NOT NULL COMMENT '邮箱',
    password_hash CHAR(60) NOT NULL COMMENT '密码哈希',
    phone VARCHAR(20) NOT NULL DEFAULT '' COMMENT '手机号',
    avatar_url VARCHAR(500) NOT NULL DEFAULT '' COMMENT '头像 URL',
    status TINYINT NOT NULL DEFAULT 1 COMMENT '状态：1正常 0禁用',
    is_deleted TINYINT NOT NULL DEFAULT 0 COMMENT '是否删除：0未删除 1已删除',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    UNIQUE KEY uk_username (username),
    UNIQUE KEY uk_email (email),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';
```

## 示例 2：常见错误对照

```sql
-- ❌ 错误风格（不要这样写！）
CREATE TABLE Users (           -- 大写、复数
    Id INT AUTO_INCREMENT,     -- 驼峰
    UserName VARCHAR(50),      -- 驼峰
    createTime DATETIME,       -- 混用驼峰
    uid INT,                   -- 缩写
    order_id VARCHAR(20),      -- 字段名含保留字（order）
    Flag TINYINT,              -- 不描述含义
    Time DATETIME              -- 保留字
);

-- ✅ 正确风格
CREATE TABLE user (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    creator_id BIGINT UNSIGNED COMMENT '创建人',
    order_id BIGINT UNSIGNED COMMENT '关联订单',
    is_active TINYINT NOT NULL DEFAULT 1,
    event_time DATETIME NOT NULL COMMENT '事件时间',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 示例 3：索引命名规范

```sql
-- 普通索引：idx_表名_字段名
CREATE INDEX idx_user_status ON user(status);
CREATE INDEX idx_user_created_at ON user(created_at);

-- 联合索引：idx_表名_字段1_字段2（按顺序）
CREATE INDEX idx_order_user_status ON user_order(user_id, status);

-- 唯一索引：uk_字段名
CREATE UNIQUE INDEX uk_user_email ON user(email);
ALTER TABLE user ADD UNIQUE KEY uk_phone (phone);

-- 外键：fk_当前表_关联表
ALTER TABLE user_order ADD CONSTRAINT fk_order_user
    FOREIGN KEY (user_id) REFERENCES user(id);

-- 主键：不用起名，或叫 pk_表名
ALTER TABLE user ADD CONSTRAINT pk_user PRIMARY KEY (id);
```
