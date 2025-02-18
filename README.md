# Milvus Data Exporter 🚀

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Milvus](https://img.shields.io/badge/Milvus-2.x%2B-orange)
![License](https://img.shields.io/badge/License-MIT-green)

一个高效可靠的Milvus数据导出工具，支持将集合数据批量导出为结构化JSON文件，并提供灵活的内存管理策略。

---

## 功能特性 ✨

- **一键导出** - 自动连接Milvus并导出所有集合数据
- **字段过滤** - 支持排除敏感或大字段（如向量`content_vector`）
- **内存友好** - 可配置是否在导出后卸载集合（`auto_release`参数）
- **分页查询** - 自动处理分页逻辑，支持大规模数据导出
- **智能类型转换** 
  - 自动转换numpy数组为Python列表
  - 二进制字段标注（`BINARY_DATA(...)`）
- **错误恢复** - 内置断点续传机制（通过offset实现）

---

## 快速开始 🚀

### 安装依赖
```bash
pip install pymilvus python-dotenv
