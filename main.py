from textual.app import App, ComposeResult
from textual import events
from textual.widgets import Button, Header, Label

class MyApp(App):
    TITLE = "PROMODO"


    def compose(self) -> ComposeResult:
        yield Header()
        yield Button("Yes", id="yes", variant="primary")
    def on_mount(self) -> None:
        self.screen.styles.background = "#414a4c" #sets the backround
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button.id)








if __name__ == "__main__":
    app = MyApp()
    app.run()
