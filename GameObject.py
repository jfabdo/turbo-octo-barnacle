from panda3d.core import Vec4, Vec3, Vec2, Plane, Point3, BitMask32
from direct.actor.Actor import Actor
from panda3d.core import CollisionSphere, CollisionNode, CollisionRay, CollisionSegment, CollisionHandlerQueue
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TextNode
from panda3d.core import AudioSound
from panda3d.core import PointLight
from State import ActorFSM
import math, random

FRICTION = 150.0

class GameObject():
    def __init__(self,pos=Vec3(0, 0, 0),modelName="dot",modelAnims="dot",maxHealth=300,maxSpeed=10):
        self.state = ActorFSM()
        self.setPos(modelName, modelAnims, pos)
        self.setSpeedAcc(maxHealth,maxSpeed)
        self.addCollider()
    
    def update(self):
        speed = self.velocity.length()
        if speed > self.maxSpeed:
            self.velocity.normalize()
            self.velocity *= self.maxSpeed
            speed = self.maxSpeed

        if not self.walking:
            frictionVal = FRICTION*dt
            if frictionVal > speed:
                self.velocity.set(0, 0, 0)
            else:
                frictionVec = -self.velocity
                frictionVec.normalize()
                frictionVec *= frictionVal

                self.velocity += frictionVec

        self.actor.setPos(self.actor.getPos() + self.velocity*dt)

    def setPos(self, modelName, modelAnims, pos):
        self.actor = Actor(modelName, modelAnims)
        self.actor.reparentTo(render)
        self.actor.setPos(pos)

    def setSpeedAcc(self,maxHealth,maxSpeed):
        self.maxHealth = maxHealth
        self.health = maxHealth

        self.maxSpeed = maxSpeed

        self.velocity = Vec3(0, 0, 0)
        self.acceleration = 300.0

        self.moving = False

    def addCollider(self):
        colliderNode = CollisionNode(colliderName)
        colliderNode.addSolid(CollisionSphere(0, 0, 0, 0.3))
        self.collider = self.actor.attachNewNode(colliderNode)
        self.collider.setPythonTag("owner", self)

class Player(GameObject):
    def __init__(self):
        GameObject.__init__()

    def update(self):
        GameObject.update(self, dt)

        if self.keymap['up']:
            self.state.request('Walking',self.acceleration*dt)
        if self.keymap['down']:
            self.state.request('Walking',-self.acceleration*dt)
        if self.keymap['left']:
            self.state.request('Walking',-self.acceleration*dt)
        if self.keymap['right']:
            self.state.request('Walking',self.acceleration*dt)
        if self.keymap['weapon']:
            self.state.request('Weapon')
        if self.keymap['magic']:
            self.state.request('Magic')
        if self.keymap['jump']:
            self.state.request('Jump')
        
        firingVector = Vec3(self.mousePos3D - self.actor.getPos())
        firingVector2D = firingVector.getXy()
        firingVector2D.normalize()
        firingVector.normalize()

        heading = self.yVector.signedAngleDeg(firingVector2D)
        self.actor.setH(heading)
        if self.keys["shoot"]:
            self.state.request("Weapon") #fire the beam

class TheCloud(GameObject):
    def __init__(self):
        pass

    def update(self):
        self.runlogic()

    def runlogic(self):
        pass

class NPC(GameObject):
    def __init__(self):
        GameObject.__init__()

    def update(self):
        self.runlogic()

    def runlogic(self):
        pass