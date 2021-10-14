from dataclasses import dataclass

@dataclass
class Match:
    pattern_index: int
    text_index: int
    length: int