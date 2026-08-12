import os
from nowhere.server import mcp
from nowhere.web import app as web_app

port = int(os.environ.get("PORT", 8000))

# 获取 MCP 的 ASGI app，path 设为 "/mcp"
mcp_app = mcp.http_app(path="/mcp")

class CombinedApp:
    def __init__(self):
        self.mcp = mcp_app
        self.web = web_app

    async def __call__(self, scope, receive, send):
        # lifespan 只给 web_app
        if scope["type"] == "lifespan":
            await self.web(scope, receive, send)
            return

        path = scope.get("path", "")

        # /mcp 和 /mcp/ 开头的都交给 MCP，不修改 path
        if path == "/mcp" or path.startswith("/mcp/"):
            await self.mcp(scope, receive, send)
        else:
            # 其他路径给 Web
            await self.web(scope, receive, send)

app = CombinedApp()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)

