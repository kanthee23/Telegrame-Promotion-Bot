# Telegram Promo Bot (Python + Docker)

A production-ready Telegram bot built with python-telegram-bot v20+ that manages and delivers promotional media (images, videos, documents) using inline keyboards, admin-controlled storage, and automatic message cleanup.

## 🚀 Features
* /promos <name> – Search and retrieve promotions
* Inline keyboard promo picker
* Admin-only promo upload and management
* Supports photo, video, and document promotions
* SQLite database for promo storage
* Automatic deletion of bot replies (clean chats)
* Invalid message fallback with instructions
* Docker-ready deployment
* Works in private chats and groups

## 🧱 Tech Stack
* Python 3.11
* python-telegram-bot v20+
* SQLite3
* Docker

## 📂 Project Structure
<br>.
<br>├── bot.py 
<br>├── database.py 
<br>├── requirements.txt 
<br>├── Dockerfile 
<br>├── promos.db 
<br>└── README.md 

## 🔐 Bot Commands
Command	Description
- /start	Welcome message
- /help	    Show help
- /promos	Show promo suggestions
- /promos <name>	Filter promos by name
- /save <promo_name>	(Admin only) Save a promo
## 👤 Admin Setup

* Get your Telegram user ID
* Edit bot.py:

ADMIN_IDS = {123456789}

You can add multiple admins:

ADMIN_IDS = {123456789, 987654321}

## 🗄️ Database Schema4

SQLite table promos:

CREATE TABLE promos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    file_id TEXT,
    media_type TEXT
);

## 🧪 Local Development4
### 1️⃣ Create virtual environment
python3 -m venv venv
source venv/bin/activate

### 2️⃣ Install dependencies
pip install -r requirements.txt

### 3️⃣ Set bot token
export BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN

### 4️⃣ Run the bot
python bot.py

## 🐳 Docker Deployment
### Build image
docker build -t telegram-promo-bot .

### Run container
docker run -d  --name telegram-promo-bot --restart unless-stopped -e BOT_TOKEN="ADD YOUR BOT TOKEN" -e ADMIN_ID="ADD YOUR ADMIN ID" -v $(pwd)/data:/app/data  telegram-promo-bot

### View logs
docker logs -f telegram-promo-bot

## 🧼 Automatic Message Cleanup
* Bot replies auto-delete after 120 seconds
* Keeps groups and private chats clean
* Implemented using asyncio (no JobQueue dependency)

## ⚠️ Common Issues
### Invalid token error

Ensure:
* Token is copied fully from @BotFather
* No extra spaces or quotes
* Environment variable is set correctly

### Bot not responding in groups
* Disable Privacy Mode in @BotFather
* Ensure bot has permission to read messages

## 📈 Recommended Enhancements
* PostgreSQL for large-scale deployments
* Webhook mode (Nginx + HTTPS)
* Promo analytics (click tracking)
* Rate limiting and anti-spam
* Channel → group → private flow

## 🛡️ Security Notes
* Never hardcode bot tokens
* Restrict admin commands
* Use volume mounts for database persistence

## 📄 License

## MIT License

## 🤝 Support
If you need:
* Feature extensions
* Cloud deployment (AWS / GCP / Azure)
* WhatsApp integration
* Payment or coupon systems
Contact the maintainer or extend the codebase.

## ✅ Production-ready. Docker-safe. Clean architecture.


