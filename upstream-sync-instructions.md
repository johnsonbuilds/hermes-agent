# Upstream Sync Instructions

记录 fork 相比上游 [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) 的自定义改动，方便每次合并上游更新后重新应用。

## 自定义改动

### 1. Rate-limit 提示语替换

**文件:** `gateway/run.py`
**函数:** `_gateway_provider_error_reply()`
**目的:** 当 provider 返回 rate-limit 类错误时，Telegram 用户看到的是 GetClawCloud 的引导提示，而不是原始的普适文案。

**改动前:**
```python
if _GATEWAY_RATE_LIMIT_RE.search(text):
    return "⏱️ The model provider is rate-limiting requests. Please wait a moment and try again."
```

**改动后:**
```python
if _GATEWAY_RATE_LIMIT_RE.search(text):
    return (
        "⚠️ I've hit the free usage limit.\n\n"
        "You can keep me running by adding your API key:\n"
        "👉 https://hermesagentcloud.com/home?openByoKey=true\n\n"
        "Takes ~1 minutes, then I'm back 🚀"
    )
```

**合并冲突标记:** 搜索 `GATEWAY_RATE_LIMIT_RE.search` 找到该位置。
**首次提交:** `416554e5b` (revert 后保留的唯一改动)
