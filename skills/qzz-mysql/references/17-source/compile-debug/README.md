# 编译与调试

> 把 MySQL 源码编译成可执行文件，用 GDB 打断点——看代码在真实数据上怎么跑。

## 为什么需要它

看源码只能看到"静态代码"，编译+调试能让你看到"代码怎么运行"——Buffer Pool 里有哪些页、B+Tree 分裂时 key 怎么分布、事务提交时锁怎么释放。这是从"看懂设计"到"理解实现"的最后一公里。

## 它是什么

从源码编译 MySQL 分为两步：
1. **CMake 配置**：设置编译选项（Debug/Release、安装路径、启用哪些功能）
2. **make 编译**：编译生成可执行文件

编译后用 GDB 附加到 mysqld 进程，在感兴趣的源码位置打断点，观察运行时状态。

## 怎么工作

### CMake 关键选项

| 选项 | 含义 | 建议 |
|------|------|------|
| `CMAKE_BUILD_TYPE` | Debug / Release | 学习用 Debug（方便调试） |
| `CMAKE_INSTALL_PREFIX` | 安装路径 | 不要覆盖系统 MySQL |
| `WITH_DEBUG` | 启用调试代码 | ON |
| `DOWNLOAD_BOOST` | 自动下载 Boost | ON（否则手动指定） |
| `WITH_ASAN` | 启用 AddressSanitizer | ON（检测内存问题） |

### GDB 调试要点

```bash
# 启动 MySQL 后附加到进程
gdb -p $(pgrep mysqld)

# 或在 GDB 中启动
gdb --args mysqld --datadir=/path/to/data

# 常用 GDB 命令
(gdb) b row_search_mvcc              # 在函数入口打断点
(gdb) b buf_page_get_gen             # 追踪 Buffer Pool 访问
(gdb) c                              # 继续执行
(gdb) p buf_pool->n_pend_reads       # 打印变量值
(gdb) bt                             # 查看调用栈
(gdb) info threads                   # 查看所有线程
```

## 怎么用

```bash
# 1. 安装依赖（Ubuntu/Debian）
apt-get install -y build-essential cmake libncurses5-dev \
  libssl-dev libaio-dev bison pkg-config

# 2. 克隆并编译
git clone https://github.com/mysql/mysql-server.git
cd mysql-server
mkdir build && cd build

# 3. CMake 配置（Debug 模式）
cmake .. \
  -DCMAKE_BUILD_TYPE=Debug \
  -DWITH_DEBUG=1 \
  -DDOWNLOAD_BOOST=1 \
  -DWITH_BOOST=/tmp/boost \
  -DCMAKE_INSTALL_PREFIX=$HOME/mysql-debug

# 4. 编译（用多核加速）
make -j$(nproc)

# 5. 初始化并启动
make install
cd $HOME/mysql-debug
bin/mysqld --initialize-insecure --datadir=data
bin/mysqld --datadir=data --port=3307 &

# 6. 用 GDB 附加调试
gdb -p $(pgrep -n mysqld)
# (gdb) b row_search_mvcc
# (gdb) c
# 在另一个终端执行 SQL 触发断点
```

## 注意事项

1. **编译很耗时**——首次编译需要 20-60 分钟（取决于机器配置）。后续增量编译快很多。
2. **不要覆盖系统 MySQL**——用 `CMAKE_INSTALL_PREFIX` 指定独立路径，用 `--port` 指定非默认端口。
3. **Debug 版比 Release 版慢很多**——Debug 禁用了大量优化，仅用于学习。不要用于性能测试。
4. **内存需求**——编译 MySQL 需要至少 8GB 内存（链接阶段消耗很大）。虚拟机请分配足够内存。

## 和什么有关

- [MySQL 源码结构](../source-structure/) —— 编译前先了解目录结构
- [InnoDB 源码导读](../innodb-source/) —— 调试 InnoDB 的关键函数
