# campaign_manager.py
import csv, json, os, re, time, random
from datetime import datetime
from typing import Dict, List, Optional, Any
from config import CSV_PATH, STATE_FILE, LOG_FILE , IMAGES_DIR
import pyautogui as pag

class WhatsAppCampaignManager:
    """Manages contacts, campaign state, logging & execution."""
    def __init__(self, csv_path: str = CSV_PATH, state_file: str = STATE_FILE, log_file: str = LOG_FILE):
        self.csv_path, self.state_file, self.log_file = csv_path, state_file, log_file
        self.contacts = []
        self.state = {"sent":{}, "failed":{}, "skipped":{}, "stats":{"total":0, "sent":0, "failed":0, "skipped":0}}
        self._load_state()
        self._parse_contacts()

    def _load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for k in self.state: self.state[k].update(data.get(k, {}))
            except: print("⚠️ Corrupt state. Starting fresh.")

    def _save_state(self):
        self.state["last_updated"] = datetime.now().isoformat()
        tmp = self.state_file + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f: json.dump(self.state, f, indent=2, ensure_ascii=False)
        os.replace(tmp, self.state_file)  # Atomic write (crash-safe)

    def _clean_phone(self, raw: str) -> Optional[str]:
        if not raw: return None
        d = re.sub(r'\D', '', raw)
        if d.startswith("0") and len(d)==11: return f"+92{d[1:]}"
        if d.startswith("92") and len(d)==12: return f"+{d}"
        if d.startswith("+92") and len(d)==13: return d
        if 10 <= len(d) <= 13: return f"+{d}"
        return None

    def _parse_contacts(self):
        try:
            with open(self.csv_path, "r", encoding="utf-8-sig") as f:
                for row in csv.DictReader(f):
                    name = row.get("Display Name", row.get("First Name", "")).strip() or "Unknown"
                    phone = self._clean_phone(row.get("Mobile Phone", "").strip())
                    if phone: self.contacts.append({"name":name, "phone":phone})
        except Exception as e: print(f"❌ CSV error: {e}")
        self.state["stats"]["total"] = len(self.contacts)
        print(f"📊 Loaded {len(self.contacts)} contacts.")

    def _log(self, phone, name, status, detail=""):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {status:8} | {name:25} | {phone:15} | {detail}\n")

    def get_pending(self) -> List[Dict]:
        return [c for c in self.contacts if c["phone"] not in self.state["sent"] and c["phone"] not in self.state["failed"]]

    import random

    def generate_message(self, name):

        with open("Data/messages.txt", "r", encoding="utf-8") as file:
            content = file.read()

        messages = content.split("---")

        # extra spaces/newlines remove
        messages = [msg.strip() for msg in messages if msg.strip()]

        selected_message = random.choice(messages)

        return selected_message.format(name=name)

    def run(self, bot: Any, delay_min=60, delay_max=150, batch_limit: Optional[int]=None, retry_failed=False):
        if not bot: raise ValueError("Bot instance required.")
        pending = self.get_pending()
        if retry_failed:
            for c in self.contacts:
                if c["phone"] in self.state["failed"] and c["phone"] not in self.state["sent"]:
                    pending.append(c); del self.state["failed"][c["phone"]]
        if not pending: print("✅ No pending contacts."); return

        print(f"\n🚀 Campaign: {len(pending)} pending")
        sent = 0
        for i, c in enumerate(pending, 1):
            if batch_limit and sent >= batch_limit: print("⏹️ Batch limit."); break
            phone, name = c["phone"], c["name"]
            print(f"\n📤 [{i}/{len(pending)}] {name} ({phone})")

            if not bot.start_new_chat(phone):
                print(f"⏭️ Skipped (Not registered)")
                self.state["skipped"][phone] = {"name":name, "reason":"Not on WA", "time":datetime.now().isoformat()}
                self.state["stats"]["skipped"] += 1
                self._log(phone, name, "SKIPPED", "No WA")
                self._save_state(); continue

            try:
                time.sleep(random.uniform(0.8, 1.5))

                if random.uniform(0,1) < 0.3:
                    bot.send_photo(IMAGES_DIR+"/Poster.png")
                time.sleep(random.uniform(0.8, 1.5))
                message = self.generate_message(name)
                bot.send_text(message)
                self.state["sent"][phone] = {"name":name, "time":datetime.now().isoformat(), "preview":message[:50]}
                self.state["stats"]["sent"] += 1; sent += 1
                self._log(phone, name, "SUCCESS"); self._save_state()
                wait = random.uniform(delay_min, delay_max)
                print(f"⏳ Waiting {wait:.0f}s..."); time.sleep(wait)
            except Exception as e:
                err = str(e)[:100]
                print(f"❌ Failed: {err}")
                self.state["failed"][phone] = {"name":name, "time":datetime.now().isoformat(), "reason":err}
                self.state["stats"]["failed"] += 1
                self._log(phone, name, "FAILED", err); self._save_state()
                time.sleep(random.uniform(15, 30))

        print(f"\n✅ Done. Sent: {sent}")
        return sent

    def summary(self): return self.state["stats"]