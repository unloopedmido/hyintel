# HyIntel: Hypixel Auction House Viewer

A lightweight, no-framework web interface for browsing Hypixel Skyblock auctions.

Built using **FastAPI** (with Jinja2 templates), plain HTML, and TailwindCSS. It fetches real-time data from the Hypixel API and displays Buy-It-Now auctions in a simple, responsive layout. Clicking on an item opens a modal with detailed item info, including formatted lore.

## ✨ Features

- 🧙 Minecraft-style lore formatting using a custom parser
- ⚡ Fast and clean UI using raw HTML + TailwindCSS
- 🪶 Zero frontend frameworks — just FastAPI + Jinja2
- 🔍 Search bar to filter auctions by item name
- 🖼 Displays item icon, name, price, and lore in a modal

## 🚀 Stack

- Python 3.11
- FastAPI
- Jinja2 (templating)
- TailwindCSS (via CDN)

> `tailwind.config.js` is only included to let IDEs (like VS Code) recognize Tailwind classes for IntelliSense — it’s not used during build/runtime.

## 📁 Structure

```bash
├── main.py             # App logic
├── templates/          # Templates folder
│   └── index.html      # Main page + modal layout
├── parser.py           # NBT data parser
├── colors.py           # Minecraft color + formatting parser
└── tailwind.config.js  # For IDE Tailwind IntelliSense only
```

## 🛠 Setup

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn jinja2 requests
   ```

2. Run the app:
   ```bash
   uvicorn main:app --reload
   ```

3. Visit [http://localhost:8000](http://localhost:8000)

## 📎 Notes

- This was a fast-build weekend project — some parts are messy by design.
- No authentication, pagination, or caching.
- Lore parser doesn't support obfuscated (`§k`) due to HTML limitations.

## 🧠 Why?

Just for fun. Wanted to make a functional Minecraft-themed UI without touching React or Vue. Surprisingly satisfying.

## 📜 License

MIT — do whatever you want.