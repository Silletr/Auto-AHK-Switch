# main.py (WSL2 version)
from switch_ahk import switch
from find_ahk import find_ahk
from pynput import keyboard as pynput_kb
from loguru import logger
from time import sleep

# Writing on WSL2, but tests on Windows 11 25H2 Pro
# So many info cuz it may affect in future when will be new updates


kb = pynput_kb.Controller()


def paste_to_cursor(text: str) -> None:
    sleep(2)
    kb.type(text)


class HotkeyState:
    def __init__(self):
        self.alt_pressed = False
        self.scripts = find_ahk()

    def on_press(self, key) -> bool | None:
        if key == pynput_kb.Key.alt_l:
            self.alt_pressed = True
        elif self.alt_pressed:
            if hasattr(key, "char") and key.char in "123456789":
                idx = int(key.char) - 1
                if idx < len(self.scripts):
                    script_path = self.scripts[idx]  # use cached self.scripts
                    logger.info("Switching to: {}", script_path)
                    # release alt BEFORE any keyboard magic
                    kb.release(pynput_kb.Key.alt_l)
                    kb.release(pynput_kb.Key.alt)

                    kb.press(pynput_kb.Key.esc)
                    kb.release(pynput_kb.Key.esc)
                    sleep(0.5)

                    output = switch(script_path)  # returns stdout
                    if output:
                        paste_to_cursor(output.strip())
                    else:
                        print(output)
            self.alt_pressed = False

        return None

    def on_release(self, key) -> bool | None:
        if key == pynput_kb.Key.alt_l:
            self.alt_pressed = False
        elif key == pynput_kb.Key.alt_r:
            return False  # pynput stops listener on False
        return None


def main():
    logger.info("Searching for scripts...")
    scripts = find_ahk()
    for index in range(min(9, len(scripts))):
        key_num = index + 1
        script_path = scripts[index]
        print(f"Alt+{key_num} → {script_path}")

    print("Listening for Alt+1. Press Esc to exit.")
    state = HotkeyState()
    if not state.scripts:
        print("No scripts found!")
        return

    for index, script_path in enumerate(state.scripts[:9]):
        print(f"Alt+{index + 1} → {script_path}")

    print("Listening for Alt+1. Press Right Alt to exit.")
    with pynput_kb.Listener(
        on_press=state.on_press,
        on_release=state.on_release,  # pyright: ignore
    ) as listener:
        listener.join()


if __name__ == "__main__":
    main()
