# Arc Raider Material Tracker

A lightweight desktop app for squads to coordinate material sharing in Arc Raider.  
Each player runs it on their own machine and posts needs/offers to a shared Discord channel.


Created with Claude Code

## Setup

**Requirements:** Python 3.9+

```bash
pip install requests
python main.py

Python 3.1x+
pip3 install requests
python3 main.py
```

## Usage

1. **Enter your name** at the top — this appears in Discord messages.
2. **Set quantities** for any materials you need or can share.
3. **Post to Discord** using the buttons at the bottom:
   - 🔴 **Post Needs** — tells the squad what you're looking for
   - 🟢 **Post Offers** — tells the squad what you have spare
   - 📤 **Post All** — sends both in one message
4. **Save** to persist your quantities between sessions.

## Discord Webhook Setup

1. Open Discord and go to the channel your squad uses.
2. Click the ⚙ gear → **Integrations** → **Webhooks** → **New Webhook**.
3. Copy the webhook URL.
4. In the app, click **⚙ Settings** and paste the URL.

Every squad member can use the same webhook URL — all posts go to the same channel.

## Customising the Material List

Click **📋 Materials** to open the editor.  
Add, remove, or rename items (one per line). Changes take effect immediately.  
You can reset to the built-in default list at any time.

The list is stored in `materials.json` next to `main.py`, so you can also edit it
in a text editor and share it with your squad so everyone uses the same list.

## Files Created

| File | Contents |
|---|---|
| `materials.json` | The material list (editable) |
| `player_data.json` | Your saved quantities |
| `config.json` | Your player name and webhook URL |

All files are created automatically on first run.
