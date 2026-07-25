# Testing Conventions

## 测试层次

| 层次 | 工具 | 触发 |
|------|------|------|
| 格式校验 | `tools/lint.py` | 每次提交前 |
| 元数据校验 | `tools/metadata.py` | 每次提交前 |
| 目录完整性 | `tools/toc.py` | 发布前 |
| 内容检查清单 | `tests/checklist.md` | 每个概念完成后 |
| 技能端到端测试 | 手动触发 | 发布前 |

## 格式校验（lint.py）

检查项：
- 7 个必须文件是否齐全
- metadata.yaml 字段完整性和类型
- Markdown 链接有效性（相对路径）
- 代码块语言标记是否缺失

## 元数据校验（metadata.py）

检查项：
- `difficulty` 取值是否合法
- `prerequisites` 中的引用路径是否存在
- `updated` 日期格式是否正确
- `topics` 标签数量 ≥ 2

## 检查清单（checklist.md）

每个概念完成后，人工确认：
- [ ] README 200-500 字
- [ ] 代码示例可独立运行
- [ ] 前置概念链接正确
- [ ] 无版权内容
- [ ] 中文正文，技术名词保留英文

## 技能端到端测试

1. 在 Claude Code 中安装技能
2. 用触发关键词激活
3. 验证输出格式和内容质量
4. 用边缘 case 测试约束条件
