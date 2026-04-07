# 智搜 (ZhiSou)

百度 AI 搜索技能 for OpenClaw

## 简介

智搜是一个集成百度 AI 搜索能力的 OpenClaw 技能，提供：
- 智能搜索（自动选择最优 API）
- 百科查询
- 热榜获取

## 功能特性

| 功能 | 说明 |
|------|------|
| 深度智能搜索 | AI 总结 + 引用，100次/天 |
| 高性能搜索 | 快速 AI 总结，100次/天 |
| 百科查询 | 词条详情/搜索，50次/天 |
| 热榜获取 | 微博/知乎/抖音/B站等，8次/天 |

## 快速开始

### 1. 安装

```bash
# 方式一：克隆仓库
git clone https://github.com/Stan-Xia/zhisou-skill.git

# 方式二：下载 ZIP
# 从 https://github.com/Stan-Xia/zhisou-skill/raw/main/zhisou-skill.zip 下载
```

### 2. 配置凭证

**必需：百度 API Key**

1. 访问 https://console.bce.baidu.com/qianfan/
2. 创建应用，获取 API Key
3. 设置环境变量：

```bash
export BAIDU_API_KEY="你的API Key"
```

### 3. 使用

```bash
# 智能搜索
python3 scripts/smart_search.py '搜索内容'

# 查询热榜
python3 scripts/trending.py weibo
python3 scripts/trending.py bilibili
```

## 注意事项

1. **凭证安全**：API Key 不要泄露给他人
2. **配额限制**：搜索有每日配额限制，超出可能收费
3. **网络**：需要能访问百度 API

## 技术支持

- GitHub: https://github.com/Stan-Xia/zhisou-skill
- 问题反馈: Issues

## 更新日志

### v1.0.1
- 添加使用方法与注意事项
- 优化文档结构

### v1.0.0
- 初始版本
- 支持智能搜索、百科查询、热榜获取