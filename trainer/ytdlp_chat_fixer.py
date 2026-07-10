# Take downloaded chat jsons from yt-dlp and convert them to one message per line txt format (input file is downloaded.json)
import json

def extract_text_from_runs(runs):
    text = ""

    for run in runs:
        if "text" in run:
            text += run["text"]

        elif "emoji" in run:
            # Keep emojis because they are useful for Flowery reactions
            text += run["emoji"].get("emojiId", "")

    return text.strip()


def convert_chat(input_file):
    messages = []

    with open(input_file, "r") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                data = json.loads(line)

            except json.JSONDecodeError:
                continue


            try:
                actions = (
                    data["replayChatItemAction"]
                    ["actions"]
                )

            except KeyError:
                continue

            for action in actions:
                try:
                    item = (
                        action["addChatItemAction"]
                        ["item"]
                    )

                except KeyError:
                    continue

                # Normal text messages
                if "liveChatTextMessageRenderer" in item:
                    renderer = (item["liveChatTextMessageRenderer"])
                    runs = (renderer["message"]["runs"])
                    message = extract_text_from_runs(runs)

                    if message:
                        messages.append(message)

                # Super chats / highlighted messages
                elif "liveChatPaidMessageRenderer" in item:
                    renderer = (item["liveChatPaidMessageRenderer"])
                    runs = (renderer["message"]["runs"])
                    message = extract_text_from_runs(runs)

                    if message:
                        messages.append(message)

    return messages

def clean_messages(messages):
    cleaned = []
    seen = set()

    for message in messages:
        message = message.strip()

        # Ignore empty
        if not message:
            continue

        # Ignore super short junk
        if len(message) < 3:
            continue

        # Remove duplicates
        key = message.lower()

        if key in seen:
            continue

        seen.add(key)
        cleaned.append(message)

    return cleaned

if __name__ == "__main__":
    input_file = "downloaded.json"
    print("Reading chat...")
    messages = convert_chat(input_file)
    print(f"Found {len(messages)} messages")
    print("Cleaning...")
    messages = clean_messages(messages)
    print(f"Keeping {len(messages)} messages")
    with open("messages.txt", "w") as f:
        for message in messages:
            f.write(message + "\n")

    print("Saved messages.txt")