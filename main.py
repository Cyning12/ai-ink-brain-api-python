"""
本地运行入口（根目录）。

说明：
- Vercel 生产环境入口由 `vercel.json` 指向 `api/index.py`，不要在这里改动部署行为。
- 这里仅做 app 转发，避免重复业务逻辑，方便 `uvicorn main:app` 直观启动。
"""

from api.index import app

