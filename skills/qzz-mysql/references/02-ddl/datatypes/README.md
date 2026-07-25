# 数据类型

> 数据类型告诉 MySQL：这列存的是数字、字符串、日期还是别的什么。

## 为什么需要它

建表时你不仅要指定每列的**名字**，还必须指定**类型**。比如 `age INT`、`name VARCHAR(32)`。

这不是 MySQL 多此一举——类型决定了一切：
- **怎么存**：数字类型直接存，字符串类型存字符，日期类型存时间戳
- **怎么比较**：`WHERE age > 20` 按数字比大小，`WHERE name > '张三'` 按字典序比
- **占多少空间**：TINYINT 占 1 字节，BIGINT 占 8 字节。选对了能省大量磁盘和内存

原则很简单：**选能存下数据的最小类型。**

## 常用类型速查

### 数字

| 类型 | 占用 | 范围 | 什么时候用 |
|------|------|------|-----------|
| TINYINT | 1B | -128~127 | 年龄、状态码、布尔值 |
| SMALLINT | 2B | ±3 万 | 小范围数量 |
| INT | 4B | ±21 亿 | 主键、大部分计数 |
| BIGINT | 8B | 巨大 | 超大计数、时间戳（毫秒） |
| DECIMAL(M,D) | 变长 | 精确小数 | **金额——永远用它，别用 FLOAT** |
| FLOAT/DOUBLE | 4/8B | 近似值 | 科学计算 |

`UNSIGNED` 可以让正整数范围翻倍（INT UNSIGNED：0~42 亿），适合不会出现负数的列。

### 字符串

| 类型 | 特点 | 什么时候用 |
|------|------|-----------|
| VARCHAR(N) | 变长，省空间 | 绝大多数文本：姓名、标题、地址 |
| CHAR(N) | 定长，少 1B 开销 | 固定长度的值：手机号、MD5、状态码 |
| TEXT | 长文本，不存行内 | 文章内容、简介（**不要对它做索引前缀**） |
| ENUM | 存整数，显示字符串 | 只有几个固定值的列，如性别 |

**VARCHAR(N) 的 N 是字符数，不是字节数。** UTF-8 下 1 个汉字 = 3 字节。VARCHAR(255) 最多 255 个汉字，但可能占 765 字节。

### 日期时间

| 类型 | 范围 | 占用 | 什么时候用 |
|------|------|------|-----------|
| DATE | 1000~9999 | 3B | 生日、日期 |
| TIME | -838~838 小时 | 3B | 时长 |
| DATETIME | 1000~9999 | 8B | 创建时间、订单时间（**推荐**） |
| TIMESTAMP | 1970~2038 | 4B | 自动更新为当前时间（有 2038 问题） |

**TIMESTAMP 只能存到 2038 年。** 新项目直接用 DATETIME，不会有后患。

## 怎么用

```sql
CREATE TABLE product (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL COMMENT '商品名',
    price       DECIMAL(10,2) NOT NULL COMMENT '价格（精确到分）',
    description TEXT COMMENT '商品描述',
    status      TINYINT NOT NULL DEFAULT 1 COMMENT '1上架 0下架',
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
```

### 选型口诀

- **整数**：默认 INT，很小用 TINYINT，很大用 BIGINT
- **小数**：金额用 DECIMAL，科学用 FLOAT
- **字符串**：默认 VARCHAR，定长用 CHAR，长文用 TEXT
- **日期**：默认 DATETIME，自动更新时间用 TIMESTAMP（小心 2038）
- **布尔**：用 TINYINT(1)，不用 BOOLEAN（MySQL 里 BOOLEAN = TINYINT 的别名）

## 注意事项

- **不要用 VARCHAR 当主键。** 太长，二级索引回表开销大。用 INT 或 BIGINT 自增。
- **不要用 FLOAT 存钱。** 0.1 + 0.2 ≠ 0.3，浮点数有精度误差。用 DECIMAL，或者在代码里用"分"当最小单位存整数。
- **VARCHAR 别盲目设超大值。** VARCHAR(255) 没问题，VARCHAR(65535) 会让 MySQL 分配过多内存。实际需要多少就设多少。

## 和什么有关

- [约束](../constraints/) — NOT NULL、DEFAULT 怎么和类型配合
- [05-function/date/](../../05-function/date/) — 日期类型的常用函数
