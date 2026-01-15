"""Creator module for generating new skill files autonomously."""

import os
import random
from pathlib import Path
from datetime import datetime


CONCEPTS = [
    {
        "name": "MathUtils",
        "description": "Utility math functions such as fibonacci.",
        "template": """
from typing import List


def fibonacci(n: int) -> List[int]:
    '''Return the Fibonacci sequence up to n terms.'''
    if n <= 0:
        return []
    if n == 1:
        return [0]
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq
""",
    },
    {
        "name": "TextProcessor",
        "description": "Simple text processing utilities.",
        "template": """
from collections import Counter
from typing import Dict


def word_frequencies(text: str) -> Dict[str, int]:
    '''Count word frequencies in the given text.'''
    words = [w.strip('.,!?;:\"\'()).lower() for w in text.split() if w.strip()]
    return dict(Counter(words))


def top_k_words(text: str, k: int = 5) -> Dict[str, int]:
    '''Return the top-k most common words.'''
    freqs = Counter([w.strip('.,!?;:\"\'()).lower() for w in text.split() if w.strip()])
    return dict(freqs.most_common(k))
""",
    },
    {
        "name": "DataLogger",
        "description": "Lightweight file-based logger.",
        "template": """
from datetime import datetime
from pathlib import Path
from typing import Any


LOG_FILE = Path(__file__).parent / "logs.txt"


def log_event(event: str, payload: Any = None) -> None:
    '''Append an event with timestamp to the log file.'''
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.utcnow().isoformat()}Z | {event} | {payload}\n"
    with LOG_FILE.open('a', encoding='utf-8') as fh:
        fh.write(line)
""",
    },
]


class Creator:
    """AI module creator - generates new skill modules autonomously"""
    
    def __init__(self, base_dir=None):
        self.base_dir = base_dir
        self.concepts = CONCEPTS
    
    def create_skill(self):
        """Create a new skill module"""
        return create_new_skill(self.base_dir)
    
    def list_concepts(self):
        """List available skill concepts"""
        return [c['name'] for c in CONCEPTS]


def create_new_skill(base_dir: str | None = None) -> str:
    """Generate a new skill file from a random concept and return its path."""
    root = Path(base_dir) if base_dir else Path(__file__).parent.parent / "skills"
    root.mkdir(parents=True, exist_ok=True)

    concept = random.choice(CONCEPTS)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    suffix = random.randint(100, 999)
    filename = f"skill_{concept['name'].lower()}_{timestamp}_{suffix}.py"
    filepath = root / filename

    header = (
        f"""
# Auto-generated skill module
# Concept: {concept['name']}
# Created: {datetime.utcnow().isoformat()}Z
# Description: {concept['description']}
"""
    )

    content = f"{header}\n{concept['template']}\n"
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


if __name__ == "__main__":
    path = create_new_skill()
    print(f"Created new skill at: {path}")
