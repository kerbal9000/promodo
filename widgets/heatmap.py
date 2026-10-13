from textual.widgets import Static
from textual.widget import Widget
from datetime import datetime,timedelta
from core.stats import sessions_per_day
from rich.text import Text

def build_heatmap(sessions,weeks=26):
        today = datetime.today()

        grid = [[0 for _ in range(weeks)] for _ in range(7)]
        start = today - timedelta(weeks=weeks - 1)
        start -= timedelta(days=(start.weekday() + 1) % 7 )

        counts = sessions_per_day(sessions=sessions)

        day = start
        for col in range(weeks):
            for row in  range(7):
                if day > today:
                    grid[row][col] = None 
                else:
                    grid[row][col] = counts.get(day,0)
                day += timedelta(days=1)

        return grid

class Heatmap(Widget):
    def __init__(self, grid=None, **kwargs):
        super().__init__(**kwargs)
        self.grid = grid or []
    
    def render(self)-> Text:
        return self.render_grid(self.grid)

    def render_grid(self,grid):
        text = Text()
        for row in grid:
            for cell in row:
                if cell is None:
                    text.append(" ")
                else:
                    color = self.color_for(cell)
                    text.append("██",style=color)
            text.append("\n")
        return text

    def color_for(self,count):
        return {
        0: "grey23",
        1: "green3",
        2: "green2",
        3: "green1",
        }.get(min(count, 3), "green1")



    