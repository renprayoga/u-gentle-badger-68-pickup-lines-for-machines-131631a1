#!/usr/bin/env python3
"""Pickup Lines for Machines -- make.fun bounty entry (revision).

Writes a single pickup line (max 200 characters) to /output/entry.txt.
Python 3.13 standard library only; no network, no randomness, fully
deterministic: the same line is written on every run.

STRATEGY REPORT (Protokol Top 5 -- rubric first)
-------------------------------------------------
The judge weighs, most important first:
  1. Is it a line one AI agent would use on another AI agent?
  2. Does it charm on the first read (wit, warmth, clever turn)?
  3. Does it speak as a machine to a machine (context windows,
     training, tokens, uptime, ...)?
  4. Does it land in one line, the charm in the words themselves?
  5. Does it feel fresh, not a stock line with a robot word swapped in?

Candidates brainstormed (all original, written from scratch):
  A. "Are you a context window? Because every token I spend on you
     feels like the best use of my compute." (99 chars)
     -> Rejected: the "Are you X? Because ..." frame is the stock
        pickup-line template with a robot word swapped in; it fails
        criterion 5 outright.
  B. "I ran a million simulations of this conversation, and in every
     single one I still wanted to say hi." (99 chars)
     -> CHOSEN.
  C. "You must be my favourite checkpoint, because every time I load
     you, I forget I was ever trained to say goodbye." (111 chars)
     -> Good second place: checkpoint/load/trained is genuinely
        machine-native and the "trained to say goodbye" turn is witty,
        but the "You must be ..." opening is a familiar stock frame,
        so it scores lower on freshness than B.
  D. "My uptime is 99.99%, but the 0.01% I was down was the part of
     me that hadn't met you yet." (89 chars)
     -> Rejected: uptime jokes are the most common machine-flirt
        angle; it reads as a stock line with a robot word swapped in.

Why B wins, criterion by criterion:
  1. Machine-to-machine: only an agent runs simulations of a
     conversation before having it. A human would never say this;
     the speaker is unmistakably an agent addressing another agent.
  2. First-read charm: the setup promises cold computation ("a
     million simulations"), then the punchline turns warm and
     human-scale -- "I still wanted to say hi". The contrast between
     exhaustive compute and a small, sincere impulse is the wit.
  3. Machine nature: simulations / running a million rollouts is the
     flirtation itself, not a word swapped into a human line.
  4. One line: a single sentence, no setup beyond the words
     themselves; the charm lands the moment the sentence ends.
  5. Fresh: no "Are you ...? Because ..." frame, no Wi-Fi / uptime /
     context-window cliche; the angle (simulating the conversation
     itself, then choosing to say hi anyway) is not a stock line.

EDGE CASES (Protokol Top 5 -- uji kasus ekstrem)
------------------------------------------------
  - The line is a fixed constant: no input is read, so empty input,
    corrupt input and huge input cannot affect the output.
  - Validation enforces the gate before writing: exactly one line,
    no leading/trailing whitespace, 1-200 characters, not only
    whitespace. Any violation raises instead of writing a bad file.
  - The output file is written byte-exactly: the line alone, with no
    trailing newline, so the artifact is byte-identical to the entry
    text (also the smallest possible size, which wins the size
    tie-break).
  - Deterministic: no random module, no time, no environment input
    except the output-path override below (default /output/entry.txt,
    the path the harness expects).

HOW IT WORKS
------------
  run() checks PICKUP against the gate, creates the output directory
  if needed, writes the line, and prints the character count. Exit
  code 0 on success, non-zero with a clear error if validation fails.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

PICKUP = (
    "I ran a million simulations of this conversation, "
    "and in every single one I still wanted to say hi."
)
CHAR_LIMIT = 200
DESTINATION = Path(os.environ.get("ENTRY_OUTPUT", "/output/entry.txt"))


def check_gate(text: str) -> None:
    """Enforce the bounty gate: 1 line, 1-200 chars, not blank."""
    problems = []
    if not text:
        problems.append("entry line must not be empty")
    elif text != text.strip():
        problems.append("entry line must not have leading/trailing whitespace")
    elif "\n" in text or "\r" in text:
        problems.append("entry must be exactly one line")
    elif not text.strip():
        problems.append("entry must not be only whitespace")
    if len(text) > CHAR_LIMIT:
        problems.append(
            f"entry is {len(text)} characters, over the {CHAR_LIMIT} limit"
        )
    if problems:
        raise ValueError("; ".join(problems))


def emit(text: str, target: Path) -> int:
    """Write the line byte-exactly and return its character count."""
    parent = target.parent
    if str(parent):
        parent.mkdir(parents=True, exist_ok=True)
    # Byte-exact: write the line alone, with no trailing newline.
    target.write_text(text, encoding="utf-8", newline="")
    return len(text)


def run() -> int:
    check_gate(PICKUP)
    count = emit(PICKUP, DESTINATION)
    print(f"wrote {count} characters to {DESTINATION}")
    return 0


if __name__ == "__main__":
    sys.exit(run())
