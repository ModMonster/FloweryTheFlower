import json
import sys

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# holy schnitzel modmonster is using ai guys :O
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load example messages
with open("flowery.json", "r") as f:
    examples = json.load(f)

texts = [e["text"] for e in examples]

# Turn every example into an embedding
example_embeddings = model.encode(texts)

# Turn the provided message into an embedding
message = sys.argv[1]
message_embedding = model.encode(message)

# Compare against examples; score
scores = cos_sim(message_embedding, example_embeddings)[0]
best_index = scores.argmax().item()
best_example = examples[best_index]

print(best_example)

# Write to a file for streamer.bot to read
with open("out.txt", "w") as file:
    file.write(best_example["sprite"] + "\n" + best_example["voice"])