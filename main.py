from fastapi import FastAPI

app = FastAPI(
    title="My FastAPI Application",
    description="這是一個範例 FastAPI 應用，內建 Swagger 文件。",
    version="1.0.0",
    # 不需要設置 root_path，因為 Ingress 的 rewrite-target 已經處理了路徑重寫
    # 設置 rewrite-target: /$1 和 path: /ai/fastapi-demo/(.*)
    # 會將請求 /ai/fastapi-demo/docs 重寫為 /docs，交由 FastAPI 處理
    
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}