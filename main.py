import sys
import os

from textual.app import App, ComposeResult
from textual import events
from textual.widgets import Button, Header, Label,Static ,TabbedContent,TabPane
from screens.TimerScreen import TimerScreen
from screens.TaskScreen import TaskScreen
from screens.DashboardScreen import DashboardScreen

from themes.themes_handler import ALL_THEMES,DEFAULT_THEME

if getattr(sys, 'frozen', False):
    # Running in a PyInstaller/Nuitka bundle
    _BASE_DIR = sys._MEIPASS
else:
    # Running in a normal Python environment
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MyApp(App): # subclass of app handles the main things
    TITLE = "PROMODO"
    CSS_PATH = [
        os.path.join(_BASE_DIR, "styles", "timer.tcss"),
        os.path.join(_BASE_DIR, "styles", "task.tcss"),
        os.path.join(_BASE_DIR, "styles", "dashboard.tcss"),
        os.path.join(_BASE_DIR, "styles", "taskrow.tcss"),
     ]
      #add the tcss to the list and let it be prefixed with the class name
    #self is the app instance 
    def compose(self) -> ComposeResult: # compose is a method that is called once to describe the widget tree
        yield Header()    
        with TabbedContent():
            with TabPane("Dashboard",id="Dashboard"):
                yield DashboardScreen()
            with TabPane("Task",id="Task"): #makes a tab pane the id will be used later to switch panes with buttons
                yield TaskScreen()
            with TabPane("Timer",id="tab-timer"):
                yield TimerScreen()
            
    def on_mount(self) -> None: # none means returns nothing
        for t in ALL_THEMES: #for all the themes in the themes folder
            self.register_theme(t) #register said theme
        self.theme = DEFAULT_THEME # make it that theme

if __name__ == "__main__":
    app = MyApp()
    app.run()
