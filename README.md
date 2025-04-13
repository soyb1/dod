
# DOD Mining Telegram Bot with Flask Web App

## Setup Locally

```bash
pip install -r requirements.txt
python app.py
```

## Deploy on Render

- **Start Command**:
```
gunicorn app:app --bind 0.0.0.0:$PORT
```

- **Environment Variables**:
  - TELEGRAM_BOT_TOKEN
  - WEB_APP_URL

- Add the Web App URL to your Telegram bot with BotFather using:
```
/setdomain
```

Enjoy your bot!
