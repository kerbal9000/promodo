from textual.widgets import Static
from textual.reactive import reactive


class CountdownDisplay(Static):
    remaining: reactive[float] = reactive(0.0)

    def watch_remaining(self) -> None:
        minutes, seconds = divmod(int(self.remaining), 60)
        self.update(f"{minutes:02d}:{seconds:02d}")