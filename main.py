import json
import sys
import os
import pickle
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import requests
import urllib
import playsound3

# holy schnitzel modmonster is using ai guys :O
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load example messages
with open("flowery.json", "r", encoding="utf-8") as f:
    examples = json.load(f)

texts = [e["text"] for e in examples]

if os.path.exists("flowery.pkl"):
    with open("flowery.pkl", "rb") as f:
        cache = pickle.load(f)
        example_embeddings = cache["embeddings"]
else:
    print("Cache file not found, creating now")
    example_embeddings = model.encode(texts, convert_to_tensor=True)

    with open("flowery.pkl", "wb") as f:
        pickle.dump({
            "embeddings": example_embeddings
        }, f)

# Turn the provided message into an embedding
message = sys.argv[1]
message_embedding = model.encode(message, convert_to_tensor=True)

# Compare against examples; score
scores = cos_sim(message_embedding, example_embeddings)[0]
best_index = scores.argmax().item()
best_example = examples[best_index]

print(best_example)

# Write to a file for streamer.bot to read
# with open("out.txt", "w", encoding="utf-8") as file:
#     file.write(best_example["sprite"] + "\n" + best_example["voice"])

# Write text box image
response = requests.get(
    f"https://www.demirramon.com/gen/undertale_text_box.gif?message=character%3Ddeltarune-flowery+mode%3Ddarkworld+box%3Ddeltarune+expression%3D{best_example["sprite"]}+{urllib.parse.quote(message)}",
)

response.raise_for_status()

with open("out-textbox.gif", "wb") as f:
    f.write(response.content)

print(response.url)

# Play sound
playsound3.playsound(f"voices/{best_example["voice"]}.wav")