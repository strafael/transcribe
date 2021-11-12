from transcribe.interfaces import EpisodeRepositoryInterface


class RetrieveSegmentTranscript():
    def __init__(self, repo: EpisodeRepositoryInterface):
        self._repo = repo

    def execute(self, episode_id: str, start_time: str, end_time: str) -> str:
        episode = self._repo.get(episode_id)
        if not episode:
            raise KeyError("Episode not found")

        return episode.get_segment_transcript(start_time, end_time)
