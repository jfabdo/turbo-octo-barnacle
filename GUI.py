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
            "shoot" : False
        }

        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.accept("mouse1", self.updateKeyMap, ["shoot", True])
        self.accept("mouse1-up", self.updateKeyMap, ["shoot", False])
        
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
        pass

    def update(self, task):
        pass
