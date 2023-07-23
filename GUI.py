from direct.showbase.ShowBase import ShowBase

from direct.actor.Actor import Actor
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionTube, CollisionNode
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import Vec4, Vec3
from panda3d.core import WindowProperties

from direct.gui.DirectGui import *

from GameObject import *

from State import MenuFSM

import random

class GUI(ShowBase):
    def __init__(self,state):
        self.state = state
        ShowBase.__init__(self)
        self.setupPanda()
        self.setscene()
        self.setkeys()
        self.setcollisions()
        
        self.score = 0

        self.scoreUI = OnscreenText(text = "0",
                                    pos = (-1.3, 0.825),
                                    mayChange = True,
                                    align = TextNode.ALeft,
                                    font = base.font)

        self.healthIcons = []
        # self.spawning()

    def setupPanda(self):
        self.disableMouse()

        self.setmonitor()

        self.exitFunc = self.cleanup
        
    def setscene(self):
        mainLight = DirectionalLight("main light")
        self.mainLightNodePath = render.attachNewNode(mainLight)
        self.mainLightNodePath.setHpr(45, -45, 0)
        render.setLight(self.mainLightNodePath)

        # ambientLight = AmbientLight("ambient light")
        # ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        # self.ambientLightNodePath = render.attachNewNode(ambientLight)
        # render.setLight(self.ambientLightNodePath)

        render.setShaderAuto()

        # self.environment = loader.loadModel("Models/Misc/environment")
        # self.environment.reparentTo(render)

        self.camera.setPos(0, 0, 32)
        self.camera.setP(-90)
    
    def setkeys(self):
        self.keyMap = {
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False,
            "weapon" : False,
            "magic"  : False,
            "jump"  : False,
        }

        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.accept("mouse1", self.updateKeyMap, ["weapon", True])
        self.accept("mouse1-up", self.updateKeyMap, ["weapon", False])
        self.accept("mouse2", self.updateKeyMap, ["magic", True])
        self.accept("mouse2-up", self.updateKeyMap, ["magic", False])
        self.accept("space", self.updateKeyMap, ["jump", True])
        self.accept("space-up", self.updateKeyMap, ["jump", False])
        
    def setcollisions(self):
        self.pusher = CollisionHandlerPusher()
        self.cTrav = CollisionTraverser()

        self.pusher.setHorizontal(True)

        wallSolid = CollisionTube(-8.0, 0, 0, 8.0, 0, 0, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)

        wallSolid = CollisionTube(-8.0, 0, 0, 8.0, 0, 0, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(-8.0)

        wallSolid = CollisionTube(0, -8.0, 0, 0, 8.0, 0, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setX(8.0)

        wallSolid = CollisionTube(0, -8.0, 0, 0, 8.0, 0, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setX(-8.0)

    def setmenus(self):
        #game over screen
        self.gameOverScreen = DirectDialog(frameSize = (-0.7, 0.7, -0.7, 0.7),
                                           fadeScreen = 0.4,
                                           relief = DGG.FLAT,
                                           frameTexture = "UI/stoneFrame.png")
        self.gameOverScreen.hide()

        # self.font = loader.loadFont("Fonts/Wbxkomik.ttf")

        # buttonImages = (
        #     loader.loadTexture("UI/UIButton.png"),
        #     loader.loadTexture("UI/UIButtonPressed.png"),
        #     loader.loadTexture("UI/UIButtonHighlighted.png"),
        #     loader.loadTexture("UI/UIButtonDisabled.png")
        # )
        
        label = DirectLabel(text = "Game Over!",
                            parent = self.gameOverScreen,
                            scale = 0.1,
                            pos = (0, 0, 0.2),
                            text_font = self.font,
                            relief = None)

        self.finalScoreLabel = DirectLabel(text = "",
                                           parent = self.gameOverScreen,
                                           scale = 0.07,
                                           pos = (0, 0, 0),
                                           text_font = self.font,
                                           relief = None)

        btn = DirectButton(text = "Restart",
                           command = self.startGame,
                           pos = (-0.3, 0, -0.2),
                           parent = self.gameOverScreen,
                           scale = 0.07,
                           text_font = self.font,
                        #    clickSound = loader.loadSfx("Sounds/UIClick.ogg"),
                           frameTexture = buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text = "Quit",
                           command = self.quit,
                           pos = (0.3, 0, -0.2),
                           parent = self.gameOverScreen,
                           scale = 0.07,
                           text_font = self.font,
                        #    clickSound = loader.loadSfx("Sounds/UIClick.ogg"),
                           frameTexture = buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)
        #title menu
        self.titleMenuBackdrop = DirectFrame(frameColor = (0, 0, 0, 1),
                                             frameSize = (-1, 1, -1, 1),
                                             parent = render2d)

        self.titleMenu = DirectFrame(frameColor = (1, 1, 1, 0))

        title = DirectLabel(text = "Panda-chan",
                            scale = 0.1,
                            pos = (0, 0, 0.9),
                            parent = self.titleMenu,
                            relief = None,
                            # text_font = self.font,
                            text_fg = (1, 1, 1, 1))
        title2 = DirectLabel(text = "and the",
                             scale = 0.07,
                             pos = (0, 0, 0.79),
                             parent = self.titleMenu,
                            #  text_font = self.font,
                             frameColor = (0.5, 0.5, 0.5, 1))
        title3 = DirectLabel(text = "Endless Horde",
                             scale = 0.125,
                             pos = (0, 0, 0.65),
                             parent = self.titleMenu,
                             relief = None,
                            #  text_font = self.font,
                             text_fg = (1, 1, 1, 1))

        btn = DirectButton(text = "Start Game",
                           command = self.startGame,
                           pos = (0, 0, 0.2),
                           parent = self.titleMenu,
                           scale = 0.1,
                        #    text_font = self.font,
                        #    clickSound = loader.loadSfx("Sounds/UIClick.ogg"),
                        #    frameTexture = buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text = "Quit",
                           command = self.quit,
                           pos = (0, 0, -0.2),
                           parent = self.titleMenu,
                           scale = 0.1,
                        #    text_font = self.font,
                        #    clickSound = loader.loadSfx("Sounds/UIClick.ogg"),
                        #    frameTexture = buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)
    
    def cleanup(self):
        self.scoreUI.removeNode()

        for icon in self.healthIcons:
            icon.removeNode()

        self.beamHitModel.removeNode()

        base.cTrav.removeCollider(self.rayNodePath)

        self.laserSoundHit.stop()
        self.laserSoundNoHit.stop()

        render.clearLight(self.beamHitLightNodePath)
        self.beamHitLightNodePath.removeNode()

        GameObject.cleanup(self)

    def update(self, task):
        mouseWatcher = base.mouseWatcherNode
        if mouseWatcher.hasMouse():
            mousePos = mouseWatcher.getMouse()
        else:
            mousePos = self.lastMousePos
    
        self.mousePos3D = Point3()
        nearPoint = Point3()
        farPoint = Point3()

        base.camLens.extrude(mousePos, nearPoint, farPoint)
        self.groundPlane.intersectsLine(self.mousePos3D,
                                        render.getRelativePoint(base.camera, nearPoint),
                                        render.getRelativePoint(base.camera, farPoint))

        self.beamHitTimer -= dt
        if self.beamHitTimer <= 0:
            self.beamHitTimer = self.beamHitPulseRate
            self.beamHitModel.setH(random.uniform(0.0, 360.0))
        self.beamHitModel.setScale(math.sin(self.beamHitTimer*3.142/self.beamHitPulseRate)*0.4 + 0.9)

        if firingVector.length() > 0.001:
            self.ray.setOrigin(self.actor.getPos())
            self.ray.setDirection(firingVector)

        self.lastMousePos = mousePos

        if self.damageTakenModelTimer > 0:
            self.damageTakenModelTimer -= dt
            self.damageTakenModel.setScale(2.0 - self.damageTakenModelTimer/self.damageTakenModelDuration)
            if self.damageTakenModelTimer <= 0:
                self.damageTakenModel.hide()
