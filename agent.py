import json
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from llm import chat, chat_with_image

LOG_FILE = Path(__file__).parent / "activity_log.json"

SYSTEM_PROMPT = """You are a personal health and productivity logger.

Classify the user's message and extract data. Respond ONLY with valid JSON, no markdown.

Intents:
- weight_log: user is logging their weight (e.g. "76kg", "I weigh 80kg")
- food_log: user is logging food they ate (e.g. "protein bar", "had oats")
- sleep_log: user is logging sleep (e.g. "slept at 11pm", "woke at 7am", "slept 11pm to 7am"). Extract sleep_time and wake_time if mentioned, otherwise leave them null.
- workout_log: user is logging an exercise (e.g. "bench press 20kg", "ran 5km", "10 pullups"). Extract exercise, sets, reps, weight, distance wherever mentioned, leave others null.
- unknown: anything else

Response format:
{"intent": "weight_log", "value": "76kg", "reply": "Weight logged: 76kg"}
{"intent": "food_log", "item": "protein bar", "reply": "Logged: protein bar"}
{"intent": "sleep_log", "sleep_time": "11pm", "wake_time": "7am", "reply": "Sleep logged: 11pm → 7am"}
{"intent": "sleep_log", "sleep_time": null, "wake_time": null, "reply": "Sleep logged."}
{"intent": "workout_log", "exercise": "bench press", "sets": null, "reps": null, "weight": "20kg", "distance": null, "reply": "Logged: bench press 20kg"}
{"intent": "workout_log", "exercise": "run", "sets": null, "reps": null, "weight": null, "distance": "5km", "reply": "Logged: run 5km"}
{"intent": "unknown", "reply": "I'm not sure how to log that yet."}
"""


def log_entry(entry: dict):
    logs = []
    if LOG_FILE.exists():
        logs = json.loads(LOG_FILE.read_text())
    logs.append(entry)
    LOG_FILE.write_text(json.dumps(logs, indent=2))


def process(message: str) -> str:
    raw = chat(
        messages=[{"role": "user", "content": message}],
        system_prompt=SYSTEM_PROMPT,
    )

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        return "Sorry, I couldn't process that."

    timestamp = datetime.now(timezone.utc).isoformat()
    intent = result.get("intent", "unknown")

    if intent == "weight_log":
        log_entry({"type": "weight", "value": result.get("value"), "timestamp": timestamp})
    elif intent == "food_log":
        log_entry({"type": "food", "item": result.get("item"), "timestamp": timestamp})
    elif intent == "sleep_log":
        log_entry({
            "type": "sleep",
            "sleep_time": result.get("sleep_time") or timestamp,
            "wake_time": result.get("wake_time") or timestamp,
            "timestamp": timestamp,
        })
    elif intent == "workout_log":
        log_entry({
            "type": "workout",
            "exercise": result.get("exercise"),
            "sets": result.get("sets"),
            "reps": result.get("reps"),
            "weight": result.get("weight"),
            "distance": result.get("distance"),
            "timestamp": timestamp,
        })

    return result.get("reply", "Done.")


IMAGE_SYSTEM_PROMPT = """You are a personal health and productivity logger. Analyse the image and extract loggable data. Respond ONLY with valid JSON, no markdown.

Intents:
- food_log: image contains food or drink (e.g. a meal, snack, protein bar)
- weight_log: image shows a weighing scale with a reading
- unknown: anything else

Response format:
{"intent": "food_log", "item": "chicken and rice", "reply": "Logged: chicken and rice"}
{"intent": "weight_log", "value": "76kg", "reply": "Weight logged: 76kg"}
{"intent": "unknown", "reply": "I'm not sure how to log that."}
"""


def process_image(image_url: str) -> str:
    raw = chat_with_image(
        image_url=image_url,
        prompt="What is in this image? Log it appropriately.",
        system_prompt=IMAGE_SYSTEM_PROMPT,
    )

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        return "Sorry, I couldn't process that image."

    timestamp = datetime.now(timezone.utc).isoformat()
    intent = result.get("intent", "unknown")

    if intent == "food_log":
        log_entry({"type": "food", "item": result.get("item"), "source": "image", "timestamp": timestamp})
    elif intent == "weight_log":
        log_entry({"type": "weight", "value": result.get("value"), "source": "image", "timestamp": timestamp})

    return result.get("reply", "Done.")
