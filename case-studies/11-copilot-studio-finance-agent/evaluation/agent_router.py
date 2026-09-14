"""Minimal simulation of the Copilot Studio topic routing.

Reads trigger phrases from ../agent-config/topics.yaml and applies the same
priority rules documented in documentation/TEST_CASES.md. It's a stand-in so
the test set can run in CI. It is not the agent.
"""
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOPICS_FILE = HERE.parent / "agent-config" / "topics.yaml"

# Routing priority. Refusals win, then requests, then knowledge topics.
PRIORITY = ["T05", "T04", "T01", "T02", "T03"]
FALLBACK = "T99"


def load_triggers(path: Path = TOPICS_FILE) -> dict[str, list[str]]:
    """Parse the YAML without a dependency. The file is simple enough."""
    triggers: dict[str, list[str]] = {}
    current_id: str | None = None
    in_triggers = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if stripped.startswith("- id:"):
            current_id = stripped.split(":", 1)[1].strip()
            triggers[current_id] = []
            in_triggers = False
            continue
        if current_id and stripped == "triggers:":
            in_triggers = True
            continue
        if in_triggers:
            if stripped.startswith("- "):
                phrase = stripped[2:].split("#", 1)[0].strip()
                triggers[current_id].append(phrase.lower())
                continue
            in_triggers = False
    return triggers


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def route(message: str, triggers: dict[str, list[str]] | None = None) -> tuple[str, str | None]:
    """Return (topic_id, matched_trigger)."""
    triggers = triggers or load_triggers()
    text = normalize(message)
    for topic_id in PRIORITY:
        for phrase in triggers.get(topic_id, []):
            if normalize(phrase) in text:
                return topic_id, phrase
    return FALLBACK, None
