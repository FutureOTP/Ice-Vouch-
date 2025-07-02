# VouchBot ✅

A clean, advanced Discord vouch bot with rich embeds, category support, and persistent data storage.

## 🧾 Features
- Slash command `/vouch`
- Custom categories (e.g. "Fast Delivery", "Trusted")
- Clean embeds with avatars, images, average ratings
- Logs to vouch + log channels
- JSON-based storage

## 🛠 Setup

1. Clone this repo
2. Create a `.env` or use Render dashboard to add:
   - `TOKEN`
   - `VOUCH_CHANNEL_ID`
   - `VOUCH_LOG_CHANNEL_ID`
3. Deploy via [Render.com](https://render.com) using `render.yaml`

## 🚀 Deploy to Render
- Connect your GitHub repo
- Render auto-deploys and runs it 24/7

## 📦 Local Dev
```bash
pip install -r requirements.txt
python bot.py
```

---
Created with ❤️ by OpenAI GPT.
