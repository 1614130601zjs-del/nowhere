#!/usr/bin/env python3
"""
Nowhere MCP + Web 合并入口

- /mcp  -> MCP Streamable HTTP（手机/AI 客户端接入）
- /     -> Web 前端（地图、状态、明信片墙，和 MCP 共享内存状态）
"""

import os
from nowhere.server import mcp          # 导入即注册所有 tool
from nowhere.web import app as web_app  # 原作者的 Starlette 前端

port = int(os.environ.get("PORT", 8000))

class CombinedApp:
    """
    路由分发器：
    - 路径以 /mcp 开头  -> 交给 MCP 处理（保留 /mcp 前缀）
    - 其他所有路径       -> 交给 Web 处理
    """
    def __init__(self, mcp_part, web_part):
        self.mcp = mcp_part
        self.web = web_part

    async def __call__(self, scope, receive, send):
        path = scope.get("path", "")
        if path.startswith("/mcp"):
            await self.mcp(scope, receive, send)
        else:
            await self.web(scope, receive, send)

app = CombinedApp(mcp, web_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
