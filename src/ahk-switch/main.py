from pynput import keyboard
from find_ahk import find_ahk
from switch_ahk import switch


def main() -> None:
    scripts = find_ahk()

    if not scripts:
        print("No scripts found!")
        return

    # build hotkey map
    hotkeys: dict[str, any] = {}  # pyright: ignore
    for i, script_path in enumerate(scripts, 1):
        if i > 9:
            break
        hotkeys[f"<alt>+{i}"] = lambda p=script_path: switch(to=p)
        print(f"Alt+{i} → {script_path}")

    print("Listening... Ctrl+C to exit")

    with keyboard.GlobalHotKeys(hotkeys) as h:
        h.join()


if __name__ == "__main__":
    main()
