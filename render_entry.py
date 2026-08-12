#!/usr/bin/env python3
"""
Nowhere MCP + Web 合并入口

- /mcp  -> MCP Streamable HTTP（手机/AI 客户端接入）
- /     -> Web 前端（地图、状态、明信片墙，和 MCP 共享内存状态）
"""

import os
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import RedirectResponse
from nowhere.server import mcp          # 导入即注册所有 tool
from nowhere.web import app as web_app  # 原作者的 Starlette 前端

port = int(os.environ.get("PORT", 8000))

# FastMCP v3: 获取真正的 ASGI app（mcp 对象本身不是 callable）
raw_mcp = mcp.http_app(path="/")

# /mcp 重定向到 /mcp/（避免缺少尾部斜杠失败）
def redirect_mcp(request):
    return RedirectResponse(str(request.url.replace(path="/mcp/")), status_code=307)

app = Starlette(
    routes=[
        Route("/mcp", endpoint=redirect_mcp, methods=["GET", "POST", "DELETE"]),
        Mount("/mcp", app=raw_mcp),
        Mount("/", app=web_app),
    ],
    lifespan=raw_mcp.lifespan,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
