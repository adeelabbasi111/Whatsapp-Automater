# WhatsApp Automater

A Windows-based WhatsApp Web automation tool for sending bulk personalized messages with human-like typing, delays, and campaign state tracking.

## Project Overview

This project automates WhatsApp Web using `pyautogui`, `win32gui`, and `win32clipboard` to:

- open or focus WhatsApp Web in the browser
- start a new chat with a phone number
- verify whether the contact is registered on WhatsApp
- send a message and optionally a photo
- manage campaign state across runs
- log success, skipped, and failed contacts
- behave more like a human with typos, timing variation, and mouse movement

## Key Features

- Personalized message generation using `Data/messages.txt`
- Contact import from `Data/contacts.csv`
- State persistence in `Data/whatsapp_state.json`
- Activity logging in `Data/whatsapp_log.txt`
- Human-like automation in `human_gui.py`
- Rate limiting and random waiting to reduce spam-like behavior
- Batch limit support for partial campaign runs

## Requirements

- Windows OS
- Python 3.8+ (recommended)
- `pyautogui`
- `pillow`
- `pywin32`

## Installation

1. Open a terminal in the project root.
2. Create a virtual environment (strongly recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install pyautogui pillow pywin32
```

> Note: This project uses Windows clipboard and window control APIs, so it is designed for Windows only.

## Project Files

- `main.py` - entry point to initialize the bot and run the campaign
- `whatsapp_handler.py` - WhatsApp Web automation logic
- `campaign_manager.py` - campaign flow, contact parsing, state management, logging
- `human_gui.py` - human-like typing/mouse behavior utilities
- `config.py` - paths, timing, and confidence settings
- `Data/contacts.csv` - phone numbers and contact names
- `Data/messages.txt` - message templates separated by `---`
- `images/` - screenshot templates for WhatsApp UI elements
- `Data/whatsapp_state.json` - campaign state and sent/failed tracking
- `Data/whatsapp_log.txt` - plain text log of all campaign actions

## Configuration

### Contact CSV

`Data/contacts.csv` should contain a header and phone numbers. Example:

```csv
Display Name,Mobile Phone
Adeel,+923215773211
```

The campaign manager supports cleaning these phone numbers and converting local Pakistani numbers like `03XXXXXXX` to `+92...`.

### Messages

`Data/messages.txt` stores message templates separated by `---`.

Example:

```
Hello {name}! This is a sample random message.
---
Hi {name}! This project uses external text files.
```

The `{name}` placeholder is replaced with each contact's name at send time.

### Images

The `images/` directory should contain UI element screenshots for WhatsApp Web automation, including:

- `new_chat.png`
- `no_results_found.png`
- `chat_input.png`
- `Poster.png`
- `search_icon.png`
- `send_message.png`
- `add_photo.png`
- `add_attachment.png`

If the UI changes or the screenshots fail, re-capture these images at the correct screen resolution and file names.

## How to Use

1. Open `main.py` or run it from the terminal.
2. Make sure your browser can open WhatsApp Web and you are logged in.
3. Run:

```powershell
python main.py
```

4. The automation will:
   - open/focus WhatsApp Web
   - wait for the New Chat button
   - send messages to pending contacts from `Data/contacts.csv`
   - update `Data/whatsapp_state.json` and `Data/whatsapp_log.txt`

## Campaign Options

`main.py` calls `campaign.run(...)` with the following important arguments:

- `delay_min` and `delay_max`: random wait between messages
- `batch_limit`: maximum number of messages to send in this run (`None` for all pending)
- `retry_failed`: whether to retry contacts that previously failed

Example configuration in `main.py`:

```python
campaign.run(
    bot=bot,
    delay_min=60, delay_max=150,
    batch_limit=10,  # Set to None for full run
    retry_failed=False
)
```

## Logs and State

- `Data/whatsapp_state.json` stores what has been sent, skipped, or failed.
- `Data/whatsapp_log.txt` stores timestamped entries for every action.
- The bot automatically skips contacts not registered on WhatsApp.

## Best Practices

- Keep your browser size and WhatsApp layout consistent with the screenshot templates.
- Ensure WhatsApp Web is logged in before running.
- Start with a small `batch_limit` first to verify behavior.
- Update `Data/messages.txt` with your own content and placeholders.
- Use `Poster.png` in `images/` if you want to send an image part of the campaign.

## Troubleshooting

- If `new_chat.png` or other image matching fails, recapture the screenshot and save it in `images/`.
- If the bot cannot focus WhatsApp, manually open WhatsApp Web and log in first.
- If your contact numbers are not recognized, verify the CSV formatting and phone cleaning rules.
- If the script fails while typing, avoid moving the mouse or interfering with the keyboard during execution.

## Customization

- Add or modify message templates in `Data/messages.txt`.
- Add new contacts to `Data/contacts.csv`.
- Tweak timing values in `config.py` for speed and safety.
- Improve UI matching by updating the screenshot files in `images/`.

## Safety Notes

This tool automates UI actions and should be used responsibly. Avoid sending spam or violating WhatsApp terms of service.

---

Enjoy using `WhatsApp Automater`!
