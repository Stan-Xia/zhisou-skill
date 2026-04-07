#!/usr/bin/env python3
"""
智能搜索调度器 - 根据优先级自动选择最佳 API
优先级：
1. 智能搜索生成 (100次/天) - 默认首选
2. 高性能版智能搜索 (100次/天) - 复杂问题备用
3. 百度百科 (50次/天) - 概念查询
4. 百度搜索 (50次/天) - 传统搜索备用
"""

import sys
import json
import os
import requests


# 配额计数器（实际生产环境应持久化到文件）
QUOTA = {
    "chat_completions": {"limit": 100, "used": 0, "name": "深度智能搜索（chat）"},
    "smart_search_pro": {"limit": 100, "used": 0, "name": "高性能版智能搜索"},
    "smart_search": {"limit": 50, "used": 0, "name": "智能搜索生成"},
    "baike_content": {"limit": 50, "used": 0, "name": "百度百科（详情）"},
    "baike_search": {"limit": 50, "used": 0, "name": "百度百科（搜索）"},
    "baidu_search": {"limit": 50, "used": 0, "name": "百度搜索"},
    # 热榜不纳入调度器，单独处理
}


def get_api_key():
    api_key = os.getenv("BAIDU_API_KEY")
    if not api_key:
        # 尝试从 .env 文件加载
        env_file = os.path.expanduser("~/.openclaw/gateway.env")
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    if line.strip().startswith("BAIDU_API_KEY"):
                        api_key = line.split("=")[1].strip().strip('"')
                        break
    if not api_key:
        raise Exception("BAIDU_API_KEY not set")
    return api_key


def smart_search(query: str, force_api: str = None):
    """
    智能搜索 - 根据优先级自动选择 API
    
    Args:
        query: 搜索关键词
        force_api: 强制使用某个 API (可选)
                  可选值: "smart_search", "smart_search_pro", "baike", "baidu_search"
    """
    api_key = get_api_key()
    
    # 如果指定了强制使用的 API
    if force_api:
        return _call_api(api_key, force_api, query)
    
    # 智能调度：按优先级尝试（深度搜索优先）
    apis_order = ["chat_completions", "smart_search_pro", "smart_search", "baidu_search"]
    
    for api_name in apis_order:
        quota = QUOTA[api_name]
        
        # 检查配额
        if quota["used"] >= quota["limit"]:
            print(f"[调度] {quota['name']} 配额已用完 ({quota['used']}/{quota['limit']})，跳过")
            continue
        
        # 配额低于 10% 时提示可能收费，并切换到下一个 API
        remaining = quota["limit"] - quota["used"]
        if remaining <= quota["limit"] * 0.1:
            print(f"[⚠️ 警告] {quota['name']} 配额剩余 {remaining} 次 (10%)，继续使用可能产生费用，切换到下一个 API...")
            continue
        
        try:
            result = _call_api(api_key, api_name, query)
            QUOTA[api_name]["used"] += 1
            print(f"[调度] 使用 {quota['name']} (已用 {QUOTA[api_name]['used']}/{quota['limit']})")
            return result
        except Exception as e:
            print(f"[调度] {quota['name']} 失败: {e}")
            continue
    
    raise Exception("所有 API 均不可用或配额已用完")


def _call_api(api_key, api_name, query):
    """调用指定的 API"""
    
    if api_name == "chat_completions":
        return _chat_completions(api_key, query)
    elif api_name == "smart_search":
        return _smart_search(api_key, query)
    elif api_name == "smart_search_pro":
        return _smart_search_pro(api_key, query)
    elif api_name == "baidu_search":
        return _baidu_search(api_key, query)
    elif api_name == "baike":
        return _baike_content(api_key, query)
    elif api_name == "baike_search":
        return _baike_search(api_key, query)
    elif api_name in ["zhihu", "bilibili", "weibo", "xhs", "kuaishou"]:
        return _trending(api_key, api_name, query)
    else:
        raise ValueError(f"Unknown API: {api_name}")


def _chat_completions(api_key, query):
    """深度智能搜索（chat/completions）- 最强 API"""
    url = "https://qianfan.baidubce.com/v2/ai_search/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-Appbuilder-From": "openclaw",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [{"content": query, "role": "user"}],
        "stream": False,
        "model": "ernie-4.5-turbo-32k",
        "instruction": "##",
        "enable_corner_markers": True,
        "enable_deep_search": True
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    results = response.json()
    
    if "code" in results:
        raise Exception(results.get("message", "Unknown error"))
    
    choices = results.get("choices", [])
    if choices:
        content = choices[0].get("message", {}).get("content", "")
        # 同时返回 references 供引用
        references = results.get("references", [])
        return {"content": content, "references": references}
    return ""


def _smart_search(api_key, query):
    """智能搜索生成"""
    url = "https://qianfan.baidubce.com/v2/ai_search/web_search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-Appbuilder-From": "openclaw",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [{"content": query, "role": "user"}],
        "edition": "standard",
        "search_source": "baidu_search_v2",
        "resource_type_filter": [{"type": "web", "top_k": 10}],
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    results = response.json()
    
    if "code" in results:
        raise Exception(results.get("message", "Unknown error"))
    
    datas = results.get("references", [])
    # 移除 snippet 字段
    for item in datas:
        item.pop("snippet", None)
    return datas


def _smart_search_pro(api_key, query):
    """高性能版智能搜索生成"""
    url = "https://qianfan.baidubce.com/v2/ai_search/web_summary"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-Appbuilder-From": "openclaw",
        "Content-Type": "application/json"
    }
    payload = {
        "instruction": "你是一个专业、简洁的AI助手，用中文回答用户问题。",
        "messages": [{"role": "user", "content": query}],
        "stream": False,
        "resource_type_filter": [{"type": "web", "top_k": 10}],
        "model": "non_thinking"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    results = response.json()
    
    if "error" in results:
        raise Exception(results["error"].get("message", "Unknown error"))
    
    choices = results.get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return ""


def _baidu_search(api_key, query):
    """传统百度搜索（作为兜底）"""
    # 使用智能搜索的标准模式
    url = "https://qianfan.baidubce.com/v2/ai_search/web_search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "X-Appbuilder-From": "openclaw",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [{"content": query, "role": "user"}],
        "edition": "lite",  # 轻量版
        "search_source": "baidu_search_v2",
        "resource_type_filter": [{"type": "web", "top_k": 10}],
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    results = response.json()
    
    if "code" in results:
        raise Exception(results.get("message", "Unknown error"))
    
    datas = results.get("references", [])
    for item in datas:
        item.pop("snippet", None)
    return datas


def _baike_content(api_key, query):
    """百度百科词条详情 - 专用 API"""
    url = "https://appbuilder.baidu.com/v2/baike/lemma/get_content"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    params = {
        "search_type": "lemmaTitle",
        "search_key": query
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    results = response.json()
    
    if "request_id" not in results:
        raise Exception(f"百度百科查询失败: {results}")
    
    result = results.get("result", {})
    return {
        "lemma_id": result.get("lemma_id"),
        "title": result.get("lemma_title"),
        "description": result.get("lemma_desc"),
        "summary": result.get("summary"),
        "url": result.get("url")
    }


def _baike_search(api_key, query):
    """百度百科词条搜索 - 专用 API"""
    url = "https://appbuilder.baidu.com/v2/baike/lemma/get_list_by_title"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    params = {"lemma_title": query}
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    results = response.json()
    
    if "request_id" not in results:
        raise Exception(f"百度百科搜索失败: {results}")
    
    items = results.get("result", [])
    return [{"lemma_id": item.get("lemma_id"),
             "title": item.get("lemma_title"),
             "description": item.get("lemma_desc"),
             "url": item.get("url")} for item in items]


# 热榜 type 映射（每个 type 每天 1 次，共 10 次）
TRENDING_TYPES = {
    "weibo": 2,        # 微博热榜
    "toutiao": 3,      # 头条热榜
    "zhihu": 7,        # 知乎热榜
    "douyin": 6,       # 抖音热榜
    "bilibili": 8,     # B站热榜
    "baidu": 4,        # 百度热榜
    "tieba": 9,        # 贴吧热议榜
    "kuaishou": 10,    # 快手热榜
    "xhs": 14,         # 小红书热榜
}


def _trending(api_key, api_name, query):
    """热榜榜单查询"""
    type_id = TRENDING_TYPES.get(api_name, 2)
    url = "https://qianfan.baidubce.com/v2/tools/trending_lists/medium"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    params = {"type": type_id}
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    results = response.json()
    
    if "data" not in results:
        raise Exception(f"热榜查询失败: {results}")
    
    items = results.get("data", [])
    return [{"title": item.get("title"), "hot": item.get("hot")} for item in items]


def get_quota_status():
    """获取当前配额状态"""
    return {
        name: {"used": data["used"], "limit": data["limit"], "name": data["name"]}
        for name, data in QUOTA.items()
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python smart_search.py '<query>' [--force api]")
        print("")
        print("Args:")
        print("  query          搜索关键词")
        print("  --force api    强制使用指定API (smart_search, smart_search_pro, baike, baidu_search)")
        print("")
        print("Example:")
        print("  python smart_search.py '如何做兼职'")
        print("  python smart_search.py '什么是量子计算' --force smart_search_pro")
        sys.exit(1)
    
    # 解析参数
    args = sys.argv[1:]
    force_api = None
    
    if "--force" in args:
        idx = args.index("--force")
        if idx + 1 < len(args):
            force_api = args[idx + 1]
            args = args[:idx] + args[idx + 2:]
    
    query = " ".join(args)
    
    try:
        result = smart_search(query, force_api)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 打印配额状态
        print("\n--- 配额状态 ---")
        status = get_quota_status()
        for k, v in status.items():
            print(f"{v['name']}: {v['used']}/{v['limit']}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)