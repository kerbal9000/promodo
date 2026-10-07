from textual.app import App, ComposeResult
from textual import events
from textual.widgets import Button, Header, Label,Static
from screens.timer import TimerScreen

class MyApp(App): # subclass of app handles the main things
    TITLE = "PROMODO"

    #self is the app instance 
    def compose(self) -> ComposeResult: # compose is a method that is called once to describe the widget tree
        yield Header()
        yield Button("EXIT", id="exit", variant="default")
        yield Button("start timer",id="start_timer" , variant="default")
        yield Button("pause timer",id="pause_timer" , variant="default")
        yield Button("stop timer",id="stop_timer" , variant="default")


    def on_mount(self) -> None: # none means returns nothing
        self.screen.styles.background = "#414a4c" #sets the backround
        self.push_screen(TimerScreen())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "exit":
                self.exit("exit")
            case "start_timer":
                pass    
            case "pause_timer":
                pass
            case "stop_timer":
                pass
            

        

if __name__ == "__main__":
    app = MyApp()
    app.run()
