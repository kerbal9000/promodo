from time import monotonic
from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Horizontal, Vertical, Center, Middle
from textual.widgets import Static, Button, ProgressBar
from textual.reactive import reactive
from textual import on

import math

# from widgets.countdown import CountdownDisplay
# from core.storage import log_session
# from core.sound import play_sound


WORK = "work"
SHORT_BREAK = "short_break"  #names for the phases 
LONG_BREAK = "long_break"

PHASE_DURATIONS = {
    WORK: 5,
    SHORT_BREAK: 1 * 60, 
    LONG_BREAK: 2 * 60,
}

class TimerScreen(Screen):
    phase=reactive(WORK)
    running=reactive(False)
    remaining=reactive(0.0)

    start_time:float = 0.0
    phase_duration:int = 0
    pomodoro_count : int = 0
    _timer = None 
    paused_at: float = 0.0 

    def compose(self):
        with Middle():
            with Center():
                yield Static("10:00",id="countdown")
                with Horizontal():

                    yield Button("Start", id="start", variant="success")
                    yield Button("Pause", id="pause", variant="primary")
                    yield Button("Skip", id="skip", variant="warning")
                    yield Button("Reset", id="reset", variant="error")

    def on_mount(self) -> None:
        self._timer = None
        self.start_phase(WORK)

    def start_phase(self,phase):
        if self._timer is not None:
            self._timer.stop()
        
        self.phase_duration = PHASE_DURATIONS[phase]
        self.start_time = monotonic() 
        self.remaining = self.phase_duration
        self.running = False

        #self._timer.resume()
        self._timer = self.set_interval(1,self.tick,pause=True)

    def tick(self):
        elapsed = monotonic() - self.start_time
        self.remaining = max(0,self.phase_duration - elapsed)
        if self.remaining <= 0:
            self.end_phase()
    
    def watch_remaining(self,value):
        total = math.ceil(value)
        minutes = total // 60
        sec = total % 60
       
        self.query_one("#countdown").update(content=f"{minutes:02d}:{int(sec):02d}")

    def end_phase(self):
        if self.phase == WORK:
            self.start_phase(SHORT_BREAK)
            self.pomodoro_count += 1
            if self.pomodoro_count >= 4:
                self.pomodoro_count = 0
                self.start_phase(LONG_BREAK)
            else:
                self.start_phase(SHORT_BREAK)

        else:
            self.start_phase(WORK)
   

    def skip_phase(self):
        self.end_phase()

    def pause(self):
        if self.running == False:
            return
        self._timer.pause()
        self.paused_at = monotonic()
        self.running = False
    
    def resume(self):

        if self.running:
            return
        if self.paused_at > 0:                         
            self.start_time += monotonic() - self.paused_at
            self.paused_at = 0.0
            
        self._timer.resume() 
        self.running = True
    
    def reset(self):
        self.start_phase(self.phase)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "start":
                self.resume()
            case "pause":
                self.pause()
                self.query_one("#start", Button).label = "Resume"
            case "reset":
                self.reset()
                self.start_phase(self.phase)
            case "skip":
                self.skip_phase()
