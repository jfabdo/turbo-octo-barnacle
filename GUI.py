from direct.showbase.ShowBase import ShowBase

# from direct.actor.Actor import Actor
# from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionTube, CollisionNode
# from panda3d.core import AmbientLight, DirectionalLight
# from panda3d.core import Vec4, Vec3
# from panda3d.core import WindowProperties

from direct.gui.DirectGui import *

# from GameObject import *

from menus import Menus

import random

class GUI(ShowBase):
    def __init__(self,manager,size):
        # self.state = state
        ShowBase.__init__(self)
        self.menus = Menus()
        self.menus.setdesktop(manager,size=size)
        # self.setupPanda()
        # self.setscene()
        # # self.setkeys()
        # self.setcollisions()
        
        # self.score = 0

        # self.scoreUI = OnscreenText(text = "0",
        #                             pos = (-1.3, 0.825),
        #                             mayChange = True,
        #                             align = TextNode.ALeft,
        #                             font = base.font)

        # self.healthIcons = []
        # # self.spawning()
        self.players = {}
        self.enemies = {}

    def setupPanda(self):
        # self.disableMouse()

        # self.setmonitor()

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

    def update(self,dt,events):#get size, update size if it changes, but update that here
        for event in events:
            if event in self.menus.register:
                self.updateTask = taskMgr.add(self.menus.register[event](),"event")
        
        for value in self.players.values():
            self.updateTask = taskMgr.add(value.update(dt), "update")

        for value in self.enemies.values():
            self.updateTask = taskMgr.add(value.update(dt), "update")

        # for player in self.players.values():
        #     self.updateTask = taskMgr.add(player.update(dt), "update")
        
        # for enemy in self.enemies.values():
        #     self.updateTask = taskMgr.add(enemy.update(dt), "update")
        # mouseWatcher = base.mouseWatcherNode
        # if mouseWatcher.hasMouse():
        #     mousePos = mouseWatcher.getMouse()
        # else:
        #     mousePos = self.lastMousePos
    
        # self.mousePos3D = Point3()
        # nearPoint = Point3()
        # farPoint = Point3()

        # base.camLens.extrude(mousePos, nearPoint, farPoint)
        # self.groundPlane.intersectsLine(self.mousePos3D,
        #                                 render.getRelativePoint(base.camera, nearPoint),
        #                                 render.getRelativePoint(base.camera, farPoint))

        # self.beamHitTimer -= dt
        # if self.beamHitTimer <= 0:
        #     self.beamHitTimer = self.beamHitPulseRate
        #     self.beamHitModel.setH(random.uniform(0.0, 360.0))
        # self.beamHitModel.setScale(math.sin(self.beamHitTimer*3.142/self.beamHitPulseRate)*0.4 + 0.9)

        # if firingVector.length() > 0.001:
        #     self.ray.setOrigin(self.actor.getPos())
        #     self.ray.setDirection(firingVector)

        # self.lastMousePos = mousePos

        # if self.damageTakenModelTimer > 0:
        #     self.damageTakenModelTimer -= dt
        #     self.damageTakenModel.setScale(2.0 - self.damageTakenModelTimer/self.damageTakenModelDuration)
        #     if self.damageTakenModelTimer <= 0:
        #         self.damageTakenModel.hide()
