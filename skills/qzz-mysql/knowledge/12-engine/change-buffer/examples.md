# 代码示例

## 示例 1：查看 Change Buffer 使用情况

```sql
SHOW ENGINE INNODB STATUS\G
```sql

找到这部分输出：

```text
-------------------------------------
INSERT BUFFER AND ADAPTIVE HASH INDEX
-------------------------------------
Ibuf: size 1, free list len 0, seg size 2, 1234 merges
merged operations:
 insert 3456, delete mark 789, delete 12
discarded operations:
 insert 0, delete mark 0, delete 0
```sql

**解读**：
- `size 1`：当前 Change Buffer 占用了 1 个页
- `1234 merges`：合并操作执行了 1234 次
- `merged operations insert 3456`：合并了 3456 条 INSERT 操作
- 合并次数高 → Change Buffer 在积极工作，写入后数据正在被访问
- `discarded operations` 全 0 → 没有因为 Change Buffer 满而丢弃操作（健康）

## 示例 2：配置 Change Buffer

```sql
-- 查看当前配置
SHOW VARIABLES LIKE 'innodb_change_buffering';
SHOW VARIABLES LIKE 'innodb_change_buffer_max_size';

-- 写入密集型场景：最大化 Change Buffer
SET GLOBAL innodb_change_buffering = 'all';
SET GLOBAL innodb_change_buffer_max_size = 50;  -- 占 Buffer Pool 50%

-- 只读 / SSD 场景：减少 Change Buffer（收益不大）
SET GLOBAL innodb_change_buffering = 'inserts';
SET GLOBAL innodb_change_buffer_max_size = 10;

-- 开发环境：也可以直接关闭（问题定位时排除干扰）
SET GLOBAL innodb_change_buffering = 'none';
```sql

## 示例 3：验证 Change Buffer 对写入的提升

```sql
-- 创建测试表（有多个二级索引，都是非唯一的）
CREATE TABLE test_cb (
    id INT PRIMARY KEY AUTO_INCREMENT,
    col1 INT NOT NULL,
    col2 INT NOT NULL,
    col3 VARCHAR(100),
    INDEX idx_col1 (col1),
    INDEX idx_col2 (col2),
    INDEX idx_col3 (col3)
) ENGINE=InnoDB;

-- 关闭 Change Buffer
SET GLOBAL innodb_change_buffering = 'none';

-- 插入 10 万行（记录耗时）
-- 这里会慢，因为每个 INSERT 都要更新 3 个二级索引的随机位置

-- 重新开启
SET GLOBAL innodb_change_buffering = 'all';
TRUNCATE TABLE test_cb;

-- 再次插入 10 万行（对比耗时）
-- 第二次应该明显更快，因为二级索引修改被 Change Buffer 缓存了
```sql

## 示例 4：监控 Change Buffer 合并

```sql
-- 查看 Change Buffer 的大小和使用量
SELECT name, count, status FROM information_schema.innodb_metrics
WHERE name LIKE '%change_buffer%'
ORDER BY name;

-- 关键指标：
-- buffer_size：当前 Change Buffer 大小
-- buffer_pages_index：索引页
-- merges：合并次数
-- merges_size：合并的总大小
```
