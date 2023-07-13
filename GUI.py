from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from screeninfo import get_monitors
import direct.gui.DirectGui as DirectGui
from direct.actor.Actor import Actor
from panda3d.core import Vec4, Vec3

class GUI(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setmonitor()
        self.intro_screen()
        self.disableMouse()
        self.attachkeys()
        self.loadscene()
        self.updateTask = taskMgr.add(self.update, "update")

    def loadscene(self):
        #loader.loadModel("Models/Misc/environment")
        # self.tempActor = Actor("Models/PandaChan/act_p3d_chan", {"walk" : "Models/PandaChan/a_p3d_chan_run"})
        # self.tempActor.reparentTo(render)
        #self.tempActor.loop("walk")
        # Move the camera to a position high above the screen
        # --that is, offset it along the z-axis.
        self.camera.setPos(0, 0, 32)
        # Tilt the camera down by setting its pitch.
        self.camera.setP(-90)

    def attachkeys(self):
        self.keyMap = {
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False,
            "leftclick" : False,
            "rightclick" : False,
            "pause" : False,
            "esc" : False
        }
        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.accept("mouse1", self.updateKeyMap, ["leftclick", True])
        self.accept("mouse1-up", self.updateKeyMap, ["leftclick", False])
        self.accept("mouse2", self.updateKeyMap, ["rightclick", True])
        self.accept("mouse2-up", self.updateKeyMap, ["rightclick", False])
        self.accept("p", self.updateKeyMap, ["pause", True])
        self.accept("p-up", self.updateKeyMap, ["pause", False])
        self.accept("esc", self.updateKeyMap, ["esc", True])
        self.accept("esc-up", self.updateKeyMap, ["esc", False])
        
    def update(self, task):
            # Get the amount of time since the last update
        self.gameplay()
        return task.cont
    
    def gameplay(self):
        dt = globalClock.getDt()

        # If any movement keys are pressed, use the above time
        # to calculate how far to move the character, and apply that.
        if self.keyMap["up"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(0, 5.0*dt, 0))
        if self.keyMap["down"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(0, -5.0*dt, 0))
        if self.keyMap["left"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(-5.0*dt, 0, 0))
        if self.keyMap["right"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(5.0*dt, 0, 0))
        if self.keyMap["leftclick"]:
            print ("Zap!")
    
    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
        print (controlName, "set to", controlState)

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
                   command = self.startgame,
                   pos = (-0.3, 0, -0.2),
                   parent = self.introscreen,
                   scale = 0.07)
        
        btn = DirectGui.DirectButton(text = "Quit",
                   command = self.quit,
                   pos = (0.3, 0, -0.2),
                   parent = self.introscreen,
                   scale = 0.07)
        
    def cleanup(self):
        pass
    
    def startgame(self):
        #set state to playing
        pass

    def quit(self):
        self.cleanup()
        base.userExit()