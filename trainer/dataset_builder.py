import json
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter

def select_from_list(title, options):
    print("\n" + title)

    completer = FuzzyWordCompleter(options)

    result = prompt(
        "> ",
        completer=completer
    )

    return result

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("messages.txt", "r") as f:
    messages = f.readlines()

print(f"{len(messages)} messages loaded.")

# Load dataset
try:
    with open("../flowery.json", "r") as f:
        examples = json.load(f)

except FileNotFoundError:
    examples = []

already_done = set()

for example in examples:
    already_done.add(example["text"].lower())

example_texts = [x["text"] for x in examples]

if example_texts:
    example_embeddings = model.encode(example_texts)
else:
    example_embeddings = []

# Load possible sprites/voices
voices = sorted([
    os.path.splitext(x)[0]
    for x in os.listdir("../voices")
])

sprites = sorted([
    os.path.splitext(x)[0]
    for x in os.listdir("../sprites")
])

for message in messages:
    if message.lower() in already_done:
        continue
    message = message.replace("\n", "")
    print(message)
    message_embedding = model.encode(message)
    if len(example_embeddings):
        similarities = cos_sim(
            message_embedding,
            example_embeddings
        )[0]

        # Top 3 most similar examples
        top = similarities.argsort(descending=True)[:3]

        print("\nTop matches:\n")

        for i, idx in enumerate(top):

            example = examples[idx]

            score = similarities[idx].item()

            print(
                f"{i+1}) "
                f"{score:.3f}  "
                f"{example['text']}"
            )

            print(
                f"   {example['voice']} / {example['sprite']}"
            )

        print()

        suggestion = examples[top[0]]

        print()
        print("Suggested: " + suggestion["voice"] + " " + suggestion["sprite"])
    choice = input(
        "\nEnter=Use best  1-3=Use suggestion  E=Custom  S=Skip\n> "
    ).lower()

    if (choice == ""):
        choice = "1"

    if choice in ["1", "2", "3"]:
        selected = examples[top[int(choice)-1]]

        examples.append({
            "text": message,
            "voice": selected["voice"],
            "sprite": selected["sprite"]
        })

        already_done.add(message.lower())
        print("Saved.")
    elif choice == "e":
        voice = select_from_list(
            "Voice:",
            voices
        )

        sprite = select_from_list(
            "Sprite:",
            sprites
        )

        examples.append({
            "text": message,
            "voice": voice,
            "sprite": sprite
        })

        already_done.add(message.lower())

        print("Saved.")
    with open("../flowery.json", "w") as f:
        json.dump(examples, f, indent=2)