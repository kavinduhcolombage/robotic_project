import whisper
import json

# Load model (base is fast and accurate enough)
model = whisper.load_model("base")

# Transcribe with word timestamps
result = model.transcribe("speak1.wav", word_timestamps=True)

# Save output as JSON
with open("speak1_words.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)
