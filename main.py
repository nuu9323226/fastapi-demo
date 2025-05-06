from fastapi import FastAPI

app = FastAPI(
    title="My FastAPI Application",
    description="這是一個範例 FastAPI 應用，內建 Swagger 文件。",
    version="1.0.0",
    root_path="/ai/fastapi-demo"
    
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