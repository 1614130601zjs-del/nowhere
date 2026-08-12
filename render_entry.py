import os
from fastapi import FastAPI
from nowhere.server import mcp
from nowhere.web import app as web_app

port = int(os.environ.get("PORT", 8000))

# ✅ 关键：path 设为 "/"，让 fastmcp 内部的路由从根开始
# fastmcp 内部会注册 /mcp 路由，所以实际端点 = mount前缀 + /mcp
mcp_app = mcp.http_app(path="/")

app = FastAPI(lifespan=mcp_app.lifespan)

# ✅ 挂载到 "/"，这样 fastmcp 内部的 /mcp 路由就是最终路径 /mcp
app.mount("/", mcp_app)

# Web 前端：由于 mcp_app 在 "/" 上，它只会处理 /mcp 相关请求
# 其他路径（/、/static 等）会返回 404
# 所以我们需要把 web_app 的路由也注册进来

# 方案：把 web_app 的路由合并到主 app
# 最简单的方式是把 web_app 挂载到一个子路径
app.mount("/app", web_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
