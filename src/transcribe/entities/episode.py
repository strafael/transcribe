from __future__ import annotations
import re
from dataclasses import dataclass
from datetime import timedelta
from typing import List

from .transcript import Transcript

# This matches transcripts from a transcript format
# It matches when a timestamp is followed by a new line, then captures
# everything until the next new line.
TRANSCRIPT_PATTERN = re.compile(r"(\d+:\d+)\s\s\n(.*?)\n")


@dataclass
class Episode:
    episode_id: str
    transcripts: List[Transcript]

    def get_segment_transcript(self, start_time, end_time) -> str:
        start = timedelta(seconds=start_time)
        end = timedelta(seconds=end_time)
        for t in self.transcripts:
            if start <= t.timestamp < end:
                return t.transcript

    @classmethod
    def from_transcript_text(cls, episode_id: str, text: str) -> Episode:
        transcripts = []
        for timestamp, text in TRANSCRIPT_PATTERN.findall(text):
            t = Transcript.from_dict(dict(timestamp=timestamp, transcript=text))
            transcripts.append(t)

        return cls(episode_id, transcripts)
