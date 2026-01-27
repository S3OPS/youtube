# 🧙 One Command to Rule Them All — Setup Guide

Welcome, traveler. This guide is the **Red Book of Westmarch** for getting the Automated YouTube Content Creation System running with **one command**, a **Python 3.12 install**, and a little dramatic flair worthy of Middle‑earth.

## ✅ The Single Command

From the project root:

```bash
./setup.sh
```

That is the One Command to Rule Them All. It will:

1. **Install Python 3.12** (if missing)
2. **Install ffmpeg**
3. **Create a virtual environment**
4. **Install dependencies**
5. **Run the setup wizard**
6. **Show the key setup docs**
7. **Remove unneeded caches**

> "All we have to decide is what to do with the time that is given to us." — Gandalf  
> First, run the command.

---

## 🧾 What You’ll Need Before the Quest

- **OpenAI API Key** (Gandalf’s staff)
- **Amazon Affiliate Tag** (your Mithril)
- **YouTube OAuth credentials** (`client_secrets.json`)
- **A working internet connection** (the Eagles)

Keep these close. You’ll add them when the setup wizard asks.

---

## 🧝 Step-by-Step (Foolproof Edition)

### Step 1: Clone the repo

```bash
git clone https://github.com/S3OPS/youtube.git
cd youtube
```

### Step 2: Run the One Command

```bash
./setup.sh
```

That’s it. No extra steps unless the script tells you otherwise.

---

## 🧪 Proof the Setup Worked

### Option A: Web Dashboard

```bash
python app.py
```

Visit: `http://localhost:5000`

### Option B: CLI Run

```bash
python create_video.py
```

If you see success output, the quest is complete.

---

## 🧹 What Gets Removed (Cleanliness of the Shire)

The setup script removes:

- `__pycache__/`
- `*.pyc`
- `.DS_Store`

No source files are harmed in the making of this quest.

---

## 📜 Docs the Script Will Show You

The One Command prints a preview of:

- `README.md`
- `QUICKSTART.md`
- `CHECKLIST.md`
- `TROUBLESHOOTING.md`
- `.env.example`

So you can read the lore without wandering the whole map.

---

## 🛡️ Common Questions

### What if Python 3.12 won’t install?
The script will point you to the official installer. Follow it, then re-run `./setup.sh`.

### Do I need admin privileges?
Yes, for installing Python 3.12 or ffmpeg on most systems. The script uses `sudo` when needed.

---

## ⚔️ Next Steps

Once setup is complete:

1. Place `client_secrets.json` in the project root.
2. Run the dashboard: `python app.py`
3. Or create a video immediately: `python create_video.py`

May your videos be swift, your scripts be sharp, and your uploads be true.  
**The road goes ever on and on.**
