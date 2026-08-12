#!/usr/bin/env python3
"""
Nowhere MCP + Web 合并入口

- /mcp  -> MCP Streamable HTTP（手机/AI 客户端接入）
- /     -> Web 前端（地图、状态、明信片墙，和 MCP 共享内存状态）
"""

import os
from starlette.applications import Starlette
from starlette.routing import Mount
from nowhere.server import mcp          # 导入即注册所有 tool
from nowhere.web import app as web_app  # 原作者的 Starlette 前端

port = int(os.environ.get("PORT", 8000))

# fastmcp v3 的 mcp 对象本身就是 ASGI app，直接挂载到 /mcp
app = Starlette(routes=[
    Mount("/mcp", app=mcp),
    Mount("/", app=web_app),
])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
