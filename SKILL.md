---
name: zhisou
description: 百度AI搜索（智搜），集成深度搜索、百科查询、热榜获取等能力。用于网络信息检索、实时资讯、知识查询。
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

## Current Status

Fully functional. 智能调度器 v2.0 已集成全部百度 API。