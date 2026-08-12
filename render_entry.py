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

# 3. 先挂载 mcp_app 到 "/mcp"
#    FastAPI 的 Mount 匹配是严格前缀 + 最长匹配优先，且一旦命中就终止后续匹配
#    所以 /mcp 开头的请求会先被这里拦截，交给 mcp_app 处理
app.mount("/mcp", mcp_app)

# 4. 再挂载 web_app 到 "/"（兜底处理 /、/state、/static 等）
#    由于 /mcp 已经被上面的 mount 拦截，这里只会处理非 /mcp 开头的请求
app.mount("/", web_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
