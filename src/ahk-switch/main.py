# main.py (WSL2 version)

from loguru import logger
from pynput import keyboard as pynput_kb

from find_ahk import find_ahk
from switch_ahk import switch


class HotkeyState:
    def __init__(self):
        self.alt_pressed = False
        self.scripts = find_ahk(extension=".py")

    def on_press(self, key):
        print("ON_PRESS:", repr(key))
        if key == pynput_kb.Key.alt_l:
            self.alt_pressed = True
            print(" alt_l detected")
        elif self.alt_pressed:
            if hasattr(key, "char") and key.char == "1":
                print("Alt+1 pressed")
                if self.scripts:
                    script_path = self.scripts[0]
                    logger.info("Switching to: {}", script_path)
                    switch(script_path)
            self.alt_pressed = False

    def on_release(self, key):
        if key == pynput_kb.Key.alt_l:
            self.alt_pressed = False
        elif key == pynput_kb.Key.esc:
            return False  # stop on Esc


def main():
    logger.info("Searching for scripts...")
    scripts = find_ahk(extension=".py")
    if not scripts:
        print("No scripts found!")
        return

    for index in range(min(9, len(scripts))):
        key_num = index + 1
        script_path = scripts[index]
        print(f"Alt+{key_num} → {script_path}")

    print("Listening for Alt+1. Press Esc to exit.")
    state = HotkeyState()
    with pynput_kb.Listener(
        on_press=state.on_press,
        on_release=state.on_release,  # pyright: ignore
    ) as listener:
        listener.join()


if __name__ == "__main__":
    main()
