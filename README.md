# WBot - 智能QQ机器人

一个基于 Flask 和 NapCat 的多功能 QQ 机器人，支持多种 AI 模型、游戏服务器查询、音乐卡片等功能。

## ✨ 功能特性

### 🤖 AI 聊天

- 支持多种 AI 模型：OpenAI GPT、DeepSeek、Gemini
- 私聊和群聊智能对话
- 上下文记忆功能

### 🎮 游戏功能

- Minecraft 服务器 Ping 查询
- Minecraft 服务器聊天转发
- 在线玩家列表查询
- Delta Force 游戏数据查询（密码、产物推荐、活动物品等）

### 🎵 娱乐功能

- 音乐卡片生成和分享
- 语音消息发送
- 表情包自动回复

### 🔧 管理功能

- 命令系统支持
- 管理员权限控制
- 日志记录和监控

## 🛠️ 技术栈

- **后端框架**: Flask
- **QQ 接口**: NapCat
- **AI 服务**: OpenAI、DeepSeek、Gemini
- **数据处理**: CSV、JSON
- **环境管理**: python-dotenv

## 📦 安装部署

### 环境要求

- Python 3.8+
- NapCat QQ 机器人框架 + FFmpeg（用于语音消息转换）

### 1. 克隆项目

```bash
git clone https://github.com/your-username/wbot.git
cd wbot
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制环境变量模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的配置：

```bash
# Flask 配置
DEBUG=True

# NapCat 配置
NAPCAT_HOST=http://localhost:3000
NAPCAT_TOKEN=your_napcat_token_here

# 机器人配置
BOT_NAME=WBot
BOT_QQ=your_bot_qq_number
ADMIN_QQ=your_admin_qq_number

# AI 服务配置
OPENAI_API_KEY=your_openai_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# 更多配置请参考 .env.example
```

### 4. 准备静态文件（如果需要）

确保 `app/static/ar_records/` 目录存在，并放入音乐记录文件：

```bash
mkdir -p app/static/ar_records/
# 将 records_list.csv 放入该目录
```

### 5. 启动应用

```bash
python run.py
```

应用将在 `http://localhost:5555` 启动。

## 🎯 使用说明

### 命令列表

#### 基础命令

- `test` - 测试机器人响应
- `/help` - 显示帮助信息

#### AI 聊天

- 直接发送消息 - AI 智能回复
- `@机器人 消息内容` - 在群聊中@机器人进行对话

#### 游戏功能

- `mcping 服务器地址` - 查询 Minecraft 服务器状态
- `#消息内容` - 转发消息到 Minecraft 服务器
- `#在线列表` - 查询在线玩家列表

#### 音乐功能

- `唱片` - 随机获取音乐卡片
- `唱片 数字` - 获取指定编号的音乐卡片

#### Delta Force 功能

- `今日密码` - 获取今日地图密码
- `产物推荐` - 获取产物推荐信息
- `活动物品` - 查看活动物品信息
- `高价浮动材料` - 查看高价材料信息
- `热门子弹` - 查看热门子弹列表
- `子弹利润` - 查看子弹利润信息

### API 接口

#### 发送群消息

```http
POST /sendGroupMessage
Content-Type: application/json

{
  "groupId": "群聊ID",
  "message": "消息内容",
  "userId": "用户ID（可选，用于@）"
}
```

#### 发送私聊消息

```http
POST /sendPrivateMessage
Content-Type: application/json

{
  "userId": "用户ID",
  "message": "消息内容"
}
```

#### 获取机器人状态

```http
GET /bot/status
```

#### AI 聊天接口

```http
POST /chat
Content-Type: application/json

{
  "message": "消息内容",
  "userId": "用户ID",
  "model": "AI模型（可选）"
}
```

## 📁 项目结构

```
wbot/
├── app/
│   ├── __init__.py              # 应用工厂函数
│   ├── config.py                # 配置文件
│   ├── handlers/
│   │   ├── commands.py          # 命令处理器
│   │   └── message.py           # 消息处理器
│   ├── models/
│   │   └── wbot.py             # 机器人核心模型
│   ├── routes/
│   │   ├── api.py              # API 路由
│   │   └── webhook.py          # Webhook 路由
│   ├── services/
│   │   ├── card_service.py     # 卡片服务
│   │   ├── chat_service.py     # 聊天服务
│   │   ├── detlaforce_service.py # Delta Force 服务
│   │   ├── mcbot_service.py    # Minecraft 服务
│   │   └── ping_service.py     # Ping 服务
│   ├── static/
│   │   └── ar_records/         # 音乐记录文件
│   └── utils/
│       └── logger.py           # 日志工具
├── .env.example                # 环境变量模板
├── .gitignore                  # Git 忽略文件
├── README.md                   # 项目说明
├── requirements.txt            # 依赖包列表
└── run.py                     # 启动文件
```

## 🔧 配置说明

### 环境变量配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DEBUG` | 调试模式 | `True` |
| `NAPCAT_HOST` | NapCat 服务地址 | `http://localhost:3000` |
| `NAPCAT_TOKEN` | NapCat 访问令牌 | - |
| `BOT_QQ` | 机器人 QQ 号 | - |
| `ADMIN_QQ` | 管理员 QQ 号 | - |
| `OPENAI_API_KEY` | OpenAI API 密钥 | - |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | - |
| `GEMINI_API_KEY` | Gemini API 密钥 | - |
| `ENABLE_VOICE_MESSAGE` | 启用语音消息 | `False` |

### NapCat 配置

确保 NapCat 正确配置并运行：

1. 安装并配置 NapCat
2. 设置正确的 HTTP 服务端口
3. 配置访问令牌
4. 确保机器人 QQ 已登录

## 🐛 故障排除

### 常见问题

1. **语音消息发送失败**
   - 确保安装 FFmpeg
   - 检查音频文件格式
   - 设置 `ENABLE_VOICE_MESSAGE=False` 禁用语音功能

2. **AI 聊天无响应**
   - 检查 API 密钥是否正确
   - 确认网络连接正常
   - 查看日志中的错误信息

3. **NapCat 连接失败**
   - 确认 NapCat 服务正在运行
   - 检查主机地址和端口配置
   - 验证访问令牌

### 日志查看

应用日志位于控制台输出，可以通过以下方式查看：

```bash
# 直接运行查看
python run.py

# 后台运行并保存日志
nohup python run.py > wbot.log 2>&1 &
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [NapCat](https://github.com/NapNeko/NapCatQQ) - QQ 机器人框架
- [Flask](https://flask.palletsprojects.com/) - Web 应用框架
- [OpenAI](https://openai.com/) - AI 服务提供商
- [DeepSeek](https://www.deepseek.com/) - AI 服务提供商

## 📞 联系方式

- 项目地址: <https://github.com/Diend2023/wbot>
- 问题反馈: <https://github.com/Diend2023/wbot/issues>

---

如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！
