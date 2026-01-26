# Getting Started Checklist (Consolidated)

This checklist has been consolidated to reduce duplicate setup steps.

## ✅ Use These Sources

1. **Quick setup:** [QUICKSTART.md](QUICKSTART.md)
2. **Full setup & automation flow:** [README.md](README.md)
3. **Setup issues:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## ✅ Minimal Verification

- [ ] Follow [QUICKSTART.md](QUICKSTART.md) for setup steps
- [ ] Run the full-auto CLI (preflight checks included):
  ```bash
  python create_video.py
  ```

## ☑️ Post-Setup

### Security

- [ ] Verify `.env` is in `.gitignore`

- [ ] Verify `client_secrets.json` is in `.gitignore`

- [ ] Never commit API keys to git

- [ ] Keep `token.pickle` local (in `.gitignore`)

### Customization

- [ ] Adjust `CONTENT_TOPIC` if needed

- [ ] Set `VIDEO_PRIVACY` (public/unlisted/private)

- [ ] Configure `CONTENT_FREQUENCY` for scheduling

### Monitoring

- [ ] Bookmark dashboard URL: http://localhost:5000

- [ ] Check `automation_history.json` for logs

- [ ] Monitor YouTube channel for uploads

---

## ☑️ Optional: Scheduling

If you want automated creation:

- [ ] Test manual creation works first

- [ ] Set desired frequency in `.env`

- [ ] Use one of these methods:

**Method 1: Cron Job (Linux/Mac)**
```bash
crontab -e
# Add: 0 9 * * * cd /path/to/youtube && python3 create_video.py
```

**Method 2: Python Scheduler**
```python
from automation_engine import AutomationEngine
automation = AutomationEngine(config)
automation.schedule_automation(frequency='daily')
```

**Method 3: System Service**
- Create a systemd service (Linux)
- Create a launchd service (Mac)
- Use Task Scheduler (Windows)

---

## ✅ Troubleshooting

If something doesn't work, check:

### Common Issues

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for the full list of setup issues and fixes.

### Getting Help

- [ ] Check the documentation:
  - [README.md](README.md) - Main docs
  - [QUICKSTART.md](QUICKSTART.md) - Quick start
  - [API.md](API.md) - API reference
  - [EXAMPLES.md](EXAMPLES.md) - Usage examples
  - [ARCHITECTURE.md](ARCHITECTURE.md) - System design

- [ ] Review the activity log in dashboard

- [ ] Check console output for errors

- [ ] Open an issue on GitHub

---

## 🎉 Success!

Once all items are checked:

✅ Your automated YouTube content system is ready!

You can now:
- Create videos on demand
- Schedule automatic uploads
- Monitor from the dashboard
- Earn from Amazon affiliate links

**Next Steps:**
1. Create your first few videos
2. Review and refine your content topic
3. Set up scheduling if desired
4. Monitor your YouTube analytics
5. Track affiliate link performance

---

**Pro Tips:**

💡 Start with `VIDEO_PRIVACY=unlisted` for testing

💡 Review generated content before making it public

💡 Monitor your OpenAI API usage/costs

💡 Check YouTube upload quotas (10,000/day)

💡 Track which topics perform best

💡 Adjust content based on audience feedback

---

Enjoy your automated content creation system! 🚀
