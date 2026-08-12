import os
from nowhere.server import mcp
from nowhere.web import app as web_app

port = int(os.environ.get("PORT", 8000))

# 获取 MCP 的 ASGI app（注意：mcp 对象本身不是 callable）
mcp_app = mcp.http_app(path="/mcp")

class CombinedApp:
    def __init__(self):
        self.mcp = mcp_app
        self.web = web_app
    
    async def __call__(self, scope, receive, send):
        # lifespan 只给 web_app（MCP 不需要）
        if scope["type"] == "lifespan":
            await self.web(scope, receive, send)
            return
        
        path = scope.get("path", "")
        
        # MCP 端点：/mcp 或 /mcp/ 开头的都交给 MCP
        if path == "/mcp":
            # fastmcp 内部只认 /mcp/，自动补斜杠
            new_scope = dict(scope)
            new_scope["path"] = "/mcp/"
            await self.mcp(new_scope, receive, send)
        elif path.startswith("/mcp/"):
            await self.mcp(scope, receive, send)
        else:
            # 其他所有路径给 Web（/、/state、/static 等）
            await self.web(scope, receive, send)

app = CombinedApp()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
