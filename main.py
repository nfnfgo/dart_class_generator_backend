# fundamentals
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# routers
import routers

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # 允许跨域的源列表
    allow_origins=["*"],
    # 跨域请求是否支持 cookie，默认是 False
    allow_credentials=False,
    # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
    allow_methods=["*"],
    # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
    allow_headers=["*"],
)

# include routers
app.include_router(routers.generate.router, prefix="/generate")


def main():
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        server_header=False,
    )


if __name__ == "__main__":
    main()
