from abc import ABC, abstractmethod
from typing import List

from transcribe.entities import Episode


class EpisodeRepositoryInterface(ABC):
    @abstractmethod
    def add(self, episode: Episode):
        ...

    @abstractmethod
    def get(self, episode_id: str) -> Episode:
        ...

    @abstractmethod
    def list(self) -> List[Episode]:
        ...
