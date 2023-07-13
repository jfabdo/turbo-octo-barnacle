from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from screeninfo import get_monitors
import direct.gui.DirectGui as DirectGui

class GUI(ShowBase):
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
        self.introscreenBackdrop = DirectGui.DirectFrame(frameColor = (0, 0, 0, 1),
                                     frameSize = (-1, 1, -1, 1),
                                     parent = render2d)
        self.introscreen = DirectGui.DirectFrame(frameColor = (1, 1, 1, 0))
        label = DirectGui.DirectLabel(text = "Wizard Union",
                    parent = self.introscreen,
                    scale = 0.1,
                    pos = (0, 0, 0.9))
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

    def cleanup(self):
        pass

    def quit(self):
        self.cleanup()

        base.userExit()