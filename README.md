# 🤖 WhatsApp Automater - Professional Campaign Manager

**WhatsApp Automater** is an advanced WhatsApp Web automation tool designed for bulk messaging campaigns, business outreach, and customer engagement. It simulates human behavior with typing delays, mouse movement, and random background activity for more natural automation.

---

## ✨ Features

✅ **Human-like Automation**
- Variable typing speed with realistic typo simulation
- Natural mouse movements using Bezier curves with tremor
- Random delays and background activity simulation
- Designed to reduce detection risk by WhatsApp anti-bot systems

✅ **Smart Campaign Management**
- CSV-based contact import with `Display Name` and `Mobile Phone`
- Automatic phone formatting for Pakistani numbers
- Campaign state tracking: `sent`, `failed`, `skipped`
- Detailed logging and recovery support
- Batch processing with configurable delays

✅ **Advanced Capabilities**
- Rate limiting and hourly message control
- Photo + message sending capability
- Retry failed recipients option
- Real-time console progress tracking
- Atomic state saves for crash-safe run recovery

---

## 📋 Prerequisites

### System Requirements
- Windows OS
- Python 3.8+
- Chrome or Microsoft Edge browser

### Python Libraries

```powershell
pip install pyautogui pillow pywin32
```

> Note: `win32gui` comes from the `pywin32` package.

---

## 🚀 Quick Start

### Step 1: Setup Project Structure

```powershell
# Clone repository
git clone https://github.com/adeelabbasi111/Whatsapp-Automater.git
cd Whatsapp-Automater

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install pyautogui pillow pywin32
```

### Step 2: Prepare Contact Data

Create `Data/contacts.csv`:

```csv
Display Name,Mobile Phone
Adeel,+923215773211
```

Supported phone formats:
- `0300XXXXXXXX` → auto-converts to `+923XXXXXXXX`
- `03001234567`
- `+923001234567`
- `923001234567`
- Standard 10–13 digit international numbers

---

### Step 3: Prepare Marketing Images

Create an `images/` folder and add these files:
- `Poster.png` — promotional image to send
- `new_chat.png` — screenshot of WhatsApp "New Chat" button
- `no_results_found.png` — screenshot of "No results found" state
- `chat_input.png` — screenshot of the WhatsApp message input box

How to capture images:
1. Open WhatsApp Web at `https://web.whatsapp.com`
2. Capture the UI elements using any screenshot tool
3. Save them as PNG in `images/`

---

### Step 4: Configure Settings

Edit `config.py` to customize:

```python
CONF_DEFAULT = 0.70           # Default matching confidence
CONF_INVITE_BTN = 0.65        # Button detection confidence
CONF_NO_RESULTS = 0.65        # "No results" detection confidence

TYPING_DELAY_MIN = 0.03       # Minimum delay between characters
TYPING_DELAY_MAX = 0.13       # Maximum delay between characters

CAMPAIGN_DELAY_MIN = 5        # Minimum wait between messages
CAMPAIGN_DELAY_MAX = 15       # Maximum wait between messages

MAX_MSG_PER_HOUR = 15         # Maximum messages per hour
```

---

## 💬 Customize Messages

Messages are generated in `campaign_manager.py` by `generate_message()`.

Example template style:

```python
def generate_message(self, name):
    messages = [
        f"Assalamualaikum {name}!`Your custom message here...`",
        f"Salam {name}!`Alternative message...`",
    ]
    return random.choice(messages)
```

- Use backticks (`) to create line breaks inside messages
- Supports Urdu, Arabic, and multilingual text
- `{name}` is replaced automatically for each contact

---

## 🧾 File Structure

```
Whatsapp-Automater/
│
├── main.py                  # 🚀 Entry point - starts the campaign
├── config.py               # ⚙️ Configuration settings & paths
├── campaign_manager.py     # 📋 Campaign logic & state management
├── whatsapp_handler.py     # 🤖 WhatsApp Web automation core
├── human_gui.py            # 👤 Human-like behavior simulator
│
├── Data/                   # 📁 Campaign data directory
│   ├── contacts.csv        # 📋 Contact list
│   ├── messages.txt        # 📝 Message templates
│   ├── whatsapp_state.json # 💾 Campaign state (generated)
│   └── whatsapp_log.txt    # 📊 Detailed logs (generated)
│
├── images/                 # 🖼️ WhatsApp UI screenshots
│   ├── Poster.png
│   ├── new_chat.png
│   ├── no_results_found.png
│   └── chat_input.png
│
└── README.md              # 📖 Project documentation
```

---

## 📦 Key Modules Overview

### `main.py`
- Initializes the WhatsApp automation bot
- Runs the campaign with configurable delays and batch size

### `whatsapp_handler.py`
- Opens/focuses WhatsApp Web
- Starts new chat sessions by phone number
- Handles text and photo sending
- Verifies if contact exists on WhatsApp

### `campaign_manager.py`
- Loads contact CSV
- Manages campaign state and retries
- Generates personalized messages
- Logs sent/skipped/failed results
- Controls batch limits and delay timing

### `human_gui.py`
- Simulates human typing and mouse movement
- Adds random wait and interaction noise
- Helps reduce anti-bot detection risk

---

## ▶️ Running the Campaign

### Method 1: Direct Execution

```powershell
venv\Scripts\activate
python main.py
```

### Method 2: Custom Parameters in `main.py`

```python
campaign.run(
    bot=bot,
    delay_min=60,           # Min delay between messages
    delay_max=150,          # Max delay between messages
    batch_limit=10,         # Send only 10 messages per run
    retry_failed=False      # Don't retry previous failures
)
```

### Method 3: Resume Failed Campaigns

```python
campaign.run(
    bot=bot,
    delay_min=60,
    delay_max=150,
    batch_limit=None,
    retry_failed=True       # Retry failed numbers
)
```

---

## 📊 Output & Monitoring

The console shows live progress like:

- `Initializing Automation...`
- `Browser focused: WhatsApp`
- `Loaded X contacts.`
- `Campaign: X pending`
- `Registered. Opening chat...`
- `Waiting XXs...`
- `Done. Sent: X`

Generated files:

- `Data/whatsapp_state.json` — campaign progress and recoverable state
- `Data/whatsapp_log.txt` — timestamped log details

Example `whatsapp_state.json` structure:

```json
{
  "sent": {
    "+923001234567": {
      "name": "Ali Ahmed",
      "time": "2026-05-23T14:30:00",
      "preview": "Assalamualaikum Ali Ahmed!..."
    }
  },
  "failed": {
    "+923002345678": {
      "name": "Hassan Ali",
      "reason": "Timeout waiting for chat",
      "time": "2026-05-23T14:35:00"
    }
  },
  "skipped": {
    "+923003456789": {
      "name": "Fatima Abbas",
      "reason": "Not on WhatsApp",
      "time": "2026-05-23T14:40:00"
    }
  },
  "stats": {"total": 50, "sent": 48, "failed": 1, "skipped": 1}
}
```

Example `whatsapp_log.txt`:

```
[2026-05-23 14:30:15] SUCCESS | Ali Ahmed              | +92xxxxxxxxxx | 
[2026-05-23 14:31:42] SKIPPED | Sara Khan              | +92xxxxxxxxxx | No WA
[2026-05-23 14:32:10] FAILED  | Hassan Ali             | +92xxxxxxxxxx | Network timeout
```

---

## ⚠️ Important Safety Notes

### WhatsApp Account Safety
✅ Use a dedicated account for automation
✅ Keep delays realistic (5–15 seconds minimum)
✅ Do not exceed the built-in rate limit
✅ Monitor logs and behavior closely

⛔ Do not use this tool for spam or messages without consent
⛔ Avoid sending to unknown or blocked contacts
⛔ Follow WhatsApp Terms of Service and local messaging regulations

---

## 🛠️ Troubleshooting

### ❌ "WA Web init failed"
- WhatsApp Web may not be loaded
- Ensure the browser is logged in at `https://web.whatsapp.com`
- Refresh the page or restart the browser

### ❌ "New Chat button not found"
- Image matching failed
- Re-capture `new_chat.png`
- Use your current screen resolution and WhatsApp layout
- Adjust `CONF_DEFAULT` lower in `config.py` if needed

### ❌ "No results found" for valid numbers
- Verify phone numbers in `Data/contacts.csv`
- Ensure formatting matches supported patterns
- Check that the number is actually registered on WhatsApp

### ❌ Campaign stops mid-run
- Check `Data/whatsapp_state.json`
- Re-run with `retry_failed=True`
- Confirm browser and WhatsApp Web are still active

### ❌ PyAutoGUI failsafe triggered
- Do not move cursor to top-left while the script runs
- If triggered accidentally, restart the script

---

## 📈 Performance Tips

- Use small batches for safe testing: `batch_limit=5`
- Increase `delay_min`/`delay_max` for slower, safer runs
- Use stable WhatsApp UI screenshots for reliable detection
- Keep your machine idle while automation is running

---

## 🧠 Advanced Usage

### Resume Previous Campaign
The tool automatically skips already-sent contacts. Simply run again to continue.

### Custom Message Logic
You can customize `generate_message()` with specialized text or conditional templates.

### Export Statistics
Use `campaign.summary()` to print totals:

```python
summary = campaign.summary()
print(f"Total: {summary['total']}")
print(f"Sent: {summary['sent']}")
print(f"Failed: {summary['failed']}")
print(f"Skipped: {summary['skipped']}")
```

---

## 🤝 Contributing & Support

- Report bugs via GitHub Issues
- Suggest improvements or new automation features
- Share updated screenshot templates and message templates

---

## 📄 License

MIT License — use and modify responsibly.

Made with ❤️ by Adeel Abbasi | 2026

> Automate smartly, message respectfully, and keep your campaign safe.
