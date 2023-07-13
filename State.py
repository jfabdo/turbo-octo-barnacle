from statemachine import StateMachine, State
from random import choice
from GUI import GUI

welcomescreen = [
    "Welcome, fool",
    "Welcome to the dungeons"
]

class MenuState(StateMachine):
    intro = State("Intro",initial=True) #introduction to game
    exited = State("Exited",final=True) #exits the game
    escaped = State("Escaped") #escape menu
    playing = State("Playing") #playing game
    paused = State("Paused") #game paused

    startgame = intro.to(playing)
    escapegame = playing.to(escaped)
    pausegame = playing.to(paused)
    quitgame = escaped.to(exited)
    backtointro = escaped.to(intro)
    resumegame = escaped.to(playing)

    def __init__(self):
        self.GUI = GUI()
        self.GUI.run()
    
    def on_enter_intro(self):
        self.GUI.introscreen["text"] = choice(welcomescreen)
        self.GUI.introscreen.setText()
        self.GUI.introscreen.show()
        pass
    
    def on_exit_intro(self):
        # self.GUI.introscreen.hide()
        pass

    def on_enter_escaped(self):
        pass #put up escape menu
    
    def on_exit_escaped(self):
        pass #pull down escape menu

    def on_enter_exited(self):
        pass #Start cleanup
    
    def on_exit_exited(self):
        pass #finish cleanup
    
    def on_enter_playing(self):
        #print(self.current_state.id) #enable key presses, motion, time, etc.
        pass
    
    def on_exit_playing(self):
        pass #disable key presses, motion, time, etc.
    
    def on_enter_paused(self):
        pass #gray out the screen

    def on_exit_paused(self):
        pass #take down the gray