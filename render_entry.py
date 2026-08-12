import os
from fastapi import FastAPI
from nowhere.server import mcp
from nowhere.web import app as web_app

port = int(os.environ.get("PORT", 8000))

# 1. 创建 MCP 的 ASGI app，path 设为 "/"（因为挂载时会指定前缀）
mcp_app = mcp.http_app(path="/")

# 2. 创建主 FastAPI 应用，关键：传入 mcp_app.lifespan
#    这会让 session_manager 在启动时正确初始化 task group
app = FastAPI(lifespan=mcp_app.lifespan)

# 3. 挂载 MCP 到 /mcp 路径
app.mount("/mcp", mcp_app)

# 4. 挂载 Web 前端（处理 /、/state、/static 等）
app.mount("/", web_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
