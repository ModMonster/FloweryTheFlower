import json
import os

JSON_FILE = "flowery.json"
SPRITES_FOLDER = "sprites"
VOICES_FOLDER = "voices"


def get_files(folder):
    if not os.path.exists(folder):
        raise FileNotFoundError(f"Missing folder: {folder}")

    return set(os.listdir(folder))


def main():
    sprites = get_files(SPRITES_FOLDER)
    voices = get_files(VOICES_FOLDER)

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        messages = json.load(f)

    missing_sprites = []
    missing_voices = []

    for i, message in enumerate(messages):
        sprite = message.get("sprite") + ".png"
        voice = message.get("voice") + ".wav"

        if sprite not in sprites:
            missing_sprites.append({
                "index": i,
                "text": message.get("text", ""),
                "missing_sprite": sprite
            })

        if voice not in voices:
            missing_voices.append({
                "index": i,
                "text": message.get("text", ""),
                "missing_voice": voice
            })

    if missing_sprites:
        print(f"Missing sprites: {len(missing_sprites)}")
        for item in missing_sprites:
            print(f"[{item['index']}] {item['missing_sprite']} -> {item['text']}")
    else:
        print("All sprites exist!")

    if missing_voices:
        print(f"Missing voices: {len(missing_voices)}")
        for item in missing_voices:
            print(f"[{item['index']}] {item['missing_voice']} -> {item['text']}")
    else:
        print("All voices exist!")

if __name__ == "__main__":
    main()