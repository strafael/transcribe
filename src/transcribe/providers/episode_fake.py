from typing import List

from transcribe.entities import Episode
from transcribe.interfaces import EpisodeRepositoryInterface


class EpisodeFakeRepository(EpisodeRepositoryInterface):
    def __init__(self):
        self._episodes = set()
        with open("tests/testdata/episode_1.txt") as fp:
            text = fp.read()

        episode = Episode.from_transcript_text("episode_1", text)
        self.add(episode)

    def add(self, episode: Episode):
        self._episodes.add(episode)

    def get(self, episode_id: str) -> Episode:
        for e in self._episodes:
            if e.episode_id == episode_id:
                return e

    def list(self) -> List[Episode]:
        return list(self._episodes)
