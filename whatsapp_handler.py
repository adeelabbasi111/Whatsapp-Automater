# whatsapp_handler.py
"""
WhatsApp Web Automation Handler
Simplified flow: New Chat → Type → Check Result → Send
"""
import os
import time
import random
import pyautogui as pag
import win32gui
import win32con
import win32clipboard
from PIL import Image
from io import BytesIO
from pyautogui import ImageNotFoundException

from human_gui import HumanGui
from config import IMAGES_DIR, CONF_DEFAULT, CONF_NO_RESULTS


class WhatsApp:
    """Main handler for WhatsApp Web automation."""

    def __init__(self):
        pag.FAILSAFE = True
        pag.PAUSE = 0.0
        self.daily_message_count = 0
        self.last_message_time = None
        self.bot = HumanGui()

    # ==================== RATE LIMITING ====================
    def _check_rate_limit(self):
        now = time.time()
        if self.daily_message_count >= 30 and now - self.last_message_time < 3600:
            print("⏸️ Rate limit reached. Waiting 30 mins...")
            self.bot.human_wait(1800)
            self.daily_message_count = 0
        if self.last_message_time and now - self.last_message_time < 60:
            self.bot.human_wait(random.uniform(60, 240) - (now - self.last_message_time))
        self.daily_message_count += 1
        self.last_message_time = time.time()

    # ==================== UTILS ====================
    def copy_image_to_clipboard(self, image_path: str):
        img = Image.open(image_path).convert("RGB")
        out = BytesIO();
        img.save(out, "BMP");
        data = out.getvalue()[14:];
        out.close()
        win32clipboard.OpenClipboard();
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        time.sleep(1)

    def wait_for_image(self, image_name: str, timeout: int = 45, confidence: float = CONF_DEFAULT) -> bool:
        path = os.path.join(IMAGES_DIR, image_name)
        print(f"⏳ Waiting for {image_name}...")
        start = time.time()
        while time.time() - start < timeout:
            try:
                if pag.locateOnScreen(path, confidence=confidence):
                    time.sleep(random.uniform(0.3, 0.8))
                    locationy =pag.locateOnScreen(path, confidence=confidence)
                    print(locationy)
                    print(f"✅ Found {image_name}")
                    return True
            except ImageNotFoundException:
                pass
            except Exception as e:
                print(f"⚠️ Img error: {e}"); break
            time.sleep(0.8)
        print(f"❌ Timeout: {image_name}");
        return False

    def focus_browser(self) -> bool:
        def cb(h, res):
            if win32gui.IsWindowVisible(h) and win32gui.GetClassName(
                    h) == "Chrome_WidgetWin_1" and win32gui.GetWindowText(h):
                res.append((h, win32gui.GetWindowText(h)))
            return True

        wins = [];
        win32gui.EnumWindows(cb, wins)
        if not wins: return False
        h, t = wins[0]
        if win32gui.IsIconic(h): win32gui.ShowWindow(h, win32con.SW_RESTORE); time.sleep(0.2)
        win32gui.ShowWindow(h, win32con.SW_MAXIMIZE);
        time.sleep(0.3)
        win32gui.SetForegroundWindow(h);
        time.sleep(0.3)
        print(f"✅ Browser focused: {t}");
        return True

    def open_or_focus_whatsapp(self) -> bool:
        if not self.focus_browser():
            print("⚠️ Opening browser...")
            try:
                os.startfile("microsoft-edge:https://web.whatsapp.com")
            except:
                import webbrowser; webbrowser.open('https://web.whatsapp.com')
            time.sleep(8);
            return True
        time.sleep(random.uniform(0.5, 0.8))
        pag.hotkey('ctrl', '1');
        time.sleep(0.3)
        for _ in range(10):
            pag.hotkey('ctrl', 'l');
            time.sleep(0.15)
            pag.hotkey('ctrl', 'a');
            time.sleep(0.1)
            pag.hotkey('ctrl', 'c');
            time.sleep(0.5)
            if 'web.whatsapp.com' in self._get_clipboard().lower():
                print("✅ WhatsApp Web already open! Refreshing...")
                pag.hotkey('ctrl', 'r');
                time.sleep(random.uniform(3, 5))
                return True
            pag.press('esc')
            pag.hotkey('ctrl', 'tab');
            time.sleep(random.uniform(0.2, 0.4))
        print("🌐 Opening new WA tab...")
        pag.hotkey('ctrl', 't');
        time.sleep(0.6)
        pag.write('https://web.whatsapp.com');
        pag.hotkey('enter');
        time.sleep(6)
        return True

    def _get_clipboard(self) -> str:
        for attempt in range(5):
            try:
                win32clipboard.OpenClipboard()
                try:
                    return win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT) or ""
                finally:
                    win32clipboard.CloseClipboard()
            except:
                time.sleep(0.1 * (attempt + 1))
        return ""

    # ==================== MAIN FLOW (TUMHARI LOGIC) ====================
    def start_new_chat(self, number: str) -> bool:
        """
        Simplified Flow:
        1. Click New Chat
        2. Type Number
        3. Check 'No results found'
        4. If not found -> Down + Enter -> Open Chat
        """
        print(f"🔍 Starting chat with: {number}")

        # 1. New Chat button pe click karo
        if not self.wait_for_image("new_chat.png", timeout=30, confidence=0.6):
            print("❌ New Chat button not found");
            return False
        try:
            loc = pag.locateCenterOnScreen(os.path.join(IMAGES_DIR, "new_chat.png"), confidence=0.6)
            if loc:
                self.bot.move_mouse(loc[0] + random.uniform(-3, 3), loc[1] + random.uniform(-3, 3))
                self.bot.click_it()
                time.sleep(random.uniform(0.6, 1.3))
        except Exception as e:
            print(f"⚠️ Click failed: {e}");
            return False

        # 2. Number type karo (Search bar auto-focus ho jata hai New Chat ke baad)
        pag.hotkey('ctrl', 'a');
        time.sleep(0.1)
        pag.press('backspace');
        time.sleep(0.2)
        pag.write(number.replace('+', ''))
        time.sleep(random.uniform(1, 1.5))  # Results load hone ka wait

        # 3. Check karo: "No results found" dikha ya nahi?
        is_not_registered = False
        try:
            if pag.locateOnScreen("images/no_results_found.png",confidence=0.7):
                is_not_registered = True
        except:
            pass

        if is_not_registered:
            print(f"❌ {number} → Not registered. Skipping...")
            pag.press('esc');
            time.sleep(0.5)
            return False

        # 4. Registered hai → First result select & open karo
        print(f"✅ {number} → Registered. Opening chat...")
        time.sleep(random.uniform(0.3, 0.6))
        pag.press('enter')
        time.sleep(random.uniform(1.5, 2.5))  # Chat open hone ka wait

        # Optional: Chat input verify karo
        try:
            pag.locateOnScreen(os.path.join(IMAGES_DIR, "chat_input.png"), confidence=0.65, timeout=3)
        except:
            pass
        return True

    # ==================== SENDING ====================
    def send_text(self, text: str):
        self.bot.type(text, send=True)
        self._check_rate_limit()

    def send_photo(self, path: str):
        self.copy_image_to_clipboard(path)
        pag.hotkey("ctrl", "v");
        time.sleep(random.uniform(3, 5))
        pag.hotkey("enter")
        self._check_rate_limit()

    def initialize(self) -> bool:
        if self.open_or_focus_whatsapp():
            return self.wait_for_image("new_chat.png", timeout=30, confidence=0.6)
        return False