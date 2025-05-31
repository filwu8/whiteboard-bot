
---

## 🧠 AI 功能集成说明（基于 Excalidraw）

本项目中使用的 **AI 功能模块** 是一个基于 Python 的中间件 HTTP 服务，其主要作用是作为前端与后端 AI 服务之间的桥梁。它接收来自 Excalidraw 前端的请求，转发至兼容 OpenAI 标准接口的 AI 后端服务（如本地部署的 Ollama / LM Studio，或云厂商提供的 API），并将处理结果返回给前端。

### ✅ 支持的 AI 后端

- 自托管服务：Ollama、LM Studio、LocalAI 等
- 第三方云服务：OpenAI、硅基流动、阿里云百炼、腾讯云、百度文心一言、讯飞星火等（需支持 OpenAI 接口标准）

---

### 🔧 集成步骤

#### 1. 修改环境变量

在 `excalidraw` 项目的环境配置文件中（如 `.env` 或 Docker 配置），设置以下变量以指定 AI 中间件地址：

```bash
VITE_APP_AI_BACKEND=http://diagram-bot
```

> ⚠️ 注意：
> - 如果你是在局域网内部署，可将 `http://diagram-bot` 替换为宿主机 IP + 暴露端口，例如：`http://192.168.1.10:5000`
> - 如果部署在公网，建议使用反向代理配置该地址，确保安全访问。

---

#### 2. 反向代理配置建议（Apache）

如果你使用 Apache 作为反向代理，请注意以下事项：

- Apache 2.5+ 版本按路径长度匹配规则进行转发（从长到短）
- 为避免路径冲突，建议使用较长路径来映射 AI 服务，例如：

```apache
ProxyPass /XXXXXXXXXXXXXXXXXXXXXXXX http://localhost:5000
ProxyPassReverse /XXXXXXXXXXXXXXXXXXXXXXXX http://localhost:5000
```

示例完整配置片段：

```apache
<Location /XXXXXXXXXXXXXXXXXXXXXXXX>
    ProxyPass http://localhost:5000/
    ProxyPassReverse http://localhost:5000/
</Location>
```

然后在前端配置中设置：

```bash
VITE_APP_AI_BACKEND=http://your-domain.com/XXXXXXXXXXXXXXXXXXXXXXXX
```

---

#### 3. 修改前端调用逻辑（可选）

如果未通过环境变量注入方式生效，可手动修改 AI 请求地址：

定位文件：

```
excalidraw/excalidraw-app/components/AI.tsx
```

查找fetch方法，并替换以下代码中的 URL：

```ts
await fetch("http://your-ai-backend", { ... })
```

将其修改为你实际部署的 AI 服务地址（即中间件地址）。

---

### 📦 示例部署拓扑图

```
[Excalidraw Frontend] 
       ↓
[Apache Reverse Proxy]
       ↓
[Ai Middleware (Python)]
       ↓
[Ai Backend (Ollama / OpenAI / Cloud API)]
```

---

### 💡 补充说明

- 本模块已集成在 [whiteboard-bot](https://github.com/filwu8/whiteboard-bot) 项目中，你可以直接 clone 并运行。
- 如需协助搭建、调试或扩展功能，欢迎联系我或提交 issue。

---
