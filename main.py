from fastapi import FastAPI
import os

# 定義 NFS 掛載的目錄
NFS_MOUNT_PATH = "/app/nfs"

# 確保目錄存在
os.makedirs(NFS_MOUNT_PATH, exist_ok=True)

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
    """
    將收到的 name 存到 NFS 目錄中的檔案，每次換行
    """
    file_path = os.path.join(NFS_MOUNT_PATH, "data.txt")
    try:
        # 以追加模式打開檔案，若檔案不存在則自動創建
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"{name}\n")  # 每次寫入一行
        return {"message": f"Hello, {name}! Data saved to NFS."}
    except Exception as e:
        return {"error": f"Failed to save data: {str(e)}"}

@app.get("/health")
def health_check():
    return {"status": "ok"}