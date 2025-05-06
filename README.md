# FastAPI 範例專案：Kubernetes 與 NFS 整合

## 概述
此專案展示如何在 Kubernetes 上部署 FastAPI 應用，並使用以下架構：

```
+-------------------+        +-------------------+         +-------------------+
|                   |         |                  |         |                   |
|   外部用戶端      |  --->   |   節點 (Node)    |  --->   |   Ingress 控制器  |
|  10.10.0.147     |         | 10.10.0.146      |         |   類型: nginx     |
|                   |         | (例如k8s-w2)     |         |   URL路由         |
+-------------------+         +-------------------+         +-------------------+
                                                                    |
                                                                    | 路徑: /ai/fastapi-demo
                                                                    v
                            +-------------------+
                            |   Service         |
                            |   類型: NodePort  |
                            |   IP: 10.102.195.249
                            |   埠: 80          |
                            |   NodePort: 31669 |
                            +-------------------+
                                   |
                                   v
                            +-------------------+
                            |   Deployment      |
                            |   Pod             |
                            |   IP: 172.16.46.29|
                            |   容器埠: 8000    |
                            |   映像檔:         |
                            |   nuu9323226/     |
                            |   fastapi-demo    |
                            +-------------------+
                                   |
                                   v
                            +-------------------+
                            |   NFS 存儲        |
                            |   IP: 10.10.0.148 |
                            |   PVC: fast-nfs   |
                            |   StorageClass:   |
                            |   nfs-csi         |
                            |   掛載路徑:       |
                            |   /app/nfs        |
                            +-------------------+
```

## 功能
- **FastAPI 應用**：基於 Python 的 Web 應用，使用 Uvicorn 運行。
- **非 root 使用者**：容器以非 root 使用者執行，提升安全性。
- **Kubernetes 部署**：應用透過 Kubernetes 的 Deployment、Service 和 Ingress 部署。
- **NFS 存儲**：使用 NFS 提供持久化存儲。



3. **檢視容器詳細資訊**：
   ```bash
   kubectl describe -n dev pod <pod-name>
   ```

## 部署步驟

1. **建置 Docker 映像檔**：
   ```bash
   docker build -t yourdockerhub/fastapi-demo:0522 .
   ```

2. **推送映像檔到 Docker Hub**：
   ```bash
   docker push yourdockerhub/fastapi-demo:0522
   ```

3. **套用 Kubernetes 配置**：
   使用提供的 `k8s_cfg.yaml` 部署應用：
   ```bash
   kubectl apply -f k8s_cfg.yaml
   ```

4. **驗證部署**：
   - 檢查 Pod 狀態：
     ```bash
     kubectl get pods -n dev
     ```
   - 檢查 Service：
     ```bash
     kubectl get svc -n dev
     ```
   - 檢查 Ingress：
     ```bash
     kubectl get ingress -n dev
     ```

5. **存取應用**：
   - 使用節點的 IP 和 NodePort 存取應用：
     ```
     http://kube.tul.com.tw/ai/fastapi-demo
     ```
   - Swagger 文件：
     ```
     http://kube.tul.com.tw/ai/fastapi-demo/docs#/
     ```


6. **NFS 存儲**：
   - 確保 NFS 伺服器正在運行且可訪問。
   - 驗證 PVC 是否已綁定：
     ```bash
     kubectl get pvc -n dev
     ```

## 容器管理與故障排除

1. **進入運行中的容器**：
   ```bash
   # 使用 kubectl exec 進入容器
   kubectl exec -it  -n dev <pod-name> -- /bin/sh
   
   # 例如：
   kubectl exec -it  -n dev fastapi-demo-694f55b87d-sx7rc -- /bin/sh
   ```

2. **查看容器日誌**：
   ```bash
   kubectl logs -n dev <pod-name>
   
   # 即時查看日誌（類似 tail -f）
   kubectl logs -f -n dev <pod-name>
   ```



## 專案結構
- `Dockerfile`：定義 FastAPI 應用的容器映像。
- `k8s_cfg.yaml`：Kubernetes 配置檔案，包含 Deployment、Service、Ingress 和 PVC。
- `main.py`：FastAPI 應用程式的程式碼。
- `requirements.txt`：應用程式的 Python 依賴項。

## 安全性
- 容器以非 root 使用者（`nobody`）執行，提升安全性。
- (option)Kubernetes 的 `securityContext` 配置強制執行非 root 運行。