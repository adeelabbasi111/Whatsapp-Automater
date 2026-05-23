# human.py
"""
HumanGui Class - Simulates realistic human typing & mouse behavior
- Variable typing speed with typos & corrections
- Bezier curve mouse movement with hesitation & tremor
- Human-like delays & random background activities
"""

import random
import pyautogui as pag
import math
import time


class HumanGui:
    """Simulates human-like interactions for automation."""

    def __init__(self):
        # PyAutoGUI safe settings
        pag.FAILSAFE = True  # Move mouse to top-left to abort
        pag.PAUSE = 0.0  # Disable default delay for custom control

    def __getattr__(self, name):
        """
        Agar koi function is class mein nahi milta,
        toh yeh usay automatically pyautogui mein dhoonde ga.
        """
        return getattr(pag, name)

    # ==================== TYPO GENERATION ====================
    def _get_typo_char(self, char: str) -> str:
        """Returns a neighboring QWERTY key for realistic mistakes."""
        keyboard_neighbors = {
            'q': ['w', 'a', '1', '2'], 'w': ['q', 'a', 's', 'e'],
            'e': ['w', 's', 'd', 'r'], 'r': ['e', 'd', 'f', 't'],
            't': ['r', 'f', 'g', 'y'], 'y': ['t', 'g', 'h', 'u'],
            'u': ['y', 'h', 'j', 'i'], 'i': ['u', 'j', 'k', 'o'],
            'o': ['i', 'k', 'l', 'p'], 'p': ['o', 'l', '[', ']'],
            'a': ['q', 'w', 's', 'z'], 's': ['a', 'w', 'e', 'd', 'x', 'z'],
            'd': ['s', 'e', 'r', 'f', 'c', 'x'], 'f': ['d', 'r', 't', 'g', 'v', 'c'],
            'g': ['f', 't', 'y', 'h', 'b', 'v'], 'h': ['g', 'y', 'u', 'j', 'n', 'b'],
            'j': ['h', 'u', 'i', 'k', 'm', 'n'], 'k': ['j', 'i', 'o', 'l', 'm'],
            'l': ['k', 'o', 'p', ';'], 'z': ['a', 's', 'x'],
            'x': ['z', 's', 'd', 'c'], 'c': ['x', 'd', 'f', 'v'],
            'v': ['c', 'f', 'g', 'b'], 'b': ['v', 'g', 'h', 'n'],
            'n': ['b', 'h', 'j', 'm'], 'm': ['n', 'j', 'k', ',']
        }
        is_upper = char.isupper()
        char_lower = char.lower()
        if char_lower in keyboard_neighbors:
            wrong_char = random.choice(keyboard_neighbors[char_lower])
            return wrong_char.upper() if is_upper else wrong_char
        return random.choice('abcdefghijklmnopqrstuvwxyz')

    # ==================== HUMAN NOISE ====================
    def add_human_noise(self):
        """Random background activities jo human karta hai."""
        if random.random() < 0.2:  # 20% chance
            # Random tab switch (Ctrl+Tab)
            pag.hotkey('ctrl', 'tab')
            self.human_wait(random.uniform(1, 3))
            pag.hotkey('ctrl', 'shift', 'tab')  # Back

        if random.random() < 0.15:  # 15% chance
            # Random copy-paste activity
            pag.hotkey('ctrl', 'c')
            self.human_wait(0.3)
            pag.hotkey('ctrl', 'v')

        if random.random() < 0.1:  # 10% chance
            # Accidental key press + correction
            pag.press(random.choice(['shift', 'ctrl', 'alt']))
            time.sleep(0.1)
            pag.press('backspace')

    # ==================== CLICKING ====================
    def click_it(self):
        """Human-like click with variable hold duration + occasional double-click."""
        pag.mouseDown()
        hold = random.uniform(0.08, 0.25)  # Natural press duration
        time.sleep(hold)
        pag.mouseUp()

        # Occasional double-click hesitation (3% chance)
        if random.random() < 0.03:
            time.sleep(random.uniform(0.15, 0.3))
            pag.click()  # Accidental double-click mimic

        self.human_wait(random.uniform(0.2, 0.5))

    # ==================== WAITING ====================
    def human_wait(self, seconds: float, variation: float = 0.4):
        """Base time ± random variation + occasional long pause."""
        delay = seconds * random.uniform(1 - variation, 1 + variation)
        if random.random() < 0.1:  # 10% chance of "distraction"
            delay += random.uniform(2, 8)
        time.sleep(max(0.1, delay))  # Minimum 0.1s delay

    # ==================== TYPING ====================
    def type(self, text: str, send: bool = False):
        """Types with variable speed, typos & punctuation pauses."""
        prev_char = ""
        for char in text:
            delay = random.uniform(0.03, 0.11)
            if char == prev_char:
                delay += random.uniform(0.04, 0.07)

            time.sleep(delay)

            # Typing mistake logic (7% chance for alphabets)
            if char.isalpha() and random.random() < 0.07:
                wrong_char = self._get_typo_char(char)
                pag.write(wrong_char)
                time.sleep(random.uniform(0.03, 0.08))
                pag.press('backspace')

            if char == '`':
                pag.hotkey("ctrl","enter")
            else:
                pag.write(char)

            # Punctuation pauses
            if char in ".,!?":
                time.sleep(random.uniform(0.2, 0.5))

            # Space ke baad extra pause (word boundary)
            if char == " ":
                time.sleep(random.uniform(0.08, 0.15))
                if random.random() < 0.08:  # 8% chance of longer pause
                    time.sleep(random.uniform(0.5, 1.2))

            prev_char = char

        # End of message pause
        time.sleep(random.uniform(1, 2))

        if send:
            pag.hotkey("enter")
            time.sleep(random.uniform(1, 2))

    # ==================== MOUSE MOVEMENT ====================
    def move_mouse(self, target_x: float, target_y: float):
        """Bezier curve + hesitation + tremor for human-like mouse movement."""
        start_x, start_y = pag.position()

        # 1. Human Hesitation (Wobble) - target dhundne ka effect
        for _ in range(random.randint(2, 4)):
            pag.moveRel(random.randint(-5, 5), random.randint(-5, 5), duration=0.05)

        # 2. Bezier Curve Logic (natural arc, not straight line)
        dx, dy = target_x - start_x, target_y - start_y
        dist = max(math.hypot(dx, dy), 1)

        # Control point for arc (perpendicular offset)
        nx, ny = -dy / dist, dx / dist
        offset = random.uniform(-0.2, 0.2) * dist
        cx, cy = (start_x + target_x) / 2 + nx * offset, (start_y + target_y) / 2 + ny * offset

        steps = 30
        for i in range(steps + 1):
            t = i / steps
            t_inv = 1 - t
            # Quadratic Bezier formula
            px = t_inv ** 2 * start_x + 2 * t_inv * t * cx + t ** 2 * target_x
            py = t_inv ** 2 * start_y + 2 * t_inv * t * cy + t ** 2 * target_y

            # Hand tremor (Gaussian noise)
            px += random.gauss(0, 1.5)
            if random.random() < 0.05:  # 5% chance of bigger hand shake
                px += random.uniform(-5, 5)
            py += random.uniform(-1, 1)

            pag.moveTo(px, py, duration=0)
            # Speed variation (natural flow)
            time.sleep(random.uniform(0.002, 0.008))

        # 3. Final Snap with Overshoot (humans rarely land perfectly first try)
        pag.moveTo(target_x, target_y, duration=random.uniform(0.1, 0.2))
        time.sleep(random.uniform(0.5, 1.5))