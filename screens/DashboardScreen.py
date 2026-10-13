from textual.containers import Horizontal, Vertical, Center, Middle
from textual.widgets import Static

from widgets.heatmap import Heatmap, build_heatmap

from core.stats import total_focus_time, current_streak
from core.storage import load_sessions
from textual.reactive import reactive

class DashboardScreen(Vertical):
    grid : reactive = None
    def compose(self):
        yield Static("Welcome Back",id="dashboard-title")
        yield Heatmap(id="heatmap")
    
    def on_mount(self):

        sessions = load_sessions()
        grid = build_heatmap(sessions,weeks=25)
        self.query_one(Heatmap).grid = grid
