from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from screeninfo import get_monitors
import direct.gui.DirectGui as DirectGui
from statemachine import StateMachine, State

class MenuState(StateMachine):
    intro = State("Intro",initial=True) #introduction to game
    escaped = State("Escaped") #escape menu
    exited = State("Exited",final=True) #exits the game
    playing = State("Playing") #playing game
    paused = State("Paused") #game paused

    startgame = intro.to(playing)
    escapegame = playing.to(escaped)
    paused = playing.to(paused)
    quitgame = escaped.to(exited)
    backtointro = escaped.to(intro)

    def __init__(self):
        self.game = Game()
    
    def on_enter_intro(self):
        self.game.introscreen.show()
    
    def on_exit_intro(self):
        self.game.introscreen.hide()

    def run(self):
        self.game.run()

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.setmonitor()
        self.intro_screen()
    
    def setmonitor(self):
        for m in get_monitors():
            if m.is_primary:
                primarymonitor = m

        properties = WindowProperties()
        properties.setSize(primarymonitor.width, primarymonitor.height)
        self.win.requestProperties(properties)

    def intro_screen(self):
        self.introscreen = DirectGui.DirectDialog(frameSize = (-0.7, 0.7, -0.7, 0.7),
                                   fadeScreen = 0.4,
                                   relief = DirectGui.DGG.FLAT)
        label = DirectGui.DirectLabel(text = "Wizard Union",
                    parent = self.introscreen,
                    scale = 0.1,
                    pos = (0, 0, 0.2))
        self.secondline = DirectGui.DirectLabel(text = "",
                                   parent = self.introscreen,
                                   scale = 0.07,
                                   pos = (0, 0, 0))
        btn = DirectGui.DirectButton(text = "Restart",
                   command = self.startGame,
                   pos = (-0.3, 0, -0.2),
                   parent = self.introscreen,
                   scale = 0.07)
        
        btn = DirectGui.DirectButton(text = "Quit",
                   command = self.quit,
                   pos = (0.3, 0, -0.2),
                   parent = self.introscreen,
                   scale = 0.07)
        
    def startGame(self):
        pass

    def quit(self):
        pass