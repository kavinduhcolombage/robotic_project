import json
from collections import defaultdict
import random

# Load Whisper transcript with word timestamps
with open("speak1_words.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract all words from all segments
all_words = []
for segment in data["segments"]:
    print(f"Processing segment from {segment['start']} to {segment['end']}")
    if "words" in segment:
        all_words.extend(segment["words"])
        print(f"Found {len(segment['words'])} words in this segment")

print(f"Total words found: {len(all_words)}")

# Parameters
chunk_duration = 1.0  # seconds
gesture_timeline = []
last_chunk_end = 0.0

# Step 1: Group words by time chunk
chunks = defaultdict(list)
for word in all_words:
    chunk_index = int(word["start"] // chunk_duration)
    chunks[chunk_index].append(word)
    print(f"Word '{word['word']}' at {word['start']} added to chunk {chunk_index}")

print(f"Total chunks created: {len(chunks)}")
print(f"Chunks: {sorted(chunks.keys())}")
print(f"Words in each chunk: {[len(chunks[k]) for k in sorted(chunks.keys())]}")
print("first 5 chunks:", {k: chunks[k] for k in sorted(chunks.keys())[:5]})

words = chunks[1]

# # Get chunk timing
# start_time = round(min(w["start"] for w in words), 1)
# print(f"Start time for chunk 1: {start_time}")
# end_time   = max(w["end"] for w in words)
# print(f"End time for chunk 1: {end_time}")
# pause_duration = start_time - last_chunk_end
# print(f"Pause duration for chunk 1: {pause_duration}")

# Step 2: Process each chunk and assign gesture
for chunk_index in sorted(chunks.keys()):
    words = chunks[chunk_index]
    if not words:
        continue

    # Get chunk timing
    start_time = round(min(w["start"] for w in words), 1)
    end_time   = max(w["end"] for w in words)
    pause_duration = start_time - last_chunk_end

    # Simple gesture decision logic
    keywords = [w["word"].lower() for w in words]
    if pause_duration > 0.7:
        gesture = "relax"
    elif any(k in keywords for k in ["welcome", "thank", "today", "introduction"]):
        gesture = "wave"
    elif len(words) > 4:
        gesture = "emphasize"
    else:
        gesture = random.choice(["point", "smallwave"])

    gesture_timeline.append({"time": start_time, "action": gesture})
    last_chunk_end = end_time

# Step 3: Save timeline
with open("gesture_timeline.json", "w", encoding="utf-8") as f:
    json.dump(gesture_timeline, f, indent=2)

# Also print output
print(json.dumps(gesture_timeline, indent=2))
