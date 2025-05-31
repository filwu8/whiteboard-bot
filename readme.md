# 说明

中间件代码是一个基于 Python 的 HTTP 服务器，负责与后端 AI 服务通信，并将请求转发到 AI 服务，然后将结果返回给前端。

后端支持任何兼容OpenAi标准的接口，
例如自拓管的 Ollam  LM Studio， 或者各大算力厂商提供的第三方提供的公开AI服务


# 集成方法：
excalidraw 的环境变量中修改，或者增加以下部分：

示例：

- VITE_APP_AI_BACKEND= http://diagram-bot


用户浏览器端会直接访问以上 http://diagram-bot 域名，
如果局域网托管，域名可以直接修改为：你的 容器对应暴露给宿主机的端口
如果公网托管，需要反向代理配置转发到这个地址，可以是目录域名，
如果 apache 用URL中的路径转发，尽量吧路径写长点，避免无法返回数据，apache 是按照长短返回的

比如我之间设置的转发 /ai/ 路径转发到容器，可以转发过去，但是数据回不来
后来设置成超长路径 /XXXXXXXXXXXXXXXXXXXXXXXX/  转发成功

因为apache 的配置不是按照路径转发顺序，是按照由长到短
我用的apache版本是2.5

