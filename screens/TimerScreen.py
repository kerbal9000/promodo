from time import monotonic
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, Center, Middle
from textual.widgets import Static, Button, ProgressBar
from textual.reactive import reactive
from textual import on

import math

import datetime
from widgets.countdown import CountdownDisplay
from core.storage import log_session
# from core.sound import play_sound

WORK = "work"
SHORT_BREAK = "short_break"  #names for the phases 
LONG_BREAK = "long_break"

PHASE_DURATIONS = {
    WORK: 25 * 60 , # working timer 25 mins
    SHORT_BREAK: 5 * 60, # short break 5 mins
    LONG_BREAK: 30 * 60, # long break 30 mins after every 4 work shifts
}

class TimerScreen(Vertical):
   
    phase=reactive(WORK)
    running=reactive(False)
    remaining=reactive(0.0)

    start_time:float = 0.0
    phase_duration:int = 0
    pomodoro_count : int = 0

    _timer = None 
    paused_at: float = 0.0 

    def compose(self):

        with Vertical(id="timer-container"):
            yield CountdownDisplay(id="countdown")
            yield ProgressBar(total=100,id="progress",show_eta=False,show_percentage=False)

            with Horizontal(id="controls"):
                yield Button("Start", id="start")
                yield Button("Pause", id="pause")
                yield Button("Skip", id="skip")
                yield Button("Reset", id="reset")


    def on_mount(self) -> None:
        self._timer = None
        self.start_phase(WORK)
        self.query_one("#progress",ProgressBar).progress = 500 # sets progress bar to 100 just for now 

    def start_phase(self,phase):
        if self._timer is not None:
            self._timer.stop()
        
        self.phase_duration = PHASE_DURATIONS[phase]
        self.start_time = monotonic() 
        self.remaining = self.phase_duration
        self.running = False

        self._timer = self.set_interval(1,self.tick,pause=True)
        self.start_dt = datetime.datetime.now() # keeps the record of the current start time

    def tick(self):
        elapsed = monotonic() - self.start_time
        self.remaining = max(0,self.phase_duration - elapsed)
        fraction = self.remaining / self.phase_duration

        self.query_one("#progress",ProgressBar).progress = fraction * 100
        self.update_bar_color(fraction)


        if self.remaining <= 0:
            self.end_phase(completed=True)

    def watch_remaining(self,value):
        total = math.ceil(value)
        minutes = total // 60
        sec = total % 60
       
        self.query_one(CountdownDisplay).remaining = value

    def end_phase(self,completed:bool = True):

        log_session(start=self.start_dt,end=datetime.datetime.now(),phase=self.phase,completed=completed)
        self.skipped = False

        if self.phase == WORK:
            self.pomodoro_count += 1

            if self.pomodoro_count >= 4:
                self.pomodoro_count = 0
                self.start_phase(LONG_BREAK)
                self.phase = LONG_BREAK
            else:
                self.start_phase(SHORT_BREAK)
                self.phase = SHORT_BREAK
            
        elif self.phase == SHORT_BREAK or self.phase == LONG_BREAK:
            self.start_phase(WORK)
            self.phase = WORK
        
    def skip_phase(self):
        self.end_phase(completed=False)
        
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
    
    def update_bar_color(self, fraction_left): 
        bar = self.query_one("#progress", ProgressBar)
        if fraction_left > 0.5:
            bar.query_one("Bar").styles.color = "green"
        elif fraction_left > 0.2:
            bar.query_one("Bar").styles.color = "yellow"
        else:
            bar.query_one("Bar").styles.color = "red"
            
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
