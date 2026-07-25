# 代码示例

## 示例 1：建一张最简的表

```sql
CREATE TABLE IF NOT EXISTS book (
    id     INT UNSIGNED NOT NULL AUTO_INCREMENT,
    title  VARCHAR(100) NOT NULL DEFAULT '' COMMENT '书名',
    author VARCHAR(50)  NOT NULL DEFAULT '' COMMENT '作者',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

三列：id（主键、自增）、title（最长 100 字符）、author（最长 50 字符）。

## 示例 2：查看表结构

```sql
DESC book;
```

输出：

```
+--------+--------------+------+-----+---------+----------------+
| Field  | Type         | Null | Key | Default | Extra          |
+--------+--------------+------+-----+---------+----------------+
| id     | int unsigned | NO   | PRI | NULL    | auto_increment |
| title  | varchar(100) | NO   |     |         |                |
| author | varchar(50)  | NO   |     |         |                |
+--------+--------------+------+-----+---------+----------------+
```

| 列 | 含义 |
|----|------|
| Field | 列名 |
| Type | 数据类型 |
| Null | NO = 不允许为空 |
| Key | PRI = 主键 |
| Default | 默认值 |
| Extra | 额外信息（auto_increment 等） |

## 示例 3：查看建表语句

```sql
SHOW CREATE TABLE book\G
```

注意 `\G` 替代 `;` 可以让输出纵向展示，更好读。这条命令显示完整的建表 SQL——包括你建表后 MySQL 补充的默认值。迁移数据库时靠它导出表结构。
