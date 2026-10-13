from textual.app import App, ComposeResult
from textual import events
from textual.widgets import Button, Header, Label,Static ,TabbedContent,TabPane
from screens.TimerScreen import TimerScreen
from screens.TaskScreen import TaskScreen
from screens.DashboardScreen import DashboardScreen

from themes.themes_handler import ALL_THEMES,DEFAULT_THEME

class MyApp(App): # subclass of app handles the main things
    TITLE = "PROMODO"
    CSS_PATH=["styles/timer.tcss","styles/task.tcss","styles/dashboard.tcss"] #add the tcss to the list and let it be prefixed with the class name
    #self is the app instance 
    def compose(self) -> ComposeResult: # compose is a method that is called once to describe the widget tree
        yield Header()
        yield Button("EXIT", id="exit", variant="default")
        
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
        

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "exit":
                self.exit("exit")

if __name__ == "__main__":
    app = MyApp()
    app.run()
