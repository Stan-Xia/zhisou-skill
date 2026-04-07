---
name: baidu-ai-search
description: 百度AI搜索，集成深度搜索、百科查询、热榜获取等能力。用于网络信息检索、实时资讯、知识查询。
metadata: { "openclaw": { "emoji": "🔍︎",  "requires": { "bins": ["python3"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# 智搜 (ZhiSou)

百度 AI 搜索（BDSE）技能，提供智能搜索、百科查询、热榜获取等功能。

## 快速开始

### 推荐方式：智能调度器（自动选最优 API）

```bash
# 自动选择最佳 API（推荐）
python3 skills/zhisou/scripts/smart_search.py '<搜索关键词>'

# 示例
python3 skills/zhisou/scripts/smart_search.py '最新科技新闻'
python3 skills/zhisou/scripts/smart_search.py '量子计算是什么'
```

### 强制使用指定 API

```bash
python3 smart_search.py '<query>' --force chat_completions   # 深度智能搜索
python3 smart_search.py '<query>' --force smart_search_pro   # 高性能版
python3 smart_search.py '<query>' --force smart_search       # 普通搜索
python3 smart_search.py '<query>' --force baike_content       # 百科详情
python3 smart_search.py '<query>' --force baike_search        # 百科搜索
python3 smart_search.py '<query>' --force zhihu               # 知乎热榜
python3 smart_search.py '<query>' --force weibo               # 微博热榜
python3 smart_search.py '<query>' --force xhs                # 小红书热榜
python3 smart_search.py '<query>' --force bilibili           # B站热榜
```

## API 完整列表

### 搜索类

| API | 端点 | 配额/天 | 说明 |
|-----|------|---------|------|
| **chat_completions** | `/v2/ai_search/chat/completions` | 100 | 最强深度搜索，AI 总结+引用 |
| **web_summary** | `/v2/ai_search/web_summary` | 100 | 高性能版 AI 总结 |
| **web_search** | `/v2/ai_search/web_search` | 50 | 普通搜索结果列表 |

### 百科类

| API | 端点 | 配额/天 | 说明 |
|-----|------|---------|------|
| **baike_content** | `/v2/baike/lemma/get_content` | 50 | 词条详情（刘德华） |
| **baike_search** | `/v2/baike/lemma/get_list_by_title` | 50 | 词条搜索（刘德华→多条结果） |

### 热榜类

| API | type | 配额/天 | 说明 |
|-----|------|---------|------|
| **weibo** | 2 | 1 | 微博热榜 |
| **toutiao** | 3 | 1 | 头条热榜 |
| **zhihu** | 7 | 1 | 知乎热榜 |
| **douyin** | 6 | 1 | 抖音热榜 |
| **bilibili** | 8 | 1 | B站热榜 |
| **baidu** | 4 | 1 | 百度热榜 |
| **tieba** | 9 | 1 | 贴吧热议榜 |
| **kuaishou** | 10 | 1 | 快手热榜 |
| **xhs** | 14 | 1 | 小红书热榜 |

## 调度优先级

```
1. chat_completions (100次/天) ← 最强深度搜索
2. web_summary (100次/天)      ← 高性能版 AI 总结
3. web_search (50次/天)       ← 普通搜索结果
4. 兜底
```

调度器会自动按优先级尝试，直到成功或全部失败。

## 热榜查询（独立脚本）

### 通用热榜
```bash
python3 skills/zhisou/scripts/trending.py <platform>
# 平台: douyin, weibo, zhihu, bilibili, xhs, baidu, kuaishou, toutiao, tieba
```

### 垂类热榜（每天8次）
```bash
python3 skills/zhisou/scripts/trending.py vertical <category> [platform]
# 示例: python3 trending.py vertical 汽车
```

### 百度热搜（每天10次）
```bash
# 默认民生
python3 skills/zhisou/scripts/trending.py baidu

# 指定分类
python3 skills/zhisou/scripts/trending.py baidu livelihood   # 民生
python3 skills/zhisou/scripts/trending.py baidu finance      # 财经
python3 skills/zhisou/scripts/trending.py baidu tech       # 科技
# 其他: society, entertainment, sports, food, car, game, edu
```

## 配额管理

| 类型 | 每日限额 | 说明 |
|------|----------|------|
| 深度智能搜索 | 100次 | 最强 AI 总结 |
| 高性能版 | 100次 | AI 总结 |
| 普通搜索 | 50次 | 搜索结果列表 |
| 百度百科 | 50次 | 词条详情/搜索 |
| 通用热榜 | 每平台1次 | 9个平台 |
| 垂类热榜 | 8次 | 超出收费1元/次 |
| 百度热搜 | 10次 | 民生/财经/科技... |

## 使用方法

### 安装

```bash
# 方式一：直接克隆
git clone https://github.com/Stan-Xia/zhisou-skill.git
cd zhisou-skill

# 方式二：下载 ZIP
# 下载 https://github.com/Stan-Xia/zhisou-skill/raw/main/zhisou-skill.zip
# 解压后放入 skills 目录
```

### 配置凭证

**必需环境变量**：`BAIDU_API_KEY`

获取方式：
1. 访问 https://console.bce.baidu.com/qianfan/overview
2. 创建应用，获取 API Key
3. 设置环境变量：

```bash
# Linux/Mac
export BAIDU_API_KEY="你的API Key"

# Windows
set BAIDU_API_KEY=你的API Key

# 或者在调用时传入
python3 scripts/smart_search.py '关键词' --api-key 你的API Key
```

### 基本使用

```bash
# 智能搜索（自动选最优 API）
python3 scripts/smart_search.py '搜索内容'

# 指定搜索
python3 scripts/smart_search.py '搜索内容' --force chat_completions

# 查询热榜
python3 scripts/trending.py weibo
python3 scripts/trending.py bilibili
```

---

## 注意事项

### ⚠️ 重要提醒

1. **凭证安全**
   - `BAIDU_API_KEY` 是你的百度账号凭证，**不要上传到公开仓库**
   - 已上传的仓库会自动忽略包含 key 的文件
   - 使用时通过环境变量传入，不要硬编码

2. **配额限制**
   - 搜索类 API 每日限额用完后会**自动失败**
   - 热榜每天**共 8 次**（不是每个平台 8 次）
   - 超出配额可能产生额外费用

3. **调度器行为**
   - 自动按优先级尝试：`chat_completions → web_summary → web_search`
   - 如果某 API 失败，会自动切换下一个
   - 全部失败才返回错误

4. **性能考虑**
   - 大关键词搜索可能返回较多结果，耗时较长
   - 建议配合 OpenClaw 的异步执行

### 故障排查

| 问题 | 解决方案 |
|------|----------|
| 提示 "API Key 无效" | 检查 `BAIDU_API_KEY` 是否正确设置 |
| 提示 "配额不足" | 等待第二天配额重置，或更换 API Key |
| 返回空结果 | 检查关键词是否正确，尝试简化搜索词 |
| 网络超时 | 检查服务器网络连接 |

---

## Current Status

Fully functional. 智能调度器 v2.0 已集成全部百度 API。