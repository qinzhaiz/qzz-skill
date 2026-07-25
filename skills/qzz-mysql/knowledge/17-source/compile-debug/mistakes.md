# 常见错误

## 错误 1：编译失败——Boost 下载超时

**症状**：CMake 配置阶段报错 `Could NOT find Boost` 或下载超时。

**原因**：CMake 默认从 SourceForge 下载 Boost，国内网络可能很慢或连不上。

**怎么修**：(1) 用 `-DDOWNLOAD_BOOST=0` 跳过自动下载，手动下载 boost_1_77_0.tar.gz 放到指定目录，(2) 用代理，(3) 用包管理器安装 `libboost-all-dev`（但版本可能不匹配）。

## 错误 2：用 Debug 版做性能测试

**症状**：编译了 Debug 版本，用 sysbench 跑了 TPS 只有 500——"MySQL 怎么这么慢"。

**原因**：Debug 版关掉了编译器优化（-O0），增加了大量 runtime 断言和调试检查。Release 版的 TPS 可能是 Debug 版的 5-10 倍。

**怎么修**：学习和调试用 Debug，性能测试用 Release（`-DCMAKE_BUILD_TYPE=Release`）。不要用 Debug 版的数据判断 MySQL 的实际性能。

## 错误 3：覆盖系统 MySQL

**症状**：`make install` 后系统的 MySQL 被替换了，原来的数据和配置不可用。

**原因**：`CMAKE_INSTALL_PREFIX` 没设，默认安装到 /usr/local/mysql，覆盖了原有的 MySQL。

**怎么修**：始终设置 `CMAKE_INSTALL_PREFIX` 指向独立目录（如 `$HOME/mysql-debug`）。用 `--port` 启动非默认端口避免和系统 MySQL 冲突。
