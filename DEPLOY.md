# 供应商管理系统部署指南

本项目已配置好 Vercel + Railway 部署，可实现随时随地访问。

## 部署架构

- **前端**：Vercel（静态网站托管）
- **后端**：Railway（云服务器 + PostgreSQL 数据库）
- **API 代理**：Vercel 转发 /api 请求到 Railway 后端

## 部署步骤

### 第一步：推送代码到 GitHub

1. **创建 GitHub 仓库**

   访问 https://github.com 并登录，点击 "New repository" 创建一个新的公开仓库，命名为 `supplier-management-system`

2. **初始化 Git 并推送代码**

   在项目根目录打开终端，执行以下命令：

```powershell
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit: Supplier Management System"

# 添加远程仓库（将 YOUR_USERNAME 替换为您的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/supplier-management-system.git

# 推送代码
git branch -M main
git push -u origin main
```

### 第二步：部署后端到 Railway

1. **注册 Railway 账号**

   访问 https://railway.app 并使用 GitHub 账号登录

2. **创建新项目**

   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择您刚创建的仓库 `supplier-management-system`

3. **配置后端部署**

   - Railway 会自动检测到 `backend` 目录中的 Python 项目
   - 在项目设置中，将 **Root Directory** 设置为 `backend`
   - Railway 会自动安装 `requirements.txt` 中的依赖

4. **添加 PostgreSQL 数据库**

   - 在项目中点击 "Add a Database"
   - 选择 "PostgreSQL"
   - Railway 会自动设置 `DATABASE_URL` 环境变量

5. **配置环境变量**（可选）

   - `SECRET_KEY`: JWT 密钥（用于用户认证）
   - Railway 会自动设置 `PORT` 环境变量

6. **等待部署完成**

   - Railway 会自动构建并部署后端
   - 部署完成后，您会获得一个 URL，例如：`https://supplier-management-api.up.railway.app`

7. **验证后端部署**

   访问 `https://supplier-management-api.up.railway.app/health`，应该返回 `{"status":"healthy"}`

### 第三步：部署前端到 Vercel

1. **注册 Vercel 账号**

   访问 https://vercel.com 并使用 GitHub 账号登录

2. **导入项目**

   - 点击 "Add New" > "Project"
   - 选择您刚创建的 GitHub 仓库
   - Vercel 会自动检测到是 Vite + Vue 项目

3. **配置项目**

   - **Framework Preset**: Vite（通常自动检测）
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **配置环境变量**

   - 点击 "Environment Variables"
   - 添加：
     - Name: `VITE_API_URL`
     - Value: `https://supplier-management-api.up.railway.app`（替换为您实际的 Railway 后端 URL）

5. **部署**

   - 点击 "Deploy"
   - Vercel 会自动构建并部署前端

6. **获取访问地址**

   部署完成后，Vercel 会提供一个 URL，例如：`https://supplier-management-system.vercel.app`

### 第四步：更新前端代理配置（重要）

部署完成后，您需要更新前端配置以指向正确的后端地址：

1. **更新 vercel.json**

   修改 `frontend/vercel.json` 中的 `destination` URL 为您实际的 Railway 后端地址：

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://your-railway-app.up.railway.app/api/$1"
    }
  ]
}
```

2. **重新部署前端**

   在 Vercel 控制台中，点击 "Redeploy" 使更改生效

## 访问系统

部署完成后，通过以下地址访问系统：

- **生产地址**: `https://supplier-management-system.vercel.app`（或您实际的 Vercel URL）
- **后端 API**: `https://supplier-management-api.up.railway.app`（用于测试）

## 本地开发

如果您想在本地继续开发：

### 后端

```powershell
cd backend
pip install -r requirements.txt
python main.py
```

后端将在 http://localhost:8000 运行

### 前端

```powershell
cd frontend
npm install
npm run dev
```

前端将在 http://localhost:5173 运行，并代理 API 请求到后端

## 常见问题

### 1. 注册功能失败

确保后端已正确部署，并且前端 vercel.json 中的 API 代理配置正确指向 Railway 后端。

### 2. 数据库连接错误

检查 Railway 的 DATABASE_URL 环境变量是否正确设置。如果使用 SQLite 本地开发，确保删除了 DATABASE_URL 环境变量。

### 3. CORS 错误

确保后端 main.py 中的 CORS 配置允许所有来源：
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    ...
)
```

## 技术栈

- **前端**: Vue 3 + TypeScript + Vite + Element Plus
- **后端**: Python 3.8 + FastAPI + SQLAlchemy
- **数据库**: PostgreSQL (Railway)
- **部署**: Vercel (前端) + Railway (后端)
