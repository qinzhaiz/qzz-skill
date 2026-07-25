# 代码示例

## 示例 1：完整编译脚本

```bash
#!/bin/bash
# MySQL 8.0 编译脚本

set -e

INSTALL_DIR="$HOME/mysql-debug"
SOURCE_DIR="$HOME/mysql-server"

# 安装依赖
sudo apt-get install -y \
  build-essential cmake libncurses5-dev \
  libssl-dev libaio-dev bison pkg-config \
  libtirpc-dev

# 配置
cd "$SOURCE_DIR"
mkdir -p build && cd build

cmake .. \
  -DCMAKE_BUILD_TYPE=Debug \
  -DWITH_DEBUG=1 \
  -DDOWNLOAD_BOOST=1 \
  -DWITH_BOOST=/tmp/boost \
  -DCMAKE_INSTALL_PREFIX="$INSTALL_DIR" \
  -DMYSQL_DATADIR="$INSTALL_DIR/data" \
  -DSYSCONFDIR="$INSTALL_DIR/etc" \
  2>&1 | tee cmake.log

# 编译
make -j$(nproc) 2>&1 | tee make.log
make install

# 初始化
cd "$INSTALL_DIR"
bin/mysqld --initialize-insecure --datadir=data

echo "MySQL compiled and installed to $INSTALL_DIR"
echo "Start: $INSTALL_DIR/bin/mysqld --datadir=$INSTALL_DIR/data --port=3307 &"
```

## 示例 2：GDB 调试实战

```bash
# 终端 1：启动 MySQL
$HOME/mysql-debug/bin/mysqld --datadir=$HOME/mysql-debug/data --port=3307

# 终端 2：附加 GDB
gdb -p $(pgrep -n mysqld)

# GDB 中设置断点
(gdb) break row_search_mvcc
Breakpoint 1 at 0x...: file storage/innobase/row/row0sel.cc, line ...

(gdb) continue
Continuing.

# 终端 3：执行查询
mysql -h 127.0.0.1 -P 3307 -u root -e "SELECT * FROM test.t WHERE id = 1"

# GDB 中断在断点处
(gdb) bt                    # 查看调用栈
#0  row_search_mvcc (...) at row0sel.cc
#1  ha_innobase::index_read (...) at ha_innodb.cc
#2  handler::ha_index_read (...) at handler.cc
#3  ...

(gdb) info locals           # 查看局部变量
(gdb) p *prebuilt->index->name  # 查看索引名
(gdb) step                  # 单步执行

(gdb) delete 1              # 删除断点
(gdb) continue              # 继续执行
```

## 示例 3：Debug 模式下查看 InnoDB 内部状态

```sql
-- Debug 编译版本才有的额外功能

-- 查看 Buffer Pool 页面状态（需要 WITH_DEBUG 编译）
-- 在 GDB 中打印
(gdb) p buf_pool->stat.n_pages_total
(gdb) p buf_pool->stat.n_pages_read
(gdb) p buf_pool->LRU.count

-- InnoDB 的 INFORMATION_SCHEMA 扩展表（Debug 版）
-- 这些表只在 Debug 编译时存在
SELECT * FROM INFORMATION_SCHEMA.INNODB_TRX;  -- 事务信息
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKS; -- 锁信息
```
