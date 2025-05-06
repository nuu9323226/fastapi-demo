FROM python:3.11-slim

# 建立非 root 使用者
# RUN useradd -m appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 調整權限
RUN chown -R nobody:nogroup /app

USER nobody

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]