from statemachine import StateMachine, State
from GUI import GUI
from random import choice

welcomescreen = [
    "Welcome, fool",
    "Welcome to the dungeons"
]

class MenuState(StateMachine):
    intro = State("Intro",initial=True) #introduction to game
    escaped = State("Escaped") #escape menu
    exited = State("Exited",final=True) #exits the game
    playing = State("Playing") #playing game
    paused = State("Paused") #game paused

    startgame = intro.to(playing, cond="start_game")
    escapegame = playing.to(escaped)
    paused = playing.to(paused)
    quitgame = escaped.to(exited)
    backtointro = escaped.to(intro)

    def __init__(self):
        self.game = GUI()
    
    def on_enter_intro(self):
        self.game.introscreen["text"] = choice(welcomescreen)
        self.game.introscreen.setText()
        self.game.introscreen.show()
    
    def on_exit_intro(self):
        self.game.introscreen.hide()
    
    def run(self):
        self.game.run()