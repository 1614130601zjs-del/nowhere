import os
from fastapi import FastAPI
from nowhere.server import mcp
from nowhere.web import app as web_app

port = int(os.environ.get("PORT", 8000))

# 1. 创建 MCP 的 ASGI app
#    path="/" 表示不在内部再加前缀，fastmcp 内部会自动注册 /mcp 路由
mcp_app = mcp.http_app(path="/")

# 2. 创建主 FastAPI 应用，传入 mcp_app.lifespan
app = FastAPI(lifespan=mcp_app.lifespan)

# 3. 先把 web_app 挂载到 "/"（兜底处理 /、/state、/static 等）
app.mount("/", web_app)

# 4. 再把 mcp_app 挂载到 "/mcp"
#    FastAPI 路由匹配是按注册顺序的，/mcp 会先于 / 被匹配
#    所以 /mcp 请求会交给 mcp_app，其他请求交给 web_app
app.mount("/mcp", mcp_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
