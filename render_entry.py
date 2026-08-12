import os
from starlette.routing import Mount
from nowhere.server import mcp
from nowhere.web import app as web_app

port = int(os.environ.get("PORT", 8000))

# 获取 FastMCP 的 HTTP ASGI app
mcp_app = mcp.http_app(path="/mcp")

# 关键：关闭 Starlette 的自动斜杠重定向（307 的根源）
if hasattr(mcp_app, 'redirect_slashes'):
    mcp_app.redirect_slashes = False

# 把 Web 前端挂载为 fallback：
# FastMCP 内部路由先匹配 /mcp，其他所有路径（/、/state、/static）fallback 给 Web
if hasattr(mcp_app, 'routes'):
    mcp_app.routes.append(Mount("/", app=web_app))
    app = mcp_app
else:
    # 保险 fallback
    from starlette.applications import Starlette
    app = Starlette(routes=[
        Mount("/mcp", app=mcp_app),
        Mount("/", app=web_app),
    ])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
