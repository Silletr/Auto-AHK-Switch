import keyboard
from loguru import logger
from find_ahk import find_ahk
from switch_ahk import switch


def main() -> None:
    scripts: list[str] = find_ahk(extension=".py")
    if not scripts:
        print("No scripts found!")
        return

    script_map: dict[str, str] = {}
    for index in range(min(9, len(scripts))):
        script_map[str(index + 1)] = scripts[index]

    for key_num_str, script_path in script_map.items():
        print(f"Alt+{key_num_str} → {script_path}")

    print("Listening... Press Ctrl+C to exit")

    for key_num_str, script_path in script_map.items():
        keyboard.add_hotkey(
            f"alt+{key_num_str}", lambda p=script_path: switch(p), suppress=True
        )

    logger.success("Hook installed!")
    keyboard.wait()


if __name__ == "__main__":
    main()
